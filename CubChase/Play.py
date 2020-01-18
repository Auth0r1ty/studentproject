import pygame
from threading import Timer
import GameConfig as config
from Player import Player
from Enemy import Enemy
from ClientConnect import ClientConnect
import sys
import Menu
from multiprocessing import Process, Queue, Value


class Play():

    def __init__(self, brojIgraca, screen, clock, gameTerrain):
        self.screen = screen
        self.clock = clock
        self.gameTerrain = gameTerrain

        ############### ja dodao by djole ###################
        self._display_surf = pygame.display.set_mode((config.width, config.height), pygame.HWSURFACE)
        self.table_for_score = pygame.image.load("img/Tabla.png") #PREBACENO
        self.table_for_score = pygame.transform.scale(self.table_for_score, (150, 115))
        self.sign_for_home = pygame.image.load("img/Left_sign.png") #PREBACENO
        self.sign_for_home = pygame.transform.scale(self.sign_for_home, (200, 50)) #PREBACENO
        self.sign_for_next_level = pygame.image.load("img/Right_sign.png") #PREBACENO
        self.sign_for_next_level = pygame.transform.scale(self.sign_for_next_level, (200, 50)) #PREBACENO

        #prva zamka
        self.mud1 = pygame.image.load("img/Mud.png")
        self.mud1 = pygame.transform.scale(self.mud1, (50, 50))
        self.mud1_status = 1 #ako ima vrednost 1, prikazi zamku, ako je 2 aktivna je, ako je 0 vec je iskoriscena
        self.mud1_timer = None
        ##########################

        #druga zamka
        self.mud2 = pygame.image.load("img/Mud.png")
        self.mud2 = pygame.transform.scale(self.mud2, (50, 50))
        self.mud2_status = 1 #ako ima vrednost 1, prikazi zamku, ako je 2 aktivna je, ako je 0 vec je iskoriscena
        self.mud2_timer = None
        ############################################
        self.tournament = False #oznacava da li se igra ili ne turnir
        self.tournament_finished = False #da li je doslo do kraja turnira tj da li je ostao samo jedan igrac
        self.bonus_level = False #ako je nereseno kod turnira daj bonus nivo

        self.player1_name = None #ime da bi se znalo ko igra (Player1, 2, 3....)
        self.player2_name = None #ime da bi se znalo ko igra (Player1, 2, 3....)
        self.player1_number = 0 #ova prom kako bih znao od kojeg player-a iz niza da uzmem poene (kako bih indeksirao niz)
        self.player2_number = 0 #ova prom kako bih znao od kojeg player-a iz niza da uzmem poene (kako bih indeksirao niz)

        self.background_for_result = None #za sliku pozadine
        self.player1_score = 0 #PREBACENO, skor igraca 1 na trenutnom levelu
        self.player1_total_score = 0 #PREBACENO, ukupan skor igraca 1 (svi leveli)
        self.player1_bonus = 0 #PREBACENO, bonus poeni igraca 1(broj preostalih zivota * 100)

        self.player2_score = 0 #PREBACENO, skor igraca 2 na trenutnom levelu
        self.player2_total_score = 0 #PREBACENO, ukupan skor igraca 2 (svi leveli)
        self.player2_bonus = 0 #PREBACENO, bonus poeni igraca 2(broj preostalih zivota * 100)

        self.player1_finished = False #PREBACENO da li je prvi igrac zavrsio igru (svuda ostavio sapice)
        self.player2_finished = False #PREBACENO da li je drugi igrac zavrsio igru (svuda ostavio sapice)

        self.player1_dead = False #PREBACENO da li je prvi igrac mrtav (izgubio sve zivote)
        self.player2_dead = False #PREBACENO da li je drugi igrac mrtav (izgubio sve zivote)

        self.game_over = False #PREBACENO kraj igre
        self.rage_quit = False #PREBACENO nasilno napustanje igre (klik na 'x')

        self.show_bonus = False #PREBACENO oznacava da li ce srce biti prikazano ili ne
        self.show_bonus_timer = None #timer koji meri 4 sekunde i onda treba prikazati zivot
        self.hide_bonus_timer = None #timer koji meri 2 sekunde i onda se brise zivot sa mape
        self.heart_counter = 0 #srce ce se ubaciti na 15 razlicitih mesta na mapi, pa mi treba brojac da bih menjao koordinate
        self.heart_coordinates = (0, 0) #koordinate gde ce biti prikazano srce

        self.online_game = 0
        self.number_of_players = brojIgraca #PREBACENO
        self.bonus_image = pygame.image.load("img/Heart.png") #PREBACENO, slika za zivot (srce)
        self.level = 1 #brojac za levele (potreban za ispis na kraju levela)
        #####################################################

        pygame.mouse.set_visible(False)
        pygame.mixer.music.stop()

        self.sprite_list = pygame.sprite.Group()
        config.map_init(self.sprite_list)

        #self.carryOn = True
        self.player1 = Player(config.simba, 5, 50, 50, 400, 400, self.gameTerrain)
        self.sprite_list.add(self.player1)

        self.enemy1 = Enemy(config.pumba, 50, 50, 300, 50, self.gameTerrain, self.sprite_list)
        self.sprite_list.add(self.enemy1)

        if brojIgraca == 2 or 3 < brojIgraca < 9:
            self.player2 = Player(config.nala, 6, 50, 50, 500, 400, self.gameTerrain)
            self.sprite_list.add(self.player2)
            self.enemy2 = Enemy(config.timon, 50, 50, 500, 50, self.gameTerrain, self.sprite_list)
            self.sprite_list.add(self.enemy2)

    def show_bonus_timer_stopped(self):
        if self.heart_counter == 0:
            self.heart_coordinates = (150, 200)
        if self.heart_counter == 1:
            self.heart_coordinates = (500, 450)
        if self.heart_counter == 2:
            self.heart_coordinates = (600, 150)
        if self.heart_counter == 3:
            self.heart_coordinates = (200, 50)
        if self.heart_counter == 4:
            self.heart_coordinates = (200, 300)
        if self.heart_counter == 5:
            self.heart_coordinates = (400, 250)
        if self.heart_counter == 6:
            self.heart_coordinates = (200, 450)
        if self.heart_counter == 7:
            self.heart_coordinates = (100, 400)
        if self.heart_counter == 8:
            self.heart_coordinates = (600, 400)
        if self.heart_counter == 9:
            self.heart_coordinates = (700, 100)
        if self.heart_counter == 10:
            self.heart_coordinates = (400, 150)
        if self.heart_counter == 11:
            self.heart_coordinates = (600, 50)
        if self.heart_counter == 12:
            self.heart_coordinates = (500, 250)
        if self.heart_counter == 13:
            self.heart_coordinates = (50, 450)
        if self.heart_counter == 14:
            self.heart_coordinates = (600, 500)

        if self.heart_counter == 14:
            self.heart_counter = 0
        else:
            self.heart_counter += 1

        self.show_bonus = True
        self.hide_bonus_timer = Timer(2.0, self.hide_bonus_timer_stopped) #posle dve sekunde se sklanja srce
        self.hide_bonus_timer.start()

    def hide_bonus_timer_stopped(self):
        self.show_bonus = False
        self.show_bonus_timer = Timer(4.0, self.show_bonus_timer_stopped)
        self.show_bonus_timer.start()

    def one_player(self):
        if self.show_bonus_timer is not None:
            self.show_bonus_timer.cancel()
        if self.hide_bonus_timer is not None:
            self.hide_bonus_timer.cancel()

        self.show_bonus_timer = Timer(2.0, self.show_bonus_timer_stopped) #posle 5 sekundi prikazi srce
        self.show_bonus_timer.start()

        while not self.player1_finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.player1_finished = True
                    self.rage_quit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.player1_finished = True
                        self.rage_quit = True

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

            if self.player1.lives <= 0:
                self.player1_finished = True
                self.game_over = True
                pygame.time.delay(500)

            if self.player1.rect.x == 750 and self.player1.rect.y == 500: #znaci da je dosao dole na izlaz
            #onda treba proveriti da li je svuda ostavio tragove, ako jeste, onda moze da izadje
                if self.player1.path_checked > 1: #trenutno sam zakucao na onoliko koliko ima praznih polja
                    self.player1_finished = True


            # iscrtavanje svih sprit-ova (igraci, zid)
            self.sprite_list.update()
            self.sprite_list.draw(self.screen)

            self.check_muds() #ja dodao by djole... dodavanje i provera za zamke da l su aktivne

            if self.enemy1.rect.x == 650 and self.enemy1.rect.y == 300:
                if self.mud1_status == 2:
                    pygame.time.wait(5000)

            if self.enemy1.rect.x == 350 and self.enemy1.rect.y == 500:
                if self.mud2_status == 2:
                    pygame.time.wait(5000)
            ##################### ispis za poene i zivote igraca BY DJOLE #################

            if self.show_bonus:
                self._display_surf.blit(self.bonus_image, self.heart_coordinates)
                if self.player1.rect.x == self.heart_coordinates[0] and self.player1.rect.y == self.heart_coordinates[1] and self.player1.lives != 4:
                    self.player1.lives += 1
                    self.show_bonus = False
            self.player1_score = self.player1.get_score()

            self.screen.blit(self.table_for_score, [5, -5])

            font = pygame.font.Font('freesansbold.ttf', 12)
            black = (255, 255, 255)

            level = font.render('Level ' + str(self.level), True, black)
            levelRect = level.get_rect()
            levelRect.center = (70, 25)

            text = font.render('Player 1', True, black)
            result = font.render(str(self.player1_score), True, black)
            textRect = text.get_rect()
            resRect = result.get_rect()
            textRect.center = (70, 40)
            resRect.center = (70, 60)

            self._display_surf.blit(level, levelRect)
            self._display_surf.blit(text, textRect)
            self._display_surf.blit(result, resRect)

            xl = 30
            yl = 70
            for i in range(0, self.player1.lives):
                self.bonus_image = pygame.image.load("img/Heart.png")
                self._display_surf.blit(self.bonus_image, [xl, yl])
                xl = xl + 25
            ##########################################################################

            # iscrtavanje celog ekrana
            pygame.display.flip()
            self.clock.tick(config.fps)

        self.player1_bonus = self.player1.lives * 100
        self.player1_total_score += self.player1_bonus + self.player1_score

        if not self.rage_quit and not self.game_over:
            pygame.time.delay(500)
            self.show_result()

        if self.game_over:
            self.show_game_over()

    def two_players_offline(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        if self.show_bonus_timer is not None:
            self.show_bonus_timer.cancel()
        if self.hide_bonus_timer is not None:
            self.hide_bonus_timer.cancel()

        self.show_bonus_timer = Timer(5.0, self.show_bonus_timer_stopped)  # posle 5 sekundi prikazi srce
        self.show_bonus_timer.start()
        while not self.player1_finished or not self.player2_finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.player1_finished = True
                    self.player2_finished = True
                    self.rage_quit = True
                    self.tournament_finished = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        self.player1_finished = True
                        self.player2_finished = True
                        self.rage_quit = True
                        self.tournament_finished = True

            keys = pygame.key.get_pressed()

            if not self.player1_dead:
                if keys[pygame.K_LEFT]:
                    self.player1.movePlayer(-config.speed, 0, self.sprite_list)
                if keys[pygame.K_RIGHT]:
                    self.player1.movePlayer(config.speed, 0, self.sprite_list)
                if keys[pygame.K_UP]:
                    self.player1.movePlayer(0, -config.speed, self.sprite_list)
                if keys[pygame.K_DOWN]:
                    self.player1.movePlayer(0, config.speed, self.sprite_list)

            if not self.player2_dead:
                if keys[pygame.K_a]:
                    self.player2.movePlayer(-config.speed, 0, self.sprite_list)
                if keys[pygame.K_d]:
                    self.player2.movePlayer(config.speed, 0, self.sprite_list)
                if keys[pygame.K_w]:
                    self.player2.movePlayer(0, -config.speed, self.sprite_list)
                if keys[pygame.K_s]:
                    self.player2.movePlayer(0, config.speed, self.sprite_list)

            self.enemy1.moveEnemy(self.sprite_list)
            self.enemy2.moveEnemy(self.sprite_list)

            emptyPathCounter = 0
            # iscrtavanje mape
            for i in range(0, 12):
                for j in range(0, 16):
                    if (self.gameTerrain[i][j]).fieldType == config.StaticEl.path:
                        self.screen.blit(config.path, (j * 50, i * 50))

                    elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.wall:
                        self.screen.blit(config.wall, (j * 50, i * 50))
                    elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.enter:
                        self.screen.blit(config.enter, (j * 50, i * 50))
                    elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.pathPlayer1:
                        self.screen.blit((self.gameTerrain[i][j]).image, (j * 50, i * 50))
                    elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.pathPlayer2:
                        self.screen.blit((self.gameTerrain[i][j]).image, (j * 50, i * 50))

                broj_cekiranih = 0
                if self.player1.lives <= 0:
                    broj_cekiranih += self.player1.path_checked
                    self.player1.image = None
                    self.sprite_list.remove(self.player1)
                    self.player1_finished = True
                    self.player1_dead = True

                if self.player2.lives <= 0:
                    broj_cekiranih += self.player2.path_checked
                    self.player2.image = None
                    self.sprite_list.remove(self.player2)
                    self.player2_finished = True
                    self.player2_dead = True

            if not self.player1_dead and self.player2_dead: #ako je drugi mrtav, onda omoguciti da moze prvi zavrsiti
                if self.player1.rect.x == 750 and self.player1.rect.y == 500:
                    broj_cekiranih += self.player1.path_checked
                    if broj_cekiranih > 1:
                        self.player1_finished = True

            if self.player1_dead and not self.player2_dead:
                if self.player2.rect.x == 750 and self.player2.rect.y == 500:
                    broj_cekiranih += self.player2.path_checked
                    if broj_cekiranih > 1:
                        self.player2_finished = True

            if self.player1.rect.x == 750 and self.player1.rect.y == 500 and self.player2.rect.x == 750 and self.player2.rect.y == 500: #znaci da su dosli na izlaz
            #onda treba proveriti da li je svuda ostavio tragove, ako jeste, onda moze da izadje
                broj_cekiranih = self.player1.path_checked + self.player2.path_checked
                if broj_cekiranih > 1: #trenutno sam zakucao na onoliko koliko ima praznih polja
                    self.player1_finished = True
                    self.player2_finished = True

            # iscrtavanje svih sprit-ova (igraci, zid)
            self.sprite_list.update()
            self.sprite_list.draw(self.screen)

            self.check_muds()  # ja dodao by djole... dodavanje i provera za zamke da l su aktivne

            if (self.enemy1.rect.x == 650 and self.enemy1.rect.y == 300) or (self.enemy2.rect.x == 650 and self.enemy2.rect.y == 300):
                if self.mud1_status == 2:
                    pygame.time.wait(5000)

            if (self.enemy1.rect.x == 350 and self.enemy1.rect.y == 500) or (self.enemy2.rect.x == 350 and self.enemy2.rect.y == 500):
                if self.mud2_status == 2:
                    pygame.time.wait(5000)

            if self.show_bonus:
                self._display_surf.blit(self.bonus_image, self.heart_coordinates)
                if self.player1.rect.x == self.heart_coordinates[0] and self.player1.rect.y == self.heart_coordinates[1] and self.player1.lives != 4:
                    self.player1.lives += 1
                    self.show_bonus = False

                if self.player2.rect.x == self.heart_coordinates[0] and self.player2.rect.y == self.heart_coordinates[1] and self.player2.lives != 4:
                    self.player2.lives += 1
                    self.show_bonus = False

            ##################### ispis za poene i zivote igraca BY DJOLE #################
            self.player1_score = self.player1.get_score()
            self.player2_score = self.player2.get_score2()

            self.screen.blit(self.table_for_score, [5, -5])
            self.screen.blit(self.table_for_score, [650, -5])

            font = pygame.font.Font('freesansbold.ttf', 12)
            black = (255, 255, 255)

            level = font.render('Level ' + str(self.level), True, black)
            levelRect = level.get_rect()
            levelRect.center = (70, 25)

            text = font.render(self.player1_name, True, black)
            result = font.render(str(self.player1_score), True, black)
            textRect = text.get_rect()
            resRect = result.get_rect()
            textRect.center = (70, 40)
            resRect.center = (70, 60)

            self._display_surf.blit(level, levelRect)
            self._display_surf.blit(text, textRect)
            self._display_surf.blit(result, resRect)

            text2 = font.render(self.player2_name, True, black)
            result2 = font.render(str(self.player2_score), True, black)
            textRect2 = text2.get_rect()
            resRect2 = result2.get_rect()
            levelRect.center = (720, 25)
            textRect2.center = (720, 40)
            resRect2.center = (720, 60)

            self._display_surf.blit(level, levelRect)
            self._display_surf.blit(text2, textRect2)
            self._display_surf.blit(result2, resRect2)
            xl = 30
            yl = 70

            for i in range(0, self.player1.lives):
                self._display_surf.blit(self.bonus_image, [xl, yl])
                xl = xl + 25

            xl = 680

            for i in range(0, self.player2.lives):
                self._display_surf.blit(self.bonus_image, [xl, yl])
                xl = xl + 25
            ######################################################################

            # iscrtavanje celog ekrana
            pygame.display.flip()
            self.clock.tick(config.fps)

        self.player1_bonus = self.player1.lives * 100
        self.player1_total_score += self.player1_bonus + self.player1_score

        self.player2_bonus = self.player2.lives * 100
        self.player2_total_score += self.player2_bonus + self.player2_score


        if self.tournament:
            if (self.player1_dead or self.player2_dead) or (not self.player1_dead or not self.player2_dead):
                self.game_over = True

                self.users[self.player1_number]['points'] = self.player1_total_score
                self.users[self.player2_number]['points'] = self.player2_total_score

                if self.users[self.player1_number]['points'] > self.users[self.player2_number]['points']:
                    self.users[self.player1_number]['winner'] = True
                    self.users[self.player2_number]['winner'] = False
                elif self.users[self.player1_number]['points'] < self.users[self.player2_number]['points']:
                    self.users[self.player1_number]['winner'] = False
                    self.users[self.player2_number]['winner'] = True
                else:
                    self.bonus_level = True
                    self.show_result_multiplayer()
                    return
        else:
            if self.player1_dead and self.player2_dead:
                self.game_over = True
                self.show_game_over_multiplayer()
                pygame.time.delay(1000)

        if not self.rage_quit and not self.game_over:
            pygame.time.delay(1000)
            self.show_result_multiplayer()

    def establish_a_connection(self):
        self.n = ClientConnect()
        startPos = read_pos1(self.n.getPos())
        self.me = startPos[2]
        if self.me == 0:
            self.player1.rect.x = startPos[0]
            self.player1.rect.y = startPos[1]
            self.player2.rect.x = 500
            self.player2.rect.y = 400
        else:
            self.player2.rect.x = startPos[0]
            self.player2.rect.y = startPos[1]
            self.player1.rect.x = 400
            self.player1.rect.y = 400

        if self.me == 1:
            self.player1_name = 'Player 1'
            self.player2_name = 'Player 2'
        else:
            self.player1_name = 'Player 2'
            self.player2_name = 'Player 1'

        self.two_players_online()

    def two_players_online(self):
        self.online_game = 1
        if self.show_bonus_timer is not None:
            self.show_bonus_timer.cancel()
        if self.hide_bonus_timer is not None:
            self.hide_bonus_timer.cancel()

        self.show_bonus_timer = Timer(5.0, self.show_bonus_timer_stopped)  # posle 5 sekundi prikazi srce
        self.show_bonus_timer.start()

        self.n.client.send(str.encode("ready"))
        rec = self.n.client.recv(2048).decode()

        #clock = pygame.time.Clock()
        #run = True
        while not self.player1_finished or not self.player2_finished:
            pygame.time.delay(25)
            #clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.player1_finished = True
                    self.player2_finished = True
                    self.rage_quit = True
                    #run = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        self.player1_finished = True
                        self.player2_finished = True
                        self.rage_quit = True
                        #run = False
            keys = pygame.key.get_pressed()

            if (not self.player1_dead and not self.player1_finished and self.me == 0) \
                    or (not self.player2_dead and not self.player2_finished and self.me == 1):
                if self.me == 0:
                    if keys[pygame.K_LEFT]:
                        self.player1.movePlayer(-config.speed, 0, self.sprite_list)
                    if keys[pygame.K_RIGHT]:
                        self.player1.movePlayer(config.speed, 0, self.sprite_list)
                    if keys[pygame.K_UP]:
                        self.player1.movePlayer(0, -config.speed, self.sprite_list)
                    if keys[pygame.K_DOWN]:
                        self.player1.movePlayer(0, config.speed, self.sprite_list)
                else:
                    if keys[pygame.K_LEFT]:
                        self.player2.movePlayer(-config.speed, 0, self.sprite_list)
                    if keys[pygame.K_RIGHT]:
                        self.player2.movePlayer(config.speed, 0, self.sprite_list)
                    if keys[pygame.K_UP]:
                        self.player2.movePlayer(0, -config.speed, self.sprite_list)
                    if keys[pygame.K_DOWN]:
                        self.player2.movePlayer(0, config.speed, self.sprite_list)
            self.enemy1.moveEnemy(self.sprite_list)
            self.enemy2.moveEnemy(self.sprite_list)

            emptyPathCounter = 0
            # iscrtavanje mape
            for i in range(0, 12):
                for j in range(0, 16):
                    if (self.gameTerrain[i][j]).fieldType == config.StaticEl.path:
                        self.screen.blit(config.path, (j * 50, i * 50))

                    elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.wall:
                        self.screen.blit(config.wall, (j * 50, i * 50))
                    elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.enter:
                        self.screen.blit(config.enter, (j * 50, i * 50))
                    elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.pathPlayer1:
                        self.screen.blit((self.gameTerrain[i][j]).image, (j * 50, i * 50))
                    elif (self.gameTerrain[i][j]).fieldType == config.StaticEl.pathPlayer2:
                        self.screen.blit((self.gameTerrain[i][j]).image, (j * 50, i * 50))
            playerPosition = (0, 0)
            if self.me == 0:
                playerPosition = read_pos(self.n.send(make_pos((self.player1.rect.x, self.player1.rect.y))))
                self.player2.rect.x = playerPosition[0]
                self.player2.rect.y = playerPosition[1]
            else:
                playerPosition = read_pos(self.n.send(make_pos((self.player2.rect.x, self.player2.rect.y ))))
                self.player1.rect.x = playerPosition[0]
                self.player1.rect.y = playerPosition[1]

                broj_cekiranih = 0
                if self.player1.lives <= 0:
                    broj_cekiranih += self.player1.path_checked
                    self.player1.image = None
                    self.sprite_list.remove(self.player1)
                    self.player1_finished = True
                    self.player1_dead = True

                if self.player2.lives <= 0:
                    broj_cekiranih += self.player2.path_checked
                    self.player2.image = None
                    self.sprite_list.remove(self.player2)
                    self.player2_finished = True
                    self.player2_dead = True

            if not self.player1_dead and self.player2_dead:  # ako je drugi mrtav, onda omoguciti da moze prvi zavrsiti
                if self.player1.rect.x == 750 and self.player1.rect.y == 500:
                    broj_cekiranih += self.player1.path_checked
                    if broj_cekiranih > 1:
                        self.player1_finished = True

            if self.player1_dead and not self.player2_dead:
                if self.player2.rect.x == 750 and self.player2.rect.y == 500:
                    broj_cekiranih += self.player2.path_checked
                    if broj_cekiranih > 1:
                        self.player2_finished = True

            if self.player1.rect.x == 750 and self.player1.rect.y == 500 and self.player2.rect.x == 750 and self.player2.rect.y == 500:  # znaci da su dosli na izlaz
                # onda treba proveriti da li je svuda ostavio tragove, ako jeste, onda moze da izadje
                broj_cekiranih = self.player1.path_checked + self.player2.path_checked
                if broj_cekiranih > 1:  # trenutno sam zakucao na onoliko koliko ima praznih polja
                    self.player1_finished = True
                    self.player2_finished = True

            # iscrtavanje svih sprit-ova (igraci, zid)
            self.sprite_list.update()
            self.sprite_list.draw(self.screen)

            self.check_muds()  # ja dodao by djole... dodavanje i provera za zamke da l su aktivne

            if (self.enemy1.rect.x == 650 and self.enemy1.rect.y == 300) or (
                    self.enemy2.rect.x == 650 and self.enemy2.rect.y == 300):
                if self.mud1_status == 2:
                    pygame.time.wait(5000)

            if (self.enemy1.rect.x == 350 and self.enemy1.rect.y == 500) or (
                    self.enemy2.rect.x == 350 and self.enemy2.rect.y == 500):
                if self.mud2_status == 2:
                    pygame.time.wait(5000)

            if self.show_bonus:
                self._display_surf.blit(self.bonus_image, self.heart_coordinates)
                if self.player1.rect.x == self.heart_coordinates[0] and self.player1.rect.y == self.heart_coordinates[1] and self.player1.lives != 4:
                    self.player1.lives += 1
                    self.show_bonus = False

                if self.player2.rect.x == self.heart_coordinates[0] and self.player2.rect.y == self.heart_coordinates[1] and self.player2.lives != 4:
                    self.player2.lives += 1
                    self.show_bonus = False

            ##################### ispis za poene i zivote igraca BY DJOLE #################
            self.player1_score = self.player1.get_score()
            self.player2_score = self.player2.get_score2()

            self.screen.blit(self.table_for_score, [5, -5])
            self.screen.blit(self.table_for_score, [650, -5])

            font = pygame.font.Font('freesansbold.ttf', 12)
            black = (255, 255, 255)

            level = font.render('Level ' + str(self.level), True, black)
            levelRect = level.get_rect()
            levelRect.center = (70, 25)

            text = font.render(self.player1_name, True, black)
            result = font.render(str(self.player1_score), True, black)
            textRect = text.get_rect()
            resRect = result.get_rect()
            textRect.center = (70, 40)
            resRect.center = (70, 60)

            self._display_surf.blit(level, levelRect)
            self._display_surf.blit(text, textRect)
            self._display_surf.blit(result, resRect)

            text2 = font.render(self.player2_name, True, black)
            result2 = font.render(str(self.player2_score), True, black)
            textRect2 = text2.get_rect()
            resRect2 = result2.get_rect()
            levelRect.center = (720, 25)
            textRect2.center = (720, 40)
            resRect2.center = (720, 60)

            self._display_surf.blit(level, levelRect)
            self._display_surf.blit(text2, textRect2)
            self._display_surf.blit(result2, resRect2)
            xl = 30
            yl = 70

            for i in range(0, self.player1.lives):
                self._display_surf.blit(self.bonus_image, [xl, yl])
                xl = xl + 25

            xl = 680

            for i in range(0, self.player2.lives):
                self._display_surf.blit(self.bonus_image, [xl, yl])
                xl = xl + 25
            ######################################################################

            # iscrtavanje celog ekrana
            pygame.display.flip()
            self.clock.tick(config.fps)

        if self.me == 0:
            self.n.send(make_pos((self.player1.rect.x, self.player1.rect.y)))
        else:
            self.n.send(make_pos((self.player2.rect.x, self.player2.rect.y)))

        self.player1_bonus = self.player1.lives * 100
        self.player1_total_score += self.player1_bonus + self.player1_score

        self.player2_bonus = self.player2.lives * 100
        self.player2_total_score += self.player2_bonus + self.player2_score

        if self.tournament:
            if (self.player1_dead or self.player2_dead) or (not self.player1_dead or not self.player2_dead):
                self.game_over = True

                self.users[self.player1_number]['points'] = self.player1_total_score
                self.users[self.player2_number]['points'] = self.player2_total_score

                if self.users[self.player1_number]['points'] > self.users[self.player2_number]['points']:
                    self.users[self.player1_number]['winner'] = True
                    self.users[self.player2_number]['winner'] = False
                elif self.users[self.player1_number]['points'] < self.users[self.player2_number]['points']:
                    self.users[self.player1_number]['winner'] = False
                    self.users[self.player2_number]['winner'] = True
                else:
                    self.bonus_level = True
                    self.show_result_multiplayer()
                    return
        else:
            if self.player1_dead and self.player2_dead:
                pygame.time.delay(5000)
                self.game_over = True
                self.show_game_over_multiplayer_online()

        if not self.rage_quit and not self.game_over:
            pygame.time.delay(5000)
            self.show_result_multiplayer_online()

    def mud1_timer_check(self): #posle 10 sekundi zamka se vise ne prikazuje
        self.mud1_status = 0

    def mud2_timer_check(self): #posle 10 sekundi zamka se vise ne prikazuje
        self.mud2_status = 0

    def check_muds(self):
        # za prvu zamku ########################################3
        if self.mud1_status == 1 or self.mud1_status == 2:
            self._display_surf.blit(self.mud1, [650, 300])

            if self.player1.rect.x == 650 and self.player1.rect.y == 300:
                if self.mud1_status == 1:
                    self.mud1_status = 2
                    self.mud1_timer = Timer(10.0, self.mud1_timer_check)
                    self.mud1_timer.start()

        if self.number_of_players == 2:
            if self.player2.rect.x == 650 and self.player2.rect.y == 300:
                if self.mud1_status == 1:
                    self.mud1_status = 2
                    self.mud1_timer = Timer(10.0, self.mud1_timer_check)
                    self.mud1_timer.start()
        #########################################################################

        #za drugu zamku##############################################
        if self.mud2_status == 1 or self.mud2_status == 2:
            self._display_surf.blit(self.mud2, [350, 500])

            if self.player1.rect.x == 350 and self.player1.rect.y == 500:
                if self.mud2_status == 1:
                    self.mud2_status = 2
                    self.mud2_timer = Timer(10.0, self.mud2_timer_check)
                    self.mud2_timer.start()

        if self.number_of_players == 2:
            if self.player2.rect.x == 650 and self.player2.rect.y == 300:
                if self.mud2_status == 1:
                    self.mud2_status = 2
                    self.mud2_timer = Timer(10.0, self.mud2_timer_check)
                    self.mud2_timer.start()
        #########################################################################

    def show_result(self): #za jednog igraca tj single player
        bg = pygame.image.load("img/white.png")
        self.screen.blit(bg, [0, 0])
        self.background_for_result = pygame.image.load("img/1player_score.jpg")
        self.screen.blit(self.background_for_result, [0, 0])

        font = pygame.font.Font('Base05.ttf', 20)
        black = (255, 204, 51)

        self.screen.blit(self.sign_for_home, [0, 535])  # dole levo
        textHome = font.render('HOME', True, black)
        textRectHome = textHome.get_rect()
        textRectHome.center = (95, 560)
        self._display_surf.blit(textHome, textRectHome)

        textLevel = font.render(str(self.level), True, black)
        textRectLevel = textLevel.get_rect()
        textRectLevel.center = (445, 158)
        self._display_surf.blit(textLevel, textRectLevel)

        self.screen.blit(self.sign_for_next_level, [600, 535])  # dole desno
        textNL = font.render('NEXT LEVEL', True, black)
        textRectNL = textNL.get_rect()
        textRectNL.center = (700, 560)
        self._display_surf.blit(textNL, textRectNL)

        # u can't catch me bonus na slici, ide broj preostalih zivota * 100

        level_total = self.player1_score + self.player1_bonus
        cant_catch_me_bonus = font.render(str(self.player1_bonus), True, black)

        # u paw track points na slici, ide sa trenutnog levela (promenljiva result), TO JE ODRADJENO
        # u level total na slici, ide sa trenutnog levela (promenljiva result)
        result = font.render(str(self.player1_score), True, black) #trenutni level
        level_total = font.render(str(level_total), True, black)

        # u total na slici, ide sve ukupno (promenljiva total_results)
        total_results = font.render(str(self.player1_total_score), True, black) #ukupno

        resRect = result.get_rect()
        totalRect = total_results.get_rect()
        cantCatchRect = cant_catch_me_bonus.get_rect()
        levelTotalRect = level_total.get_rect()

        resRect.center = (420, 220)
        totalRect.center = (420, 540)
        cantCatchRect.center = (420, 420)
        levelTotalRect.center = (420, 485)

        pygame.mouse.set_visible(True)
        self._display_surf.blit(result, resRect)
        self._display_surf.blit(cant_catch_me_bonus, cantCatchRect)
        self._display_surf.blit(level_total, levelTotalRect)

        self._display_surf.blit(total_results, totalRect)
        pygame.display.update()

        wait_click_for_next_level = True  # za NEXT LEVEL
        wait_click_for_home = True  # za HOME
        while wait_click_for_next_level and wait_click_for_home:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait_click_for_home = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if 625 < mouse_pos[0] < 788 and 535 < mouse_pos[1] < 585: #za NEXT_LEVEL
                        wait_click_for_next_level = False

                    if 30 < mouse_pos[0] < 180 and 535 < mouse_pos[1] < 585: #za HOME
                        pygame.time.delay(500)
                        wait_click_for_home = False

        if not wait_click_for_next_level:
            config.map_init(self.sprite_list)
            self.player1.rect.x = 400
            self.player1.rect.y = 400
            self.player1.lives = 3
            self.player1_score = 0
            self.player1_finished = False

            self.enemy1.rect.x = 300
            self.enemy1.rect.y = 50
            self.level += 1

            self.show_bonus = False
            self.heart_counter = 0
            self.game_over = False

            self.mud1_status = 1  # ako ima vrednost 1, prikazi zamku, ako je 2 aktivna je, ako je 0 vec je iskoriscena
            self.mud1_timer = None
            self.mud2_status = 1  # ako ima vrednost 1, prikazi zamku, ako je 2 aktivna je, ako je 0 vec je iskoriscena
            self.mud2_timer = None

            self.one_player()

    def show_game_over(self): #za jednog igraca tj single player
        bg = pygame.image.load("img/white.png")
        self.screen.blit(bg, [0, 0])
        self.background_for_result = pygame.image.load("img/1player_game_over.jpg")
        self.screen.blit(self.background_for_result, [0, 0])

        font = pygame.font.Font('Base05.ttf', 20)
        black = (255, 204, 51)

        self.screen.blit(self.sign_for_home, [0, 535])  # dole levo
        textHome = font.render('HOME', True, black)
        textRectHome = textHome.get_rect()
        textRectHome.center = (95, 560)
        self._display_surf.blit(textHome, textRectHome)

        textLevel = font.render(str(self.level), True, black)
        textRectLevel = textLevel.get_rect()
        textRectLevel.center = (445, 158)
        self._display_surf.blit(textLevel, textRectLevel)
        # u can't catch me bonus na slici, ide broj preostalih zivota * 100

        level_total = self.player1_score + self.player1_bonus
        cant_catch_me_bonus = font.render(str(self.player1_bonus), True, black)

        # u paw track points na slici, ide sa trenutnog levela (promenljiva result), TO JE ODRADJENO
        # u level total na slici, ide sa trenutnog levela (promenljiva result)
        result = font.render(str(self.player1_score), True, black)  # trenutni level
        level_total = font.render(str(level_total), True, black)

        # u total na slici, ide sve ukupno (promenljiva total_results)
        total_results = font.render(str(self.player1_total_score), True, black)  # ukupno

        resRect = result.get_rect()
        totalRect = total_results.get_rect()
        cantCatchRect = cant_catch_me_bonus.get_rect()
        levelTotalRect = level_total.get_rect()

        resRect.center = (420, 220)
        totalRect.center = (420, 545)
        cantCatchRect.center = (420, 420)
        levelTotalRect.center = (420, 485)

        pygame.mouse.set_visible(True)
        self._display_surf.blit(result, resRect)
        self._display_surf.blit(cant_catch_me_bonus, cantCatchRect)
        self._display_surf.blit(level_total, levelTotalRect)

        self._display_surf.blit(total_results, totalRect)
        pygame.display.update()

        wait = True
        while wait:
            # pratiti poziciju kursora
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if 30 < mouse_pos[0] < 180 and 535 < mouse_pos[1] < 585:  # za HOME
                        print('uso za home')
                        wait = False

    def show_result_multiplayer_online(self):
        if self.online_game == 1:
            if self.me == 0:
                self.n.send(make_pos((self.player1.rect.x, self.player1.rect.y)))
            else:
                self.n.send(make_pos((self.player2.rect.x, self.player2.rect.y)))
            self.n.client.send(str.encode("finished"))

        bg = pygame.image.load("img/white.png")
        self.screen.blit(bg, [0, 0])

        font = pygame.font.Font('Base05.ttf', 20)
        black = (255, 204, 51)

        self.background_for_result = pygame.image.load("img/2player_score.jpg")
        self.screen.blit(self.background_for_result, [0, 0])

        self.screen.blit(self.sign_for_home, [0, 535])  # dole levo

        textHome = font.render('HOME', True, black)
        textRectHome = textHome.get_rect()
        textRectHome.center = (95, 560)
        self._display_surf.blit(textHome, textRectHome)

        # ispis koji je trenutni nivo
        textLevel = font.render(str(self.level), True, black)
        textRectLevel = textLevel.get_rect()
        textRectLevel.center = (402, 156)
        self._display_surf.blit(textLevel, textRectLevel)

        self.screen.blit(self.sign_for_next_level, [600, 535])  # dole desno
        textNL = font.render('NEXT LEVEL', True, black)
        textRectNL = textNL.get_rect()
        textRectNL.center = (700, 560)
        self._display_surf.blit(textNL, textRectNL)

        # REZULTAT ZA PRVOG IGRACA #####################################################################

        # u can't catch me bonus na slici, ide broj preostalih zivota * 100
        cant_catch_me_bonus_player1 = font.render(str(self.player1_bonus), True, black)

        # u paw track points na slici, ide sa trenutnog levela (promenljiva result)
        result_player1 = font.render(str(self.player1_score), True, black)
        # level total je skor + bonus za zivote
        level_total_player1 = self.player1_score + self.player1_bonus
        level_total_player1 = font.render(str(level_total_player1), True, black)

        # u total na slici, ide sve ukupno (promenljiva total_results)
        total_results_player1 = font.render(str(self.player1_total_score), True, black)

        resRect = result_player1.get_rect()
        cantCatchRect = cant_catch_me_bonus_player1.get_rect()
        levelTotalRect = level_total_player1.get_rect()
        totalRect = total_results_player1.get_rect()

        resRect.center = (230, 220)
        cantCatchRect.center = (230, 420)
        levelTotalRect.center = (230, 485)
        totalRect.center = (230, 540)

        pygame.mouse.set_visible(True)
        self._display_surf.blit(result_player1, resRect)
        self._display_surf.blit(cant_catch_me_bonus_player1, cantCatchRect)
        self._display_surf.blit(level_total_player1, levelTotalRect)
        self._display_surf.blit(total_results_player1, totalRect)
        ############################################################################################

        # REZULTAT ZA DRUGOG IGRACA #####################################################################

        # u can't catch me bonus na slici, ide broj preostalih zivota * 100
        cant_catch_me_bonus_player2 = font.render(str(self.player2_bonus), True, black)

        # u paw track points na slici, ide sa trenutnog levela (promenljiva result)
        result_player2 = font.render(str(self.player2_score), True, black)
        # level total je skor + bonus za zivote
        level_total_player2 = self.player2_score + self.player2_bonus
        level_total_player2 = font.render(str(level_total_player2), True, black)

        # u total na slici, ide sve ukupno (promenljiva total_results)
        total_results_player2 = font.render(str(self.player2_total_score), True, black)

        resRect = result_player2.get_rect()
        cantCatchRect = cant_catch_me_bonus_player2.get_rect()
        levelTotalRect = level_total_player2.get_rect()
        totalRect = total_results_player2.get_rect()

        resRect.center = (540, 220)
        cantCatchRect.center = (540, 420)
        levelTotalRect.center = (540, 485)
        totalRect.center = (540, 540)

        pygame.mouse.set_visible(True)
        self._display_surf.blit(result_player2, resRect)
        self._display_surf.blit(cant_catch_me_bonus_player2, cantCatchRect)
        self._display_surf.blit(level_total_player2, levelTotalRect)
        self._display_surf.blit(total_results_player2, totalRect)
        ############################################################################################
        pygame.display.update()

        wait = True
        wait1 = True  # za NEXT LEVEL
        wait2 = True  # za HOME
        while wait and wait2:
            # pratiti poziciju kursora
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                    self.rage_quit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if 625 < mouse_pos[0] < 788 and 535 < mouse_pos[1] < 585:
                        wait1 = False
                        wait = False

                    if 30 < mouse_pos[0] < 180 and 535 < mouse_pos[1] < 585:  # za HOME
                        self.rage_quit = True
                        pygame.time.delay(500)
                        wait2 = False
        if not wait1:
            config.map_init(self.sprite_list)
            if self.player1_dead:
                self.player1 = Player(config.simba, 5, 50, 50, 400, 400, self.gameTerrain)
                self.sprite_list.add(self.player1)
                self.player1_dead = False

            self.player1.rect.x = 400
            self.player1.rect.y = 400
            self.player1.lives = 3
            self.player1_score = 0
            self.player1_finished = False

            if self.player2_dead:
                self.player2 = Player(config.nala, 6, 50, 50, 500, 400, self.gameTerrain)
                self.sprite_list.add(self.player2)
                self.player2_dead = False

            self.player2.rect.x = 500
            self.player2.rect.y = 400

            self.player2.lives = 3
            self.player2_score = 0
            self.player2_finished = False

            self.enemy1.rect.x = 300
            self.enemy1.rect.y = 50
            self.enemy2.rect.x = 500
            self.enemy2.rect.y = 50

            self.level += 1
            self.show_bonus = False
            self.heart_counter = 0
            self.game_over = False

            self.mud1_status = 1  # ako ima vrednost 1, prikazi zamku, ako je 2 aktivna je, ako je 0 vec je iskoriscena
            self.mud1_timer = None
            self.mud2_status = 1  # ako ima vrednost 1, prikazi zamku, ako je 2 aktivna je, ako je 0 vec je iskoriscena
            self.mud2_timer = None
            if self.online_game == 1:
                self.two_players_online()
            else:
                self.one_player()

    def show_game_over_multiplayer_online(self):
        if not self.rage_quit:
            bg = pygame.image.load("img/white.png")
            self.screen.blit(bg, [0, 0])
            winner = pygame.image.load("img/Winner.png")
            loser = pygame.image.load("img/Loser.png")

            font = pygame.font.Font('Base05.ttf', 20)
            black = (255, 204, 51)

            self.background_for_result = pygame.image.load("img/2player_game_over.jpg")
            self.screen.blit(self.background_for_result, [0, 0])

            self.screen.blit(self.sign_for_home, [0, 535])  # dole levo
            textHome = font.render('HOME', True, black)
            textRectHome = textHome.get_rect()
            textRectHome.center = (95, 560)
            self._display_surf.blit(textHome, textRectHome)

            # ispis koji je trenutni nivo
            textLevel = font.render(str(self.level), True, black)
            textRectLevel = textLevel.get_rect()
            textRectLevel.center = (402, 156)
            self._display_surf.blit(textLevel, textRectLevel)


            # REZULTAT ZA PRVOG IGRACA #####################################################################

            # u can't catch me bonus na slici, ide broj preostalih zivota * 100
            cant_catch_me_bonus_player1 = font.render(str(self.player1_bonus), True, black)

            # u paw track points na slici, ide sa trenutnog levela (promenljiva result)
            result_player1 = font.render(str(self.player1_score), True, black)
            # level total je skor + bonus za zivote
            level_total_player1 = self.player1_score + self.player1_bonus
            level_total_player1 = font.render(str(level_total_player1), True, black)

            # u total na slici, ide sve ukupno (promenljiva total_results)
            total_results_player1 = font.render(str(self.player1_total_score), True, black)
            resRect = result_player1.get_rect()
            cantCatchRect = cant_catch_me_bonus_player1.get_rect()
            levelTotalRect = level_total_player1.get_rect()
            totalRect = total_results_player1.get_rect()

            resRect.center = (230, 220)
            cantCatchRect.center = (230, 420)
            levelTotalRect.center = (230, 485)
            totalRect.center = (230, 540)

            pygame.mouse.set_visible(True)
            self._display_surf.blit(result_player1, resRect)
            self._display_surf.blit(cant_catch_me_bonus_player1, cantCatchRect)
            self._display_surf.blit(level_total_player1, levelTotalRect)
            self._display_surf.blit(total_results_player1, totalRect)
            ############################################################################################

            # REZULTAT ZA DRUGOG IGRACA #####################################################################

            # u can't catch me bonus na slici, ide broj preostalih zivota * 100
            cant_catch_me_bonus_player2 = font.render(str(self.player2_bonus), True, black)

            # u paw track points na slici, ide sa trenutnog levela (promenljiva result)
            result_player2 = font.render(str(self.player2_score), True, black)
            # level total je skor + bonus za zivote
            level_total_player2 = self.player2_score + self.player2_bonus
            level_total_player2 = font.render(str(level_total_player2), True, black)

            # u total na slici, ide sve ukupno (promenljiva total_results)
            total_results_player2 = font.render(str(self.player2_total_score), True, black)

            resRect = result_player2.get_rect()
            cantCatchRect = cant_catch_me_bonus_player2.get_rect()
            levelTotalRect = level_total_player2.get_rect()
            totalRect = total_results_player2.get_rect()

            resRect.center = (540, 220)
            cantCatchRect.center = (540, 420)
            levelTotalRect.center = (540, 485)
            totalRect.center = (540, 540)

            pygame.mouse.set_visible(True)
            self._display_surf.blit(result_player2, resRect)
            self._display_surf.blit(cant_catch_me_bonus_player2, cantCatchRect)
            self._display_surf.blit(level_total_player2, levelTotalRect)
            self._display_surf.blit(total_results_player2, totalRect)

            if self.player1_total_score > self.player2_total_score:
                self.screen.blit(winner, [50, 120]) #prvi pobedio
                self.screen.blit(loser, [600, 120]) #drugi izgubio
            elif self.player1_total_score < self.player2_total_score:
                self.screen.blit(loser, [50, 120]) #prvi izgubio
                self.screen.blit(winner, [600, 120]) #drugi pobedio
            ############################################################################################
            pygame.display.update()

            wait = True
            while wait:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.rage_quit = True
                        wait = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if 30 < mouse_pos[0] < 180 and 535 < mouse_pos[1] < 585:
                            self.rage_quit = True
                            wait = False

    def show_result_multiplayer(self):

        if not self.rage_quit:
            bg = pygame.image.load("img/white.png")
            self.screen.blit(bg, [0, 0])

            font = pygame.font.Font('Base05.ttf', 20)
            black = (255, 204, 51)

            if self.tournament and self.bonus_level:
                self.background_for_result = pygame.image.load("img/Tournament_level_score.jpg")
                self.screen.blit(self.background_for_result, [0, 0])

                player1Name = font.render(self.player1_name, True, black)
                player1Rect = player1Name.get_rect()
                player1Rect.center = (202, 156)
                self._display_surf.blit(player1Name, player1Rect)

                player2Name = font.render(self.player2_name, True, black)
                player2Rect = player2Name.get_rect()
                player2Rect.center = (602, 156)
                self._display_surf.blit(player2Name, player2Rect)
            else:
                self.background_for_result = pygame.image.load("img/2player_score.jpg")
                self.screen.blit(self.background_for_result, [0, 0])

            self.screen.blit(self.sign_for_home, [0, 535])  # dole levo

            textHome = font.render('HOME', True, black)
            textRectHome = textHome.get_rect()
            textRectHome.center = (95, 560)
            self._display_surf.blit(textHome, textRectHome)

            #ispis koji je trenutni nivo
            textLevel = font.render(str(self.level), True, black)
            textRectLevel = textLevel.get_rect()
            textRectLevel.center = (402, 156)
            self._display_surf.blit(textLevel, textRectLevel)

            self.screen.blit(self.sign_for_next_level, [600, 535])  # dole desno
            textNL = font.render('NEXT LEVEL', True, black)
            textRectNL = textNL.get_rect()
            textRectNL.center = (700, 560)
            self._display_surf.blit(textNL, textRectNL)

            #REZULTAT ZA PRVOG IGRACA #####################################################################

            # u can't catch me bonus na slici, ide broj preostalih zivota * 100
            cant_catch_me_bonus_player1 = font.render(str(self.player1_bonus), True, black)

            # u paw track points na slici, ide sa trenutnog levela (promenljiva result)
            result_player1 = font.render(str(self.player1_score), True, black)
            # level total je skor + bonus za zivote
            level_total_player1 = self.player1_score + self.player1_bonus
            level_total_player1 = font.render(str(level_total_player1), True, black)

            # u total na slici, ide sve ukupno (promenljiva total_results)
            total_results_player1 = font.render(str(self.player1_total_score), True, black)

            resRect = result_player1.get_rect()
            cantCatchRect = cant_catch_me_bonus_player1.get_rect()
            levelTotalRect = level_total_player1.get_rect()
            totalRect = total_results_player1.get_rect()

            resRect.center = (230, 220)
            cantCatchRect.center = (230, 420)
            levelTotalRect.center = (230, 485)
            totalRect.center = (230, 540)

            pygame.mouse.set_visible(True)
            self._display_surf.blit(result_player1, resRect)
            self._display_surf.blit(cant_catch_me_bonus_player1, cantCatchRect)
            self._display_surf.blit(level_total_player1, levelTotalRect)
            self._display_surf.blit(total_results_player1, totalRect)
            ############################################################################################

            # REZULTAT ZA DRUGOG IGRACA #####################################################################

            # u can't catch me bonus na slici, ide broj preostalih zivota * 100
            cant_catch_me_bonus_player2 = font.render(str(self.player2_bonus), True, black)

            # u paw track points na slici, ide sa trenutnog levela (promenljiva result)
            result_player2 = font.render(str(self.player2_score), True, black)
            # level total je skor + bonus za zivote
            level_total_player2 = self.player2_score + self.player2_bonus
            level_total_player2 = font.render(str(level_total_player2), True, black)

            # u total na slici, ide sve ukupno (promenljiva total_results)
            total_results_player2 = font.render(str(self.player2_total_score), True, black)

            resRect = result_player2.get_rect()
            cantCatchRect = cant_catch_me_bonus_player2.get_rect()
            levelTotalRect = level_total_player2.get_rect()
            totalRect = total_results_player2.get_rect()

            resRect.center = (540, 220)
            cantCatchRect.center = (540, 420)
            levelTotalRect.center = (540, 485)
            totalRect.center = (540, 540)

            pygame.mouse.set_visible(True)
            self._display_surf.blit(result_player2, resRect)
            self._display_surf.blit(cant_catch_me_bonus_player2, cantCatchRect)
            self._display_surf.blit(level_total_player2, levelTotalRect)
            self._display_surf.blit(total_results_player2, totalRect)
            ############################################################################################
            pygame.display.update()

            wait = True
            wait1 = True  # za NEXT LEVEL
            wait2 = True  # za HOME
            while wait and wait2:
                # pratiti poziciju kursora
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        wait = False
                        self.rage_quit = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if 625 < mouse_pos[0] < 788 and 535 < mouse_pos[1] < 585:
                            wait1 = False
                            wait = False

                        if 30 < mouse_pos[0] < 180 and 535 < mouse_pos[1] < 585:  # za HOME
                            self.rage_quit = True
                            pygame.time.delay(500)
                            wait2 = False

            if not wait1:
                #config.speed_enemy += 1
                config.map_init(self.sprite_list)
                if self.player1_dead:
                    self.player1 = Player(config.simba, 5, 50, 50, 400, 400, self.gameTerrain)
                    self.sprite_list.add(self.player1)
                    self.player1_dead = False

                self.player1.rect.x = 400
                self.player1.rect.y = 400
                self.player1.lives = 3
                self.player1_score = 0
                self.player1_finished = False

                if self.player2_dead:
                    self.player2 = Player(config.nala, 6, 50, 50, 500, 400, self.gameTerrain)
                    self.sprite_list.add(self.player2)
                    self.player2_dead = False

                self.player2.rect.x = 500
                self.player2.rect.y = 400

                self.player2.lives = 3
                self.player2_score = 0
                self.player2_finished = False

                self.enemy1.rect.x = 300
                self.enemy1.rect.y = 50
                self.enemy2.rect.x = 500
                self.enemy2.rect.y = 50

                self.level += 1
                self.show_bonus = False
                self.heart_counter = 0
                self.game_over = False

                self.mud1_status = 1  # ako ima vrednost 1, prikazi zamku, ako je 2 aktivna je, ako je 0 vec je iskoriscena
                self.mud1_timer = None
                self.mud2_status = 1  # ako ima vrednost 1, prikazi zamku, ako je 2 aktivna je, ako je 0 vec je iskoriscena
                self.mud2_timer = None

                self.two_players_offline(self.player1_name, self.player2_name)

    def show_game_over_multiplayer(self):
        if not self.rage_quit:
            bg = pygame.image.load("img/white.png")
            self.screen.blit(bg, [0, 0])
            winner = pygame.image.load("img/Winner.png")
            loser = pygame.image.load("img/Loser.png")

            font = pygame.font.Font('Base05.ttf', 20)
            black = (255, 204, 51)

            if self.tournament:
                self.background_for_result = pygame.image.load("img/Tournament_round_over.jpg")
                self.screen.blit(self.background_for_result, [0, 0])

                player1Name = font.render(self.player1_name, True, black)
                player1Rect = player1Name.get_rect()
                player1Rect.center = (230, 156)
                self._display_surf.blit(player1Name, player1Rect)

                player2Name = font.render(self.player2_name, True, black)
                player2Rect = player2Name.get_rect()
                player2Rect.center = (570, 156)
                self._display_surf.blit(player2Name, player2Rect)
            else:
                self.background_for_result = pygame.image.load("img/2player_game_over.jpg")
                self.screen.blit(self.background_for_result, [0, 0])

            self.screen.blit(self.sign_for_home, [0, 535])  # dole levo
            textHome = font.render('HOME', True, black)
            textRectHome = textHome.get_rect()
            textRectHome.center = (95, 560)
            self._display_surf.blit(textHome, textRectHome)

            # ispis koji je trenutni nivo
            textLevel = font.render(str(self.level), True, black)
            textRectLevel = textLevel.get_rect()
            textRectLevel.center = (402, 156)
            self._display_surf.blit(textLevel, textRectLevel)

            if self.tournament and not self.tournament_finished: #ako nema pobednika, ponudi mu next_round, u suprotnom ima samo home
                self.screen.blit(self.sign_for_next_level, [600, 535])  # dole desno
                textNL = font.render('NEXT ROUND', True, black)
                textRectNL = textNL.get_rect()
                textRectNL.center = (700, 560)
                self._display_surf.blit(textNL, textRectNL)

            # REZULTAT ZA PRVOG IGRACA #####################################################################

            # u can't catch me bonus na slici, ide broj preostalih zivota * 100
            cant_catch_me_bonus_player1 = font.render(str(self.player1_bonus), True, black)

            # u paw track points na slici, ide sa trenutnog levela (promenljiva result)
            result_player1 = font.render(str(self.player1_score), True, black)
            # level total je skor + bonus za zivote
            level_total_player1 = self.player1_score + self.player1_bonus
            level_total_player1 = font.render(str(level_total_player1), True, black)

            # u total na slici, ide sve ukupno (promenljiva total_results)
            total_results_player1 = font.render(str(self.player1_total_score), True, black)
            resRect = result_player1.get_rect()
            cantCatchRect = cant_catch_me_bonus_player1.get_rect()
            levelTotalRect = level_total_player1.get_rect()
            totalRect = total_results_player1.get_rect()

            resRect.center = (230, 220)
            cantCatchRect.center = (230, 420)
            levelTotalRect.center = (230, 485)
            totalRect.center = (230, 540)

            pygame.mouse.set_visible(True)
            self._display_surf.blit(result_player1, resRect)
            self._display_surf.blit(cant_catch_me_bonus_player1, cantCatchRect)
            self._display_surf.blit(level_total_player1, levelTotalRect)
            self._display_surf.blit(total_results_player1, totalRect)
            ############################################################################################

            # REZULTAT ZA DRUGOG IGRACA #####################################################################

            # u can't catch me bonus na slici, ide broj preostalih zivota * 100
            cant_catch_me_bonus_player2 = font.render(str(self.player2_bonus), True, black)

            # u paw track points na slici, ide sa trenutnog levela (promenljiva result)
            result_player2 = font.render(str(self.player2_score), True, black)
            # level total je skor + bonus za zivote
            level_total_player2 = self.player2_score + self.player2_bonus
            level_total_player2 = font.render(str(level_total_player2), True, black)

            # u total na slici, ide sve ukupno (promenljiva total_results)
            total_results_player2 = font.render(str(self.player2_total_score), True, black)

            resRect = result_player2.get_rect()
            cantCatchRect = cant_catch_me_bonus_player2.get_rect()
            levelTotalRect = level_total_player2.get_rect()
            totalRect = total_results_player2.get_rect()

            resRect.center = (540, 220)
            cantCatchRect.center = (540, 420)
            levelTotalRect.center = (540, 485)
            totalRect.center = (540, 540)

            pygame.mouse.set_visible(True)
            self._display_surf.blit(result_player2, resRect)
            self._display_surf.blit(cant_catch_me_bonus_player2, cantCatchRect)
            self._display_surf.blit(level_total_player2, levelTotalRect)
            self._display_surf.blit(total_results_player2, totalRect)

            if self.player1_total_score > self.player2_total_score:
                self.screen.blit(winner, [50, 120]) #prvi pobedio
                self.screen.blit(loser, [600, 120]) #drugi izgubio
            elif self.player1_total_score < self.player2_total_score:
                self.screen.blit(loser, [50, 120]) #prvi izgubio
                self.screen.blit(winner, [600, 120]) #drugi pobedio
            ############################################################################################
            pygame.display.update()

            wait = True  # za next round
            wait2 = True  # za HOME
            while wait and wait2:
                # pratiti poziciju kursora
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.rage_quit = True
                        wait2 = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if 30 < mouse_pos[0] < 180 and 535 < mouse_pos[1] < 585:  # za HOME
                            self.rage_quit = True
                            wait2 = False
                        if self.tournament:
                            if 625 < mouse_pos[0] < 788 and 535 < mouse_pos[1] < 585:  # za next_round
                                wait = False
            if not wait:
                config.map_init(self.sprite_list)
                if self.player1_dead:
                    self.player1 = Player(config.simba, 5, 50, 50, 400, 400, self.gameTerrain)
                    self.sprite_list.add(self.player1)
                    self.player1_dead = False

                self.player1.rect.x = 400
                self.player1.rect.y = 400
                self.player1.lives = 3
                self.player1_score = 0
                self.player1_finished = False

                if self.player2_dead:
                    self.player2 = Player(config.nala, 6, 50, 50, 500, 400, self.gameTerrain)
                    self.sprite_list.add(self.player2)
                    self.player2_dead = False

                self.player2.rect.x = 500
                self.player2.rect.y = 400

                self.player2.lives = 3
                self.player2_score = 0
                self.player2_finished = False

                self.enemy1.rect.x = 300
                self.enemy1.rect.y = 50
                self.enemy2.rect.x = 500
                self.enemy2.rect.y = 50

                self.level = 1
                self.show_bonus = False
                self.heart_counter = 0
                self.game_over = False

                self.mud1_status = 1  # ako ima vrednost 1, prikazi zamku, ako je 2 aktivna je, ako je 0 vec je iskoriscena
                self.mud1_timer = None
                self.mud2_status = 1  # ako ima vrednost 1, prikazi zamku, ako je 2 aktivna je, ako je 0 vec je iskoriscena
                self.mud2_timer = None
                return

    def initialize_tournament(self):
        self.users = [{} for i in range(self.number_of_players)] #koliko ima igraca toliko ide u niz

        for i in range(0, self.number_of_players): #ubacimo sve igrace u niz
            self.users[i]['name'] = 'Player ' + str(i+1)
            self.users[i]['points'] = 0
            self.users[i]['winner'] = False

        self.check_for_players()

    def check_for_players(self):
        self.tournament = True

        if self.number_of_players % 2 == 0:
            for i in range(0, self.number_of_players, 2):
                self.player1_name = self.users[i]['name']
                self.player2_name = self.users[i+1]['name']
                self.player1_number = i
                self.player2_number = i + 1
                self.player1_total_score = 0
                self.player2_total_score = 0
                self.two_players_offline(self.player1_name, self.player2_name) #napravi funkciju
                if not self.rage_quit:
                    self.show_game_over_multiplayer() #napravi funkciju
                else:
                    return
            self.number_of_winners = self.number_of_players // 2
        else:
            for i in range(0, self.number_of_players-1, 2):
                self.player1_name = self.users[i]['name']
                self.player2_name = self.users[i+1]['name']
                self.player1_number = i
                self.player2_number = i + 1
                self.player1_total_score = 0
                self.player2_total_score = 0
                self.two_players_offline(self.player1_name, self.player2_name) #napravi funkciju

                if not self.rage_quit:
                    self.show_game_over_multiplayer()  # napravi funkciju
                else:
                    return
            self.number_of_winners = self.number_of_players // 2 + 1
            self.users[self.number_of_players - 1]['winner'] = True  # ako ima neparno igraca, jedan ide dalje tj onaj poslednji

        # DRUGI KRUG TURNIRA:
        while self.number_of_winners > 1:
            self.players_winner = [{} for i in range(self.number_of_winners)]  # niz sa pobednicima
            win_positions = []  # pozicija pobednika u nizu self.users

            j = 0
            for i in range(0, self.number_of_players):
                if self.users[i]['winner']:
                    self.players_winner[j] = self.users[i]  # kopiranje pobednika u novi niz
                    win_positions.insert(j, i)  # i = pozicija u nizu self.users
                    j += 1  # j = pozicija u nizu users_winners

            if self.number_of_winners % 2 == 0:
                for i in range(0, self.number_of_winners, 2):
                    self.player1_name = self.players_winner[i]['name']
                    self.player1_number = win_positions[i]
                    k = i + 1
                    self.player2_number = win_positions[k]
                    self.player2_name = self.players_winner[k]['name']
                    self.player1_total_score = 0
                    self.player2_total_score = 0
                    self.two_players_offline(self.player1_name, self.player2_name) #napravi funkciju
                    self.number_of_winners -= 1
                    if self.number_of_winners == 1:
                        self.tournament_finished = True
                    self.show_game_over_multiplayer()  # napravi funkciju
            else:
                for i in range(0, self.number_of_winners - 1, 2):
                    self.player1_name = self.players_winner[i]['name']
                    self.player1_number = win_positions[i]
                    k = i + 1
                    self.player2_number = win_positions[k]
                    self.player2_name = self.players_winner[k]['name']
                    self.player1_total_score = 0
                    self.player2_total_score = 0
                    self.two_players_offline(self.player1_name, self.player2_name)  # napravi funkciju
                    self.number_of_winners -= 1
                    if self.number_of_winners == 1:
                        self.tournament_finished = True
                    self.show_game_over_multiplayer()  # napravi funkciju

def read_pos1(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2])

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])
