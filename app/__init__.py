import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Background
os.environ['background'] = os.path.join(ROOT_DIR, "resources", "static", "game_background.png")
os.environ['backgound_grid'] = os.path.join(ROOT_DIR, "resources", "static", "game_background_grid.png")
os.environ['table_grid'] = os.path.join(ROOT_DIR, "resources", "static", "table_grid.png")
os.environ['player_grid'] = os.path.join(ROOT_DIR, "resources", "static", "player_grid.png")

# Botoes
os.environ['draw_unlock'] = os.path.join(ROOT_DIR, "resources", "buttons", "draw.png")
os.environ['end_turn'] = os.path.join(ROOT_DIR, "resources", "buttons", "end_turn.png")
os.environ['undo'] = os.path.join(ROOT_DIR, "resources", "buttons", "undo.png")
os.environ['sort_rep'] = os.path.join(ROOT_DIR, "resources", "buttons", "sort_rep.png")
os.environ['sort_seq'] = os.path.join(ROOT_DIR, "resources", "buttons", "sort_seq.png")

# Caixa de informacao de jogador
os.environ['player_board'] = os.path.join(ROOT_DIR, "resources", "static", "player_board.png")

# Pecas / diretorio
os.environ['pieces'] = os.path.join(ROOT_DIR, "resources", "pieces")

# Fontes
os.environ["player_font"] = os.path.join(ROOT_DIR, "resources", "fonts", "zephyrea.ttf")
