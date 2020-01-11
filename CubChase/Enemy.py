import pygame
import random
import GameConfig as config
from GameStaticObject import Orientation
import time
pygame.init()

class Enemy (pygame.sprite.Sprite):
    # u slucaju vise slika, proslediti sliku kao argument konstuktora
    def __init__(self, image, width, height, x, y, gameMap, gameTerrain, sprite_list):
        # poziv konstruktora od roditelja
        super ().__init__()

        # visina i sirana slike
        self.image = pygame.Surface ([width, height])
        self.image = image

        # napravi se pravougaonik cije su dimenzije jednake dimenziji slike
        self.rect = self.image.get_rect()

        # pocetni polozaj igraca
        self.rect.x = x
        self.rect.y = y

        self.gameMap = gameMap

        self.decisionX=config.speed
        self.decisionY=0

        for temp in sprite_list:

            if temp.__class__.__name__ == "Player":
                self.player = temp
                break


    def makeDecision(self):

        if self.rect.x % 50 == 0 and self.rect.y % 50 == 0:
            current = config.gameTerrain[self.rect.y // 50][self.rect.x // 50]

            if current.isCrossroad:
                try:
                    putanja = random.choice(current.orientations)
                except:
                    putanja = 0

                if putanja == Orientation.up:
                    self.decisionY = -config.speed
                    self.decisionX = 0
                elif putanja == Orientation.down:
                    self.decisionY = config.speed
                    self.decisionX = 0
                elif putanja == Orientation.left:
                    self.decisionY = 0
                    self.decisionX = -config.speed
                elif putanja == Orientation.right:
                    self.decisionY = 0
                    self.decisionX = config.speed
                else:
                    self.decisionX = 0
                    self.decisionY = 0


    def moveEnemy(self, sprite_list):     #sprite list je lista objekata (zidovi, igraci i ostalo)

        if not self.spotEnemy(sprite_list):
            self.makeDecision()

        self.rect.x += self.decisionX
        self.rect.y += self.decisionY

        collision_list = pygame.sprite.spritecollide (self, sprite_list, False)
        for temp in collision_list:
            if temp != self:
                if self.decisionX > 0:  # igrac se pomera desno
                    self.rect.right = temp.rect.left

                elif self.decisionX < 0:  # levo
                    self.rect.left = temp.rect.right

                elif self.decisionY > 0:  # dole
                    self.rect.bottom = temp.rect.top

                elif self.decisionY < 0:  # gore
                    self.rect.top = temp.rect.bottom

    def spotEnemy(self, sprite_list):



        if self.rect.x % 50 == 0 and self.player.rect.x % 50 == 0:
            # i == y, j == x koordinatama
            enemyX = self.rect.x // 50
            enemyY = (self.rect.y - self.rect.y % 50) // 50
            playerX = self.player.rect.x // 50
            playerY = (self.player.rect.y - self.player.rect.y % 50) // 50

            if enemyX == playerX:
                self.decisionX = 0
                if enemyY > playerY:
                    self.decisionY = -config.speed
                else:
                    self.decisionY = config.speed
                return True

        elif self.rect.y % 50 == 0 and self.player.rect.y % 50 == 0:
            enemyX = (self.rect.x - self.rect.x % 50) // 50
            enemyY = self.rect.y // 50
            playerX = (self.player.rect.x - self.player.rect.x % 50) // 50
            playerY = self.player.rect.y // 50

            if enemyY == playerY:
                self.decisionY = 0
                if enemyX > playerX:
                    self.decisionX = -config.speed
                else:
                    self.decisionX = config.speed
                return True

        return False