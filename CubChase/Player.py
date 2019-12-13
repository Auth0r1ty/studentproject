import pygame
import GameConfig as config


class Player (pygame.sprite.Sprite):

    pathPlayer = None

    # u slucaju vise slika, proslediti sliku kao argument konstuktora
    def __init__(self, image, pathPlayer, width, height, x, y):
        # poziv konstruktora od roditelja
        super ().__init__()

        self.pathPlayer = pathPlayer

        # visina i sirana slike
        self.image = pygame.Surface ([width, height])
        self.image = image

        # maska oko slike, koristi se za detektovanje kolizije sa drugim Sprite-ovima
        # self.mask = pygame.mask.from_surface (self.image)

        # napravi se pravougaonik cije su dimenzije jednake dimenziji slike
        self.rect = self.image.get_rect()

        # pocetni polozaj igraca
        self.rect.x = x
        self.rect.y = y

    def movePlayer(self, x, y, sprite_list):

        if self.rect.y % 50 == 0 & self.rect.x % 50 == 0:
            # i == y, j == x koordinatama
            config.gameMap[self.rect.y // 50][self.rect.x // 50] = config.StaticEl(self.pathPlayer)


    def moveUp(self, pixels, image):
        self.rect.y -= pixels
        self.image = image

    def moveDown(self, pixels, image):
        self.rect.y += pixels
        self.image = image

    def movePlayer(self, x, y, sprite_list):

        if (self.rect.y % 50) == 0:
            self.rect.x += x

        if (self.rect.x % 50) == 0:
            self.rect.y += y
        # da ne moze da se krece dijagonalno
        if self.rect.y % 50 == 0:
            self.rect.x += x
        if self.rect.x % 50 == 0:
            self.rect.y += y



        # kolizija sa zidom
        collision_list = pygame.sprite.spritecollide (self, sprite_list, False)
        for temp in collision_list:
            if temp != self:
                if x > 0:       # igrac se pomera desno
                    self.rect.right = temp.rect.left
                if x < 0:       # levo
                    self.rect.left = temp.rect.right
                if y > 0:       # dole
                    self.rect.bottom = temp.rect.top
                if y < 0:       # gore
                    self.rect.top = temp.rect.bottom
