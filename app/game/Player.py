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
        peca = deck.draw_piece()
        peca.whereAt = PieceLocale.HAND
        self.hand.append(peca)
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


    # Calcula o valor do initial meld
    def initial_meld(self, pieces_placed: List[Piece], tabuleiro: List[List[Piece]]):
        for i in pieces_placed:
            print(i)
        soma = 0
        if len(pieces_placed) < 3:
            return 0
        for group in tabuleiro:
            for p in range(1, len(group) + 1):
                for k in pieces_placed:
                    if k.id == group[p - 1].id:
                        if k.value != PieceValue.JOKER:
                            soma += k.value.value
                        else:
                            # Se o coringa faz parte de trinca
                            if group[0].value.value == group[1].value.value and \
                                    group[0].value.value == group[2].value.value:
                                soma += group[p - 1].value.value
                            # Se o coringa faz parte de sequencia
                            else:
                                soma += group[p - 1].value.value + 1
        return soma
