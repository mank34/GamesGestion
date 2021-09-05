from game import Game
from envVar import *

# TODO: Generate world menu: ??/??/??/back
# TODO: Option menu: Max FPS/Back
# TODO: 3D iso

# PyGame init
pygame.init()

# GenerateWindows
pygame.display.set_caption(GameName)
screen = pygame.display.set_mode((windowSize, windowSize))

# Load BackGround
background = pygame.image.load(BGpath)

# Clock init
clock = pygame.time.Clock()

# Start game
running = True

# Load the game
game = Game()


def quit_game():
    pygame.quit()
    return False


# Game loop
while running:

    # Limit FPS
    clock.tick(maxFPS)
    if showFPS:
        print("FPS: " + str(int(clock.get_fps())))

    # Display background
    screen.blit(background, (0, 0))

    # The game is update only if is_starting is true
    if game.is_starting:
        game.update(screen)
    # Game menu
    else:
        game.menu(screen)

    # Update screen
    pygame.display.flip()

    # Check the pygame's event
    for event in pygame.event.get():

        # Close event
        if event.type == pygame.QUIT:
            running = quit_game()

        elif game.is_starting:
            game.check_game_event(event)

        else:
            if not game.check_menu_event(event):
                running = quit_game()
