import pygame
import random
import GameConfig as config
from GameStaticObject import *
import time
pygame.init()


class Enemy (pygame.sprite.Sprite):
    # u slucaju vise slika, proslediti sliku kao argument konstuktora
    def __init__(self, image, width, height, x, y, gameTerrain, sprite_list):
        # poziv konstruktora od roditelja
        super().__init__()

        # visina i sirana slika (dodate su ostale slike)
        self.leftImage = pygame.Surface([width, height])
        self.leftImage = image[0]
        self.rightImage = pygame.Surface([width, height])
        self.rightImage = image[1]
        self.upImage = pygame.Surface([width, height])
        self.upImage = image[2]
        self.downImage = pygame.Surface([width, height])
        self.downImage = image[3]

        self.image = pygame.Surface([width, height])
        self.image = self.downImage

        # napravi se pravougaonik cije su dimenzije jednake dimenziji slike
        self.rect = self.image.get_rect()

        # pocetni polozaj igraca
        self.rect.x = x
        self.rect.y = y

        self.gameTerrain = gameTerrain

        self.decisionX = config.speed
        self.decisionY = 0

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
                    self.image = self.upImage
                    self.decisionY = -config.speed
                    self.decisionX = 0
                elif putanja == Orientation.down:
                    self.image = self.downImage
                    self.decisionY = config.speed
                    self.decisionX = 0
                elif putanja == Orientation.left:
                    self.image = self.leftImage
                    self.decisionY = 0
                    self.decisionX = -config.speed
                elif putanja == Orientation.right:
                    self.image = self.rightImage
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

        collision_list = pygame.sprite.spritecollide(self, sprite_list, False)
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
            playerX = self.player.rect.x // 50
            enemyY = (self.rect.y - self.rect.y % 50) // 50
            playerY = (self.player.rect.y - self.player.rect.y % 50) // 50

            if enemyX == playerX:

                if enemyY > playerY:
                    #proveri da li na toj liniji ima prepreka, ako ima ne moze ga videti -> return False, odnosno pozvace se makeDecision
                    for i in range(playerY, enemyY):
                        if (self.gameTerrain[i][enemyX]).fieldType == StaticEl.wall:
                            return False
                    self.image=self.upImage
                    self.decisionY = -config.speed
                else:
                    # proveri da li na toj liniji ima prepreka, ako ima ne moze ga videti -> return False, odnosno pozvace se makeDecision
                    for i in range(enemyY, playerY):
                        if (self.gameTerrain[i][enemyX]).fieldType == StaticEl.wall:
                            return False
                    self.image = self.downImage
                    self.decisionY = config.speed
                self.decisionX = 0
                return True

        elif self.rect.y % 50 == 0 and self.player.rect.y % 50 == 0:
            enemyY = self.rect.y // 50
            playerY = self.player.rect.y // 50
            enemyX = (self.rect.x - self.rect.x % 50) // 50
            playerX = (self.player.rect.x - self.player.rect.x % 50) // 50

            if enemyY == playerY:
                if enemyX > playerX:
                    # proveri da li na toj liniji ima prepreka, ako ima ne moze ga videti -> return False, odnosno pozvace se makeDecision
                    for i in range(playerX, enemyX):
                        if (self.gameTerrain[enemyY][i]).fieldType == StaticEl.wall:
                            return False
                    self.image=self.leftImage
                    self.decisionX = -config.speed
                else:
                    # proveri da li na toj liniji ima prepreka, ako ima ne moze ga videti -> return False, odnosno pozvace se makeDecision
                    for i in range(enemyX, playerX):
                        if (self.gameTerrain[enemyY][i]).fieldType == StaticEl.wall:
                            return False
                    self.image = self.rightImage
                    self.decisionX = config.speed
                self.decisionY = 0
                return True

        return False
