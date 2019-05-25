import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ['background'] = os.path.join(ROOT_DIR, "resources", "static", "game_background.png")
os.environ['draw_unlock'] = os.path.join(ROOT_DIR, "resources", "buttons", "comprar_mais.png")
os.environ['draw_lock'] = os.path.join(ROOT_DIR, "resources", "buttons", "comprar_mais_lock.png")
os.environ['backgound_grid'] = os.path.join(ROOT_DIR, "resources", "static", "game_background_grid.png")
os.environ['table_grid'] = os.path.join(ROOT_DIR, "resources", "static", "table_grid.png")
os.environ['end_turn'] = os.path.join(ROOT_DIR, "resources", "buttons", "end_turn.png")
os.environ['pieces'] = os.path.join(ROOT_DIR, "resources", "pieces")
