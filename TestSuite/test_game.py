import pytest
from app.game.Game import Game
from app.game.Player import Player
from app.game.Piece import Piece
from app.game.GameEnums import *


class TestClass(object):
    @pytest.fixture(scope="module")
    def game_w_score(self):
        jogo = Game()
        player = Player("a", 0, False)
        player.score = 100
        player2 = Player("b", 1, False)
        player2.score = -50
        player3 = Player("c", 2, False)
        player3.score = 90
        jogo.players.append(player)
        jogo.players.append(player2)
        jogo.players.append(player3)
        return jogo

    def test_winner(self, game_w_score):
        winner = game_w_score.calc_winner()
        assert winner[0].score == 100
