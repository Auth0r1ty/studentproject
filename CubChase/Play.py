import pygame
import GameConfig as config
from Player import Player
from Enemy import Enemy
import multiprocessing as mp

class Play():

    def __init__(self, brojIgraca, screen, clock, gameMap):
        self.screen = screen
        self.clock = clock
        self.gameMap = gameMap

        pygame.mouse.set_visible(False)
        pygame.mixer.music.stop()

        self.sprite_list = pygame.sprite.Group()
        config.map_init (self.sprite_list)

        self.player1 = Player (config.simba, 5, 50, 50, 400, 400, self.gameMap)
        self.sprite_list.add (self.player1)
        self.carryOn1 = True

        self.enemy1 = Enemy(config.nala, 50, 50, 300, 50, self.gameMap)
        self.sprite_list.add(self.enemy1)

        if brojIgraca == 2:
            self.player2 = Player (config.nala, 6, 50, 50, 500, 400, self.gameMap)
            self.sprite_list.add (self.player2)
            self.carryOn2 = True


    # region One player
    def one_player(self):
        while self.carryOn1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.carryOn1 = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        self.carryOn1 = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player1.movePlayer(-config.speed, 0, self.sprite_list)
            if keys[pygame.K_RIGHT]:
                self.player1.movePlayer(config.speed, 0, self.sprite_list)
            if keys[pygame.K_UP]:
                self.player1.movePlayer(0, -config.speed, self.sprite_list)
            if keys[pygame.K_DOWN]:
                self.player1.movePlayer(0, config.speed, self.sprite_list)

            #enemy movement

            self.enemy1.moveEnemy(self.sprite_list)


            # iscrtavanje mape
            for i in range(0, 12):
                for j in range(0, 16):
                    if self.gameMap[i][j] == config.StaticEl.path:
                        self.screen.blit(config.path, (j * 50, i * 50))
                    elif self.gameMap[i][j] == config.StaticEl.wall:
                        self.screen.blit(config.wall, (j * 50, i * 50))
                    elif self.gameMap[i][j] == config.StaticEl.enter:
                        self.screen.blit(config.enter, (j * 50, i * 50))
                    elif self.gameMap[i][j] == config.StaticEl.pathPlayer1:
                        self.screen.blit(config.pathPlayer1, (j * 50, i * 50))
                    elif self.gameMap[i][j] == config.StaticEl.pathPlayer2:
                        self.screen.blit (config.pathPlayer2, (j * 50, i * 50))

            # iscrtavanje svih sprit-ova (igraci, zid)
            self.sprite_list.update ()
            self.sprite_list.draw(self.screen)

            # iscrtavanje celog ekrana
            pygame.display.flip()
            self.clock.tick(config.fps)

        return
    # endregion

    # region Two players
    def two_players_firstPlayer(self):
        while self.carryOn1:
            for event in pygame.event.get ():
                if event.type == pygame.QUIT:
                    self.carryOn1 = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        self.carryOn1 = False

            keys = pygame.key.get_pressed ()
            if keys[pygame.K_LEFT]:
                self.player1.movePlayer (-config.speed, 0, self.sprite_list)
            if keys[pygame.K_RIGHT]:
                self.player1.movePlayer (config.speed, 0, self.sprite_list)
            if keys[pygame.K_UP]:
                self.player1.movePlayer (0, -config.speed, self.sprite_list)
            if keys[pygame.K_DOWN]:
                self.player1.movePlayer (0, config.speed, self.sprite_list)

            if keys[pygame.K_a]:
                self.player2.movePlayer (-config.speed, 0, self.sprite_list)
            if keys[pygame.K_d]:
                self.player2.movePlayer (config.speed, 0, self.sprite_list)
            if keys[pygame.K_w]:
                self.player2.movePlayer (0, -config.speed, self.sprite_list)
            if keys[pygame.K_s]:
                self.player2.movePlayer (0, config.speed, self.sprite_list)

            # iscrtavanje mape
            for i in range (0, 12):
                for j in range (0, 16):
                    if self.gameMap[i][j] == config.StaticEl.path:
                        self.screen.blit (config.path, (j * 50, i * 50))
                    elif self.gameMap[i][j] == config.StaticEl.wall:
                        self.screen.blit (config.wall, (j * 50, i * 50))
                    elif self.gameMap[i][j] == config.StaticEl.enter:
                        self.screen.blit (config.enter, (j * 50, i * 50))
                    elif self.gameMap[i][j] == config.StaticEl.pathPlayer1:
                        self.screen.blit (config.pathPlayer1, (j * 50, i * 50))
                    elif self.gameMap[i][j] == config.StaticEl.pathPlayer2:
                        self.screen.blit (config.pathPlayer2, (j * 50, i * 50))

            # iscrtavanje svih sprit-ova (igraci, zid)
            self.sprite_list.update ()
            self.sprite_list.draw (self.screen)

            # iscrtavanje celog ekrana
            pygame.display.flip ()
            self.clock.tick (config.fps)

    def two_players_secondPlayer(self):
        while self.carryOn2:
            for event in pygame.event.get ():
                if event.type == pygame.QUIT:
                    self.carryOn2 = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        self.carryOn2 = False

            keys = pygame.key.get_pressed ()
            if keys[pygame.K_a]:
                self.player2.movePlayer (-config.speed, 0, self.sprite_list)
            if keys[pygame.K_d]:
                self.player2.movePlayer (config.speed, 0, self.sprite_list)
            if keys[pygame.K_w]:
                self.player2.movePlayer (0, -config.speed, self.sprite_list)
            if keys[pygame.K_s]:
                self.player2.movePlayer (0, config.speed, self.sprite_list)

            # iscrtavanje mape
            for i in range (0, 12):
                for j in range (0, 16):
                    if self.gameMap[i][j] == config.StaticEl.path:
                        self.screen.blit (config.path, (j * 50, i * 50))
                    elif self.gameMap[i][j] == config.StaticEl.wall:
                        self.screen.blit (config.wall, (j * 50, i * 50))
                    elif self.gameMap[i][j] == config.StaticEl.enter:
                        self.screen.blit (config.enter, (j * 50, i * 50))
                    elif self.gameMap[i][j] == config.StaticEl.pathPlayer1:
                        self.screen.blit (config.pathPlayer1, (j * 50, i * 50))
                    elif self.gameMap[i][j] == config.StaticEl.pathPlayer2:
                        self.screen.blit (config.pathPlayer2, (j * 50, i * 50))

            # iscrtavanje svih sprit-ova (igraci, zid)
            self.sprite_list.update ()
            self.sprite_list.draw (self.screen)

            # iscrtavanje celog ekrana
            pygame.display.flip ()
            self.clock.tick (config.fps)

    #endregion

    def two_players_online(self):
        print("aa")



