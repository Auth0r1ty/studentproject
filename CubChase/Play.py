import pygame
from enum import Enum
from Player import Player

pygame.init()



########################################################################################################


# elementi koji se ne krecu na mapi da pratimo na mapi (preko enumeracije)
class StaticEl(Enum):
    path = 1
    wall = 2
    enter = 8
    trap = 3
    pathPlayer1 = 4   #
    pathPlayer2 = 5
    pathPlayer3 = 6
    pathPlayer4 = 7


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

i = 0;

# napravi se objekat tipa Player
player = Player(timon, 50, 50, 150, 200)
# sprites_list sadrzi sve sprit-ove napravljene u igrici
sprites_list = pygame.sprite.Group()
sprites_list.add(player)

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








# -------- Main Program Loop -----------
while carryOn:


    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop

        # --- Game logic should go here

        # --- Drawing code should go here
        # First, clear the screen to white.

    keys = pygame.key.get_pressed ()
    if keys[pygame.K_LEFT]:
        player.moveLeft (2, timon)
    if keys[pygame.K_RIGHT]:
        player.moveRight (2, timon)
    if keys[pygame.K_UP]:
        player.moveUp (2, timon)
    if keys[pygame.K_DOWN]:
        player.moveDown (2, timon)

    sprites_list.update()
    # screen.fill(WHITE)

    #iscrtavanje mape
    for i in range(0, 12):
        for j in range(0, 16):
            if(gameMap[i][j] == StaticEl.path):
                screen.blit(path, (j*50, i*50))
            elif (gameMap[i][j] == StaticEl.wall):
                screen.blit(wall, (j * 50, i * 50))
    # The you can draw different shapes and lines or add text to your background stage.

    sprites_list.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()