import pygame
from envVar import *


# Class for the tile entity
class MousseIcon(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.icon = pygame.image.load(MousseFarm)
        self.icon = pygame.transform.scale(self.icon, (Mousse_icon_size, Mousse_icon_size))

        self.rect = self.icon.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.isEnable = False
        self.item_selected = "none"

    def set_image(self, path):
        self.icon = pygame.image.load(path)
        self.icon = pygame.transform.scale(self.icon, (Mousse_icon_size, Mousse_icon_size))
        self.rect = self.icon.get_rect()
