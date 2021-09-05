import pygame
from envVar import *


# TODO: Level
# TODO: optimize cost/prod

# Class for the tile entity
class Tile(pygame.sprite.Sprite):

    def __init__(self, x=windowBoarder, y=windowBoarder):
        super().__init__()

        self.type = "empty"
        self.level = 0

        self.poProduction = {
            "empty": 0,
            "farm": 5,
            "market": 5
        }
        self.foodProduction = {
            "empty": 0,
            "farm": 5,
            "market": 5
        }

        self.set_image()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # Apply a filter on the over tile
    def set_over(self, isOver):
        self.set_image()
        if isOver:
            self.set_filter()

    # Change the tile's type (level reset)
    def update_in(self, new_type):
        self.type = new_type
        self.set_image()
        self.level = 0

    # Apply the filter
    def set_filter(self):
        colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
        colorImage.fill((200, 200, 200))
        self.image.blit(colorImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Set the image
    def set_image(self):
        self.image = resource[self.type]
        self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
