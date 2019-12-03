import pygame
pygame.init()


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
