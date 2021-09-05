from HUD import HUD
from tile import Tile
from mousseIcon import MousseIcon
from envVar import *


# Class game
class Game:
    def __init__(self):

        # Flag to known the game state
        self.is_starting = False
        self.is_pausing = False
        self.in_configuring = False

        # Game menu
        self.game_name = GameNameFont.render(GameName, False, (0, 0, 0))
        self.game_name_rect = self.game_name.get_rect()
        self.game_name_rect.x = int(windowSize * 0.33)
        self.game_name_rect.y = int(windowSize * 0.25)

        self.game_start = GameMenuFont.render("Start", False, (0, 0, 0))
        self.game_start_rect = self.game_start.get_rect()
        self.game_start_rect.x = int(windowSize * 0.45)
        self.game_start_rect.y = int(windowSize * 0.4)

        self.game_option = GameMenuFont.render("Options", False, (0, 0, 0))
        self.game_option_rect = self.game_option.get_rect()
        self.game_option_rect.x = int(windowSize * 0.44)
        self.game_option_rect.y = int(windowSize * 0.45)

        self.game_quit = GameMenuFont.render("Quit", False, (0, 0, 0))
        self.game_quit_rect = self.game_quit.get_rect()
        self.game_quit_rect.x = int(windowSize * 0.46)
        self.game_quit_rect.y = int(windowSize * 0.50)

        # Init var to count a day duration
        self.cnt_day = 0
        self.nb_day = 1

        # Flag to enable the HUD menu
        self.show_HUD = {}
        for menu in HUD_main_menu:
            self.show_HUD[menu] = False

        # Camera configuration
        self.cam_velocity = 2

        self.cam_pos = {
            "x": 0,
            "y": 0
        }

        # Define the game zone
        self.start_game_zone = dict(x=int(-nb_tile_x / 2 * tileSize) + windowSize / 2,
                                    y=int(-nb_tile_y / 2 * tileSize) + windowSize / 2)
        self.end_game_zone = dict(x=int(nb_tile_x / 2 * tileSize) - windowSize / 2,
                                  y=int(nb_tile_y / 2 * tileSize) - windowSize / 2)

        # Generate all the tiles
        self.tiles = {}

        for y in range(nb_tile_y):
            for x in range(nb_tile_x):
                self.tiles[str(y * nb_tile_x + x)] = Tile(self.start_game_zone["x"] + x * tileSize,
                                                          self.start_game_zone["y"] + y * tileSize)
                if showLoading:
                    print(str(int((y * nb_tile_x + x) / (nb_tile_x * nb_tile_y) * 100)) + "%")

        # HUD
        self.hud = HUD()

        # Mousse icon
        self.mousseIcon = MousseIcon()

    def menu(self, screen):
        if self.is_pausing:
            self.game_start = GameMenuFont.render("Resume", False, (0, 0, 0))
        else:
            self.game_start = GameMenuFont.render("Start", False, (0, 0, 0))

        screen.blit(self.game_name, self.game_name_rect)
        screen.blit(self.game_start, self.game_start_rect)
        screen.blit(self.game_option, self.game_option_rect)
        screen.blit(self.game_quit, self.game_quit_rect)

    def update(self, screen):
        # Display tile
        for tileName in self.tiles:
            screen.blit(self.tiles[tileName].image, self.tiles[tileName].rect)

        # Display HUD
        self.hud.show_HUD(screen, self.show_HUD)

        # Mousse icon
        if self.mousseIcon.isEnable:
            self.mousseIcon.rect.x = pygame.mouse.get_pos()[0]
            self.mousseIcon.rect.y = pygame.mouse.get_pos()[1]
            screen.blit(self.mousseIcon.icon, self.mousseIcon.rect)

        # Manage day
        self.cnt_day += 1
        if self.cnt_day > Nb_tick_day:
            # Update resource
            self.update_prod_value()
            self.cnt_day = 0
            self.nb_day += 1
            print("Day " + str(self.nb_day))

        # Check mouse position
        for tileName in self.tiles:
            self.tiles[tileName].set_over(self.tiles[tileName].rect.collidepoint(pygame.mouse.get_pos()))

        # Camera move only if all the menu are close
        cam_move = True
        for menu_HUD in self.show_HUD:
            if self.show_HUD[menu_HUD]:
                cam_move = False

        if cam_move:
            self.move()

    def move(self):

        right = pygame.mouse.get_pos()[0] > windowSize - windowBoarder
        left = pygame.mouse.get_pos()[0] < windowBoarder
        up = pygame.mouse.get_pos()[1] < windowBoarder
        down = pygame.mouse.get_pos()[1] > windowSize - windowBoarder - HUD_size

        right = right and pygame.mouse.get_pos()[1] < windowSize - HUD_size
        left = left and pygame.mouse.get_pos()[1] < windowSize - HUD_size
        down = down and pygame.mouse.get_pos()[1] < windowSize - HUD_size

        if right and self.cam_pos["x"] < self.start_game_zone["x"] - windowBoarder:
            right = False
        if left and self.cam_pos["x"] > self.end_game_zone["x"] + windowBoarder:
            left = False

        if down and self.cam_pos["y"] < self.start_game_zone["y"] - HUD_size:
            down = False
        if up and self.cam_pos["y"] > self.end_game_zone["y"] + windowBoarder:
            up = False

        for tileName in self.tiles:
            self.tiles[tileName].rect.x += self.cam_velocity * left
            self.tiles[tileName].rect.x -= self.cam_velocity * right
            self.tiles[tileName].rect.y += self.cam_velocity * up
            self.tiles[tileName].rect.y -= self.cam_velocity * down

        self.cam_pos["x"] += self.cam_velocity * left
        self.cam_pos["x"] -= self.cam_velocity * right
        self.cam_pos["y"] += self.cam_velocity * up
        self.cam_pos["y"] -= self.cam_velocity * down

    def update_prod_value(self):
        for tileName in self.tiles:
            res_available = True

            # Verify all the cost
            for res_cost in self.tiles[tileName].cost:
                if self.hud.cityRes[res_cost] < self.tiles[tileName].cost[res_cost]:
                    res_available = False

            # If all res are available deduce the res and add the prod
            if res_available:
                for res_cost in self.tiles[tileName].cost:
                    self.hud.cityRes[res_cost] -= self.tiles[tileName].cost[res_cost]
                    self.hud.cityRes[res_cost] += self.tiles[tileName].production[res_cost]

    def disable_all_hud(self):
        for menu_HUD in self.show_HUD:
            self.show_HUD[menu_HUD] = False

    def check_game_event(self, event):

        # Mouse event - clique left
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
            # Click on tile
            if pygame.mouse.get_pos()[1] < windowSize - HUD_size:
                if self.show_HUD["hud_construct"]:
                    for menu in self.hud.construct_HUD_button:
                        if self.hud.construct_HUD_button[menu].rect.collidepoint(pygame.mouse.get_pos()):
                            self.mousseIcon.set_image(resource[menu])
                            self.mousseIcon.isEnable = True
                            self.mousseIcon.item_selected = menu.split('_')[-1]

                else:
                    for tileName in self.tiles:
                        if self.tiles[tileName].rect.collidepoint(pygame.mouse.get_pos()):
                            print("Tile " + tileName + " clicked")
                            if self.mousseIcon.isEnable:
                                self.tiles[tileName].update_in(self.mousseIcon.item_selected)
                                self.mousseIcon.isEnable = False

                self.disable_all_hud()

            # Click on HUD
            else:
                for menu in self.hud.main_HUD_button:
                    if self.hud.main_HUD_button[menu].rect.collidepoint(pygame.mouse.get_pos()):
                        print(menu + " button clicked")
                        self.show_HUD[menu] = True
                    else:
                        self.disable_all_hud()

        # Mouse event - clique right
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[2]:
            self.disable_all_hud()
            self.mousseIcon.isEnable = False

        elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.is_starting = False
            self.is_pausing = True

    def check_menu_event(self, event):
        running = True
        # Mouse event - clique left
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
            if self.game_start_rect.collidepoint(pygame.mouse.get_pos()):
                self.is_starting = True
                self.is_pausing = False

            elif self.game_quit_rect.collidepoint(pygame.mouse.get_pos()):
                running = False
        return running
