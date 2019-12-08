import pygame


class Player (pygame.sprite.Sprite):
    # u slucaju vise slika, proslediti sliku kao argument konstuktora
    def __init__(self, image, width, height, x, y):
        # poziv konstruktora od roditelja
        super ().__init__()

        # visina i sirana slike
        self.image = pygame.Surface ([width, height])
        self.image = image

        # maska oko slike, koristi se za detektovanje kolizije sa drugim Sprite-ovima
        self.mask = pygame.mask.from_surface (self.image)

        # napravi se pravougaonik cije su dimenzije jednake dimenziji slike
        self.rect = self.image.get_rect ()

        # pocetni polozaj igraca
        self.rect.x = x
        self.rect.y = y

    def moveRight(self, pixels, image):
        self.rect.x += pixels
        self.image = image

    def moveLeft(self, pixels, image):
        self.rect.x -= pixels
        self.image = image

    def moveUp(self, pixels, image):
        self.rect.y -= pixels
        self.image = image

    def moveDown(self, pixels, image):
        self.rect.y += pixels
        self.image = image
