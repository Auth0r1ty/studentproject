from Menu import *
from pygame.locals import *
from collections import OrderedDict
import sys
import pygame
import GameConfig as config


class Play():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cub chase menu")
        music = pygame.mixer.music.load(music_path + "menu.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        self.font = pygame.font.SysFont("monospace", 30)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.main_menu = self.activate_menu()

    def activate_menu(self):
        main_menu = Menu(self.screen,
                           OrderedDict(
                               [('Single player', self.one_player),

                                ('Multiplayer - Offline', self.two_players_offline),

                                ('Multiplayer - Online', self.two_players_online),

                                ('Controls', self.show_controls),

                                ('Exit', self.leave_game)]))
        return main_menu

    def one_player(self):
        self.main_menu.active = False
        pygame.mouse.set_visible(False)
        pygame.mixer.music.stop()
        carryOn = True
        size = (800, 600)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("CubChaseTest")
        clock = pygame.time.Clock()
        WHITE = (255, 255, 255)
        config.map_init()

        # -------- Main Program Loop -----------
        while carryOn:
            # --- Main event loop
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    carryOn = False  # Flag that we are done so we exit this loop
                # --- Game logic should go here

                # --- Drawing code should go here
                # First, clear the screen to white.
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                config.player.movePlayer(-config.speed, 0, config.sprite_list)
                # player.moveLeft (2, timon)
            if keys[pygame.K_RIGHT]:
                config.player.movePlayer(config.speed, 0, config.sprite_list)
                # player.moveRight (2, timon)
            if keys[pygame.K_UP]:
                config.player.movePlayer(0, -config.speed, config.sprite_list)
                # player.moveUp (2, timon)
            if keys[pygame.K_DOWN]:
                config.player.movePlayer(0, config.speed, config.sprite_list)
                # player.moveDown (2, timon)
            config.sprite_list.update()
            screen.fill(WHITE)
            # iscrtavanje mape
            for i in range(0, 12):
                for j in range(0, 16):
                    if config.gameMap[i][j] == config.StaticEl.path:
                        screen.blit(config.path, (j * 50, i * 50))
                    elif config.gameMap[i][j] == config.StaticEl.wall:
                        screen.blit(config.wall, (j * 50, i * 50))
                    elif config.gameMap[i][j] == config.StaticEl.enter:  # pathPlayer1
                        screen.blit(config.enter, (j * 50, i * 50))
                    elif config.gameMap[i][j] == config.StaticEl.pathPlayer1:
                        screen.blit(config.pathPlayer1, (j * 50, i * 50))
            # The you can draw different shapes and lines or add text to your background stage.
            config.sprite_list.draw(screen)
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            # --- Limit to 60 frames per second
            clock.tick(config.fps)

        # Once we have exited the main program loop we can stop the game engine:

        pygame.quit()
        sys.exit()

    def two_players_offline(self):
        print("aa")

    def two_players_online(self):
        print("aa")

    def leave_game(self):
        pygame.quit()
        sys.exit()

    def show_controls(self):
        # pygame.mixer.music.pause()
        pygame.mixer.music.set_volume(0.3)
        self.main_menu.active = False
        start_screen_image = pygame.transform.scale(pygame.image.load(menu_image_path + "Controls.jpg"), (width,
                                                                                                        height))
        self.screen.blit(start_screen_image, (0, 0))
        pygame.display.update()
        pygame.time.delay(5000)
        self.menu_back_from_controls()

    def menu_back_from_controls(self):
        # pygame.mixer.music.unpause()
        pygame.mixer.music.set_volume(0.5)
        self.main_menu.active = True
        while self.main_menu.active:
            self.main_menu.draw()
            self.handle_menu_event(self.main_menu)
            pygame.display.update()
            self.clock.tick(30)

    def start_menu(self):
        self.main_menu.active = True
        while self.main_menu.active:
            self.main_menu.draw()
            self.handle_menu_event(self.main_menu)
            pygame.display.update()
            self.clock.tick(30)

    def handle_menu_event(self, main_menu):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.leave_game()
            elif event.type == MOUSEBUTTONUP:
                for option in main_menu.options:
                    if option.is_selected:
                        if not isinstance(option.function, tuple):
                            option.function()
                        else:
                            option.function[0](option.function[1])

    def run_game(self):
        self.start_menu()

