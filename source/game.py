from HUD import HUD
from tile import Tile
from mousseIcon import MousseIcon
from envVar import *


# Class game
class Game:
    def __init__(self, w, h):

        self.FPS_selected = 3
        self.res_selected = 3

        self.width = w
        self.height = h

        # Flag to known the game state
        self.is_starting = False
        self.is_pausing = False
        self.in_configuring = False

        # Game menu
        self.game_name = GameNameFont.render(GameName, False, (0, 0, 0))
        self.game_name_rect = self.game_name.get_rect()
        self.game_name_rect.x = int(self.width * 0.33)
        self.game_name_rect.y = int(self.height * 0.25)

        self.game_start = GameMenuFont.render("Start", False, (0, 0, 0))
        self.game_start_rect = self.game_start.get_rect()
        self.game_start_rect.x = int(self.width * 0.45)
        self.game_start_rect.y = int(self.height * 0.4)

        self.game_option = GameMenuFont.render("Options", False, (0, 0, 0))
        self.game_option_rect = self.game_option.get_rect()
        self.game_option_rect.x = int(self.width * 0.44)
        self.game_option_rect.y = int(self.height * 0.45)

        self.game_quit = GameMenuFont.render("Quit", False, (0, 0, 0))
        self.game_quit_rect = self.game_quit.get_rect()
        self.game_quit_rect.x = int(self.width * 0.46)
        self.game_quit_rect.y = int(self.height * 0.50)

        # Config menu
        self.option_name = GameNameFont.render("Option", False, (0, 0, 0))
        self.option_name_rect = self.option_name.get_rect()
        self.option_name_rect.x = int(self.width * 0.4)
        self.option_name_rect.y = int(self.height * 0.25)

        self.lessFPS_button = GameMenuFont.render("<-", False, (0, 0, 0))
        self.lessFPS_button_rect = self.lessFPS_button.get_rect()
        self.lessFPS_button_rect.x = int(self.width * 0.38)
        self.lessFPS_button_rect.y = int(self.height * 0.4)

        self.limitFPS = GameMenuFont.render("Max FPS: " + str(FPS_available[self.FPS_selected]), False, (0, 0, 0))
        self.limitFPS_rect = self.limitFPS.get_rect()
        self.limitFPS_rect.x = int(self.width * 0.42)
        self.limitFPS_rect.y = int(self.height * 0.4)

        self.moreFPS_button = GameMenuFont.render("->", False, (0, 0, 0))
        self.moreFPS_button_rect = self.moreFPS_button.get_rect()
        self.moreFPS_button_rect.x = int(self.width * 0.60)
        self.moreFPS_button_rect.y = int(self.height * 0.4)

        self.lessRes_button = GameMenuFont.render("<-", False, (0, 0, 0))
        self.lessRes_button_rect = self.lessRes_button.get_rect()
        self.lessRes_button_rect.x = int(self.width * 0.38)
        self.lessRes_button_rect.y = int(self.height * 0.5)

        self.resolution = GameMenuFont.render("Resolution: " + str(resolution_available[self.res_selected]),
                                              False, (0, 0, 0))
        self.resolution_rect = self.resolution.get_rect()
        self.resolution_rect.x = int(self.width * 0.42)
        self.resolution_rect.y = int(self.height * 0.5)

        self.moreRes_button = GameMenuFont.render("->", False, (0, 0, 0))
        self.moreRes_button_rect = self.moreRes_button.get_rect()
        self.moreRes_button_rect.x = int(self.width * 0.60)
        self.moreRes_button_rect.y = int(self.height * 0.5)

        self.back_button = GameMenuFont.render("Back", False, (0, 0, 0))
        self.back_button_rect = self.back_button.get_rect()
        self.back_button_rect.x = int(self.width * 0.46)
        self.back_button_rect.y = int(self.height * 0.6)

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
        self.game_zone_x = (tileSize_x / tile_factor_size) * nb_tile_x
        self.game_zone_y = (tileSize_y / tile_factor_size) * nb_tile_y



        #        self.start_game_zone = dict(x=int(-nb_tile_x / 2 * tileSize) + self.width / 2,
        #                                    y=int(-nb_tile_y / 2 * tileSize) + self.height / 2)
        #        self.end_game_zone = dict(x=int(nb_tile_x / 2 * tileSize) - self.width / 2,
        #                                  y=int(nb_tile_y / 2 * tileSize) - self.height / 2)

        # Generate all the tiles
        self.tiles = {}

        for y in range(nb_tile_y):
            for x in range(nb_tile_x):
                self.tiles[str(y * nb_tile_x + x)] = Tile(self.width / 2 +
                                                          (x - y) * tileSize_x / 2 / tile_factor_size,
                                                          -self.game_zone_y / 2 + self.height/2 +
                                                          (x + y) * tileSize_y / 2 / tile_factor_size)
                if showLoading:
                    print(str(int((y * nb_tile_x + x) / (nb_tile_x * nb_tile_y) * 100)) + "%")

        # HUD
        self.hud = HUD(self.width, self.height)

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

    def option_menu(self, screen):
        screen.blit(self.option_name, self.option_name_rect)
        screen.blit(self.lessFPS_button, self.lessFPS_button_rect)
        screen.blit(self.limitFPS, self.limitFPS_rect)
        screen.blit(self.moreFPS_button, self.moreFPS_button_rect)
        screen.blit(self.lessRes_button, self.lessRes_button_rect)
        screen.blit(self.resolution, self.resolution_rect)
        screen.blit(self.moreRes_button, self.moreRes_button_rect)
        screen.blit(self.back_button, self.back_button_rect)

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
        if self.cnt_day > 30000 / FPS_available[self.FPS_selected]:
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

        right = pygame.mouse.get_pos()[0] > self.width - windowBoarder
        left = pygame.mouse.get_pos()[0] < windowBoarder
        up = pygame.mouse.get_pos()[1] < windowBoarder
        down = pygame.mouse.get_pos()[1] > self.height - windowBoarder - HUD_size

        right = right and pygame.mouse.get_pos()[1] < self.width - HUD_size
        left = left and pygame.mouse.get_pos()[1] < self.width - HUD_size
        down = down and pygame.mouse.get_pos()[1] < self.height - HUD_size

        shift_x = (self.game_zone_x - self.width) / 2

        shift_y = (self.game_zone_y - self.height - HUD_size) / 2

        print(str(shift_x) + " " + str(shift_y))

        if shift_x > 0:
            if right and self.cam_pos["x"] <= -shift_x - windowBoarder:
                right = False
            if left and self.cam_pos["x"] >= shift_x:
                left = False
        else:
            right = False
            left = False

        if shift_y > 0:
            if down and self.cam_pos["y"] <= -shift_y - tileSize_x/tile_factor_size - windowBoarder :
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

    def check_game_event(self, event):

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

            elif self.game_option_rect.collidepoint(pygame.mouse.get_pos()):
                self.in_configuring = True

            elif self.game_quit_rect.collidepoint(pygame.mouse.get_pos()):
                running = False
        return running

    def check_option_event(self, event):
        # Mouse event - clique left
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
            if self.back_button_rect.collidepoint(pygame.mouse.get_pos()):
                self.in_configuring = False
                return resolution_available[self.res_selected]

            elif self.lessFPS_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.FPS_selected > 0:
                    self.FPS_selected -= 1
                    self.limitFPS = GameMenuFont.render("Max FPS: " + str(FPS_available[self.FPS_selected]),
                                                        False, (0, 0, 0))

            elif self.moreFPS_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.FPS_selected < len(FPS_available) - 1:
                    self.FPS_selected += 1
                    self.limitFPS = GameMenuFont.render("Max FPS: " + str(FPS_available[self.FPS_selected]),
                                                        False, (0, 0, 0))

            elif self.lessRes_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.res_selected > 0:
                    self.res_selected -= 1
                    self.resolution = GameMenuFont.render("Resolution: " + str(resolution_available[self.res_selected]),
                                                          False, (0, 0, 0))

            elif self.moreRes_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.res_selected < len(resolution_available) - 1:
                    self.res_selected += 1
                    self.resolution = GameMenuFont.render("Resolution: " + str(resolution_available[self.res_selected]),
                                                          False, (0, 0, 0))

        return "NULL"
