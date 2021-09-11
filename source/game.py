from HUD import HUD
from configMenu import configMenu
from envVar import *
from mainMenu import mainMenu
from mousseIcon import MousseIcon
from tile import Tile


# Class game
class Game:
    def __init__(self, w, h):

        self.width = w
        self.height = h

        self.tile_factor_size = 2

        # Flag to known the game state
        self.is_starting = False
        self.is_pausing = False
        self.in_configuring = False

        # Game menu
        self.main_menu = mainMenu(w, h)

        # Config menu
        self.config_menu = configMenu(w, h)

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
        self.game_zone_x = (tileSize_x / self.tile_factor_size) * nb_tile_x
        self.game_zone_y = (tileSize_y["empty"] / self.tile_factor_size) * nb_tile_y

        # Generate all the tiles
        self.tiles = {}

        self.init = False
        for y in range(nb_tile_y):
            for x in range(nb_tile_x):
                pos_x, pos_y = self.calculate_positioning(x, y, 0)
                self.tiles[str(y * nb_tile_x + x)] = Tile(pos_x, pos_y, self.tile_factor_size)

                if showLoading:
                    print(str(int((y * nb_tile_x + x) / (nb_tile_x * nb_tile_y) * 100)) + "%")

        self.init = True
        # HUD
        self.hud = HUD(self.width, self.height)

        # Mousse icon
        self.mousseIcon = MousseIcon()

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
        if self.cnt_day > 30000 / FPS_available[self.config_menu.FPS_selected]:
            # Update resource
            self.update_prod_value()
            self.cnt_day = 0
            self.nb_day += 1
            print("Day " + str(self.nb_day))

        # Check mouse position
        for tileName in self.tiles:
            self.tiles[tileName].set_over(self.tiles[tileName].is_in(self.tile_factor_size), self.tile_factor_size)

        # Camera move only if all the menu are close
        cam_move = True
        for menu_HUD in self.show_HUD:
            if self.show_HUD[menu_HUD]:
                cam_move = False

        if cam_move:
            self.move()

    def move(self):

        right = pygame.mouse.get_pos()[0] > self.width - windowBoarder
        left = pygame.mouse.get_pos()[0] < windowBoarder
        up = pygame.mouse.get_pos()[1] < windowBoarder
        down = pygame.mouse.get_pos()[1] > self.height - windowBoarder - HUD_size

        right = right and pygame.mouse.get_pos()[1] < self.width - HUD_size
        left = left and pygame.mouse.get_pos()[1] < self.width - HUD_size
        down = down and pygame.mouse.get_pos()[1] < self.height - HUD_size

        shift_x = (self.game_zone_x - self.width) / 2
        shift_y = (self.game_zone_y - self.height - HUD_size) / 2

        if shift_x > 0:
            if right and self.cam_pos["x"] <= -shift_x - windowBoarder:
                right = False
            if left and self.cam_pos["x"] >= shift_x:
                left = False
        else:
            right = False
            left = False

        if shift_y > 0:
            if down and self.cam_pos["y"] <= -shift_y - tileSize_x / self.tile_factor_size - windowBoarder:
                down = False
            if up and self.cam_pos["y"] >= shift_y + windowBoarder:
                up = False
        else:
            down = False
            up = False

        if left or right or up or down:
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

    def check_game_event(self, event, screen):

        # Mouse event - clique left
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
            # Click on tile
            if pygame.mouse.get_pos()[1] < self.height - HUD_size:
                if self.show_HUD["hud_construct"]:
                    for menu in self.hud.construct_HUD_button:
                        if self.hud.construct_HUD_button[menu].rect.collidepoint(pygame.mouse.get_pos()):
                            self.mousseIcon.set_image(resource[menu])
                            self.mousseIcon.isEnable = True
                            self.mousseIcon.item_selected = menu.split('_')[-1]

                else:
                    for tileName in self.tiles:
                        if self.tiles[tileName].is_in(self.tile_factor_size):
                            print("Tile " + tileName + " clicked")
                            if self.mousseIcon.isEnable:
                                self.tiles[tileName].update_in(self.mousseIcon.item_selected, self.tile_factor_size)
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

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.tile_factor_size -= 0.4
            if self.tile_factor_size <= 1:
                self.tile_factor_size = 1

            self.update_tiles_resizing(screen)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.tile_factor_size += 0.4
            if self.tile_factor_size >= 5:
                self.tile_factor_size = 5

            self.update_tiles_resizing(screen)

    def calculate_positioning(self, x, y, gap_y):
        pos_x = self.width / 2 + (x - y) * (tileSize_x / 2 / self.tile_factor_size)

        pos_y = -self.game_zone_y / 2 + self.height / 2 + (x + y) * (tileSize_y["empty"] / 2 / self.tile_factor_size)
        pos_y -= gap_y / self.tile_factor_size
        return pos_x, pos_y

    def update_tiles_resizing(self, screen):
        for y in range(nb_tile_y):
            for x in range(nb_tile_x):
                pos_x, pos_y = self.calculate_positioning(x, y, self.tiles[str(y * nb_tile_x + x)].gap_y)
                self.tiles[str(y * nb_tile_x + x)].update_size(pos_x, pos_y)

        self.game_zone_x = (tileSize_x / self.tile_factor_size) * nb_tile_x
        self.game_zone_y = (tileSize_y["empty"] / self.tile_factor_size) * nb_tile_y

        if self.init:
            for tileName in self.tiles:
                self.tiles[tileName].set_image(self.tile_factor_size)
                screen.blit(self.tiles[tileName].image, self.tiles[tileName].rect)
