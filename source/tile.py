from envVar import *


# Class for the tile entity
class Tile(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, tile_factor_size):
        super().__init__()

        self.type = "empty"
        self.level = 0

        self.production = {}
        self.set_prod()

        self.cost = {}
        self.set_cost()

        self.set_image(tile_factor_size)

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    # Apply a filter on the over tile
    def set_over(self, isOver, tile_factor_size):
        self.set_image(tile_factor_size)
        if isOver:
            self.set_filter()

    # Change the tile's type (level reset)
    def update_in(self, new_type, tile_factor_size):
        self.rect.y -= (tileSize_y[new_type] - tileSize_y[self.type])/tile_factor_size
        self.type = new_type
        self.set_image(tile_factor_size)
        self.set_prod()
        self.set_cost()
        self.level = 0

    def update_size(self, pos_x, pos_y):
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    # Apply the filter
    def set_filter(self):
        colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
        colorImage.fill((200, 200, 200))
        self.image.blit(colorImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Set the image
    def set_image(self, tile_factor_size):
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

    def is_in(self, tile_factor_size):
        point = pygame.mouse.get_pos()

        A = (self.rect.x + tileSize_x / 2 / tile_factor_size,
             self.rect.y + (tileSize_y[self.type] - tileSize_y["empty"])/tile_factor_size)
        B = (self.rect.x, self.rect.y + tileSize_y["empty"] / 2 / tile_factor_size)
        C = (self.rect.x + tileSize_x / 2 / tile_factor_size,
             self.rect.y + tileSize_y[self.type] / tile_factor_size)
        D = (self.rect.x + tileSize_x / tile_factor_size, self.rect.y + tileSize_y[self.type] / 2 / tile_factor_size)

        # Algo
        # result = (yp - y1) * (x2 -x1) - (xp - x1) * (y2 - y1)
        # result > 0: the point is to left of the line
        # result = 0: the point is on of the line
        # result < 0: the point is to right of the line

        cond_1 = False
        cond_2 = False
        cond_3 = False
        cond_4 = False

        # The point is in if:
        # cond_1: the point is to left of the AB line
        result = (point[1] - A[1]) * (B[0] - A[0]) - (point[0] - A[0]) * (B[1] - A[1])
        if result <= 0:
            cond_1 = True

        # cond_2: the point is to left of the BC line
        result = (point[1] - B[1]) * (C[0] - B[0]) - (point[0] - B[0]) * (C[1] - B[1])
        if result <= 0:
            cond_2 = True

        # cond_3: the point is to right of the DC line
        result = (point[1] - D[1]) * (C[0] - D[0]) - (point[0] - D[0]) * (C[1] - D[1])
        if result > 0:
            cond_3 = True

        # cond_4: the point is to right of the AD line
        result = (point[1] - A[1]) * (D[0] - A[0]) - (point[0] - A[0]) * (D[1] - A[1])
        if result > 0:
            cond_4 = True

        return cond_1 and cond_2 and cond_3 and cond_4
