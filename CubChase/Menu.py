from GameConfig import *


class MenuOptions(pygame.font.Font):

    def __init__(self, text, function,
                 position=(0, 0), font=None, font_size=50, font_color=(221, 221, 0)):
        pygame.font.Font.__init__(self, font, font_size)
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