from app.game.Button import Button
from app.game.Player import *
from app.game.Table import *
from app.game.Background import *
from app.game.PlayerGrid import *
from app.game.PlayerInfoCard import *
import os


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Size.WindowWidth, Size.WindowHeight))
        pygame.display.set_caption("Rummikub")
        self.background = Background(os.environ.get("background"), [0, 0])
        self.table = GameTable(os.environ.get("table_grid"), (40, 40))
        self.playergrid = PlayerGrid(os.environ.get("player_grid"), (25, self.table.rect.y + self.table.rect.height + 15))
        self.deck = Deck()
        self.deck.shuffle()
        self.screen.fill(RGB.BOARD_BLACK.value)
        self.players: List[Player] = []
        self.player_boards: List[PlayerInfoCard] = []
        # self.turn_display_font = pygame.font.SysFont(os.environ.get("player_font"), 50)
        self.turn_display_font = pygame.font.Font(os.environ.get("player_font"), 30)
        self.turn_display = self.turn_display_font.render(' Teste', False, (100, 55, 155))
        self.buttons = Button()

    def reset_player_tiles_position(self, player):
        grid_position_x = self.playergrid.rect.x + 20
        grid_position_y = self.playergrid.rect.y
        underset_y = 0
        for i in range(len(player.hand)):
            delta = i
            # Determina se joga as pecas para baixo no grid
            if i > 19:
                underset_y = player.hand[i].rect.height
                delta = i - 20
                # offset = (i - 17) * player.hand[i].rect.width // self.background.rect.width
            if i > 39:
                underset_y = 2 * player.hand[i].rect.height
                delta = i - 39
            offset = (delta + 1) * player.hand[i].rect.width // self.background.rect.width
            background_width = self.background.rect.width
            piece_height = player.hand[i].rect.height
            player.hand[i].rect.x = grid_position_x + delta * player.hand[i].rect.width - offset * (background_width - 4)
            player.hand[i].rect.y = grid_position_y - offset * (piece_height + 4) + underset_y
            player.hand[i].originalPlace = (player.hand[i].rect.x, player.hand[i].rect.y)
        for i in range(Table.ROWS.value):
            for j in range(Table.COLUMNS.value):
                if self.table.tabuleiro[i][j].whereAt == PieceLocale.HAND:
                    self.table.tabuleiro[i][j] = Piece(PieceValue.BLANK, PieceColor.BLANK, -1)
                    self.table.tabuleiro[i][j].whereAt = PieceLocale.TABLE
                if self.table.tabuleiro[i][j].value != PieceValue.BLANK:
                    self.table.tabuleiro[i][j].originalPlace = (self.table.tabuleiro[i][j].rect.x, self.table.tabuleiro[i][j].rect.y)

    def add_player(self, name, id_, IA = False):
        self.players.append(Player(name, id_, IA))
        self.player_boards.append(PlayerInfoCard(id_, name))

    def update_frame(self, player):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.table.image, self.table.rect)
        self.screen.blit(self.playergrid.image, self.playergrid.rect)
        self.screen.blit(self.buttons.buttnDrawImage, self.buttons.buttnDrawRect)
        self.screen.blit(self.buttons.buttnMeldImage, self.buttons.buttnMeldRect)
        self.screen.blit(self.buttons.buttnUndoImage, self.buttons.buttnUndoRect)
        self.screen.blit(self.buttons.buttnSortSeqImage, self.buttons.buttnSortSeqRect)
        self.screen.blit(self.buttons.buttnSortRepImage, self.buttons.buttnSortRepRect)

        self.screen.blit(self.turn_display, (Size.WindowWidth * 0.85, Size.WindowHeight*0.05))

        for i in range(len(self.players)):
            self.screen.blit(self.player_boards[i].cardImage, self.player_boards[i].cardRect)
            self.player_boards[i].display_name(str(len(self.players[i].hand)))
            self.screen.blit(self.player_boards[i].cardCountDisplay, self.player_boards[i].cardCountDisplayPos)
            self.screen.blit(self.player_boards[i].playerDisplay, self.player_boards[i].playerDisplayPos)

        if not player.IA:
            for i in player.hand:
                self.screen.blit(i.image, i.rect)
        for row in range(Table.ROWS.value):
            for col in range(Table.COLUMNS.value):
                if self.table.tabuleiro[row][col].value.value != -1:
                    self.screen.blit(self.table.tabuleiro[row][col].image, self.table.tabuleiro[row][col].rect)


    # Verifica se o mouse esta sobre algum dos botoes/pecas na vez do jogador, e vai indicar se ele está clicável ou não
    def update_on_hover(self, mouse_pos):

        # Botao de comprar mais pecas
        if self.buttons.buttnDrawRect.collidepoint(mouse_pos):
            if not self.buttons.buttnDrawOnHover:
                self.buttons.buttnDrawRect.x -= 3
                self.buttons.buttnDrawRect.y -= 3
                self.buttons.buttnDrawOnHover = True
            return
        else:
            if self.buttons.buttnDrawOnHover:
                self.buttons.button_reset_pos()
                self.buttons.buttnDrawOnHover = False
                return

        # Botao de validar jogadas
        if self.buttons.buttnMeldRect.collidepoint(mouse_pos):
            if not self.buttons.buttnMeldOnHover:
                self.buttons.buttnMeldRect.x -= 3
                self.buttons.buttnMeldRect.y -= 3
                self.buttons.buttnMeldOnHover = True
            return
        else:
            if self.buttons.buttnMeldOnHover:
                self.buttons.button_reset_pos()
                self.buttons.buttnMeldOnHover = False
                return
