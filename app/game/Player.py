from app.game.Deck import *
from operator import itemgetter

# Classe que representa um jogador, que possui name, id e uma mão
class Player(object):
    def __init__(self, name, id, IA):
        self.name = name
        self.hand: List[Piece] = []
        self.id = id
        self.IA = IA
        self.doneMeld = False

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

    def initial_meld(self, pieces_placed: List[Piece], tabuleiro: List[List[Piece]]):
        sorted_pieces = sorted(pieces_placed, key=lambda x: x.value)
        for i in sorted_pieces:
            print(i)
        print("----")
        for group in tabuleiro:
            for p in range(1, len(group) + 1):
                print(group[p-1])

        if len(pieces_placed) < 3:
            return 0
        soma = 0
        # Verificando
        for tab in tabuleiro:
            soma_len = 0
            for group_p in tab:
                for piece in sorted_pieces:
                    if piece.id == group_p.id:
                        soma_len += 1
            if 0 < soma_len < len(tab):
                return 0

        for k in range(len(sorted_pieces)):
            for group in tabuleiro:
                # Verificando se esse grupo é formado somente por peças do jogador
                # sum_pieces_in_line = sum(1 if piece.id == group_p.id else 0 for group_p in group for piece in sorted_pieces)
                # if 0 < sum_pieces_in_line < len(group):
                #     return 0
                # elif sum_pieces_in_line == 0:
                #     break

                joker_count = sum(p.value == PieceValue.JOKER for p in group)
                print("joker count = " + str(joker_count))

                # Se nao houver coringa no initial meld
                if joker_count == 0:
                    for p in range(len(group)):
                        if sorted_pieces[k].id == group[p].id:
                            soma += sorted_pieces[k].value.value
                # Se houver coringa no initial meld
                else:
                    for diff in group:
                        if diff.value != PieceValue.JOKER:
                            # Trinca/Quadra
                            if sum(p.value == diff.value for p in group) > 1:
                                print("passou aqui 0")
                                return diff.value.value * len(group)
                    # Sequencia
                    for p in range(len(group)):
                        # Calculos de PA
                        if group[0].value != PieceValue.JOKER:
                            print("passou aqui 1")
                            return (group[0].value.value + (group[0].value.value + len(group) - 1)) * len(group)/2
                        if group[1].value != PieceValue.JOKER:
                            return group[1].value.value - 1 + (group[1].value.value + (group[1].value.value + len(group) - 2)) * (len(group)-1)/2
                        return group[2].value.value - 1 + group[2].value.value - 2 + (
                                    group[1].value.value + (group[1].value.value + len(group) - 3)) * (
                                           len(group) - 2) / 2
        return soma

    #heuristica básica para uma eventual IA, considera numero de peças em mão e o somatório de seus valores(quanto mais peças e maior o valor, pior)
    def hand_value(self):
        pieces = len(self.hand)
        if pieces == 0:
            return 100 #valor a ser substituido pela soma da pontuação dos outros jogadores
        value = 0
        for piece in self.hand:
            if piece.value == PieceValue.JOKER:
                value -= 30
            else:
                value -= piece.value

        return (pieces * -20) + value