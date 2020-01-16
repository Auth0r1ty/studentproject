import pygame
import GameConfig as config
from Player import Player
from Enemy import Enemy
import Menu
import multiprocessing as mp
import threading


class Play():

    def __init__(self, brojIgraca, screen, clock, gameTerrain):
        self.screen = screen
        self.clock = clock
        self.gameTerrain = gameTerrain

        ############### ja dodao by djole ###################
        self._display_surf = pygame.display.set_mode((config.width, config.height), pygame.HWSURFACE)
        self.number_of_players = brojIgraca
        #####################################################

        pygame.mouse.set_visible(False)
        pygame.mixer.music.stop()

        self.sprite_list = pygame.sprite.Group()
        config.map_init(self.sprite_list)

        self.carryOn = [True]
        self.player1 = Player(config.simba, 5, 400, 400, self.gameTerrain, self._display_surf, self.sprite_list,
                              self.carryOn, self.screen, self.clock)
        self.sprite_list.add(self.player1)

        self.enemy1 = Enemy(config.pumba, 300, 50, self.gameTerrain, self.sprite_list, self.carryOn, screen)
        self.sprite_list.add(self.enemy1)

        if brojIgraca == 2:
            self.player2 = Player(config.nala, 6, 500, 400, self.gameTerrain, self._display_surf, self.sprite_list,
                                  self.carryOn, self.screen, self.clock)
            self.sprite_list.add(self.player2)
            self.enemy2 = Enemy(config.timon, 500, 50, self.gameTerrain, self.sprite_list, self.carryOn, screen)
            self.sprite_list.add(self.enemy2)



    def one_player(self):
        while self.carryOn[0]:
           self.player1.run()
           self.enemy1.run()
        #t1 = threading.Thread(target=self.player1.run, args=())
        #t1.start()

        #t2 = threading.Thread(target=self.enemy1.run, args=())
        #t2.start()

        #t1.join()
        #t2.join()

    def two_players_firstPlayer(self):
        pass
        """while self.carryOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.carryOn = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        self.carryOn = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player1.movePlayer(-config.speed, 0, self.sprite_list)
            if keys[pygame.K_RIGHT]:
                self.player1.movePlayer(config.speed, 0, self.sprite_list)
            if keys[pygame.K_UP]:
                self.player1.movePlayer(0, -config.speed, self.sprite_list)
            if keys[pygame.K_DOWN]:
                self.player1.movePlayer(0, config.speed, self.sprite_list)

            if keys[pygame.K_a]:
                self.player2.movePlayer(-config.speed, 0, self.sprite_list)
            if keys[pygame.K_d]:
                self.player2.movePlayer(config.speed, 0, self.sprite_list)
            if keys[pygame.K_w]:
                self.player2.movePlayer(0, -config.speed, self.sprite_list)
            if keys[pygame.K_s]:
                self.player2.movePlayer(0, config.speed, self.sprite_list)

            self.enemy1.moveEnemy()
            self.enemy2.moveEnemy()

            emptyPathCounter = 0
            # iscrtavanje mape
            for i in range(0, 12):
                for j in range(0, 16):
                    if (self.gameTerrain[i][j]).fieldType == config.StaticEl.path:
                        self.screen.blit(config.path, (j * 50, i * 50))
                        emptyPathCounter += 1
                    elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.wall:
                        self.screen.blit(config.wall, (j * 50, i * 50))
                    elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.enter:
                        self.screen.blit(config.enter, (j * 50, i * 50))
                    elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.pathPlayer1:
                        self.screen.blit((self.gameTerrain[i][j]).image, (j * 50, i * 50))
                    elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.pathPlayer2:
                        self.screen.blit((self.gameTerrain[i][j]).image, (j * 50, i * 50))

            if emptyPathCounter == 4:
                for temp in self.sprite_list:
                    if temp.__class__.__name__ == "GameStaticObject" and temp.fieldType == config.StaticEl.exit:
                        self.sprite_list.remove(temp)

            if self.player1.rect.x > 799 or self.player2.rect.x > 799:
                self.carryOn = False

            # iscrtavanje svih sprit-ova (igraci, zid)
            self.sprite_list.update()
            self.sprite_list.draw(self.screen)

            ##################### ispis za poene i zivote igraca BY DJOLE #################
            self.player_one_score = self.player_one_get_score.get_score()
            self.player_two_score = self.player_two_get_score.get_score2()

            self.screen.blit(self.table_for_score, [5, 5])
            self.screen.blit(self.table_for_score, [650, 5])

            font = pygame.font.Font('freesansbold.ttf', 12)
            black = (255, 255, 255)

            text = font.render('Player 1', True, black)
            result = font.render(str(self.player_one_score), True, black)
            textRect = text.get_rect()
            resRect = result.get_rect()
            textRect.center = (70, 35)
            resRect.center = (70, 55)
            self._display_surf.blit(text, textRect)
            self._display_surf.blit(result, resRect)

            text2 = font.render('Player 2', True, black)
            result2 = font.render(str(self.player_two_score), True, black)
            textRect2 = text2.get_rect()
            resRect2 = result2.get_rect()
            textRect2.center = (720, 35)
            resRect2.center = (720, 55)
            self._display_surf.blit(text2, textRect2)
            self._display_surf.blit(result2, resRect2)
            xl = 35
            yl = 65
            for i in range(0, self.player_one_lives):
                self._display_surf.blit(self.life, [xl, yl])
                xl = xl + 25

            xl = 680

            for i in range(0, self.player_two_lives):
                self._display_surf.blit(self.life, [xl, yl])
                xl = xl + 25
            ######################################################################

            # iscrtavanje celog ekrana
            pygame.display.flip()
            self.clock.tick(config.fps)"""

    # endregion
