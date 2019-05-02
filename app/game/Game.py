from app.game.Player import *
from app.game.Table import *
from app.game.Background import *
import os


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Size.WindowWidth, Size.WindowHeight))
        pygame.display.set_caption("Rummikub")
        self.background = Background(os.environ.get("background"), [0, 0])
        self.table = GameTable(os.path.abspath(os.path.join(os.path.curdir, "resources", "static", "table_grid.png")), (40, 40))
        self.deck = Deck()
        self.deck.shuffle()
        self.screen.fill(RGB.BOARD_BLACK.value)
        self.players: List[Player] = []

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

<<<<<<< HEAD
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
                            #Se a peca selecionada estiver no tabuleiro, guardar local onde esta caso o jogador tente coloca la num local invalido
                            if self.players[0].hand[tile_moving].whereAt == PieceLocale.TABLE:
                                last_x = self.players[0].hand[tile_moving].rect.x
                                last_y = self.players[0].hand[tile_moving].rect.y


                # Quando solta o pressionar do mouse
                if event.type == pygame.MOUSEBUTTONUP:
                    # Se verdade, significa que o clique foi em cima de uma peca, entao essa peca pode ter sido movida
                    if is_moving_piece:
                        x, y = self.table.collidePiece(self.players[0].hand[tile_moving])
                        if x == -1:
                            # Retorna la a posicao inicial somente se ela nao tiver passado pelo tabuleiro ainda
                            if self.players[0].hand[tile_moving].whereAt == PieceLocale.HAND:
                                self.players[0].hand[tile_moving].rect.x, self.players[0].hand[tile_moving].rect.y = self.players[0].hand[tile_moving].originalPlace
                            else:
                                self.players[0].hand[tile_moving].rect.x = last_x
                                self.players[0].hand[tile_moving].rect.y = last_y
                        else:
                            self.players[0].hand[tile_moving].rect.x = x
                            self.players[0].hand[tile_moving].rect.y = y
                            self.players[0].hand[tile_moving].whereAt = PieceLocale.TABLE
                        tile_moving = -1
                        is_moving_piece = False
                        mouse_offset = (0, 0)
            if is_moving_piece:
                self.players[0].hand[tile_moving].rect.x = pygame.mouse.get_pos()[0] - mouse_offset[0]
                self.players[0].hand[tile_moving].rect.y = pygame.mouse.get_pos()[1] - mouse_offset[1]
            self.update_frame()
            pygame.display.update()
=======
>>>>>>> c56408b902f9a12c30eb83614ff0080c02fa37e8
