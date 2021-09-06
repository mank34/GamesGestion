from envVar import *


# Class for the tile entity
class Tile(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.type = "empty"
        self.level = 0

        self.production = {}
        self.set_prod()

        self.cost = {}
        self.set_cost()

        self.set_image()

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    # Apply a filter on the over tile
    def set_over(self, isOver):
        self.set_image()
        if isOver:
            self.set_filter()

    # Change the tile's type (level reset)
    def update_in(self, new_type):
        self.rect.y -= (tileSize_y[new_type] - tileSize_y[self.type])
        self.type = new_type
        self.set_image()
        self.set_prod()
        self.set_cost()
        self.level = 0

    # Apply the filter
    def set_filter(self):
        colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
        colorImage.fill((200, 200, 200))
        self.image.blit(colorImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Set the image
    def set_image(self):
        self.image = resource[self.type]
        self.image = pygame.transform.scale(self.image,
                                            (int(tileSize_x / tile_factor_size),
                                             int((tileSize_base+tileSize_y[self.type]) / tile_factor_size)))

    def set_prod(self):
        self.production = dict(po=po_production[self.type],
                               food=food_production[self.type],
                               wood=wood_production[self.type])

    def set_cost(self):
        self.cost = dict(po=po_cost[self.type],
                         food=food_cost[self.type],
                         wood=wood_cost[self.type])
