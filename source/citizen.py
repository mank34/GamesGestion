import math

from envVar import *


# Class for the tile entity
class citizen(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # Human need
        self.hungry = 0
        self.tired = 0

        self.happy = 100 - self.hungry - self.tired

        self.image = pygame.image.load("../asset/PNJ/citizen.png")
        self.image = pygame.transform.scale(self.image, (citizen_size_x, citizen_size_y))

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.rect.x = 700 / 2 + (0 - 1) * (tileSize_x / 2) - 5

        game_zone_y = (tileSize_y["empty"]) * nb_tile_y
        self.rect.y = -game_zone_y / 2 + 700 / 2 + (0 + 1) * (tileSize_y["empty"] / 2)
        self.rect.y += tileSize_y["empty"] / 2
        self.rect.y -= citizen_size_y

        self.direction = 3
        self.current_tile = "5"

    def move(self):
        if self.direction == 0 and (int(self.current_tile) + 1) % nb_tile_x:  # Right
            self.rect.y += math.tan(0.52) * 2
            self.rect.x += 2
        elif self.direction == 1 and int(self.current_tile) % nb_tile_x:  # left
            self.rect.y -= 1  # math.tan(0.52) * 2 around down
            self.rect.x -= 2
        elif self.direction == 2 and int(self.current_tile) > nb_tile_y-1:  # up
            self.rect.x += 4  # math.tan(1.072) * 2 around up
            self.rect.y -= 2
        elif self.direction == 3 and int(self.current_tile) < nb_tile_y * nb_tile_x - nb_tile_x:  # down
            self.rect.x -= math.tan(1.0472) * 2
            self.rect.y += 2
