import os

os.environ['backgound'] = 'resources/static/game_background.png'
os.environ['draw_unlock'] = 'resources/buttons/comprar_mais.png'
os.environ['draw_lock'] = 'resources/buttons/comprar_mais_lock.png'
os.environ['backgound_grid'] = 'resources/static/game_background_grid.png'


from app.game.Game import *
jogo = Game()
jogo.addPlayer('Player1', 0)
jogo.main_loop()