from app.game.GameEnums import *
import pygame
import os

# Classe que representa uma peça do jogo, quando instanciada ela recebe um valor e uma cor,
# assim como o caminho do seu sprite.
class Piece(object):
    def __init__(self, value: PieceValue, color: PieceColor):
        self.value = value
        self.color = color
        self.whereAt = PieceLocale.DECK
        self.originalPlace = (0, 0)
        if value != PieceValue.BLANK:
            if value != PieceValue.JOKER:
                self.image: pygame.image = pygame.image.load(os.path.join('resources/pieces',
                                                                          color.name.lower() + "_" + str(
                                                                              value.value) + ".png"))
            else:
                self.image = pygame.image.load(
                    os.path.join('resources/pieces', color.name.lower() + "_1.png"))
            self.rect: pygame.Rect = self.image.get_rect()

    def toString(self):
        return str(self.value.value) + "-" + self.color.value

    def show(self):
        print("{} - {} ".format(self.color, self.value))