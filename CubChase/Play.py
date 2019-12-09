import pygame
import GameConfig as config

pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("CubChaseTest")
# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
# The clock will be used to control how fast the screen updates
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
            elif config.gameMap[i][j] == config.StaticEl.enter:
                screen.blit(config.enter, (j * 50, i * 50))
    # The you can draw different shapes and lines or add text to your background stage.
    config.sprite_list.draw(screen)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(config.fps)
# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
