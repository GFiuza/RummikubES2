import pygame
from game.GameEnums import *
import random
import os.path

from game.GameSprites import Path


# Classe que representa a matriz do tabuleiro, na grid
class Table(object):
    def __init__(self):
        self.tabuleiro = [[] * Table.ROWS.value for i in range(Table.COLUMNS.value)]


# Classe que representa uma peça do jogo, quando instanciada ela recebe um valor e uma cor,
# assim como o caminho do seu sprite.
class Piece(object):
    def __init__(self, value: PieceValue, color: Color):
        self.value = value
        self.color = color
        self.whereAt = PieceLocale.DECK
        if value != PieceValue.JOKER:
            self.image = pygame.image.load(os.path.join(os.path.os.path.curdir, '..', 'sprites/pieces',
                                                        color.name.lower() + "_" + str(value.value) + ".png"))
        else:
            self.image = pygame.image.load(
                os.path.join(os.path.os.path.curdir, '..', 'sprites/pieces', color.name.lower() + "_1.png"))
        self.rect = self.image.get_rect()

    def show(self):
        print("{} - {} ".format(self.color, self.value))


# Classe que representa o 'deck' de peças, quando instanciado ele chama a função build()
# que popula com todas as 104 peças
class Deck(object):
    def __init__(self):
        self.pieces = []
        self.build()
        self.drawButtnImage = pygame.image.load(Path.draw_unlock)  # Caminho da imagem
        self.drawButtnRect = self.drawButtnImage.get_rect()  # 'hitbox' da imagem

    # Popula um deck de 104 pecas
    def build(self):
        for color in Color:
            for value in PieceValue:
                if value == PieceValue.JOKER or color == Color.JOKER:
                    continue
                self.pieces.append(Piece(value, color))
                self.pieces.append(Piece(value, color))
        self.pieces.append(Piece(PieceValue.JOKER, Color.JOKER))
        self.pieces.append(Piece(PieceValue.JOKER, Color.JOKER))

    # Realiza um shuffle
    def shuffle(self):
        for i in range(len(self.pieces) - 1, 0, -1):
            r = random.randint(0, i)
            self.pieces[i], self.pieces[r] = self.pieces[r], self.pieces[i]

    # Função que remove uma peça do deck
    def drawpiece(self):
        if not self.is_empty():
            return self.pieces.pop()

    # Print das peças no terminal
    def show(self):
        for p in self.pieces:
            p.show()

    # Verifica se o deck esta vazio ou não
    def is_empty(self):
        if len(self.pieces) == 0:
            return True
        return False


# Classe que representa um jogador, que possui name, id e uma mão
class Player(object):
    def __init__(self, name, id):
        self.name = name
        self.hand = []
        self.id = id

    # Método em que o jogador adiciona à mão dele uma peça do deck
    def draw(self, deck):
        self.hand.append(deck.drawPiece())
        return self

    # Mostra a mão do jogador no terminal
    def show_hand(self):
        print("Mao de {}:".format(self.name))
        for piece in self.hand:
            piece.show()

    # todo sorting de mão
    # def sortHand(self):
