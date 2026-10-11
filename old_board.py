from Piece import piece, Color, Direction, PieceType
import random
import math



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
        if piece_clicked.direction == Direction.FORWARD:
            if self.get_information(row=(piece_clicked.row + 1), col=(piece_clicked.col - 1)) is None and 0 <= (piece_clicked.row + 1) <= 10 and 0 <= (piece_clicked.col - 1) <= 8:  # links
                self.possible_moves.append((piece_clicked.row + 1, piece_clicked.col - 1))
            if self.get_information(row=(piece_clicked.row + 1), col=(piece_clicked.col + 1)) is None and 0 <= (piece_clicked.row + 1) <= 10 and 0 <= (piece_clicked.col + 1) <= 8:  # rechts
                self.possible_moves.append((piece_clicked.row + 1, piece_clicked.col + 1))
            if self.get_information(row=(piece_clicked.row + 1), col=(piece_clicked.col - 1)) is not None and self.get_information(row=(piece_clicked.row + 1), col=(piece_clicked.col - 1)).color.team != piece_clicked.color.team and 0 <= (piece_clicked.row + 1) <= 10 and 0 <= (piece_clicked.col - 1) <= 8:
                if self.get_information(row=(piece_clicked.row + 2), col=(piece_clicked.col - 2)) is None and 0 <= (piece_clicked.row + 2) <= 10 and 0 <= (piece_clicked.col - 2) <= 8:  # links KILL
                    self.possible_moves.append((piece_clicked.row + 2, piece_clicked.col - 2))
            if self.get_information(row=(piece_clicked.row + 1), col=(piece_clicked.col + 1)) is not None and self.get_information(row=(piece_clicked.row + 1), col=(piece_clicked.col + 1)).color.team != piece_clicked.color.team and 0 <= (piece_clicked.row + 1) <= 10 and 0 <= (piece_clicked.col + 1) <= 8:
                if self.get_information(row=(piece_clicked.row + 2), col=(piece_clicked.col + 2)) is None and 0 <= (piece_clicked.row + 2) <= 10 and 0 <= (piece_clicked.col + 2) <= 8:  # rechts KILL
                    self.possible_moves.append((piece_clicked.row + 2, piece_clicked.col + 2))

        if piece_clicked.direction == Direction.BACKWARD:
            if self.get_information(row=(piece_clicked.row - 1), col=(piece_clicked.col - 1)) is None and 0 <= (piece_clicked.row - 1) <= 10 and 0 <= (piece_clicked.col - 1) <= 8:  # links
                self.possible_moves.append((piece_clicked.row - 1, piece_clicked.col - 1))
            if self.get_information(row=(piece_clicked.row - 1), col=(piece_clicked.col + 1)) is None and 0 <= (piece_clicked.row - 1) <= 10 and 0 <= (piece_clicked.col + 1) <= 8:  # rechts
                self.possible_moves.append((piece_clicked.row - 1, piece_clicked.col + 1))
            if self.get_information(row=(piece_clicked.row - 1), col=(piece_clicked.col - 1)) is not None and self.get_information(row=(piece_clicked.row - 1), col=(piece_clicked.col - 1)).color.team != piece_clicked.color.team and 0 <= (piece_clicked.row - 1) <= 10 and 0 <= (piece_clicked.col - 1) <= 8:
                if self.get_information(row=(piece_clicked.row - 2), col=(piece_clicked.col - 2)) is None and 0 <= (piece_clicked.row - 2) <= 10 and 0 <= (piece_clicked.col - 2) <= 8:  # links KILL
                    self.possible_moves.append((piece_clicked.row - 2, piece_clicked.col - 2))
            if self.get_information(row=(piece_clicked.row - 1), col=(piece_clicked.col + 1)) is not None and self.get_information(row=(piece_clicked.row - 1), col=(piece_clicked.col + 1)).color.team != piece_clicked.color.team and 0 <= (piece_clicked.row - 1) <= 10 and 0 <= (piece_clicked.col + 1) <= 8:
                if self.get_information(row=(piece_clicked.row - 2), col=(piece_clicked.col + 2)) is None and 0 <= (piece_clicked.row - 2) <= 10 and 0 <= (piece_clicked.col + 2) <= 8:  # rechts KILL
                    self.possible_moves.append((piece_clicked.row - 2, piece_clicked.col + 2))


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
        self.no_move_made = True
        self.schwarz_has_ball = False



        for bot_piece in self.piece_list:
            if bot_piece.color == Color.SCHWARZ and bot_piece.has_ball == True:
                self.schwarz_has_ball = True

        if self.schwarz_has_ball:
            self.goal_row = 9
            self.goal_col = 4

        self.collection_of_possible_moves = []
        if self.schwarz_has_ball and not self.game_over:
            for bot_piece in self.piece_list:
                if bot_piece.color == Color.SCHWARZ and bot_piece.player_or_basket == PieceType.PLAYER and bot_piece.has_ball == True:
                    self.show_possible_moves(bot_piece)
                    for move_row, move_col in self.possible_moves:
                        self.which_distance = math.dist((self.goal_row, self.goal_col), (move_row, move_col))
                        self.collection_of_possible_moves.append((self.which_distance, bot_piece, move_row, move_col))

            self.collection_of_possible_moves.sort(key=lambda x: x[0], reverse=False)
            if self.collection_of_possible_moves:
                self.distance_of_next_move, self.piece_clicked, self.move_row, self.move_col = self.collection_of_possible_moves[0]
                print(f"Hey die Figur {self.move_row, self.move_col} scheint mir der beste Zug zu sein in diesem Fall. Distanz: {self.distance_of_next_move}")

                self.show_possible_moves(self.piece_clicked)
                self.make_possible_move(self.piece_clicked, self.move_row, self.move_col)


        if not self.schwarz_has_ball and not self.game_over:
            for piece in self.piece_list:
                if piece.color == Color.WEISS and piece.player_or_basket == PieceType.PLAYER and piece.has_ball == True:
                    self.goal_row = piece.row
                    self.goal_col = piece.col
                    break

            for bot_piece in self.piece_list:
                if bot_piece.color == Color.SCHWARZ and bot_piece.player_or_basket == PieceType.PLAYER and self.no_move_made:
                    self.show_possible_moves(bot_piece)
                    for move_row, move_col in self.possible_moves:
                        if self.goal_row == (bot_piece.row + move_row) // 2 and self.goal_col == (bot_piece.col + move_col) // 2:
                            self.piece_clicked = bot_piece
                            print(f"Hey die Figur {self.piece_clicked} scheint mir der beste Zug zu sein in diesem Fall. Überspringen war möglich!")

                            self.show_possible_moves(self.piece_clicked)
                            self.make_possible_move(self.piece_clicked, move_row, move_col)
                            self.no_move_made = False
                            break

            if self.no_move_made:
                self.collection_of_possible_moves = []
                for bot_piece in self.piece_list:
                    if bot_piece.color == Color.SCHWARZ and bot_piece.player_or_basket == PieceType.PLAYER:
                        self.show_possible_moves(bot_piece)
                        for move_row, move_col in self.possible_moves:
                            self.which_distance = math.dist((self.goal_row, self.goal_col), (move_row, move_col))
                            self.collection_of_possible_moves.append((self.which_distance, bot_piece, move_row, move_col))

                self.collection_of_possible_moves.sort(key=lambda x: x[0], reverse=False)
                if self.collection_of_possible_moves:
                    self.distance_of_next_move, self.piece_clicked, self.move_row, self.move_col = self.collection_of_possible_moves[0]
                    print(f"(391)Hey die Figur {self.move_row, self.move_col} scheint mir der beste Zug zu sein in diesem Fall. Distanz: {self.distance_of_next_move}")

                    self.show_possible_moves(self.piece_clicked)
                    self.make_possible_move(self.piece_clicked, self.move_row, self.move_col)
                    self.no_move_made = False


        self.my_turn = True # Muss am Ende sein damit Spieler wieder tippen kann!!!!!!!
