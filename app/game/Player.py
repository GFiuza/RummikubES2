from app.game.Deck import *



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

    # todo sorting de mão
    # def sortHand(self):
