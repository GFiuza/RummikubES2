import random
from typing import List
from app.game.Piece import *

turn_buttons_y = Size.WindowHeight * 3 / 4
turn_buttons_x = Size.WindowWidth * 6 / 7

sort_buttons_y = Size.WindowHeight * 3 / 4 + 10
sort_buttons_x = Size.WindowWidth * 7 / 9

buttons_offset = 50


class PlayerInfoCard(object):
    def __init__(self, player_index: int, name: str):
        player_board_offset_x = Size.WindowWidth * 91 / 100
        player_board_offset_y = Size.WindowHeight * ( 1 + player_index) / 7

        self.playerName = name
        self.playerId = player_index
        self.cardImage = pygame.image.load(os.environ.get("player_board"))  # Caminho da imagem
        self.cardRect: pygame.Rect = self.cardImage.get_rect()  # 'hitbox' da imagem
        self.cardRect.center = (player_board_offset_x, player_board_offset_y)

        self.playerFont = pygame.font.Font(os.environ.get("player_font"), 30)
        self.playerDisplay = self.playerFont.render(self.playerName, False, (155, 100, 100))
        self.playerDisplayPos = (self.cardRect.x + 15, self.cardRect.y + self.cardRect.height / 2 -
                                 self.playerFont.get_height() / 2)

        self.cardCountDisplay = self.playerFont.render('0', False, (190, 50, 0))

        self.cardCountDisplayPos = (self.cardRect.x + self.cardRect.width * 8/10, self.cardRect.y +
                                    self.cardRect.height / 2 - self.playerFont.get_height() / 2)

    def display_name(self, card_count: str):
        self.playerDisplay = self.playerFont.render(self.playerName, False, (100, 55, 155))
        self.cardCountDisplay = self.playerFont.render(card_count, False, (190, 50, 0))
