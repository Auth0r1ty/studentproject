import pygame
from enum import Enum
import GameConfig as config


# all methods and data that enemy and player have in common
class GameDynamicObject(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, image, gameTerrain, carryOn, sprite_list, screen):

        # parent ctor [v]
        super().__init__()

        # fields [v]
        self.width = width
        self.height = height
        self.image = pygame.Surface([50, 50])
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.gameTerrain = gameTerrain
        self.carryOn = carryOn
        self.sprite_list = sprite_list
        self.screen = screen
        self.emptyPathCounter = 0

    def draw_map(self):
        self.emptyPathCounter = 0
        # iscrtavanje mape
        for i in range(0, 12):
            for j in range(0, 16):
                if (self.gameTerrain[i][j]).fieldType == config.StaticEl.path:
                    self.screen.blit(config.path, (j * 50, i * 50))
                    self.emptyPathCounter += 1
                elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.wall:
                    self.screen.blit(config.wall, (j * 50, i * 50))
                elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.enter:
                    self.screen.blit(config.enter, (j * 50, i * 50))
                elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.pathPlayer1:
                    self.screen.blit((self.gameTerrain[i][j]).image, (j * 50, i * 50))

        #self.endgame_check(emptyPathCounter)