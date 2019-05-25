import pytest
from app.game.Game import Game
from app.game.Player import Player


class TestClass(object):

    @pytest.fixture(scope="module")
    def base_player(self):
        player = Player("TestUser", 0, False)
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

    def test_draw(self, base_player, base_game):
        bef_hand = base_player.hand.copy()
        base_player.draw(base_game.deck)
        assert bef_hand != base_player.hand

    def test_draw_empty_hand(self, base_player, base_game):
        bef_hand = base_player.hand.copy()
        base_player.draw(base_game.deck)
        assert bef_hand == base_player.hand

