import pygame
from enum import Enum


class StaticEl(Enum):
    path = 1
    wall = 2
    enter = 3
    trap = 4
    pathPlayer1 = 5   #
    pathPlayer2 = 6
    none = 7


class Orientation(Enum):
    left = 1
    right = 2
    up = 3
    down = 4


class GameStaticObject(pygame.sprite.Sprite):
    def __init__(self, fieldType: StaticEl, image, width, height, xx, yy, canMove: bool = False, isCrossroad: bool = False):
        super().__init__()

        #nova polja
        self.fieldType = fieldType
        self.isCrossroad = isCrossroad
        self.orientations = []
        self.canMove = canMove

        self.x = xx
        self.y = yy
        self.width = width
        self.height = height
        # visina i sirana slike
        self.image = pygame.Surface([width, height])
        self.image = image
        # maska oko slike, koristi se za detektovanje kolizije sa drugim Sprite-ovima
        # self.mask = pygame.mask.from_surface(self.image)
        # napravi se pravougaonik cije su dimenzije jednake dimenziji slike
        self.rect = self.image.get_rect()
        # pocetni polozaj igraca
        self.rect.x = xx
        self.rect.y = yy

    def insertOrientation(self, o: Orientation):
        self.orientations.append(o)

    def crossroadCheck(self):
        if len(self.orientations) > 2 or len(self.orientations) == 1:
            self.isCrossroad = True
        elif len(self.orientations) == 2:
            if self.orientations.__contains__(Orientation.right) and self.orientations.__contains__(Orientation.up):
                self.isCrossroad = True
            elif self.orientations.__contains__(Orientation.right) and self.orientations.__contains__(Orientation.down):
                self.isCrossroad = True
            elif self.orientations.__contains__(Orientation.left) and self.orientations.__contains__(Orientation.up):
                self.isCrossroad = True
            elif self.orientations.__contains__(Orientation.left) and self.orientations.__contains__(Orientation.down):
                self.isCrossroad = True

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_image(self):
        return self.image
