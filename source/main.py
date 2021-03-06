from game import Game
from envVar import *

from citizen import path_finding

# TODO: End sound for the destruction and the market

# PyGame init
pygame.init()

# GenerateWindows
pygame.display.set_caption(GameName)

resolution = pygame.display.Info()  # Get the users resolution
width = 700  # resolution.current_w
height = 700  # resolution.current_h

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF, 16)  # , pygame.FULLSCREEN | pygame.SCALED)
screen.set_alpha(None)

# Load BackGround
background = pygame.image.load(BGpath)

# Clock init
clock = pygame.time.Clock()

# Start game
running = True

# Load the game
game = Game(width, height)

# Music
main_sound.play(-1)


# path_finding()

def quit_game():
    pygame.quit()
    return False


# Game loop
while running:

    # Limit FPS
    clock.tick(FPS_available[game.config_menu.FPS_selected])
    if showFPS:
        print("FPS: " + str(int(clock.get_fps())))

    # Display background
    screen.blit(background, (0, 0))

    # The game is update only if is_starting is true
    if game.in_sound_menu:
        game.sound_menu.update(screen)
    elif game.in_configuring:
        game.config_menu.update(screen)
    elif game.is_starting:
        game.update(screen)
    # Game menu
    else:
        game.main_menu.update(screen, game.is_pausing)

    # Check the pygame's event
    for event in pygame.event.get():

        # Close event
        if event.type == pygame.QUIT:
            running = quit_game()

        elif game.in_sound_menu:
            game.in_sound_menu = game.sound_menu.check_event(event)

        elif game.in_configuring:
            res, game.in_sound_menu = game.config_menu.check_event(event)
            if res != "NULL":
                game.in_configuring = False
                # if res == "Full screen":
                #    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.SCALED)
                # else:
                # screen = pygame.display.set_mode((int(res.split('x')[0]), int(res.split('x')[1])))
                #   screen = pygame.display.set_mode((500, 500))

        elif game.is_starting:
            game.check_game_event(event, screen)

        else:
            running, game.is_starting, game.is_pausing, game.in_configuring = \
                game.main_menu.check_event(event,
                                           game.is_starting,
                                           game.is_pausing,
                                           game.in_configuring)
            if not running:
                running = quit_game()

    # Update screen
    if running:
        pygame.display.flip()
