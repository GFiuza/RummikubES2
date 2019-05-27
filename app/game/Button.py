import random
from typing import List
from app.game.Piece import *

turn_buttons_y = Size.WindowHeight * 3 / 4
turn_buttons_x = Size.WindowWidth * 6 / 7

sort_buttons_y = Size.WindowHeight * 3 / 4 + 10
sort_buttons_x = Size.WindowWidth * 7 / 9

buttons_offset = 50


class Button(object):
    def __init__(self):


        #Comprar peca
        self.buttnDrawImage = pygame.image.load(os.environ.get("draw_unlock"))  # Caminho da imagem
        self.buttnDrawRect: pygame.Rect = self.buttnDrawImage.get_rect()  # 'hitbox' da imagem
        self.buttnDrawRect.center = (turn_buttons_x, turn_buttons_y)
        self.buttnDrawOnHover = False

        #Confirmar turno
        self.buttnMeldImage = pygame.image.load(os.environ.get("end_turn"))
        self.buttnMeldRect = pygame.Rect = self.buttnMeldImage.get_rect()
        self.buttnMeldRect.center = (turn_buttons_x + buttons_offset, turn_buttons_y)
        self.buttnMeldOnHover = False

        # Undo
        self.buttnUndoImage = pygame.image.load(os.environ.get("undo"))
        self.buttnUndoRect = pygame.Rect = self.buttnUndoImage.get_rect()
        self.buttnUndoRect.center = (turn_buttons_x + 2 * buttons_offset, turn_buttons_y)
        self.buttnUndoOnHover = False

        #Sort de sequencia
        self.buttnSortSeqImage = pygame.image.load(os.environ.get("sort_seq"))
        self.buttnSortSeqRect = pygame.Rect = self.buttnSortSeqImage.get_rect()
        self.buttnSortSeqRect.center = (sort_buttons_x, sort_buttons_y)

        # Sort de trincas
        self.buttnSortRepImage = pygame.image.load(os.environ.get("sort_rep"))
        self.buttnSortRepRect = pygame.Rect = self.buttnSortSeqImage.get_rect()
        self.buttnSortRepRect.center = (sort_buttons_x, sort_buttons_y + buttons_offset)


    def button_reset_pos(self):
        self.buttnDrawRect.center = (turn_buttons_x, turn_buttons_y)
        self.buttnMeldRect.center = (turn_buttons_x + buttons_offset, turn_buttons_y)
        self.buttnUndoRect.center = (turn_buttons_x + 2 * buttons_offset, turn_buttons_y)
        self.buttnSortSeqRect.center = (sort_buttons_x, sort_buttons_y)
        self.buttnSortRepRect.center = (sort_buttons_x , sort_buttons_y + buttons_offset + 5)
