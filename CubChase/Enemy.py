import pygame
import random
import GameConfig as config
from GameStaticObject import *
import time
pygame.init()


class Enemy:
    def __init__(self):
        self.x = config.speed
        self.y = 0
        self.player_x = 0
        self.player_y = 0
        self.enemy_x = 0
        self.enemy_y = 0
        self.finished = False
        self.game_terrain = None

    def moveEnemy(self):
        if not self.spotEnemy():
            self.makeDecision()

    def spotEnemy(self):
        if self.enemy_x % 50 == 0 and self.player_x % 50 == 0:
            # i == y, j == x koordinatama
            enemyX = self.enemy_x // 50
            playerX = self.player_x // 50
            enemyY = (self.enemy_y - self.enemy_y % 50) // 50
            playerY = (self.player_y - self.player_y % 50) // 50

            if enemyX == playerX:

                if enemyY > playerY:
                    #proveri da li na toj liniji ima prepreka, ako ima ne moze ga videti -> return False, odnosno pozvace se makeDecision
                    for i in range(playerY, enemyY):
                        if (config.gameMap[i][enemyX]) == StaticEl.wall:
                            return False
                    self.y = -config.speed_enemy
                else:
                    # proveri da li na toj liniji ima prepreka, ako ima ne moze ga videti -> return False, odnosno pozvace se makeDecision
                    for i in range(enemyY, playerY):
                        if (config.gameMap[i][enemyX]) == StaticEl.wall:
                            return False
                    self.y = config.speed_enemy
                self.x = 0
                return True

        elif self.enemy_y % 50 == 0 and self.player_y % 50 == 0:
            enemyY = self.enemy_y // 50
            playerY = self.player_y // 50
            enemyX = (self.enemy_x - self.enemy_x % 50) // 50
            playerX = (self.player_x - self.player_x % 50) // 50

            if enemyY == playerY:
                if enemyX > playerX:
                    # proveri da li na toj liniji ima prepreka, ako ima ne moze ga videti -> return False, odnosno pozvace se makeDecision
                    for i in range(playerX, enemyX):
                        if (config.gameMap[enemyY][i]) == StaticEl.wall:
                            return False
                    self.x = -config.speed_enemy
                else:
                    # proveri da li na toj liniji ima prepreka, ako ima ne moze ga videti -> return False, odnosno pozvace se makeDecision
                    for i in range(enemyX, playerX):
                        if (config.gameMap[enemyY][i]) == StaticEl.wall:
                            return False
                    self.x = config.speed_enemy
                self.y = 0
                return True

        return False

    def makeDecision(self):

        if self.enemy_x % 50 == 0 and self.enemy_y % 50 == 0:
            current = self.game_terrain[self.enemy_y // 50][self.enemy_x // 50]

            if current.is_crossroad:
                try:
                    putanja = random.choice(current.orientations)
                except:
                    putanja = 0

                if putanja == Orientation.up:
                    self.y = -config.speed_enemy
                    self.x = 0
                elif putanja == Orientation.down:
                    self.y = config.speed_enemy
                    self.x = 0
                elif putanja == Orientation.left:
                    self.y = 0
                    self.x = -config.speed_enemy
                elif putanja == Orientation.right:
                    self.y = 0
                    self.x = config.speed_enemy
                else:
                    self.y = 0
                    self.x = 0

    def return_new_coordinates(self, queue):
        queue.put((self.x, self.y, self.carryOn))

    # process
    def run_enemy(self, queue, queue1):
        self.queue = queue
        while not self.finished:
            data = queue1.get ()
            self.carryOn = data[0]
            self.player_x = data[1][0]
            self.player_y = data[1][1]
            self.enemy_x = data[2][0]
            self.enemy_y = data[2][1]
            self.game_terrain = data[3]
            self.moveEnemy ()
            self.return_new_coordinates (self.queue)


class EnemyRender (pygame.sprite.Sprite):
    # u slucaju vise slika, proslediti sliku kao argument konstuktora
    def __init__(self, enemy, image, width, height, x, y, sprite_list):
        # poziv konstruktora od roditelja
        super().__init__()

        self.enemy = enemy
        # visina i sirana slike
        self.image = pygame.Surface([width, height])
        self.image = image

        # napravi se pravougaonik cije su dimenzije jednake dimenziji slike
        self.rect = self.image.get_rect()

        # pocetni polozaj igraca
        self.rect.x = x
        self.rect.y = y

        self.decisionX = config.speed_enemy
        self.decisionY = 0

        self.sprite_list = sprite_list

        for temp in sprite_list:

            if temp.__class__.__name__ == "PlayerRender":
                self.player = temp
                break

    def moveEnemy(self, x, y):
        self.rect.x += x
        self.rect.y += y

    # x, y povrtane vrednosti iz procesa za uvecavanje koordinata enemy-a
    def collision(self, x, y):
        collision_list = pygame.sprite.spritecollide (self, self.sprite_list, False)
        for temp in collision_list:
            if temp.__class__.__name__ != "EnemyRender":
                if x > 0:  # igrac se pomera desno
                    self.rect.right = temp.rect.left
                if x < 0:  # levo
                    self.rect.left = temp.rect.right
                if y > 0:  # dole
                    self.rect.bottom = temp.rect.top
                if y < 0:  # gore
                    self.rect.top = temp.rect.bottom
                if temp.__class__.__name__ == "PlayerRender":
                    if temp.lives > 0:
                        temp.lives -= 1
                        temp.rect.x = temp.start_position[0]
                        temp.rect.y = temp.start_position[1]
