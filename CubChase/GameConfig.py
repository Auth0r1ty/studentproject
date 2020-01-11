from enum import Enum
import pygame
import os
import Field
from GameStaticObject import GameStaticObject
from Player import Player


########################################   IMAGES   ###############################################

# define wall image
wall = pygame.image.load("img/wall2.jpg")
wall = pygame.transform.scale(wall, (50, 50))

# define path image
path = pygame.image.load("img/sand_empty.png")
path = pygame.transform.scale(path, (50, 50))

# define player1, player2 image and their path
simba = pygame.image.load("img/simba.png")
simba = pygame.transform.scale(simba, (50, 50))
nala = pygame.image.load("img/nala.png")
nala = pygame.transform.scale(nala, (50, 50))

pathPlayer1 = pygame.image.load("img/sand_blue.png")
pathPlayer1 = pygame.transform.scale(pathPlayer1, (50, 50))

pathPlayer2 = pygame.image.load("img/sand_red.png")
pathPlayer2 = pygame.transform.scale(pathPlayer2, (50, 50))

# enter image
enter = pygame.image.load("img/sand_red.png")
enter = pygame.transform.scale(enter, (50, 50))

# define path for images (menu, score) and music
app_path = os.path.dirname(__file__)+'/'
files_path = app_path + 'img/'

# ########################################   ENUMS   ################################################


class FieldType(Enum):
    path = 1
    wall = 2
    enter = 3
    trap = 4
    pathPlayer1 = 5   #
    pathPlayer2 = 6

class StaticEl(Enum):
    path = 1
    wall = 2
    enter = 3
    trap = 4
    pathPlayer1 = 5   #
    pathPlayer2 = 6


# ######################################   CONSTANTS   ##############################################

height = 600
width = 800
speed = 2
fps = 60

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


def map_init(sprite_list):
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
