import pygame
from envVar import *


# Class for the tile entity
class Tile(pygame.sprite.Sprite):

    def __init__(self, name="undefined", x=windowBoarder, y=windowBoarder):
        super().__init__()

        self.name = name
        self.type = "empty"

        self.poProduction = 0
        self.foodProduction = 0

        self.imageNoOver = pygame.image.load(EmptyTile)
        self.imageOver = pygame.image.load(EmptyTileOver)

        self.image = self.imageNoOver;
        self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
        pygame.draw.rect(self.image, black, (0, 0, self.image.get_width(), self.image.get_height()), boarderSize)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isOver = False

    def set_tile_name(self, name):
        self.name = name

    def set_over(self, isOver):
        self.isOver = isOver
        if isOver:
            self.image = self.imageOver
        else:
            self.image = self.imageNoOver

        self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
        pygame.draw.rect(self.image, black, (0, 0, self.image.get_width(), self.image.get_height()), boarderSize)

    def update_in_farm(self, code):
        self.type = "farm"
        self.name = "farm_" + code

        self.imageNoOver = pygame.image.load(FarmTile)
        self.imageOver = pygame.image.load(FarmTileOver)

        if self.isOver:
            self.image = self.imageOver
        else:
            self.image = self.imageNoOver
        self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
        pygame.draw.rect(self.image, black, (0, 0, self.image.get_width(), self.image.get_height()), boarderSize)

        self.poProduction = 5
        self.foodProduction = 5

    def update_in_market(self, code):
        self.type = "market"
        self.name = "market_" + code

        self.imageNoOver = pygame.image.load(MarketTile)
        self.imageOver = pygame.image.load(MarketTileOver)

        if self.isOver:
            self.image = self.imageOver
        else:
            self.image = self.imageNoOver
        self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
        pygame.draw.rect(self.image, black, (0, 0, self.image.get_width(), self.image.get_height()), boarderSize)

        self.poProduction = 5
        self.foodProduction = 5
