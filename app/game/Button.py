import random
from typing import List
from app.game.Piece import *


class Button(object):
    def __init__(self):
        #Botao de comprar peca
        self.drawButtnImage = pygame.image.load(os.environ.get("draw_unlock"))  # Caminho da imagem
        self.drawButtnRect: pygame.Rect = self.drawButtnImage.get_rect()  # 'hitbox' da imagem
        self.drawButtnRect.center = (Size.WindowWidth * 0.87, 2 * Size.WindowHeight / 3)
        self.drawButtnOnHover = False

        #Botao de confirmar turno
        self.validateTurnImage = pygame.image.load(os.environ.get("end_turn"))
        self.validadeTurnRect = pygame.Rect = self.validateTurnImage.get_rect()
        self.validadeTurnRect.center = (Size.WindowWidth * 0.94, 2 * Size.WindowHeight / 3)
        self.validadeTurnOnHover = False

    def button_reset_pos(self):
        self.drawButtnRect.center = (Size.WindowWidth * 0.87, 2 * Size.WindowHeight / 3)
        self.validadeTurnRect.center = (Size.WindowWidth * 0.94, 2 * Size.WindowHeight / 3)