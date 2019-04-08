from app.game.GameClasses import *
from app.game.GameEnums import *
from typing import List
import os


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Size.WindowWidth, Size.WindowHeight))
        pygame.display.set_caption("Rummikub")
        self.background = Background(os.path.abspath(os.path.join(os.path.curdir, "resources", "static", "game_background.png")), [0, 0])
        self.table = GameTable(os.path.abspath(os.path.join(os.path.curdir, "resources", "static", "table_grid.png")), (40, 40))
        self.deck = Deck()
        self.deck.shuffle()
        self.screen.fill(RGB.BOARD_BLACK.value)
        self.players: List[Player] = []
        self.exit = False

    def reset_player_tiles_position(self):
        for i in range(len(self.players[0].hand)):
            self.players[0].hand[i].rect.x = (i * self.players[0].hand[i].rect.width)
            self.players[0].hand[i].rect.y = Size.WindowHeight - self.players[0].hand[i].rect.height
            self.players[0].hand[i].originalPlace = (self.players[0].hand[i].rect.x, self.players[0].hand[i].rect.y)

    def add_player(self, name, id_):
        self.players.append(Player(name, id_))

    def update_frame(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.table.image, self.table.rect)
        self.screen.blit(self.deck.drawButtnImage, self.deck.drawButtnRect)
        for i in self.players[0].hand:
            self.screen.blit(i.image, i.rect)

    # todo clicar para adicionar peca
    # todo peca pode se mover
    def main_loop(self):
        is_moving_piece = False
        mouse_offset = (0, 0)
        tile_moving = -1
        while not self.exit:
            self.deck.drawButtnRect.x = Size.WindowWidth * 0.9
            self.deck.drawButtnRect.y = Size.WindowHeight / 2
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                    break
                if event.type == pygame.MOUSEBUTTONDOWN and self.deck.drawButtnRect.collidepoint(
                        pygame.mouse.get_pos()):
                    self.players[0].draw(self.deck)
                    self.reset_player_tiles_position()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(self.players[0].hand)):
                        if self.players[0].hand[i].rect.collidepoint(pygame.mouse.get_pos()):
                            is_moving_piece = True
                            mouse_offset = (pygame.mouse.get_pos()[0] - self.players[0].hand[i].rect.x,
                                            pygame.mouse.get_pos()[1] - self.players[0].hand[i].rect.y)
                            tile_moving = i
                if event.type == pygame.MOUSEBUTTONUP:
                    if is_moving_piece:
                        x, y = self.table.collidePiece(self.players[0].hand[tile_moving])
                        if x == -1:
                            self.players[0].hand[tile_moving].rect.x, self.players[0].hand[tile_moving].rect.y = self.players[0].hand[tile_moving].originalPlace
                        else:
                            self.players[0].hand[tile_moving].rect.x = x
                            self.players[0].hand[tile_moving].rect.y = y
                        tile_moving = -1
                        is_moving_piece = False
                        mouse_offset = (0, 0)
            if is_moving_piece:
                self.players[0].hand[tile_moving].rect.x = pygame.mouse.get_pos()[0] - mouse_offset[0]
                self.players[0].hand[tile_moving].rect.y = pygame.mouse.get_pos()[1] - mouse_offset[1]
            self.update_frame()
            pygame.display.update()
