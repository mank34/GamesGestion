from envVar import *
from hud_button import HUD_button


# Class for the tile entity
class HUD(pygame.sprite.Sprite):

    def __init__(self, w, h):
        super().__init__()

        self.width = w
        self.height = h

        # Value
        self.cityRes = default_res

        # Main HUD generation
        self.main_HUD_button = {}
        for i in range(len(HUD_main_menu)):
            self.main_HUD_button[HUD_main_menu[i]] = HUD_button(i, resource[HUD_main_menu[i]], self.width, self.height)

        # Construct HUD generation
        self.construct_HUD_button = {}
        for i in range(len(HUD_construct_menu)):
            self.construct_HUD_button[HUD_construct_menu[i]] = HUD_button(i, resource[HUD_construct_menu[i]],
                                                                          self.width, self.height, 1)

        # Resource information generation
        # Parent >= 20 == resource information
        self.HUD_resource_button = {}
        for i in range(len(HUD_resource)):
            index = len(HUD_resource) - i - 1
            self.HUD_resource_button[HUD_resource[index]] = HUD_button(20 + i, resource[HUD_resource[index]],
                                                                       self.width, self.height, 0, HUD_resource[index])

    def updateHUD(self):
        for hud_but in self.HUD_resource_button:
            self.HUD_resource_button[hud_but].value = font.render(str(self.cityRes[hud_but.split('_')[-1]]),
                                                                  False, (0, 0, 0))

    def show_HUD(self, screen, show_HUD):
        self.draw_background(screen)
        for hud_but in self.main_HUD_button:
            screen.blit(self.main_HUD_button[hud_but].button, self.main_HUD_button[hud_but].rect)

        self.updateHUD()

        for hud_but in self.HUD_resource_button:
            screen.blit(self.HUD_resource_button[hud_but].button, self.HUD_resource_button[hud_but].rect)
            screen.blit(self.HUD_resource_button[hud_but].value, self.HUD_resource_button[hud_but].value_rect)

        if show_HUD["hud_construct"]:
            self.draw_construct_background(screen)

            for hud_but in self.construct_HUD_button:
                screen.blit(self.construct_HUD_button[hud_but].button, self.construct_HUD_button[hud_but].rect)

    def draw_background(self, surface):
        # HUD background
        HUD_background_color = (128, 128, 128)
        HUD_position = [0, self.height - HUD_size, self.width, HUD_size]
        pygame.draw.rect(surface, HUD_background_color, HUD_position)

    def draw_construct_background(self, surface):
        # HUD background
        HUD_background_color = (192, 192, 192)
        HUD_position = [0, self.height - 2 * HUD_size, (HUD_size + HUD_margin) * len(HUD_construct_menu), HUD_size]
        pygame.draw.rect(surface, HUD_background_color, HUD_position)
