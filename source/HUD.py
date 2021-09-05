from envVar import *


# Class for the tile entity
def draw_background(surface):
    # HUD background
    HUD_background_color = (128, 128, 128)
    HUD_position = [0, windowSize - HUD_size, windowSize, HUD_size]
    pygame.draw.rect(surface, HUD_background_color, HUD_position)


def draw_construct_background(surface):
    # HUD background
    HUD_background_color = (192, 192, 192)
    HUD_position = [0, windowSize - 2 * HUD_size, (HUD_size + HUD_margin) * len(construct), HUD_size]
    pygame.draw.rect(surface, HUD_background_color, HUD_position)


def show_HUD(screen, game, show_construct_HUD):
    draw_background(screen)
    screen.blit(game.hud.construct_button, game.hud.construct_button_rect)
    game.hud.updateHUD()
    screen.blit(game.hud.po_icon, game.hud.po_icon_rect)
    screen.blit(game.hud.poValue, game.hud.poValue_rect)
    screen.blit(game.hud.food_icon, game.hud.food_icon_rect)
    screen.blit(game.hud.foodValue, game.hud.foodValue_rect)

    if show_construct_HUD:
        draw_construct_background(screen)
        screen.blit(game.hud.farm_construct_button, game.hud.farm_construct_button_rect)
        screen.blit(game.hud.market_construct_button, game.hud.market_construct_button_rect)


class HUD(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # Value
        self.po = 500
        self.food = 0

        # HUD construct button
        self.construct_button = pygame.image.load(ConstructionButton)
        self.construct_button = pygame.transform.scale(self.construct_button,
                                                       (HUD_size_button, HUD_size_button))
        self.construct_button_rect = self.construct_button.get_rect()
        self.construct_button_rect.x = 0
        self.construct_button_rect.y = windowSize - HUD_size + HUD_margin

        # Construct farm
        self.farm_construct_button = pygame.image.load(MousseFarm)
        self.farm_construct_button = pygame.transform.scale(self.farm_construct_button,
                                                            (HUD_size_button, HUD_size_button))
        self.farm_construct_button_rect = self.farm_construct_button.get_rect()
        self.farm_construct_button_rect.x = HUD_size + HUD_margin
        self.farm_construct_button_rect.y = windowSize - 2 * HUD_size + HUD_margin

        # Construct market
        self.market_construct_button = pygame.image.load(MousseMarket)
        self.market_construct_button = pygame.transform.scale(self.market_construct_button,
                                                              (HUD_size_button, HUD_size_button))
        self.market_construct_button_rect = self.market_construct_button.get_rect()
        self.market_construct_button_rect.x = 0 + HUD_margin
        self.market_construct_button_rect.y = windowSize - 2 * HUD_size + HUD_margin

        # PO information
        self.po_icon = pygame.image.load(Gold_Icon)
        self.po_icon = pygame.transform.scale(self.po_icon, (int(HUD_size_button / 2), int(HUD_size_button / 2)))
        self.po_icon_rect = self.po_icon.get_rect()
        self.po_icon_rect.x = windowSize - HUD_size_button / 2 - Info_text_size
        self.po_icon_rect.y = windowSize - HUD_size + HUD_margin

        self.poValue = font.render(str(self.po), False, (0, 0, 0))
        self.poValue_rect = self.poValue.get_rect()
        self.poValue_rect.x = self.po_icon_rect.x + HUD_size_button / 2 + 5
        self.poValue_rect.y = self.po_icon_rect.y - 7

        # Food information
        self.food_icon = pygame.image.load(Food_Icon)
        self.food_icon = pygame.transform.scale(self.food_icon, (int(HUD_size_button / 2), int(HUD_size_button / 2)))
        self.food_icon_rect = self.food_icon.get_rect()
        self.food_icon_rect.x = windowSize - HUD_size_button / 2 - Info_text_size
        self.food_icon_rect.y = windowSize - HUD_size + HUD_margin + HUD_size_button / 2 + HUD_margin

        self.foodValue = font.render(str(self.food), False, (0, 0, 0))
        self.foodValue_rect = self.poValue.get_rect()
        self.foodValue_rect.x = self.food_icon_rect.x + HUD_size_button / 2 + 5
        self.foodValue_rect.y = self.food_icon_rect.y - 7

    def updateHUD(self):
        self.poValue = font.render(str(self.po), False, (0, 0, 0))
        self.foodValue = font.render(str(self.food), False, (0, 0, 0))
