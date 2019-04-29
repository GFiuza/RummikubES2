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
        for i in range(Table.ROWS.value):
            for j in range(Table.COLUMNS.value):
                if self.table.tabuleiro[i][j].whereAt == PieceLocale.HAND:
                    self.table.tabuleiro[i][j] = Piece(PieceValue.BLANK, PieceColor.BLANK)

    def add_player(self, name, id_):
        self.players.append(Player(name, id_))

    def update_frame(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.table.image, self.table.rect)
        self.screen.blit(self.deck.drawButtnImage, self.deck.drawButtnRect)
        for i in self.players[0].hand:
            self.screen.blit(i.image, i.rect)
        for row in range(Table.ROWS.value):
            for col in range(Table.COLUMNS.value):
                if self.table.tabuleiro[row][col].value.value != -1:
                    self.screen.blit(self.table.tabuleiro[row][col].image, self.table.tabuleiro[row][col].rect)

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
                # Se esta clicando no botao de comprar pecas
                if event.type == pygame.MOUSEBUTTONDOWN and self.deck.drawButtnRect.collidepoint(
                        pygame.mouse.get_pos()):
                    self.players[0].draw(self.deck)
                    self.reset_player_tiles_position()
                # Se esta clicando em outra area ( depois especificar se esta clicando dentro do grid ou da mao)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(self.players[0].hand)):
                        if self.players[0].hand[i].rect.collidepoint(pygame.mouse.get_pos()):
                            is_moving_piece = True
                            mouse_offset = (pygame.mouse.get_pos()[0] - self.players[0].hand[i].rect.x,
                                            pygame.mouse.get_pos()[1] - self.players[0].hand[i].rect.y)
                            tile_moving = i
                # Quando solta o pressionar do mouse
                if event.type == pygame.MOUSEBUTTONUP:
                    # Se verdade, significa que o clique foi em cima de uma peca, entao essa peca pode ter sido movida
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
