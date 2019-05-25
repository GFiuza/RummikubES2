from app.game.GameEnums import *
import pygame
import os

# Classe que representa uma peça do jogo, quando instanciada ela recebe um valor e uma cor,
# assim como o caminho do seu sprite.


class Piece(object):
    def __init__(self, value: PieceValue, color: PieceColor, id: int):
        self.value = value
        self.color = color
        self.id = id
        self.whereAt = PieceLocale.DECK
        self.originalPlace = (0, 0)
        self.onHover = False
        if value != PieceValue.BLANK:
            if value != PieceValue.JOKER:
                self.image: pygame.image = pygame.image.load(os.path.join(os.environ.get("pieces"),
                                                                          color.name.lower() + "_" + str(
                                                                              value.value) + ".png"))
            else:
                self.image = pygame.image.load(
                    os.path.join(os.environ.get("pieces"), color.name.lower() + "_1.png"))
            self.rect: pygame.Rect = self.image.get_rect()

    def __str__(self):
        return str(self.value.value) + "-" + str(self.color.value) + "/" + str(self.id) + "/" + str(self.whereAt)

    def show(self):
        print("{} - {} / {}".format(self.color, self.value, self.id))
