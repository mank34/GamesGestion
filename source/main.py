from game import Game
from envVar import *

# TODO: Mettre le marché en iso

# PyGame init
pygame.init()

# GenerateWindows
pygame.display.set_caption(GameName)

resolution = pygame.display.Info()  # Get the users resolution
width = resolution.current_w
height = resolution.current_h

screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.SCALED)

# Load BackGround
background = pygame.image.load(BGpath)

# Clock init
clock = pygame.time.Clock()

# Start game
running = True

# Load the game
game = Game(width, height)


def quit_game():
    pygame.quit()
    return False


# Game loop
while running:

    # Limit FPS
    clock.tick(FPS_available[game.FPS_selected])
    if showFPS:
        print("FPS: " + str(int(clock.get_fps())))

    # Display background
    screen.blit(background, (0, 0))

    # The game is update only if is_starting is true
    if game.in_configuring:
        game.option_menu(screen)
    elif game.is_starting:
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

        elif game.in_configuring:
            res = game.check_option_event(event)
            if res != "NULL":
                if res == "Full screen":
                    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.SCALED)
                else:
                    # screen = pygame.display.set_mode((int(res.split('x')[0]), int(res.split('x')[1])))
                    screen = pygame.display.set_mode((500, 500))

        elif game.is_starting:
            game.check_game_event(event)

        else:
            if not game.check_menu_event(event):
                running = quit_game()
