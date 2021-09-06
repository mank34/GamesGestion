from envVar import *


# Class for the tile entity
class HUD_button(pygame.sprite.Sprite):

    def __init__(self, num, img, w, h, parent=0, name="null"):
        super().__init__()

        self.width = w
        self.height = h

        self.button = img
        if num < 20:
            self.button = pygame.transform.scale(self.button,
                                                 (HUD_size_button, HUD_size_button))
            self.rect = self.button.get_rect()

            self.rect.x = HUD_margin + (HUD_size_button + HUD_margin) * num
            self.rect.y = self.height - (1 + parent) * HUD_size + HUD_margin

        else:
            self.button = pygame.transform.scale(self.button,
                                                 (int(HUD_size_button / 2), int(HUD_size_button / 2)))
            self.rect = self.button.get_rect()

            shift_by_element = Info_text_size - HUD_size_button / 2
            self.rect.x = self.width - shift_by_element + shift_by_element * int((20 - num) / 2)
            self.rect.y = self.height - HUD_size + HUD_margin + (num % 2) * (HUD_size_button / 2 + HUD_margin)

            self.value = font.render(str(default_res[name.split('_')[-1]]), False, (0, 0, 0))
            self.value_rect = self.value.get_rect()
            self.value_rect.x = self.rect.x + HUD_size_button / 2 + 5
            self.value_rect.y = self.rect.y - 7
