from Piece import piece, Color, Direction, PieceType
from typing import cast
import random



class Board:
    def __init__(self, row, col):
        self.distance_of_next_move = None
        self.schwarz_has_ball = None
        self.piece_clicked = None
        self.row = row
        self.col = col
        self.piece_list = []
        self.possible_moves = []
        self.game_over = False
        self.turn = Color.SCHWARZ
        self.winner = None
        self.my_turn = True
        self.goal_col = 4
        self.goal_row = 9

    def setup_board(self, against_bot):
        random_player_starter = False
        self.piece_list = []

        for row in range(self.row):
            for col in range(self.col):
                if (row + col) % 2 != 0:
                    if row < 2:
                        self.piece_list.append(
                            piece(row, col, Color.SCHWARZ, Direction.FORWARD, PieceType.BASKET if row == 1 and col == 4 else PieceType.PLAYER,False))
                    elif row >= self.row - 2:
                        self.piece_list.append(piece(row, col, Color.WEISS, Direction.BACKWARD, PieceType.BASKET if row == self.row - 2 and col == 4 else PieceType.PLAYER, False))

        while not random_player_starter:
            random_player_starter = random.choice(self.piece_list)

            if against_bot:
                if random_player_starter.player_or_basket == PieceType.PLAYER and random_player_starter.color == Color.WEISS:
                    random_player_starter.has_ball = True
                else:
                    random_player_starter = False

            else:
                if random_player_starter.player_or_basket == PieceType.PLAYER:
                    random_player_starter.has_ball = True
                else:
                    random_player_starter = False

        self.turn = random_player_starter.color
        self.my_turn = True

    def get_information(self, row, col):
        for piece in self.piece_list:
            if piece.row == row and piece.col == col:
                return piece

    def show_that_clicked_piece(self, piece_clicked):
        if piece_clicked is None:
            for piece in self.piece_list:
                if piece.color == Color.WEISS_AUSGEWAEHLT:
                    piece.color = Color.WEISS
                elif piece.color == Color.SCHWARZ_AUSGEWAEHLT:
                    piece.color = Color.SCHWARZ
        else:

            for piece in self.piece_list:
                if piece.color == Color.WEISS_AUSGEWAEHLT:
                    piece.color = Color.WEISS
                elif piece.color == Color.SCHWARZ_AUSGEWAEHLT:
                    piece.color = Color.SCHWARZ

                if piece_clicked.color == Color.WEISS:
                    piece_clicked.color = Color.WEISS_AUSGEWAEHLT
                if piece_clicked.color == Color.SCHWARZ:
                    piece_clicked.color = Color.SCHWARZ_AUSGEWAEHLT

    def show_possible_moves(self, piece_clicked):
        self.possible_moves.clear()
        row_step = 1
        if piece_clicked.direction == Direction.BACKWARD:
            row_step = -1

        for col_step in (-1, 1):
            step_row = piece_clicked.row + row_step
            step_col = piece_clicked.col + col_step
            if self.get_information(row=step_row, col=step_col) is None and 0 <= step_row <= 10 and 0 <= step_col <= 8:
                self.possible_moves.append((step_row, step_col))

        for col_step in (-1, 1):
            step_row = piece_clicked.row + row_step
            step_col = piece_clicked.col + col_step
            step_piece = self.get_information(row=step_row, col=step_col)
            if step_piece is not None and step_piece.color.team != piece_clicked.color.team and 0 <= step_row <= 10 and 0 <= step_col <= 8:
                jump_row = piece_clicked.row + row_step * 2
                jump_col = piece_clicked.col + col_step * 2
                if self.get_information(row=jump_row, col=jump_col) is None and 0 <= jump_row <= 10 and 0 <= jump_col <= 8:
                    self.possible_moves.append((jump_row, jump_col))


        # Ab hier kein Kill oder Move sondern Scan und Pass
        if piece_clicked.has_ball:
            scan_right = piece_clicked.col + 1
            while scan_right <= 8:
                found = self.get_information(row=piece_clicked.row, col=scan_right)
                if found is not None:
                    if found.color.team == piece_clicked.color.team and found.player_or_basket == PieceType.PLAYER:
                        self.possible_moves.append((found.row, found.col))
                    break
                scan_right = scan_right + 1
            scan_left = piece_clicked.col - 1
            while scan_left >= 0:
                found = self.get_information(row=piece_clicked.row, col=scan_left)
                if found is not None:
                    if found.color.team == piece_clicked.color.team and found.player_or_basket == PieceType.PLAYER:
                        self.possible_moves.append((found.row, found.col))
                    break
                scan_left = scan_left - 1
            scan_down = piece_clicked.row + 1
            while scan_down <= 10:
                found = self.get_information(row=scan_down, col=piece_clicked.col)
                if found is not None:
                    if found.color.team == piece_clicked.color.team and found.player_or_basket == PieceType.PLAYER:
                        self.possible_moves.append((found.row, found.col))
                    break
                scan_down = scan_down + 1
            scan_up = piece_clicked.row - 1
            while scan_up >= 0:
                found = self.get_information(row=scan_up, col=piece_clicked.col)
                if found is not None:
                    if found.color.team == piece_clicked.color.team and found.player_or_basket == PieceType.PLAYER:
                        self.possible_moves.append((found.row, found.col))
                    break
                scan_up = scan_up - 1

    def make_possible_move(self, piece_clicked, row, col):
        self.piece_clicked = piece_clicked
        if (row, col) in self.possible_moves:
            if piece_clicked.has_ball and self.get_information(row=row, col=col) is not None:
                piece_clicked.has_ball = False
                self.get_information(row=row, col=col).has_ball = True
            else:
                old_row = piece_clicked.row
                old_col = piece_clicked.col
                if abs(row - old_row) == 2:
                    jumped = self.get_information(row=(old_row + row) // 2, col=(old_col + col) // 2)
                    if jumped is not None:
                        if jumped.player_or_basket == PieceType.BASKET and piece_clicked.has_ball == True:
                            self.game_over = True
                            self.winner = self.turn
                            jumped.has_ball = True
                            piece_clicked.has_ball = False
                        elif jumped.player_or_basket == PieceType.PLAYER:
                            self.piece_list.remove(jumped)
                            if jumped.has_ball:
                                jumped.has_ball = False
                                piece_clicked.has_ball = True
                piece_clicked.row = row
                piece_clicked.col = col
            self.possible_moves.clear()
            for piece in self.piece_list:
                if piece.color == Color.WEISS_AUSGEWAEHLT:
                    piece.color = Color.WEISS
                elif piece.color == Color.SCHWARZ_AUSGEWAEHLT:
                    piece.color = Color.SCHWARZ
            self.test_time_stay_basket()
            self.sanctions_time_stay_basket()
            if self.turn == Color.SCHWARZ:
                self.turn = Color.WEISS
            elif self.turn == Color.WEISS:
                self.turn = Color.SCHWARZ
            if piece_clicked.color == Color.SCHWARZ:
                if piece_clicked.direction == Direction.FORWARD:
                    if piece_clicked.row == 10:
                        piece_clicked.direction = Direction.BACKWARD
                if piece_clicked.direction == Direction.BACKWARD:
                    if piece_clicked.row == 0:
                        piece_clicked.direction = Direction.FORWARD
            if piece_clicked.color == Color.WEISS:
                if piece_clicked.direction == Direction.FORWARD:
                    if piece_clicked.row == 10:
                        piece_clicked.direction = Direction.BACKWARD
                if piece_clicked.direction == Direction.BACKWARD:
                    if piece_clicked.row == 0:
                        piece_clicked.direction = Direction.FORWARD

    def test_time_stay_basket(self):
        for piece in self.piece_list:
            if piece.player_or_basket == PieceType.PLAYER and piece.color == self.turn:
                if piece.col == 3:
                    if piece.row == 8 or piece.row == 10:
                        piece.time_stay_basket += 1
                        print(f"Momentane Zeit von Piece in Col 3 und Reihe {piece.row} um den Basket herum beträgt {piece.time_stay_basket}")
                    elif piece.row == 0 or piece.row == 2:
                        piece.time_stay_basket += 1
                        print(f"Momentane Zeit von Piece in Col 3 und Reihe {piece.row} um den Basket herum beträgt {piece.time_stay_basket}")
                    elif piece.time_stay_basket != 0:
                        piece.time_stay_basket = 0
                        print(f"Die Zeit von Piece {piece.row},{piece.col}(Row,Col) wurde zurückgesetzt auf {piece.time_stay_basket}")
                elif piece.col == 5:
                    if piece.row == 8 or piece.row == 10:
                        piece.time_stay_basket += 1
                        print(f"Momentane Zeit des Piece in Col 5 und Reihe {piece.row} um den Basket herum beträgt {piece.time_stay_basket}")
                    elif piece.row == 0 or piece.row == 2:
                        piece.time_stay_basket += 1
                        print(f"Momentane Zeit des Piece in Col 5 und Reihe {piece.row} um den Basket herum beträgt {piece.time_stay_basket}")
                    elif piece.time_stay_basket != 0:
                        piece.time_stay_basket = 0
                        print(f"Die Zeit von Piece {piece.row},{piece.col}(Row,Col) wurde zurückgesetzt auf {piece.time_stay_basket}")
                elif piece.col == 0 or piece.col == 1 or piece.col == 2 or piece.col == 4 or piece.col == 6 or piece.col == 7 or piece.col == 8:
                    if piece.time_stay_basket != 0:
                        piece.time_stay_basket = 0
                        print(f"Die Zeit von Piece {piece.row},{piece.col}(Row,Col) wurde zurückgesetzt auf {piece.time_stay_basket}")

    def sanctions_time_stay_basket(self):
        remove_pieces = []
        for piece in self.piece_list:
            if piece.time_stay_basket == 4:
                remove_pieces.append(piece)
        for piece in remove_pieces:
            if piece.has_ball == True:
                piece.has_ball = False
                for other in self.piece_list:
                    if other != piece and other not in remove_pieces and other.player_or_basket == PieceType.PLAYER and other.color != piece.color:
                        other.has_ball = True
                        print("Turn Over führte zu einem Ball Besitz Wechsel")
                        break
            self.piece_list.remove(piece)
            print(f"Piece auf {piece.row},{piece.col}(Row,Col) wurde entfernt, weil er zu lange um den Korb war")

    def bot_think(self):
        self.my_turn = False
        self.schwarz_has_ball = False
        self.collection_of_possible_moves = []

        self.info_has_bot_ball()


        self.shooter = self.get_information(row=8, col=3)
        if (
                    self.schwarz_has_ball
                    and not self.game_over
                    and self.shooter is not None
                    and self.shooter.color.team == Color.SCHWARZ
                    and self.shooter.has_ball
                    and self.get_information(row=10, col=5) is None
            ):
                self.show_possible_moves(cast(piece, self.shooter))
                if (10, 5) in self.possible_moves:
                    self.make_possible_move(cast(piece, self.shooter), 10, 5)
                    self.my_turn = True
                    return

        self.shooter = self.get_information(row=8, col=5)
        if (
                    self.schwarz_has_ball
                    and not self.game_over
                    and self.shooter is not None
                    and self.shooter.color.team == Color.SCHWARZ
                    and self.shooter.has_ball
                    and self.get_information(row=10, col=3) is None
            ):
                self.show_possible_moves(cast(piece, self.shooter))
                if (10, 3) in self.possible_moves:
                    self.make_possible_move(cast(piece, self.shooter), 10, 3)
                    self.my_turn = True
                    return

        self.shooter = self.get_information(row=10, col=3)
        if (
                self.schwarz_has_ball
                and not self.game_over
                and self.shooter is not None
                and self.shooter.color.team == Color.SCHWARZ
                and self.shooter.has_ball
                and self.get_information(row=8, col=5) is None
        ):
            self.show_possible_moves(cast(piece, self.shooter))
            if (10, 5) in self.possible_moves:
                self.make_possible_move(cast(piece, self.shooter), 10, 5)
                self.my_turn = True
                return

        self.shooter = self.get_information(row=10, col=5)
        if (
                self.schwarz_has_ball
                and not self.game_over
                and self.shooter is not None
                and self.shooter.color.team == Color.SCHWARZ
                and self.shooter.has_ball
                and self.get_information(row=8, col=3) is None
        ):
            self.show_possible_moves(cast(piece, self.shooter))
            if (10, 3) in self.possible_moves:
                self.make_possible_move(cast(piece, self.shooter), 10, 3)
                self.my_turn = True
                return

        self.block_row = None
        self.block_col = None

        self.attacker = self.get_information(row=2, col=3)
        if (
                not self.schwarz_has_ball
                and not self.game_over
                and self.attacker is not None
                and self.attacker.color.team == Color.WEISS
                and self.attacker.has_ball
                and self.get_information(row=0, col=5) is None
        ):
            self.block_row = 0
            self.block_col = 5

        self.attacker = self.get_information(row=2, col=5)
        if (
                not self.schwarz_has_ball
                and not self.game_over
                and self.attacker is not None
                and self.attacker.color.team == Color.WEISS
                and self.attacker.has_ball
                and self.get_information(row=0, col=3) is None
        ):
            self.block_row = 0
            self.block_col = 3


        for bot_piece in self.piece_list:
            if bot_piece.color == Color.SCHWARZ and bot_piece.player_or_basket == PieceType.PLAYER:

                self.has_bot_ball_ask(bot_piece)
                self.show_possible_moves(bot_piece)
                self.get_score_of_everyone(bot_piece)

        if not self.collection_of_possible_moves:
            self.my_turn = True
            return

        self.bot_next_move = max(self.collection_of_possible_moves, key=lambda x: x[0])

        if self.my_turn == False:
            self.distance_of_next_move, self.piece_clicked, self.move_row, self.move_col = self.bot_next_move
            self.show_possible_moves(self.piece_clicked)
            print(f"Hey die Figur {self.move_row, self.move_col} scheint mir der beste Zug zu sein in diesem Fall. Score: {self.distance_of_next_move}")
            self.make_possible_move(self.piece_clicked, self.move_row, self.move_col)

        self.my_turn = True # Muss am Ende sein damit Spieler wieder tippen kann!

    def info_has_bot_ball(self):
        for bot_piece in self.piece_list:
            if bot_piece.color == Color.SCHWARZ and bot_piece.has_ball == True:
                self.schwarz_has_ball = True

    def get_score_of_everyone(self, bot_piece): #hier startet score

        for move_row, move_col in self.possible_moves:
            self.which_distance = 2 * abs(self.goal_row - move_row) + abs(self.goal_col - move_col)
            self.score = -self.which_distance + random.random() * 0.01

            if move_row == self.block_row and move_col == self.block_col:
                self.score += 540

            if self.is_attackable(move_row, move_col, Color.WEISS, leaving=bot_piece):
                if bot_piece.has_ball or self.get_information(row=move_row, col=move_col) is not None:
                    self.score -= 460
                else:
                    self.score -= 35

            if self.get_information(((bot_piece.row + move_row) // 2), ((bot_piece.col + move_col) // 2)) is not None:
                piece_there = self.get_information(((bot_piece.row + move_row) // 2), ((bot_piece.col + move_col) // 2))
                if piece_there.color == Color.WEISS:
                    if piece_there.has_ball:
                        self.score += 700
                    else:
                        self.score += 8

            if self.get_information(bot_piece.row, bot_piece.col).time_stay_basket == 3:
                self.score += 16
            if self.get_information(bot_piece.row, bot_piece.col).time_stay_basket == 2:
                self.score += 8
            if self.get_information(bot_piece.row, bot_piece.col).time_stay_basket == 1:
                self.score += 3

            if move_row >= 7 and 2 <= move_col <= 6 and bot_piece.row <= 6 and self.schwarz_has_ball:
                self.score += 8

            if bot_piece.row == 0 and (bot_piece.col == 3 or bot_piece.col == 5) and not self.schwarz_has_ball:
                self.score -= 45

            if self.schwarz_has_ball:
                if bot_piece.row == 10 and (bot_piece.col == 3 or bot_piece.col == 5):
                    self.score += 90
                if move_row == 10 and (move_col == 3 or move_col == 5):
                    self.score -= 120
                if move_row == 8 and move_col == 5 and bot_piece.has_ball:
                    self.score += 400
                if move_row == 8 and move_col == 3 and bot_piece.has_ball:
                    self.score += 400
                if not bot_piece.has_ball:
                    self.score -= 80
                if bot_piece.row == move_row:
                    self.score -= 12

            self.collection_of_possible_moves.append((self.score, bot_piece, move_row, move_col))

    def has_bot_ball_ask(self, bot_piece):

        if self.schwarz_has_ball and not self.game_over:
            self.goal_row = 8
            nearer_to_83 =  2 * abs(8 - bot_piece.row) + abs(3 - bot_piece.col)
            nearer_to_85 =  2 * abs(8 - bot_piece.row) + abs(5 - bot_piece.col)

            if nearer_to_83 < nearer_to_85:
                self.goal_col = 3
            else:
                self.goal_col = 5

        elif not self.schwarz_has_ball and not self.game_over and self.my_turn == False:
            for weiss_piece in self.piece_list:
                if weiss_piece.color == Color.WEISS and weiss_piece.player_or_basket == PieceType.PLAYER and weiss_piece.has_ball == True:
                    self.goal_row = weiss_piece.row
                    self.goal_col = weiss_piece.col
                    break

    def is_attackable(self, row, col, by_color, leaving=None):
        for enemy in self.piece_list:
            if enemy.player_or_basket != PieceType.PLAYER or enemy.color.team != by_color:
                continue
            if abs(enemy.row - row) != 1 or abs(enemy.col - col) != 1:
                continue
            if enemy.direction == Direction.FORWARD and row != enemy.row + 1:
                continue
            if enemy.direction == Direction.BACKWARD and row != enemy.row - 1:
                continue
            land_row = 2 * row - enemy.row
            land_col = 2 * col - enemy.col
            if not (0 <= land_row <= 10 and 0 <= land_col <= 8):
                continue
            landing = self.get_information(row=land_row, col=land_col)
            if landing is None or (leaving is not None and landing is leaving):
                return True
        return False



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def bot_think_simulation(self):
        self.my_turn = False
        self.schwarz_has_ball = True
        self.collection_of_possible_moves = []

        self.info_has_bot_ball_simulation()


        self.shooter = self.get_information(row=2, col=3)
        if (
                    not self.schwarz_has_ball
                    and not self.game_over
                    and self.shooter is not None
                    and self.shooter.color.team == Color.WEISS
                    and self.shooter.has_ball
                    and self.get_information(row=0, col=5) is None
            ):
                self.show_possible_moves(cast(piece, self.shooter))
                if (0, 5) in self.possible_moves:
                    self.make_possible_move(cast(piece, self.shooter), 0, 5)
                    self.my_turn = True
                    return

        self.shooter = self.get_information(row=2, col=5)
        if (
                    not self.schwarz_has_ball
                    and not self.game_over
                    and self.shooter is not None
                    and self.shooter.color.team == Color.WEISS
                    and self.shooter.has_ball
                    and self.get_information(row=0, col=3) is None
            ):
                self.show_possible_moves(cast(piece, self.shooter))
                if (0, 3) in self.possible_moves:
                    self.make_possible_move(cast(piece, self.shooter), 0, 3)
                    self.my_turn = True
                    return

        self.shooter = self.get_information(row=0, col=3)
        if (
                not self.schwarz_has_ball
                and not self.game_over
                and self.shooter is not None
                and self.shooter.color.team == Color.WEISS
                and self.shooter.has_ball
                and self.get_information(row=2, col=5) is None
        ):
            self.show_possible_moves(cast(piece, self.shooter))
            if (0, 5) in self.possible_moves:
                self.make_possible_move(cast(piece, self.shooter), 0, 5)
                self.my_turn = True
                return

        self.shooter = self.get_information(row=0, col=5)
        if (
                not self.schwarz_has_ball
                and not self.game_over
                and self.shooter is not None
                and self.shooter.color.team == Color.WEISS
                and self.shooter.has_ball
                and self.get_information(row=2, col=3) is None
        ):
            self.show_possible_moves(cast(piece, self.shooter))
            if (0, 3) in self.possible_moves:
                self.make_possible_move(cast(piece, self.shooter), 0, 3)
                self.my_turn = True
                return

        self.block_row = None
        self.block_col = None

        self.attacker = self.get_information(row=8, col=3)
        if (
                self.schwarz_has_ball
                and not self.game_over
                and self.attacker is not None
                and self.attacker.color.team == Color.SCHWARZ
                and self.attacker.has_ball
                and self.get_information(row=10, col=5) is None
        ):
            self.block_row = 10
            self.block_col = 5

        self.attacker = self.get_information(row=8, col=5)
        if (
                self.schwarz_has_ball
                and not self.game_over
                and self.attacker is not None
                and self.attacker.color.team == Color.SCHWARZ
                and self.attacker.has_ball
                and self.get_information(row=10, col=3) is None
        ):
            self.block_row = 10
            self.block_col = 3


        for bot_piece in self.piece_list:
            if bot_piece.color == Color.WEISS and bot_piece.player_or_basket == PieceType.PLAYER:

                self.has_bot_ball_ask_simulation(bot_piece)
                self.show_possible_moves(bot_piece)
                self.get_score_of_everyone_simulation(bot_piece)

        if not self.collection_of_possible_moves:
            self.my_turn = True
            return

        self.bot_next_move = max(self.collection_of_possible_moves, key=lambda x: x[0])

        if self.my_turn == False:
            self.distance_of_next_move, self.piece_clicked, self.move_row, self.move_col = self.bot_next_move
            self.show_possible_moves(self.piece_clicked)
            print(f"Hey die Figur {self.move_row, self.move_col} scheint mir der beste Zug zu sein in diesem Fall. Score: {self.distance_of_next_move}")
            self.make_possible_move(self.piece_clicked, self.move_row, self.move_col)

        self.my_turn = True # Muss am Ende sein damit Spieler wieder tippen kann!

    def has_bot_ball_ask_simulation(self, bot_piece):

        if not self.schwarz_has_ball and not self.game_over:
            self.goal_row = 2
            nearer_to_13 =  2 * abs(2 - bot_piece.row) + abs(3 - bot_piece.col)
            nearer_to_15 =  2 * abs(2 - bot_piece.row) + abs(5 - bot_piece.col)

            if nearer_to_13 < nearer_to_15:
                self.goal_col = 3
            else:
                self.goal_col = 5

        elif self.schwarz_has_ball and not self.game_over and self.my_turn == False:
            for schwarz_piece in self.piece_list:
                if schwarz_piece.color == Color.SCHWARZ and schwarz_piece.player_or_basket == PieceType.PLAYER and schwarz_piece.has_ball == True:
                    self.goal_row = schwarz_piece.row
                    self.goal_col = schwarz_piece.col
                    break

    def info_has_bot_ball_simulation(self):

        for bot_piece in self.piece_list:
            if bot_piece.color == Color.WEISS and bot_piece.has_ball == True:
                self.schwarz_has_ball = False

    def get_score_of_everyone_simulation(self, bot_piece): #hier startet score

        for move_row, move_col in self.possible_moves:
            self.which_distance = 2 * abs(self.goal_row - move_row) + abs(self.goal_col - move_col)
            self.score = -self.which_distance + random.random() * 0.01

            if move_row == self.block_row and move_col == self.block_col:
                self.score += 540

            if self.is_attackable(move_row, move_col, Color.SCHWARZ, leaving=bot_piece):
                if bot_piece.has_ball or self.get_information(row=move_row, col=move_col) is not None:
                    self.score -= 460
                else:
                    self.score -= 35

            if self.get_information(((bot_piece.row + move_row) // 2), ((bot_piece.col + move_col) // 2)) is not None:
                piece_there = self.get_information(((bot_piece.row + move_row) // 2), ((bot_piece.col + move_col) // 2))
                if piece_there.color == Color.SCHWARZ:
                    if piece_there.has_ball:
                        self.score += 700
                    else:
                        self.score += 8

            if self.get_information(bot_piece.row, bot_piece.col).time_stay_basket == 3:
                self.score += 16
            if self.get_information(bot_piece.row, bot_piece.col).time_stay_basket == 2:
                self.score += 8
            if self.get_information(bot_piece.row, bot_piece.col).time_stay_basket == 1:
                self.score += 3

            if move_row <= 3 and 2 <= move_col <= 6 and bot_piece.row >= 4 and not self.schwarz_has_ball:
                self.score += 8

            if bot_piece.row == 10 and (bot_piece.col == 3 or bot_piece.col == 5) and self.schwarz_has_ball:
                self.score -= 45

            if not self.schwarz_has_ball:
                if bot_piece.row == 0 and (bot_piece.col == 3 or bot_piece.col == 5):
                    self.score += 90
                if move_row == 0 and (move_col == 3 or move_col == 5):
                    self.score -= 120
                if move_row == 2 and move_col == 5 and bot_piece.has_ball:
                    self.score += 400
                if move_row == 2 and move_col == 3 and bot_piece.has_ball:
                    self.score += 400
                if not bot_piece.has_ball:
                    self.score -= 80
                if bot_piece.row == move_row:
                    self.score -= 12

            self.collection_of_possible_moves.append((self.score, bot_piece, move_row, move_col))

