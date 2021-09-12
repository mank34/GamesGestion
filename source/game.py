from HUD import HUD
from citizen import citizen
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

        self.tile_factor_size = 1

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
        self.cnt_move_entity = 0
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

        # Citizen
        self.change_dir = True
        self.citizen = citizen()

    def update(self, screen):

        # Display tile
        update_screen = False
        for tileName in self.tiles:
            if self.width >= self.tiles[tileName].rect.x >= -tileSize_x and \
                    self.height >= self.tiles[tileName].rect.y >= -tileSize_y[self.tiles[tileName].type]:

                self.tiles[tileName].set_over(self.tiles[tileName].is_in(
                    self.tile_factor_size, pygame.mouse.get_pos()), self.tile_factor_size)

                if self.tiles[tileName].shall_be_update:
                    update_screen = True

        # Manage day
        self.cnt_day += 1
        if self.cnt_day > 30000 / FPS_available[self.config_menu.FPS_selected]:
            # Update resource
            self.update_prod_value()
            self.cnt_day = 0
            self.nb_day += 1

        day_information = GameInfoFont.render("Day " + str(self.nb_day), False, (0, 0, 0))
        day_information_rect = day_information.get_rect()
        day_information_rect.x = 10
        day_information_rect.y = 10
        screen.blit(day_information, day_information_rect)

        # Camera move only if all the menu are close
        cam_move = True
        for menu_HUD in self.show_HUD:
            if self.show_HUD[menu_HUD]:
                cam_move = False

        if cam_move:
            update_screen = update_screen or self.move()

        # Tile
        update_screen = True
        if update_screen:
            for tileName in self.tiles:
                if self.width >= self.tiles[tileName].rect.x >= -tileSize_x and \
                        self.height >= self.tiles[tileName].rect.y >= -tileSize_y[self.tiles[tileName].type]:
                    screen.blit(self.tiles[tileName].image, self.tiles[tileName].rect)

        # Citizen
        self.cnt_move_entity += 1
        if self.cnt_move_entity > 1500 / FPS_available[self.config_menu.FPS_selected]:
            self.citizen.move()
            self.cnt_move_entity = 0
            for tileName in self.tiles:
                if self.tiles[tileName].is_in(self.tile_factor_size,
                                              (self.citizen.rect.x + citizen_size_x,
                                               self.citizen.rect.y + citizen_size_y)):

                    if tileName != self.citizen.current_tile and self.change_dir:
                        # self.citizen.direction = randint(0, 3)
                        self.citizen.move()
                        self.change_dir = False
                    else:
                        self.change_dir = True

                    self.citizen.current_tile = tileName
                    # print("citizen is in " + tileName)
        screen.blit(self.citizen.image, self.citizen.rect)

        # Display HUD
        self.hud.show_HUD(screen, self.show_HUD)

        # Mousse icon
        if self.mousseIcon.isEnable:
            self.mousseIcon.rect.x = pygame.mouse.get_pos()[0]
            self.mousseIcon.rect.y = pygame.mouse.get_pos()[1]
            screen.blit(self.mousseIcon.icon, self.mousseIcon.rect)

        # Display tile information
        for tileName in self.tiles:
            if self.tiles[tileName].show_information_enable:
                self.tiles[tileName].show_information(None, self.width, screen)

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

        return left or right or up or down

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
            previously_open = self.disable_all_tile_information()
            if pygame.mouse.get_pos()[1] < self.height - HUD_size:
                if self.show_HUD["hud_construct"]:
                    for menu in self.hud.construct_HUD_button:
                        if self.hud.construct_HUD_button[menu].rect.collidepoint(pygame.mouse.get_pos()):
                            self.mousseIcon.set_image(resource[menu])
                            self.mousseIcon.isEnable = True
                            self.mousseIcon.item_selected = menu.split('_')[-1]

                else:
                    for tileName in self.tiles:
                        if self.tiles[tileName].is_in(self.tile_factor_size, pygame.mouse.get_pos()):
                            print("Tile " + tileName + " clicked")
                            if self.mousseIcon.isEnable:
                                self.tiles[tileName].update_in(self.mousseIcon.item_selected, self.tile_factor_size)
                                self.mousseIcon.isEnable = False
                            else:
                                if not previously_open:
                                    self.tiles[tileName].show_information(pygame.mouse.get_pos(), self.width, screen)

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
        pos_x = self.width / 2 + (x - y) * (
                tileSize_x / 2 / self.tile_factor_size) - tileSize_x / self.tile_factor_size / 2

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

    def disable_all_tile_information(self):
        for tileName in self.tiles:
            if self.tiles[tileName].show_information_enable:
                self.tiles[tileName].show_information_enable = False
                return True
        return False
