import pytest
from app.game.Game import Game
from app.game.Player import Player
from app.game.Piece import Piece
from app.game.GameEnums import *


class TestClass(object):

    @pytest.fixture(scope="module")
    def base_player_empty_hands(self):
        player = Player("TestUser", 0, False)
        return player

    @pytest.fixture(scope="module")
    def base_player_with_pieces_unsorted(self):
        player = Player("TestUser", 0, False)
        player.hand.append(Piece(PieceValue.EIGHT, PieceColor.BLUE, 0))
        player.hand.append(Piece(PieceValue.SIX, PieceColor.BLUE, 2))
        player.hand.append(Piece(PieceValue.NINE, PieceColor.BLUE, 3))
        return player

    @pytest.fixture(scope="module")
    def base_game(self):
        jogo = Game()
        return jogo

    @pytest.fixture(scope="module")
    def base_game_empty_deck(self):
        jogo = Game()
        jogo.deck.pieces = []
        return jogo

    def test_draw(self, base_player_empty_hands, base_game):
        bef_hand = base_player_empty_hands.hand.copy()
        base_player_empty_hands.draw(base_game.deck)
        assert len(bef_hand) < len(base_player_empty_hands.hand)

    def test_draw_empty_deck(self, base_player_empty_hands, base_game_empty_deck):
        bef_hand = base_player_empty_hands.hand.copy()
        base_player_empty_hands.draw(base_game_empty_deck.deck)
        assert len(bef_hand) == len(base_player_empty_hands.hand)

    def test_sort_hand_sequence(self, base_player_with_pieces_unsorted):
        base_player_with_pieces_unsorted.sort_hand_sequence()
        prev = -1
        for piece in base_player_with_pieces_unsorted.hand:
            assert piece.value.value > prev
            prev = piece.value.value
