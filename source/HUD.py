from envVar import *
from hud_button import HUD_button


# Class for the tile entity
def draw_background(surface):
    # HUD background
    HUD_background_color = (128, 128, 128)
    HUD_position = [0, windowSize - HUD_size, windowSize, HUD_size]
    pygame.draw.rect(surface, HUD_background_color, HUD_position)


def draw_construct_background(surface):
    # HUD background
    HUD_background_color = (192, 192, 192)
    HUD_position = [0, windowSize - 2 * HUD_size, (HUD_size + HUD_margin) * len(HUD_construct_menu), HUD_size]
    pygame.draw.rect(surface, HUD_background_color, HUD_position)


class HUD(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # Value
        self.cityRes = default_res

        # Main HUD generation
        self.main_HUD_button = {}
        for i in range(len(HUD_main_menu)):
            self.main_HUD_button[HUD_main_menu[i]] = HUD_button(i, resource[HUD_main_menu[i]])

        # Construct HUD generation
        self.construct_HUD_button = {}
        for i in range(len(HUD_construct_menu)):
            self.construct_HUD_button[HUD_construct_menu[i]] = HUD_button(i, resource[HUD_construct_menu[i]], 1)

        # Resource information generation
        # Parent >= 20 == resource information
        self.HUD_resource_button = {}
        for i in range(len(HUD_resource)):
            print(len(HUD_resource) - i - 1)
            index = len(HUD_resource) - i - 1
            self.HUD_resource_button[HUD_resource[index]] = HUD_button(20 + i, resource[HUD_resource[index]], 0,
                                                                       HUD_resource[index])

    def updateHUD(self):
        for hud_but in self.HUD_resource_button:
            self.HUD_resource_button[hud_but].value = font.render(str(self.cityRes[hud_but.split('_')[-1]]),
                                                                  False, (0, 0, 0))

    def show_HUD(self, screen, show_HUD):
        draw_background(screen)
        for hud_but in self.main_HUD_button:
            screen.blit(self.main_HUD_button[hud_but].button, self.main_HUD_button[hud_but].rect)

        self.updateHUD()

        for hud_but in self.HUD_resource_button:
            screen.blit(self.HUD_resource_button[hud_but].button, self.HUD_resource_button[hud_but].rect)
            screen.blit(self.HUD_resource_button[hud_but].value, self.HUD_resource_button[hud_but].value_rect)

        if show_HUD["hud_construct"]:
            draw_construct_background(screen)

            for hud_but in self.construct_HUD_button:
                screen.blit(self.construct_HUD_button[hud_but].button, self.construct_HUD_button[hud_but].rect)
