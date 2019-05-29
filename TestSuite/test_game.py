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
        player.hand.append(Piece(PieceValue.JOKER, PieceColor.BLUE, 0))
        player2 = Player("b", 1, False)
        player2.hand.append(Piece(PieceValue.FOUR, PieceColor.BLUE, 1))
        player3 = Player("c", 2, False)
        player3.hand.append(Piece(PieceValue.EIGHT, PieceColor.BLUE, 2))
        jogo.players.append(player)
        jogo.players.append(player2)
        jogo.players.append(player3)
        return jogo

    def test_round_winner(self, game_w_score):
        winner = game_w_score.calc_pont_players()
        assert winner.current_score == 4

    def test_winner(self, game_w_score):
        winner = game_w_score.calc_winner()
        assert winner[0].score == 38

    def test_restart_players(self, game_w_score):
        game_w_score.restart_players()
        for player in game_w_score.players:
            assert not player.doneMeld
            assert player.current_score == 0
            assert not player.hand
