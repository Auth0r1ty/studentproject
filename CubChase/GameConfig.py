
import pygame
import os
from GameStaticObject import *
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
gameTerrain = [[[] for j in range(16)]for i in range(12)]

def map_init(sprite_list):
    for i in range(0, 12):
        for j in range(0, 16):
            if gameMap[i][j] == StaticEl.wall:
                obj = GameStaticObject(StaticEl.wall, wall, 50, 50, j * 50, i * 50, False)
                sprite_list.add(obj)
                gameTerrain[i][j] = obj
            elif gameMap[i][j] == StaticEl.path:
                obj = GameStaticObject(StaticEl.path, path, 50, 50, j * 50, i * 50, True)

                if i-1 > -1 and gameMap[i-1][j] == StaticEl.path:
                    obj.insertOrientation(Orientation.up)
                if i+1 < 12 and gameMap[i+1][j] == StaticEl.path:
                    obj.insertOrientation(Orientation.down)
                if j-1 > -1 and gameMap[i][j-1] == StaticEl.path:
                    obj.insertOrientation(Orientation.left)
                if j+1 < 16 and gameMap[i][j+1] == StaticEl.path:
                    obj.insertOrientation(Orientation.right)

                obj.crossroadCheck()
                gameTerrain[i][j] = obj

    # popravka da igraci ne izlaze van mape
    i = -1
    for j in range(0, 16):
        obj = GameStaticObject(StaticEl.wall, wall, 50, 50, j * 50, i * 50)
        sprite_list.add(obj)
    i = 12
    for j in range(0, 16):
        obj = GameStaticObject(StaticEl.wall, wall, 50, 50, j * 50, i * 50)
        sprite_list.add(obj)
    j = -1
    for i in range(0, 12):
        obj = GameStaticObject(StaticEl.wall, wall, 50, 50, j * 50, i * 50)
        sprite_list.add(obj)
    j = 16
    for i in range(0, 12):
        obj = GameStaticObject(StaticEl.wall, wall, 50, 50, j * 50, i * 50)
        sprite_list.add(obj)
