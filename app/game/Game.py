from app.game.Button import Button
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
        self.table = GameTable(os.environ.get("table_grid"), (40, 40))
        self.deck = Deck()
        self.deck.shuffle()
        self.screen.fill(RGB.BOARD_BLACK.value)
        self.players: List[Player] = []
        self.turn_display_font = pygame.font.SysFont('Comic Sans MS',30)
        self.turn_display = self.turn_display_font.render(' Teste', False, (0, 0, 0))
        self.point_display = self.turn_display_font.render(' Pontos:', False, (0, 0, 0))
        self.buttons = Button()

    def reset_player_tiles_position(self, player):
        for i in range(len(player.hand)):
            offset = (i + 1) * player.hand[i].rect.width // self.background.rect.width
            background_width = self.background.rect.width
            piece_height = player.hand[i].rect.height
            player.hand[i].rect.x = i * player.hand[i].rect.width - offset * (background_width - 4)
            player.hand[i].rect.y = Size.WindowHeight - player.hand[i].rect.height - offset * (piece_height + 4)
            player.hand[i].originalPlace = (player.hand[i].rect.x, player.hand[i].rect.y)
        for i in range(Table.ROWS.value):
            for j in range(Table.COLUMNS.value):
                if self.table.tabuleiro[i][j].whereAt == PieceLocale.HAND:
                    self.table.tabuleiro[i][j] = Piece(PieceValue.BLANK, PieceColor.BLANK, -1)
                    self.table.tabuleiro[i][j].whereAt = PieceLocale.TABLE
                if self.table.tabuleiro[i][j].value != PieceValue.BLANK:
                    self.table.tabuleiro[i][j].originalPlace = (self.table.tabuleiro[i][j].rect.x, self.table.tabuleiro[i][j].rect.y)

    def add_player(self, name, id_, IA=False):
        self.players.append(Player(name, id_, IA))

    def update_frame(self, player):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.table.image, self.table.rect)
        self.screen.blit(self.buttons.drawButtnImage, self.buttons.drawButtnRect)
        self.screen.blit(self.buttons.validateTurnImage, self.buttons.validadeTurnRect)

        self.screen.blit(self.turn_display, (Size.WindowWidth * 0.85, Size.WindowHeight*0.05))
        self.screen.blit(self.point_display, (Size.WindowWidth * 0.85, Size.WindowHeight*0.10))
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
        if self.buttons.drawButtnRect.collidepoint(mouse_pos):
            if not self.buttons.drawButtnOnHover:
                self.buttons.drawButtnRect.x -= 3
                self.buttons.drawButtnRect.y -= 3
                self.buttons.drawButtnOnHover = True
            return
        else:
            if self.buttons.drawButtnOnHover:
                self.buttons.button_reset_pos()
                self.buttons.drawButtnOnHover = False
                return

        # Botao de validar jogadas
        if self.buttons.validadeTurnRect.collidepoint(mouse_pos):
            if not self.buttons.validadeTurnOnHover:
                self.buttons.validadeTurnRect.x -= 3
                self.buttons.validadeTurnRect.y -= 3
                self.buttons.validadeTurnOnHover = True
            return
        else:
            if self.buttons.validadeTurnOnHover:
                self.buttons.button_reset_pos()
                self.buttons.validadeTurnOnHover = False
                return
