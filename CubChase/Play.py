import pygame
from enum import Enum
from Player import Player
from GameStaticObject import GameStaticObject

pygame.init()


########################################################################################################




# elementi koji se ne krecu na mapi da pratimo na mapi (preko enumeracije)
class StaticEl(Enum):
    path = 1
    wall = 2
    enter = 3
    trap = 4
    endmap = 5
    pathPlayer1 = 6   #
    pathPlayer2 = 7
    pathPlayer3 = 8
    pathPlayer4 = 9


size = (800, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("CubChaseTest")

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
WHITE = (255,255,255)


# LOAD NECESSARY IMAGES
# define wall image
wall = pygame.image.load("img/wall.png")
wall = pygame.transform.scale(wall, (50, 50))
# define path image
path = pygame.image.load("img/sand_empty.png")
path = pygame.transform.scale(path, (50, 50))
# define player image
timon = pygame.image.load("img/timon.png")
timon = pygame.transform.scale(timon, (50, 50))
#enter image
enter = pygame.image.load("img/sapice_red.png")
enter = pygame.transform.scale(enter, (50, 50))





gameMap = (
        # 1 (9)             2 (10)           3 (11)       4 (12)        5(13)           6(14)         7(15)          8(16)
        (StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.path,
         StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path),

        (StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path,
         StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path),

        (StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall,
         StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.enter, StaticEl.wall, StaticEl.path, StaticEl.path),

        (StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.wall, StaticEl.path,
         StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.path),

        (StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.path,
         StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.path),

        (StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall,
         StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path),

        (StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path,
         StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path),

        (StaticEl.path, StaticEl.wall, StaticEl.enter, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall,
         StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path),
        #9 red je ovaj ispod
        (StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path,
         StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.wall, StaticEl.path),
        #10 red je ovaj ispod
        (StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall,
         StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path),

        (StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path,
         StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall),

        (StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.wall, StaticEl.wall, StaticEl.wall,
         StaticEl.wall, StaticEl.wall, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.path, StaticEl.enter),

    )

########################################################################################################

# sprites_list sadrzi sve sprit-ove napravljene u igrici
sprite_list = pygame.sprite.Group()

for i in range(0, 12):
    for j in range(0, 16):
        if gameMap[i][j] == StaticEl.wall:
            obj = GameStaticObject(wall, 50, 50, j*50, i*50)
            sprite_list.add(obj)
i = -1
for j in range(0, 16):
    obj = GameStaticObject(wall, 50, 50, j * 50, i * 50)
    sprite_list.add(obj)
i = 12
for j in range(0, 16):
    obj = GameStaticObject(wall, 50, 50, j * 50, i * 50)
    sprite_list.add(obj)
j = -1
for i in range(0, 12):
    obj = GameStaticObject(wall, 50, 50, j * 50, i * 50)
    sprite_list.add(obj)
j = 16
for i in range(0, 12):
    obj = GameStaticObject(wall, 50, 50, j * 50, i * 50)
    sprite_list.add(obj)

# napravi se objekat tipa Player
player = Player(timon, 50, 50, 250, 400)
player1 = Player(timon, 50, 50, 250, 350)


sprite_list.add(player)
sprite_list.add(player1)

player.sprite_list = sprite_list
player1.sprite_list = sprite_list




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
        player.movePlayer(-2, 0, sprite_list)
        # player.moveLeft (2, timon)
    if keys[pygame.K_RIGHT]:
        player.movePlayer (2, 0, sprite_list)
        # player.moveRight (2, timon)
    if keys[pygame.K_UP]:
        player.movePlayer (0, -2, sprite_list)
        # player.moveUp (2, timon)
    if keys[pygame.K_DOWN]:
        player.movePlayer (0, 2, sprite_list)
        # player.moveDown (2, timon)

    sprite_list.update()
    screen.fill(WHITE)

    #iscrtavanje mape
    for i in range(0, 12):
        for j in range(0, 16):
            if(gameMap[i][j] == StaticEl.path):
                screen.blit(path, (j*50, i*50))
            elif (gameMap[i][j] == StaticEl.wall):
                screen.blit(wall, (j * 50, i * 50))
            elif (gameMap[i][j] == StaticEl.enter):
                screen.blit(enter, (j * 50, i * 50))
    # The you can draw different shapes and lines or add text to your background stage.

    sprite_list.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()