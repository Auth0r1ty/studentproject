import pygame
from Enums import *


class GameStaticObject:
    def __init__(self, fieldType):
        self.is_crossroad = False
        self.orientations = []
        self.field_type = fieldType


class GameStaticObjectRender(pygame.sprite.Sprite):
    def __init__(self, fieldType: StaticEl, image, width, height, xx, yy, canMove: bool = False, isCrossroad: bool = False):
        super().__init__()

        self.game_static_object = GameStaticObject(fieldType)

        self.fieldType = fieldType
        self.isCrossroad = isCrossroad
        self.orientations = []

        self.canMove = canMove
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
        self.game_static_object.orientations.append(o)

    def crossroadCheck(self):
        if len(self.orientations) > 2 or len(self.orientations) == 1:
            self.isCrossroad = True
            self.game_static_object.is_crossroad = True
        elif len(self.orientations) == 2:
            if self.orientations.__contains__(Orientation.right) and self.orientations.__contains__(Orientation.up):
                self.isCrossroad = True
                self.game_static_object.is_crossroad = True
            elif self.orientations.__contains__(Orientation.right) and self.orientations.__contains__(Orientation.down):
                self.isCrossroad = True
                self.game_static_object.is_crossroad = True
            elif self.orientations.__contains__(Orientation.left) and self.orientations.__contains__(Orientation.up):
                self.isCrossroad = True
                self.game_static_object.is_crossroad = True
            elif self.orientations.__contains__(Orientation.left) and self.orientations.__contains__(Orientation.down):
                self.isCrossroad = True
                self.game_static_object.is_crossroad = True

