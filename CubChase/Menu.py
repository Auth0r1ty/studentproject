from GameConfig import *
from Play import *
from pygame.locals import *
from collections import OrderedDict
import sys
import multiprocessing as mp


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
        self._display_surf = pygame.display.set_mode((config.width, config.height), pygame.HWSURFACE)

    def activate_menu(self):
        main_menu = Menu(self.screen,
                           OrderedDict(
                               [('Single player', self.one_player),

                                ('Multiplayer - Offline', self.two_players_offline),

                                ('Multiplayer - Online', self.two_players_online),

                                ('Tournament', self.tournament),

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
        pygame.mixer.music.set_volume(0.3)
        global active
        active = False
        start_screen_image = pygame.transform.scale(pygame.image.load(files_path + "Controls.jpg"), (width,
                                                                                                        height))
        self.screen.blit(start_screen_image, (0, 0))
        pygame.display.update()
        pygame.time.delay(5000)

        self.start_menu()

    def tournament(self):
        bg = pygame.image.load("img/white.png")
        self.screen.blit(bg, [0, 0])
        background_for_result = pygame.image.load("img/Tournament_start_screen.jpg")
        self.screen.blit(background_for_result, [0, 0])

        font = pygame.font.Font('Base05.ttf', 20)
        black = (255, 204, 51)
        back_table = pygame.image.load("img/Left_sign.png")
        back_table = pygame.transform.scale(back_table, (200, 50))

        table_for_number_of_players = pygame.image.load("img/Right_sign.png")
        table_for_number_of_players = pygame.transform.scale(table_for_number_of_players, (200, 50))

        self.screen.blit(back_table, [0, 535])  # dole levo

        back_text = font.render('HOME', True, black)
        backRect = back_text.get_rect()
        backRect.center = (95, 560)
        self._display_surf.blit(back_text, backRect)

        self.screen.blit(table_for_number_of_players, [300, 465])  # 8 igraca tabla
        self.screen.blit(table_for_number_of_players, [300, 400])   # 7 igraca tabla
        self.screen.blit(table_for_number_of_players, [300, 335])   # 6 igraca tabla
        self.screen.blit(table_for_number_of_players, [300, 270])   # 5 igraca tabla
        self.screen.blit(table_for_number_of_players, [300, 205])   # 4 igraca tabla

        four_players_text = font.render('4 PLAYERS', True, black)
        four_players_rect = four_players_text.get_rect()
        four_players_rect.center = (400, 230)

        five_players_text = font.render('5 PLAYERS', True, black)
        five_players_rect = five_players_text.get_rect()
        five_players_rect.center = (400, 295)

        six_players_text = font.render('6 PLAYERS', True, black)
        six_players_rect = six_players_text.get_rect()
        six_players_rect.center = (400, 360)

        seven_players_text = font.render('7 PLAYERS', True, black)
        seven_players_rect = seven_players_text.get_rect()
        seven_players_rect.center = (400, 425)

        eight_players_text = font.render('8 PLAYERS', True, black)
        eight_players_rect = eight_players_text.get_rect()
        eight_players_rect.center = (400, 490)

        self._display_surf.blit(four_players_text, four_players_rect)
        self._display_surf.blit(five_players_text, five_players_rect)
        self._display_surf.blit(six_players_text, six_players_rect)
        self._display_surf.blit(seven_players_text, seven_players_rect)
        self._display_surf.blit(eight_players_text, eight_players_rect)

        pygame.display.update()
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.time.delay(500)
                    self.start_menu()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if 322 < mouse_pos[0] < 490 and 205 < mouse_pos[1] < 255: #za 4 igraca
                        print('4 igraca')
                        play = Play(4, self.screen, self.clock, gameTerrain)
                        process = mp.Process(target=play.initialize_tournament())
                        process.start()
                        process.join()
                        pygame.mouse.set_visible(True)
                        pygame.mixer.music.play(-1)
                        self.start_menu()
                        return

                    if 322 < mouse_pos[0] < 490 and 270 < mouse_pos[1] < 320: #za 5 igraca
                        print('5 igraca')
                        play = Play(5, self.screen, self.clock, gameTerrain)
                        process = mp.Process(target=play.initialize_tournament())
                        process.start()
                        process.join()
                        pygame.mouse.set_visible(True)
                        pygame.mixer.music.play(-1)
                        self.start_menu()
                        return

                    if 322 < mouse_pos[0] < 490 and 335 < mouse_pos[1] < 385: #za 6 igraca
                        print('6 igraca')
                        play = Play(6, self.screen, self.clock, gameTerrain)
                        process = mp.Process(target=play.initialize_tournament())
                        process.start()
                        process.join()
                        pygame.mouse.set_visible(True)
                        pygame.mixer.music.play(-1)
                        self.start_menu()
                        return

                    if 322 < mouse_pos[0] < 490 and 400 < mouse_pos[1] < 450: #za 7 igraca
                        print('7 igraca')
                        play = Play(7, self.screen, self.clock, gameTerrain)
                        process = mp.Process(target=play.initialize_tournament())
                        process.start()
                        process.join()
                        pygame.mouse.set_visible(True)
                        pygame.mixer.music.play(-1)
                        self.start_menu()
                        return

                    if 322 < mouse_pos[0] < 490 and 465 < mouse_pos[1] < 515: #za 8 igraca
                        print('8 igraca')
                        play = Play(8, self.screen, self.clock, gameTerrain)
                        process = mp.Process(target=play.initialize_tournament())
                        process.start()
                        process.join()
                        pygame.mouse.set_visible(True)
                        pygame.mixer.music.play(-1)
                        self.start_menu()
                        return

                    if 30 < mouse_pos[0] < 180 and 535 < mouse_pos[1] < 585:  # za HOME
                        pygame.mouse.set_visible(True)
                        pygame.mixer.music.play(-1)
                        pygame.time.delay(500)
                        self.start_menu()
                        return

    def one_player(self):
        active = False
        play = Play(1, self.screen, self.clock, gameTerrain)
        play.one_player()
        #process = mp.Process(target=play.one_player())
        #process.start()
        #process.join()

        pygame.mouse.set_visible(True)
        pygame.mixer.music.play(-1)

        self.start_menu()
        return

    def two_players_offline(self):
        play = Play(2, self.screen, self.clock, gameTerrain)
        play.two_players_offline('Player 1', 'Player 2')
        #process = mp.Process(target=play.two_players_offline, args=('Player 1', 'Player 2'))

        #process.start()
        #process.join()

        pygame.mouse.set_visible(True)
        pygame.mixer.music.play(-1)

        self.start_menu()
        return

    def two_players_online(self):
        bg = pygame.image.load("img/white.png")
        self.screen.blit(bg, [0, 0])
        background_for_result = pygame.image.load("img/Online_start_screen2.jpg")
        self.screen.blit(background_for_result, [0, 0])

        font = pygame.font.Font('Base05.ttf', 20)
        black = (255, 204, 51)
        back_table = pygame.image.load("img/Left_sign.png")
        back_table = pygame.transform.scale(back_table, (200, 50))

        table_for_connect = pygame.image.load("img/Right_sign.png")
        table_for_connect = pygame.transform.scale(table_for_connect, (200, 50))

        self.screen.blit(back_table, [0, 535])  # dole levo

        back_text = font.render('HOME', True, black)
        backRect = back_text.get_rect()
        backRect.center = (95, 560)
        self._display_surf.blit(back_text, backRect)

        self.screen.blit(table_for_connect, [325, 335]) #bilo 300 i 335

        connect_text = font.render('CONNECT', True, black)
        connect_text_rect = connect_text.get_rect()
        connect_text_rect.center = (425, 360) #bilo 400 i 360

        self._display_surf.blit(connect_text, connect_text_rect)

        pygame.display.update()
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.time.delay(500)
                    self.start_menu()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    #bilo 322 i 490
                    if 347 < mouse_pos[0] < 505 and 335 < mouse_pos[1] < 385:  # za click na connect
                        #print('Connect')
                        play = Play(2, self.screen, self.clock, gameTerrain)
                        process = mp.Process(target=play.establish_a_connection())
                        process.start()
                        process.join()
                        pygame.mouse.set_visible(True)
                        pygame.mixer.music.play(-1)
                        self.start_menu()
                        return

                    if 30 < mouse_pos[0] < 180 and 535 < mouse_pos[1] < 585:  # za HOME
                        pygame.mouse.set_visible(True)
                        pygame.mixer.music.play(-1)
                        pygame.time.delay(500)
                        self.start_menu()
                        return

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
                menu_option.set_position(250, height - 135)
            elif menu_option.text == "Exit":
                menu_option.set_position(250, height - 85)
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