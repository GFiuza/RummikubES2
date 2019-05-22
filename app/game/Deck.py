import random
from typing import List
from app.game.Piece import *

# Classe que representa o 'deck' de peças, quando instanciado ele chama a função build()
# que popula com todas as 104 peças
class Deck(object):
    def __init__(self):
        self.pieces: List[Piece] = []
        self.build()

    # Popula um deck de 104 pecas
    def build(self):
        id = 1
        for color in PieceColor:
            for value in PieceValue:
                if value == PieceValue.JOKER or color == PieceColor.JOKER or value == PieceValue.BLANK or color == PieceColor.BLANK:
                    continue
                self.pieces.append(Piece(value, color, id))
                self.pieces.append(Piece(value, color, id + 1))
                id += 2
        self.pieces.append(Piece(PieceValue.JOKER, PieceColor.JOKER, id))
        self.pieces.append(Piece(PieceValue.JOKER, PieceColor.JOKER, id + 1))

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
