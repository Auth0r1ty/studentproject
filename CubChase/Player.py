import pygame
import GameConfig as config
import GameDynamicObject
import GameStaticObject


# GameDynamicObject inherits from pygame.sprite.Sprite
class Player(GameDynamicObject.GameDynamicObject):
    pathPlayer = None

    # u slucaju vise slika, proslediti sliku kao argument konstuktora
    def __init__(self, image, pathPlayer, x, y, gameTerrain, display_surf, sprite_list, carryOn, screen, clock, lives: int = 3):
        # parent ctor
        super().__init__(50, 50, x, y, image, gameTerrain, carryOn, sprite_list, screen)

        # additional fields for player
        self.lives = lives
        self.clock = clock
        self.score = 0
        self._display_surf = display_surf
        self.pathPlayer = pathPlayer



    def movePlayer(self, x, y, sprite_list):
        self.leave_tracks(x, y)

        rectXpomocna = self.rect.x
        rectYpomocna = self.rect.y

        # da ne moze da se krece dijagonalno
        if self.rect.y % 50 == 0:
            rectXpomocna += x
        if self.rect.x % 50 == 0:
            rectYpomocna += y

        self.rect.x = rectXpomocna
        self.rect.y = rectYpomocna

        self.collision(x, y, sprite_list)

    def leave_tracks(self, x, y):
        # ostavljanje tragova
        if self.rect.y % 50 == 0 and self.rect.x % 50 == 0:
            currTerrain = self.gameTerrain[self.rect.y // 50][self.rect.x // 50]
            if currTerrain.fieldType == config.StaticEl.path or currTerrain.fieldType == config.StaticEl (
                    self.pathPlayer):
                # i == y, j == x koordinatama
                currTerrain.fieldType = config.StaticEl (self.pathPlayer)
                currTerrain.image = config.pathPlayer1 if self.pathPlayer == 5 else config.pathPlayer2
                if x > 0:
                    currTerrain.image = pygame.transform.rotate (currTerrain.image, 270)
                elif x < 0:
                    currTerrain.image = pygame.transform.rotate (currTerrain.image, 90)
                elif y < 0:
                    pass
                elif y > 0:
                    currTerrain.image = pygame.transform.rotate (currTerrain.image, 180)

    def collision(self, x, y, sprite_list):
        # kolizija sa zidom i drugim igracima
        collision_list = pygame.sprite.spritecollide (self, sprite_list, False)
        for temp in collision_list:
            if temp != self:
                if x > 0:  # igrac se pomera desno
                    self.rect.right = temp.rect.left
                if x < 0:  # levo
                    self.rect.left = temp.rect.right
                if y > 0:  # dole
                    self.rect.bottom = temp.rect.top
                if y < 0:  # gore
                    self.rect.top = temp.rect.bottom

    # keyboard commands
    def player_control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.carryOn[0] = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.carryOn[0] = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.movePlayer(-config.speed, 0, self.sprite_list)
        if keys[pygame.K_RIGHT]:
            self.movePlayer(config.speed, 0, self.sprite_list)
        if keys[pygame.K_UP]:
            self.movePlayer(0, -config.speed, self.sprite_list)
        if keys[pygame.K_DOWN]:
            self.movePlayer(0, config.speed, self.sprite_list)

    # draw map on every frame
    def draw_map(self):
        super().draw_map()

        self.endgame_check(self.emptyPathCounter)

    # check if all fields are covered by steps and if player went out, called from draw_map
    def endgame_check(self, emptyPathCounter):
        if emptyPathCounter == 4:
            for temp in self.sprite_list:
                if temp.__class__.__name__ == "GameStaticObject" and temp.fieldType == config.StaticEl.exit:
                    self.sprite_list.remove(temp)

        if self.rect.x > 799:
            self.carryOn[0] = False

    def print_score(self, screen):
        self.screen.blit (config.table_for_score, [5, 5])

        font = pygame.font.Font ('freesansbold.ttf', 12)
        black = (255, 255, 255)

        text = font.render ('Player 1', True, black)
        result = font.render (str (self.score), True, black)
        textRect = text.get_rect ()
        resRect = result.get_rect ()
        textRect.center = (70, 35)
        resRect.center = (70, 55)
        self._display_surf.blit (text, textRect)
        self._display_surf.blit (result, resRect)

        xl = 35
        yl = 65
        for i in range (0, self.lives):
            self._display_surf.blit (config.life, [xl, yl])
            xl = xl + 25

        ##################### ispis za poene i zivote igraca BY DJOLE #################
        #self.player_one_score = self.player_one_get_score.get_score()

        #screen.blit(self.table_for_score, [5, 5])
        #font = pygame.font.Font('freesansbold.ttf', 12)
        #black = (255, 255, 255)

        #text = font.render('Player 1', True, black)
        #result = font.render(str(self.player_one_score), True, black)
        #textRect = text.get_rect()
        #resRect = result.get_rect()
        #textRect.center = (70, 35)
        #resRect.center = (70, 55)
        #self._display_surf.blit(text, textRect)
        #self._display_surf.blit(result, resRect)

        #xl = 35
        #yl = 65
        #for i in range(0, self.player_one_lives):
        #    self._display_surf.blit(self.life, [xl, yl])
        #    xl = xl + 25
        ##########################################################################

    # run method is used to run player as a thread
    def run(self):
        #while self.carryOn[0]:
            self.player_control()
            ################################################################
            # enemy movement
            # self.enemy1.moveEnemy(self.sprite_list)
            ################################################################

            self.draw_map()

            # iscrtavanje svih sprit-ova (igraci, zid), poziv iz roditeljske klase
            self.sprite_list.update()
            self.sprite_list.draw(self.screen)

            self.get_score()
            self.print_score(self.screen)

            # iscrtavanje celog ekrana
            pygame.display.flip()
            self.clock.tick(config.fps)

    def get_score(self):
        sum = 0
        for i in range(0, 12):
            for j in range(0, 16):
                if (config.gameTerrain[i][j]).fieldType == GameStaticObject.StaticEl.pathPlayer1:
                    sum += 1

        self.score = sum * 100