from enum import Enum


class Color(Enum):
    SCHWARZ = "Schwarz"
    WEISS = "Weiss"
    SCHWARZ_AUSGEWAEHLT = "Schwarz ausgewählt"
    WEISS_AUSGEWAEHLT = "Weiss ausgewählt"

    @property # visuelle in logische umwandeln. Lani evt noch nachfragen
    def team(self):
        if self in (Color.SCHWARZ, Color.SCHWARZ_AUSGEWAEHLT):
            return Color.SCHWARZ
        return Color.WEISS


class Direction(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"


class PieceType(Enum):
    PLAYER = "player"
    BASKET = "basket"


class piece:
    def __init__(self, row, col, color, direction, player_or_basket, has_ball):
        self.row = row
        self.col = col
        self.color = color
        self.direction = direction
        self.player_or_basket = player_or_basket
        self.has_ball = has_ball
        self.time_stay_basket = 0


    def __repr__(self):
        return f"{self.color.value[0]}({self.row},{self.col}, {self.direction.value}, {self.player_or_basket.value}. {self.has_ball}), Um Basketballfeld Zeit:{self.time_stay_basket}"
