from app.game.Deck import *
from operator import itemgetter


# Classe que representa um jogador, que possui name, id e uma mão
class Player(object):
    def __init__(self, name: str, id: int):
        self.name: str = name
        self.hand: List[Piece] = []
        self.id: int = id

    # Método em que o jogador adiciona à mão dele uma peça do deck
    def draw(self, deck: Deck):
        self.hand.append(deck.draw_piece())
        self.hand[-1].whereAt = PieceLocale.HAND
        return self

    # Mostra a mão do jogador no terminal
    def show_hand(self):
        print("Mao de {}:".format(self.name))
        for piece in self.hand:
            piece.show()

    def sort_hand_sequence(self):
        i = 1
        while i < len(self.hand):
            piece = self.hand[i]
            j = i-1
            while j >= 0 and piece.value < self.hand[j].value:
                self.hand[j+1] = self.hand[j]
                j -= 1
            while j >= 0 and piece.color.value < self.hand[j].color.value and piece.value == self.hand[j].value:
                self.hand[j+1] = self.hand[j]
                j -= 1
            self.hand[j+1] = piece
            i += 1

    def sort_hand_rep(self):
        i = 1
        while i < len(self.hand):
            piece = self.hand[i]
            j = i-1
            while j >= 0 and piece.color.value < self.hand[j].color.value:
                self.hand[j+1] = self.hand[j]
                j -= 1
            while j >= 0 and piece.value < self.hand[j].value and piece.color.value == self.hand[j].color.value:
                self.hand[j+1] = self.hand[j]
                j -= 1
            self.hand[j+1] = piece
            i += 1

