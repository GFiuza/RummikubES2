from game.GameClasses import *
from game.GameEnums import *
from game.GameSprites import *


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
        self.backGround = Background(Path.backgound_grid, [0, 0])
        self.deck = Deck()
        self.deck.shuffle()
        self.screen.fill(RGB.BOARD_BLACK.value)
        self.players = []
        self.exit = False

    def resetPlayerTilesPosition(self):
        for i in range(len(self.players[0].hand)):
            self.players[0].hand[i].rect.x = (i * self.players[0].hand[i].rect.width)
            self.players[0].hand[i].rect.y = Size.WindowHeight - self.players[0].hand[i].rect.height

    def addPlayer(self, name: str, id : int):
        self.players.append(Player(name, id))

    def updateFrame(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.backGround.image, self.backGround.rect)
        self.screen.blit(self.deck.drawButtnImage, self.deck.drawButtnRect)
        for i in self.players[0].hand:
            self.screen.blit(i.image, i.rect)

    # todo clicar para adicionar peca
    # todo peca pode se mover
    def main_loop(self):
        mouse_clicked = False
        mouse_position = (0, 0)
        tileMoving = -1
        while not self.exit:
            self.deck.drawButtnRect.x = Size.WindowWidth * 0.9
            self.deck.drawButtnRect.y = Size.WindowHeight / 2
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                if event.type == pygame.MOUSEBUTTONDOWN and self.deck.drawButtnRect.collidepoint(pygame.mouse.get_pos()):
                    self.players[0].draw(self.deck)
                    self.resetPlayerTilesPosition()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(self.players[0].hand)):
                        if self.players[0].hand[i].rect.collidepoint(pygame.mouse.get_pos()):
                            mouse_clicked = True
                            mouse_position = (pygame.mouse.get_pos()[0] - self.players[0].hand[i].rect.x,
                                              pygame.mouse.get_pos()[1] - self.players[0].hand[i].rect.y)
                            tileMoving = i
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_clicked = False
            if mouse_clicked:
                self.players[0].hand[tileMoving].rect.x = pygame.mouse.get_pos()[0] - mouse_position[0]
                self.players[0].hand[tileMoving].rect.y = pygame.mouse.get_pos()[1] - mouse_position[1]
            self.updateFrame()
            pygame.display.update()
