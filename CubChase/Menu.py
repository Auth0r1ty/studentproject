from GameConfig import *
from Play import *
from pygame.locals import *
from collections import OrderedDict
import sys
from copy import deepcopy

active = None


# 1 se poziva
class StartMenu():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cub chase")
        music = pygame.mixer.music.load(files_path + "menu.mp3")
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

    def start_menu(self):
        pygame.mixer.music.set_volume(0.5)
        global active
        active = True
        while active:
            self.main_menu.draw()
            self.handle_menu_event(self.main_menu)
            pygame.display.update()
            self.clock.tick(config.fps)

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

    def show_controls(self):
        # pygame.mixer.music.pause()
        pygame.mixer.music.set_volume(0.3)
        global active
        active = False
        start_screen_image = pygame.transform.scale(pygame.image.load(files_path + "Controls.jpg"), (width,
                                                                                                        height))
        self.screen.blit(start_screen_image, (0, 0))
        pygame.display.update()
        pygame.time.delay(5000)

        self.start_menu()

    def one_player(self):
        active = False
        play = Play(1, self.screen, self.clock, gameTerrain)
        queue = mp.Queue()
        process = mp.Process (target=play.one_player())
        process.start ()
        process.join()
        #gameMapReturned = queue.get()
        pygame.mouse.set_visible (True)
        pygame.mixer.music.play (-1)

        score = 0
        for i in range(0, 12):
            for j in range (0, 16):
                if (gameTerrain[i][j]).fieldType == StaticEl.pathPlayer1:
                    score += 100
        print(score)
        """
        player_score = pygame.transform.scale (pygame.image.load (files_path + "1player_score.jpg"), (width,
                                                                                                       height))
        self.screen.blit(player_score, (0, 0))
        pygame.display.update ()
        pygame.time.delay (5000)
        
        font_obj = pygame.font.Font ('freesansbold.ttf', 32)
        text_surface_obj = font_obj.render ('Hello World!', True, (0, 255, 0), (0, 0, 180))
        text_rect_obj = text_surface_obj.get_rect ()
        self.screen.fill((0, 0, 0))
        self.screen.blit (text_surface_obj, text_rect_obj)
        pygame.display.update ()
        pygame.time.delay (5000)
        """
        self.start_menu()

        return

    def two_players_offline(self):
        play = Play(2, self.screen, self.clock, gameTerrain)
        process = mp.Process (target=play.two_players_firstPlayer())
        #process1 = mp.Process (target=play.two_players_secondPlayer())

        process.start()
        #process1.start()
        process.join ()
        #process1.join ()

        pygame.mouse.set_visible (True)
        pygame.mixer.music.play (-1)

        score = 0
        for i in range(0, 12):
            for j in range(0, 16):
                if (gameTerrain[i][j]).fieldType == StaticEl.pathPlayer1:
                    score += 100
        print(score)

        self.start_menu()

        return

    def two_players_online(self):
        a = 5

    # proba
    def two_players_firstPlayer(self):
        for i in range(0, 10):
            print("Prvi proces", i)

    def two_players_secondPlayer(self):
        for i in range(0, 10):
            print("Drugi proces", i)

    def leave_game(self):
        pygame.quit()
        sys.exit()


class Menu():

    def __init__(self, screen, functions, bg_color=(0, 0, 0)):
        self.active = True
        self.screen = screen
        self.background = pygame.image.load(files_path + "Menu.jpg")
        self.window_width = self.screen.get_rect().width
        self.window_height = self.screen.get_rect().height
        self.bg_color = bg_color
        self.options = [] #sve opcije iz menu
        self.active_option = None #aktivna opcija tj gde je kursor
        self.functions = functions
        for index, option in enumerate(functions.keys()):
            menu_option = MenuOptions(option, functions[option])
            height2 = menu_option.rect.height

            pos_x = self.window_width - 550
            pos_y = self.window_height - 430 + index * height2 * 2.2
            if menu_option.text == "Single player":
                menu_option.set_position(250, 180)
            elif menu_option.text == "Controls":
                menu_option.set_position(250, height - 205)
            elif menu_option.text == "Exit":
                menu_option.set_position(250, height - 135)
            else:
                menu_option.set_position(pos_x, pos_y)
            self.options.append(menu_option)

    def draw(self):
        start_screen_image = pygame.transform.scale(self.background, (width, height))

        self.screen.fill(self.bg_color)
        self.screen.blit(start_screen_image, (0, 0))

        for option in self.options:
            option.check_for_mouse_selection(pygame.mouse.get_pos())
            if self.active_option is not None:
                self.options[self.active_option].highlight()
            self.screen.blit(option.label, option.position)


class MenuOptions(pygame.font.Font):

    def __init__(self, text, function,
                 position=(0, 0), font=None, font_size=50, font_color=(221, 221, 0)):
        super().__init__(font, font_size)
        self.text = text
        self.function = function
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, font_color)
        self.rect = self.label.get_rect(left=position[0], top=position[1])
        self.position = position
        self.is_selected = False

    def set_position(self, x, y):
        self.position = (x, y)
        self.rect = self.label.get_rect(left=x, top=y)

    def highlight(self, color=(255, 0, 0)):
        self.font_color = color
        self.label = self.render(self.text, 1, self.font_color)
        self.is_selected = True
        self.set_bold(1)

    def unhighlight(self, color=(0, 0, 139)):
        self.font_color = color
        self.label = self.render(self.text, 1, self.font_color)
        self.is_selected = False
        self.set_italic(1)
        self.set_bold(0)

    def check_for_mouse_selection(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.highlight()
        else:
            self.unhighlight()