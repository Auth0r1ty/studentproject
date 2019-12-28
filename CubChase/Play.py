import pygame
import GameConfig as config
from Player import Player
import multiprocessing as mp

class Play():

    def __init__(self, screen, clock, gameMap):
        self.screen = screen
        self.clock = clock
        self.gameMap = gameMap
        self.sprite_list = pygame.sprite.Group()
        config.map_init (self.sprite_list)
        # self.queue = mp.Queue()

    # region One player
    def one_player(self):
        player = Player(config.simba, 5, 50, 50, 500, 400, self.gameMap)
        self.sprite_list.add(player)
        pygame.mouse.set_visible(False)
        pygame.mixer.music.stop()
        carryOn = True

        while carryOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    carryOn = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        carryOn = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.movePlayer(-config.speed, 0, self.sprite_list)
            if keys[pygame.K_RIGHT]:
                player.movePlayer(config.speed, 0, self.sprite_list)
            if keys[pygame.K_UP]:
                player.movePlayer(0, -config.speed, self.sprite_list)
            if keys[pygame.K_DOWN]:
                player.movePlayer(0, config.speed, self.sprite_list)

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
    def two_players_1stplayer(self):
        a = 5

    def two_players_2ndplayer(self):
        a = 5
    #endregion

    def two_players_online(self):
        print("aa")



