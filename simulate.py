"""Monte Carlo Analyse des Bots, ohne Fenster.

Startet viele Spiele mit festen Seeds und misst:
  1. Bot gegen Bot: Siegquote pro Team, Vorteil des Startteams, Spiellänge
  2. Bot gegen Zufall: wie stark ist der Bot gegen eine Zufallsstrategie

Start:  python simulate.py           (2000 Spiele pro Experiment)
        python simulate.py 10000
"""
import contextlib
import io
import math
import random
import sys
from collections import Counter

from board import Board
from Piece import Color, PieceType

MAX_PLIES = 400  # Ein Spiel ohne Sieger nach 400 Halbzügen zählt als offen


def random_policy(board):
    """Wählt einen zufälligen legalen Zug für Weiss."""
    moves = []
    for p in list(board.piece_list):
        if p.color == Color.WEISS and p.player_or_basket == PieceType.PLAYER:
            board.show_possible_moves(p)
            moves += [(p, r, c) for r, c in board.possible_moves]
    if moves:
        p, r, c = random.choice(moves)
        board.show_possible_moves(p)
        board.make_possible_move(p, r, c)


def play(seed, white_policy):
    """Spielt ein Spiel. Gleicher Seed gibt das gleiche Spiel."""
    random.seed(seed)
    board = Board(row=11, col=9)
    with contextlib.redirect_stdout(io.StringIO()):  # Prints von board.py ausblenden
        board.setup_board(against_bot=False)
        starter = board.turn
        plies = 0
        while not board.game_over and plies < MAX_PLIES:
            if board.turn == Color.SCHWARZ:
                board.bot_think()
                board.turn = Color.WEISS
            else:
                white_policy(board)
                board.turn = Color.SCHWARZ
            plies += 1
    return starter, board.winner, plies


def wilson(k, n, z=1.96):
    """95 % Konfidenzintervall für eine Quote k / n (Wilson)."""
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return centre - half, centre + half


def rate(k, n):
    lo, hi = wilson(k, n)
    return f"{k / n:6.1%}  (95 % CI {lo:.1%} bis {hi:.1%})"


def report(title, results):
    done = [r for r in results if r[1] is not None]
    n = len(done)
    wins = Counter(r[1] for r in done)
    lengths = sorted(r[2] for r in done)
    print(f"\n{title}")
    print(f"  Spiele {len(results)}, mit Sieger {n}, offen {len(results) - n}")
    for team in (Color.SCHWARZ, Color.WEISS):
        print(f"  {team.value:8} gewinnt {rate(wins[team], n)}")
    print(f"  Startteam gewinnt {rate(sum(r[0] == r[1] for r in done), n)}")
    print(f"  Halbzüge: Median {lengths[n // 2]}, P10 {lengths[n // 10]}, P90 {lengths[n * 9 // 10]}")


if __name__ == "__main__":
    games = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    report("Bot gegen Bot", [play(s, Board.bot_think_simulation) for s in range(games)])
    report("Bot (Schwarz) gegen Zufall (Weiss)", [play(s, random_policy) for s in range(games)])
