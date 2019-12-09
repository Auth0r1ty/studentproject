import pygame


class GameStaticObject(pygame.sprite.Sprite):
    def __init__(self, image, width, height, xx, yy):
        super().__init__()
        self.x = xx
        self.y = yy
        self.width = width
        self.height = height
        # visina i sirana slike
        self.image = pygame.Surface([width, height])
        self.image = image
        # maska oko slike, koristi se za detektovanje kolizije sa drugim Sprite-ovima
        self.mask = pygame.mask.from_surface(self.image)
        # napravi se pravougaonik cije su dimenzije jednake dimenziji slike
        self.rect = self.image.get_rect()
        # pocetni polozaj igraca
        self.rect.x = xx
        self.rect.y = yy

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
