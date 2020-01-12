import pygame
import GameConfig as config


class Player (pygame.sprite.Sprite):

    pathPlayer = None

    # u slucaju vise slika, proslediti sliku kao argument konstuktora
    def __init__(self, image, pathPlayer, width, height, x, y, gameMap, lives: int = 3):
        # poziv konstruktora od roditelja
        super ().__init__()

        #broj zivota
        self.lives = lives


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

        self.gameMap = gameMap

    def movePlayer(self, x, y, sprite_list):

        # ostavljanje tragova
        if self.rect.y % 50 == 0 and self.rect.x % 50 == 0:
            if self.gameMap[self.rect.y // 50][self.rect.x // 50] == config.StaticEl.path:
                # i == y, j == x koordinatama
                self.gameMap[self.rect.y // 50][self.rect.x // 50] = config.StaticEl(self.pathPlayer)

        rectXpomocna = self.rect.x
        rectYpomocna = self.rect.y

        # da ne moze da se krece dijagonalno
        if self.rect.y % 50 == 0:
            rectXpomocna += x
        if self.rect.x % 50 == 0:
            rectYpomocna += y

        self.rect.x = rectXpomocna
        self.rect.y = rectYpomocna

        # kolizija sa zidom i drugim igracima
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
