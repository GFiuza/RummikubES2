from enum import Enum, IntEnum


# Arquivos de enumeradores para melhor organização

class Table(Enum):
    ROWS = 8
    COLUMNS = 24


class Size(IntEnum):
    WindowHeight = 720
    WindowWidth = 1280  # Window Height and Width


class PieceValue(IntEnum):
    JOKER = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    THIRTEEN = 13


class Color(Enum):
    RED = 'Red'
    BLUE = 'Blue'
    BLACK = 'Black'
    YELLOW = 'Yellow'
    JOKER = 'Joker'


class PieceLocale(Enum):
    DECK = 0
    TABLE = 1
    HAND = 2


class RGB(Enum):
    BOARD_GREEN = 30, 120, 30
    BOARD_BLACK = 0, 0, 0
