import pygame
import GameConfig as config
import keyboard
from enum import Enum
import time
from Enums import StaticEl, Orientation


class Player:

    def __init__(self, player):
        self.x = 0
        self.y = 0
        self.finished = False
        self.list = []
        self.player = player


    # detect what key is pressed
    def player_control(self):

        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            self.finished = True

        if self.player == 1 or self.player == 3:
            if keyboard.is_pressed(keyboard.key_to_scan_codes("left arrow")):
                self.movePlayer(-config.speed, 0)
            if keyboard.is_pressed(keyboard.key_to_scan_codes("right arrow")):
                self.movePlayer(config.speed, 0)
            if keyboard.is_pressed(keyboard.key_to_scan_codes("up arrow")):
                self.movePlayer(0, -config.speed)
            if keyboard.is_pressed(keyboard.key_to_scan_codes("down arrow")):
                self.movePlayer(0, config.speed)
        elif self.player == 2:
            if keyboard.is_pressed(keyboard.key_to_scan_codes("a")):
                self.movePlayer(-config.speed, 0)
            if keyboard.is_pressed("d"):
                self.movePlayer(config.speed, 0)
            if keyboard.is_pressed(keyboard.key_to_scan_codes("w")):
                self.movePlayer(0, -config.speed)
            if keyboard.is_pressed(keyboard.key_to_scan_codes("s")):
                self.movePlayer(0, config.speed)


    # change coordinates of player
    def movePlayer(self, x, y):
        self.x = x
        self.y = y
        self.list.append((self.x, self.y))

    def return_new_coordinates(self, queue):
        queue.put((self.list, self.finished))
        self.list = []

    # process
    def run_player(self, queue, queue1):
        self.queue = queue
        while not self.finished:
            self.finished = queue1.get()
            self.player_control()
            self.return_new_coordinates(self.queue)


class PlayerRender(pygame.sprite.Sprite):
    def __init__(self, x, y, player, path_player, screen, image, width, height, game_terrain, sprite_list, display_surf, lives: int = 3):

        super().__init__()

        self.player = player
        self.path_player = path_player
        self.screen = screen
        self.image = pygame.Surface([width, height])
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_position = (x, y)
        self.game_terrain = game_terrain
        self.sprite_list = sprite_list

        self.enemy_traped = False
        self.lives = lives
        self.score = 0
        self.total_score = 0
        self.path_checked = 0
        self.emptyPathCounter = 0

        self.display_surf = display_surf

    def move_player(self, x, y):
        tempX = self.rect.x
        tempY = self.rect.y

        if self.rect.y % 50 == 0:
            tempX += x
        if self.rect.x % 50 == 0:
            tempY += y

        self.rect.x = tempX
        self.rect.y = tempY

    def leave_tracks(self, x, y):
        # ostavljanje tragova
        if self.rect.y % 50 == 0 and self.rect.x % 50 == 0:
            currTerrain = self.game_terrain[self.rect.y // 50][self.rect.x // 50]
            if currTerrain.fieldType == config.StaticEl.path or currTerrain.fieldType == self.path_player:
                # i == y, j == x koordinatama
                currTerrain.fieldType = self.path_player
                currTerrain.image = config.pathPlayer1 if self.path_player == StaticEl.pathPlayer1 else config.pathPlayer2
                if x > 0:
                    currTerrain.image = pygame.transform.rotate(currTerrain.image, 270)
                elif x < 0:
                    currTerrain.image = pygame.transform.rotate(currTerrain.image, 90)
                elif y < 0:
                    pass
                elif y > 0:
                    currTerrain.image = pygame.transform.rotate(currTerrain.image, 180)

    def collision(self, x, y):
        # kolizija sa zidom i drugim igracima
        collision_list = pygame.sprite.spritecollide(self, self.sprite_list, False)
        for temp in collision_list:
            if temp.__class__.__name__ != "PlayerRender":
                if x > 0:  # igrac se pomera desno
                    self.rect.right = temp.rect.left
                if x < 0:  # levo
                    self.rect.left = temp.rect.right
                if y > 0:  # dole
                    self.rect.bottom = temp.rect.top
                if y < 0:  # gore
                    self.rect.top = temp.rect.bottom
                if temp.__class__.__name__ == "EnemyRender" and not self.enemy_traped:
                    if self.lives > 0:
                        self.lives -= 1
                        self.rect.x = self.start_position[0]
                        self.rect.y = self.start_position[1]

    def draw_map(self):
        self.emptyPathCounter = 0
        # iscrtavanje mape
        for i in range(0, 12):
            for j in range(0, 16):
                if (self.game_terrain[i][j]).fieldType == StaticEl.path:
                    self.screen.blit(config.path, (j * 50, i * 50))
                    self.emptyPathCounter += 1
                elif (self.game_terrain[i][j]).fieldType == StaticEl.wall:
                    self.screen.blit(config.wall, (j * 50, i * 50))
                elif (self.game_terrain[i][j]).fieldType == StaticEl.enter:
                    self.screen.blit(config.enter, (j * 50, i * 50))
                elif (self.game_terrain[i][j]).fieldType == self.path_player:
                    self.screen.blit((self.game_terrain[i][j]).image, (j * 50, i * 50))
        self.endgame_check(self.emptyPathCounter)

    def endgame_check(self, emptyPathCounter):
        if emptyPathCounter == 0:
            for temp in self.sprite_list:
                if temp.__class__.__name__ == "GameStaticObjectRender" and temp.fieldType == StaticEl.exit:
                    self.sprite_list.remove(temp)

        if emptyPathCounter == 0 and self.rect.x == 750:
            self.player.finished = True

    def get_score(self):
        suma = 0
        for i in range(0, 12):
            for j in range(0, 16):
                if (config.gameTerrain[i][j]).fieldType == self.path_player:
                    suma += 1

        self.score = suma * 100

    def show_score(self, name, level, coordinatesX, coordinatesY, x, x1):
        self.screen.blit (config.table_for_score, [coordinatesX, coordinatesY])

        font = pygame.font.Font ('freesansbold.ttf', 12)
        black = (255, 255, 255)

        level = font.render ('Level ' + str (level), True, black)
        levelRect = level.get_rect ()


        text = font.render (name, True, black)
        result = font.render (str (self.score), True, black)
        textRect = text.get_rect ()
        resRect = result.get_rect ()
        levelRect.center = (x, 25)
        textRect.center = (x, 40)
        resRect.center = (x, 60)


        self.display_surf.blit (level, levelRect)
        self.display_surf.blit (text, textRect)
        self.display_surf.blit (result, resRect)

        # pozicija srca u drvetu-> preostali broj zivota
        xl = x1
        yl = 70
        for i in range (0, self.lives):
            self.display_surf.blit (config.heart, [xl, yl])
            xl = xl + 25