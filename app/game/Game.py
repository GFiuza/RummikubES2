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
            offset = (i + 1) * self.players[0].hand[i].rect.width // self.background.rect.width
            background_width = self.background.rect.width
            piece_height = self.players[0].hand[i].rect.height
            self.players[0].hand[i].rect.x = i * self.players[0].hand[i].rect.width - offset * (background_width - 4)
            self.players[0].hand[i].rect.y = Size.WindowHeight - self.players[0].hand[i].rect.height - offset * (piece_height + 4)
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
