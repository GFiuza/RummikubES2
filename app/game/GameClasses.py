import pygame
from app.game.GameEnums import *
from typing import List, Tuple
import random
import os.path


# Classe que representa uma peça do jogo, quando instanciada ela recebe um valor e uma cor,
# assim como o caminho do seu sprite.
class Piece(object):
    def __init__(self, value: PieceValue, color: Color):
        self.value = value
        self.color = color
        self.whereAt = PieceLocale.DECK
        self.originalPlace = (0, 0)
        if value != PieceValue.BLANK:
            if value != PieceValue.JOKER:
                self.image: pygame.image = pygame.image.load(os.path.join('resources/pieces',
                                                             color.name.lower() + "_" + str(value.value) + ".png"))
            else:
                self.image = pygame.image.load(
                    os.path.join('resources/pieces', color.name.lower() + "_1.png"))
            self.rect: pygame.Rect = self.image.get_rect()

    def toString(self):
        return str(self.value.value) + "-" + self.color.value

    def show(self):
        print("{} - {} ".format(self.color, self.value))


# Classe que representa a matriz do tabuleiro, na grid
class GameTable(object):
    def __init__(self, image_file, location):
        self.tabuleiro: List[List[Piece]] = [[Piece(PieceValue.BLANK, Color.BLANK) for x in range(Table.COLUMNS.value)] for y in range(Table.ROWS.value)]
        self.image: pygame.image = pygame.image.load(image_file)
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def __str__(self):
        string = ""
        for row in self.tabuleiro:
            for cell in row:
                string += "|" + cell.toString() + "|"
            string += "\n"
        return string

    def collidePiece(self, piece: Piece) -> Tuple[int, int]:
        # 24 de largura por 8 de altura
        if self.rect.colliderect(piece.rect):
            baseCoord = (self.rect.x, self.rect.y)
            pieceCoord = piece.rect.center
            height = self.rect.height / 8
            width = self.rect.width / 24

            relativeX: int = (pieceCoord[0] - baseCoord[0]) // width
            relativeY: int = (pieceCoord[1] - baseCoord[1]) // height

            if relativeX < 0:
                relativeX = 0
            if relativeY < 0:
                relativeY = 0

            self.tabuleiro[int(relativeY)][int(relativeX)] = piece

            relativeX = relativeX * width + baseCoord[0]
            relativeY = relativeY * height + baseCoord[1]

            print(self)

            return relativeX, relativeY
        return -1, -1


# Classe que representa o 'deck' de peças, quando instanciado ele chama a função build()
# que popula com todas as 104 peças
class Deck(object):
    def __init__(self):
        self.pieces: List[Piece] = []
        self.build()
        self.drawButtnImage = pygame.image.load(os.environ.get("draw_unlock"))  # Caminho da imagem
        self.drawButtnRect: pygame.Rect = self.drawButtnImage.get_rect()  # 'hitbox' da imagem

    # Popula um deck de 104 pecas
    def build(self):
        for color in Color:
            for value in PieceValue:
                if value == PieceValue.JOKER or color == Color.JOKER or value == PieceValue.BLANK or color == Color.BLANK:
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
    def draw_piece(self) -> Piece:
        if not self.is_empty():
            return self.pieces.pop()

    # Print das peças no terminal
    def show(self):
        for p in self.pieces:
            p.show()

    # Verifica se o deck esta vazio ou não
    def is_empty(self) -> bool:
        if len(self.pieces) == 0:
            return True
        return False





# Classe que representa um jogador, que possui name, id e uma mão
class Player(object):
    def __init__(self, name: str, id: int):
        self.name: str = name
        self.hand: List[Piece] = []
        self.id: int = id

    # Método em que o jogador adiciona à mão dele uma peça do deck
    def draw(self, deck: Deck):
        self.hand.append(deck.draw_piece())
        return self

    # Mostra a mão do jogador no terminal
    def show_hand(self):
        print("Mao de {}:".format(self.name))
        for piece in self.hand:
            piece.show()

    # todo sorting de mão
    # def sortHand(self):
