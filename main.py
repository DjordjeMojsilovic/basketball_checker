import pygame
from board import Board
from Piece import Color, PieceType
WIDTH = 800
HEIGHT = 800

def ask_mode():
    print("Modus:")
    print("  bot / b          gegen Bot")
    print("  1v1 / 1 / v      1 gegen 1")
    print("  simulation / s   Simulation")

    while True:
        choice = input("> ").strip().lower().replace(" ", "")

        if choice in ("bot", "b"):
            return True, False          # against_bot, simulation
        if choice in ("1v1", "1", "v"):
            return False, False
        if choice in ("simulation", "s"):
            pygame.time.wait(500)
            return False, True

        print("Geht nicht. bot, 1v1 oder simulation.")

against_bot, simulation = ask_mode()


pygame.init() # Hier beginnts

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basketball Checker")
running = True
board = Board(row=11, col=9)
font = pygame.font.SysFont(None, 40)
start_ticks = pygame.time.get_ticks()
end_ticks = None
info_of_piece = None
color = "gray88"
outline = "gray40"
till_close_yourself = 0
board.setup_board(against_bot)

# Hier startet das eigentliche Spieel
while running:

    if against_bot:
        if board.turn == Color.SCHWARZ and not board.game_over and not simulation:
            board.bot_think()
            pygame.time.wait(500)
            board.turn = Color.WEISS
            board.my_turn = True
        elif board.turn == Color.WEISS:
            board.my_turn = True
    elif not simulation and not board.game_over:
        board.my_turn = True

    if simulation and not board.game_over and not against_bot:
        if board.turn == Color.SCHWARZ:
            board.bot_think() #black
            pygame.time.wait(500)
            board.turn = Color.WEISS
            board.my_turn = True
        elif board.turn == Color.WEISS:
            board.bot_think_simulation() #white
            pygame.time.wait(500)
            board.turn = Color.SCHWARZ
            board.my_turn = False
    # 1. Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and board.game_over == False and simulation == False:
            if board.my_turn == True:
                mouse_x, mouse_y = event.pos
                position_x = (mouse_x - 175) // 50
                position_y = (mouse_y - 150) // 50
                if 0 <= position_x <= 8 and 0 <= position_y <= 10:
                    print("Koordinaten:", "Row: ", position_y, "Collumn: ", position_x)
                    if board.get_information(row=position_y, col=position_x) is not None:
                        print(board.get_information(row=position_y, col=position_x))
                    if board.get_information(row=position_y, col=position_x) is not None and board.get_information(row=position_y, col=position_x).player_or_basket == PieceType.PLAYER and (position_y,position_x) not in board.possible_moves and board.get_information(row=position_y, col=position_x).color == board.turn and board.my_turn:
                        info_of_piece = board.get_information(row=position_y, col=position_x)
                        board.show_that_clicked_piece(info_of_piece)
                        board.show_possible_moves(info_of_piece)
                        board.my_turn = False
                    if board.my_turn:
                        board.make_possible_move(piece_clicked=info_of_piece, row=position_y, col=position_x)
                        board.my_turn = False

                    if board.get_information(row=position_y, col=position_x) is None and board.my_turn:
                        info_of_piece = board.get_information(row=position_y, col=position_x)
                        board.possible_moves.clear()
                        board.show_that_clicked_piece(info_of_piece)
                        board.my_turn = False

    # 2. Updates

    # 3. Zeichnen
    if board.turn == Color.SCHWARZ:
        screen.fill("grey8")
    elif board.turn == Color.WEISS:
        screen.fill("gray8")
    if board.game_over:
        screen.fill("darkorange")
    for row in range(11):
        for column in range(9):

            x = column * 50 + 175
            y = row * 50 + 150

            if (row + column) % 2 == 0:
                if (row, column) in board.possible_moves:
                    color = "gray36"
                else:
                    color = "gray22"
            elif (row + column) % 2 == 1:
                if (row, column) in board.possible_moves:
                    color = "gray36"
                else:
                    color = "gray14"


            pygame.draw.rect(screen , color, (x, y, 50, 50))



    for piece in board.piece_list:
        center_x = piece.col * 50 + 175 + 25
        center_y = piece.row * 50 + 150 + 25
        if piece.color == Color.SCHWARZ:
            color = "gray8"
            if board.turn == Color.SCHWARZ:
                outline = "darkorange2"
            else:
                outline = "gray60"
        elif piece.color == Color.WEISS:
            color = "gray88"
            if board.turn == Color.WEISS:
                outline = "darkorange2"
            else:
                outline = "gray40"
        elif piece.color == Color.WEISS_AUSGEWAEHLT:
            color = "gray88"
            outline = "chocolate1"
        elif piece.color == Color.SCHWARZ_AUSGEWAEHLT:
            color = "gray8"
            outline = "chocolate1"


        pygame.draw.circle(screen, outline, (center_x, center_y), 20)
        pygame.draw.circle(screen, color, (center_x, center_y), 16)
        if piece.player_or_basket == PieceType.BASKET:
            pygame.draw.circle(screen, "chocolate1", (center_x, center_y), 20)
            pygame.draw.circle(screen, "gray10", (center_x, center_y), 16)
            pygame.draw.circle(screen, "chocolate1", (center_x, center_y), 8, 3)
        if piece.has_ball == True:
            pygame.draw.circle(screen, "chocolate1", (center_x, center_y), 12)
        if piece.time_stay_basket == 1:
            pygame.draw.circle(screen, "gold", (center_x, center_y), 5)
        if piece.time_stay_basket == 2:
            pygame.draw.circle(screen, "lightsalmon1", (center_x, center_y), 5)
        if piece.time_stay_basket == 3:
            pygame.draw.circle(screen, "firebrick2", (center_x, center_y), 5)

    if board.game_over and end_ticks is None:
        end_ticks = pygame.time.get_ticks()
    if board.game_over:
        current_ticks = end_ticks
    else:
        current_ticks = pygame.time.get_ticks()
    total_seconds = (current_ticks - start_ticks) // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    time_text = f"{minutes:02}:{seconds:02}"

    if board.game_over:

        till_close_yourself += 1
        label = font.render(time_text + "  " + board.winner.value + " gewinnt!", True, "white")
        if till_close_yourself == 20:
            running = False
            print("Spiel beendet.")
        if not till_close_yourself == 1:
            pygame.time.wait(1000)
        print(f"{20 - till_close_yourself} Sekunden verbleibend bis zur automatischen Schliessung")
    else:
        label = font.render(time_text, True, "white")
    screen.blit(label, (280, 60))
    pygame.display.flip()  # updated den Screen
    pygame.time.wait(0)


# Hier endet das eigentliche Spiel
pygame.quit() # Hier endet alles