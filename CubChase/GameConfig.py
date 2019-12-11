from enum import Enum
import pygame
from GameStaticObject import GameStaticObject
from Player import Player


########################################   IMAGES   ###############################################


# define wall image
wall = pygame.image.load("img/wall.png")
wall = pygame.transform.scale(wall, (50, 50))
# define path image
path = pygame.image.load("img/sand_empty.png")
path = pygame.transform.scale(path, (50, 50))
# define player1 image and his path
timon = pygame.image.load("img/timon.png")
timon = pygame.transform.scale(timon, (50, 50))
pathPlayer1 = pygame.image.load("img/sapice_red.png")
pathPlayer1 = pygame.transform.scale(pathPlayer1, (50, 50))
# enter image
enter = pygame.image.load("img/sapice_red.png")
enter = pygame.transform.scale(enter, (50, 50))


# ########################################   ENUMS   ################################################


class StaticEl(Enum):
    path = 1
    wall = 2
    enter = 3
    trap = 4
    pathPlayer1 = 5   #
    pathPlayer2 = 6
    pathPlayer3 = 7
    pathPlayer4 = 8


# ######################################   CONSTANTS   ##############################################


speed = 5
fps = 60
sprite_list = pygame.sprite.Group()
player = Player(timon, 5, 50, 50, 250, 400)

sprite_list.add(player)
player.sprite_list = sprite_list

gameMap = [
        # 1 (9)             2 (10)         3 (11)       4 (12)        5(13)           6(14)         7(15)          8(16)
        [StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.path,
         StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path],

        [StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path,
         StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path],

        [StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall,
         StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.enter, StaticEl.wall, StaticEl.path, StaticEl.path],

        [StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.wall, StaticEl.path,
         StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.path],

        [StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.path,
         StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.path],

        [StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall,
         StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path],

        [StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path,
         StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path],

        [StaticEl.path, StaticEl.wall, StaticEl.enter, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall,
         StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path],
        # 9 red je ovaj ispod
        [StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path,
         StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.wall, StaticEl.path],
        # 10 red je ovaj ispod
        [StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall,
         StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path],

        [StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path,
         StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall],

        [StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall,
         StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.enter],

    ]


# ######################################   INITMAP   ##############################################


def map_init():
    for i in range(0, 12):
        for j in range(0, 16):
            if gameMap[i][j] == StaticEl.wall:
                obj = GameStaticObject(wall, 50, 50, j * 50, i * 50)
                sprite_list.add(obj)
    i = -1
    for j in range(0, 16):
        obj = GameStaticObject(wall, 50, 50, j * 50, i * 50)
        sprite_list.add(obj)
    i = 12
    for j in range(0, 16):
        obj = GameStaticObject(wall, 50, 50, j * 50, i * 50)
        sprite_list.add(obj)
    j = -1
    for i in range(0, 12):
        obj = GameStaticObject(wall, 50, 50, j * 50, i * 50)
        sprite_list.add(obj)
    j = 16
    for i in range(0, 12):
        obj = GameStaticObject(wall, 50, 50, j * 50, i * 50)
        sprite_list.add(obj)
