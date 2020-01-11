import pygame
import random
import GameConfig as config
import time
pygame.init()

class Enemy (pygame.sprite.Sprite):
    # u slucaju vise slika, proslediti sliku kao argument konstuktora
    def __init__(self, image, width, height, x, y, gameMap):
        # poziv konstruktora od roditelja
        super ().__init__()

        # visina i sirana slike
        self.image = pygame.Surface ([width, height])
        self.image = image

        # napravi se pravougaonik cije su dimenzije jednake dimenziji slike
        self.rect = self.image.get_rect()

        # pocetni polozaj igraca
        self.rect.x = x
        self.rect.y = y

        self.gameMap = gameMap

        self.decisionX=config.speed
        self.decisionY=0

    def makeDecision(self):
        lista = []
        if self.gameMap[self.rect.y // 50 - 1][self.rect.x // 50] == config.StaticEl.path:
            lista.append (1)
        if self.gameMap[self.rect.y // 50 + 1][self.rect.x // 50] == config.StaticEl.path:
            lista.append (2)
        if self.gameMap[self.rect.y // 50][self.rect.x // 50 - 1] == config.StaticEl.path:
            lista.append (3)
        if self.gameMap[self.rect.y // 50][self.rect.x // 50 + 1] == config.StaticEl.path:
            lista.append (4)

        try:
            putanja = 4
        except:
            putanja = 0

        if putanja == 1:
            self.decisionY = -config.speed
            self.decisionX = 0
        elif putanja == 2:
            self.decisionY = config.speed
            self.decisionX = 0
        elif putanja == 3:
            self.decisionY = 0
            self.decisionX = -config.speed
        elif putanja == 4:
            self.decisionY = 0
            self.decisionX = config.speed
        else:
            self.decisionX = 0
            self.decisionY = 0

    def moveEnemy(self, sprite_list):     #sprite list je lista objekata (zidovi, igraci i ostalo)
        if(self.rect.x % 50 == 0):
            self.makeDecision()
        elif(self.rect.y % 50 == 0):
            self.makeDecision()
        # self.rect.x // 50
        # self.rect.y // 50
        rectXpomocna = self.rect.x
        rectYpomocna = self.rect.y

        # da ne moze da se krece dijagonalno
        if self.rect.y % 50 == 0:
            rectXpomocna += self.decisionX
        if self.rect.x % 50 == 0:
            rectYpomocna += self.decisionY

        self.rect.x = rectXpomocna
        self.rect.y = rectYpomocna

        collision_list = pygame.sprite.spritecollide (self, sprite_list, False)
        for temp in collision_list:
            if temp != self:
                if self.decisionX > 0:  # igrac se pomera desno
                    self.rect.right = temp.rect.left

                elif self.decisionX < 0:  # levo
                    self.rect.left = temp.rect.right

                elif self.decisionY > 0:  # dole
                    self.rect.bottom = temp.rect.top

                elif self.decisionY < 0:  # gore
                    self.rect.top = temp.rect.bottom

        """
        # kolizija sa zidom i drugim igracima
        collision_list = pygame.sprite.spritecollide (self, sprite_list, False)
        for temp in collision_list:
            if temp != self:
                if self.decisionX > 0:       # igrac se pomera desno
                    self.rect.right = temp.rect.left
                    if self.rect.x % 50 == 0:

                        self.decisionY=random.choice([config.speed, -config.speed])
                        self.decisionX=0


                elif self.decisionX < 0:       # levo
                    self.rect.left = temp.rect.right
                    self.decisionX=random.choice([0, config.speed])
                    if (self.decisionX == 0):
                        self.decisionY = random.choice ([-config.speed, config.speed])
                    else:
                        self.decisionY = 0


                elif self.decisionY > 0:       # dole
                    self.rect.bottom = temp.rect.top
                    self.decisionY=random.choice([0, -config.speed])
                    if (self.decisionY == 0):
                        self.decisionX = random.choice ([-config.speed, config.speed])
                    else:
                        self.decisionX = 0


                elif self.decisionY < 0:       # gore
                    self.rect.top = temp.rect.bottom
                    self.decisionY=random.choice([0, config.speed])
                    if (self.decisionY == 0):
                        self.decisionX = random.choice ([-config.speed, config.speed])
                    else:
                        self.decisionX = 0
"""





































def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.movex = 0  # move along X
    self.movey = 0  # move along Y
    self.frame = 0  # count frames, mislim da nam ovo treba za animacije

    def control(self, x, y):            #funkcija za kretanje
        '''
        control player movement
        '''
        self.movex += x
        self.movey += y

    def update(self):                   #update pozicije neprijatelja
        '''
        Update sprite position
        '''
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

    #funkcija koja ce birati put po kom se neprijatelj krece kad uoci igraca
    def choosePath(self, player):
        if(self.movex==player.movex | self.movey==player.movey):  #neprijatelj je uocio igraca u svojoj koloni ili vrsti, dalja provera
            if(player.movex > self.movex):
                print("Krecem se ka dole")
