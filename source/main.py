import pygame
from HUD import show_HUD
from game import Game
from envVar import *

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
loading = False

# Load the game
game = Game()

# Init var to count a day duration
cnt_day = 0
nb_day = 1

# Flag to enable the construct menu
show_construct_HUD = False

# Game loop
while running:

    # Limit FPS
    clock.tick(maxFPS)
    print("FPS: " + str(int(clock.get_fps())))

    # Display background
    screen.blit(background, (0, 0))

    # Display tile
    for tileName in game.tiles:
        screen.blit(game.tiles[tileName].image, game.tiles[tileName].rect)

    # Display HUD
    show_HUD(screen, game, show_construct_HUD)

    # Mousse icon
    if game.mousseIcon.isEnable:
        game.mousseIcon.rect.x = pygame.mouse.get_pos()[0]
        game.mousseIcon.rect.y = pygame.mouse.get_pos()[1]
        screen.blit(game.mousseIcon.icon, game.mousseIcon.rect)

    # Update screen
    pygame.display.flip()

    # Manage day
    cnt_day += 1
    if cnt_day > Nb_tick_day:
        # Update resource
        game.update_prod_value()
        cnt_day = 0
        nb_day += 1
        print("Day " + str(nb_day))

    # Check mouse position
    for tileName in game.tiles:
        game.tiles[tileName].set_over(game.tiles[tileName].rect.collidepoint(pygame.mouse.get_pos()))

    game.move()

    # Check the pygame's event
    for event in pygame.event.get():

        # Close event
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        # Mouse event - clique left
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
            # Click on tile
            if pygame.mouse.get_pos()[1] < windowSize - HUD_size:
                if (show_construct_HUD and
                        game.hud.farm_construct_button_rect.collidepoint(pygame.mouse.get_pos())):
                    game.mousseIcon.set_image(MousseFarm)
                    game.mousseIcon.isEnable = True
                    game.mousseIcon.item_selected = "farm"
                    show_construct_HUD = False

                elif (show_construct_HUD and
                      game.hud.market_construct_button_rect.collidepoint(pygame.mouse.get_pos())):
                    game.mousseIcon.set_image(MousseMarket)
                    game.mousseIcon.isEnable = True
                    game.mousseIcon.item_selected = "market"
                    show_construct_HUD = False

                else:
                    for tileName in game.tiles:
                        if game.tiles[tileName].rect.collidepoint(pygame.mouse.get_pos()):
                            print("Tile " + tileName + " clicked")
                            if game.mousseIcon.isEnable:
                                game.tiles[tileName].update_in(game.mousseIcon.item_selected)
                                game.mousseIcon.isEnable = False
                                show_construct_HUD = False

            # Click on HUD
            else:
                if game.hud.construct_button_rect.collidepoint(pygame.mouse.get_pos()):
                    print("Construct button clicked")
                    show_construct_HUD = True

        # Mouse event - clique right
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[2]:
            show_construct_HUD = False
            game.mousseIcon.isEnable = False
