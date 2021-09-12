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

        self.construct = True
        self.cnt_construct = 0

        self.shall_be_update = True
        self.is_Over = False
        self.set_image(tile_factor_size)

        self.rect = self.image.get_rect()

        self.rect.x = pos_x
        self.rect.y = pos_y

        self.gap_y = 0

        self.show_information_enable = False
        self.info_position = [0, 0, 0, 0]

        self.remove_button = GameInfoFont.render("Destroy", False, (0, 0, 0))
        self.remove_button_rect = self.remove_button.get_rect()

    # Apply a filter on the over tile
    def set_over(self, isOver, tile_factor_size):
        if not isOver and self.is_Over:
            self.is_Over = False

        self.set_image(tile_factor_size)
        if isOver:
            self.is_Over = True
            self.set_filter()

    # Change the tile's type (level reset)
    def update_in(self, new_type, tile_factor_size):
        self.gap_y = (tileSize_y["empty"] - tileSize_y[self.type])
        self.rect.y -= self.gap_y / tile_factor_size
        self.type = new_type
        self.shall_be_update = True
        self.construct = False
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
        if self.construct:
            self.image = resource[self.type]
        else:
            self.image = resource["empty"]

        if self.construct:
            self.image = pygame.transform.scale(self.image,
                                                (int(tileSize_x / tile_factor_size),
                                                 int((tileSize_base + tileSize_y[self.type]) / tile_factor_size)))
        else:
            self.image = pygame.transform.scale(self.image,
                                                (int(tileSize_x / tile_factor_size),
                                                 int((tileSize_base + tileSize_y["empty"]) / tile_factor_size)))

    def set_prod(self):
        self.production = dict(po=po_production[self.type],
                               food=food_production[self.type],
                               wood=wood_production[self.type])

    def set_cost(self):
        self.cost = dict(po=po_cost[self.type],
                         food=food_cost[self.type],
                         wood=wood_cost[self.type])

    def is_in(self, tile_factor_size, point):

        A = (self.rect.x + tileSize_x / 2 / tile_factor_size,
             self.rect.y + (tileSize_y[self.type] - tileSize_y["empty"]) / tile_factor_size)
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

    def show_progress_construction(self, surface, FPS, tile_factor_size):
        background_color = (128, 128, 128)
        progress_color = (0, 255, 0)
        self.cnt_construct += 1

        if self.cnt_construct >= (construction_time[self.type] / FPS) and not self.construct:
            self.construct = True
            self.gap_y = (tileSize_y[self.type] - tileSize_y["empty"])
            self.rect.y -= self.gap_y / tile_factor_size

        if not self.construct:
            background_progress = [self.rect.x + self.rect.width / 2 -
                                   int(self.rect.width * 0.7 / 2),

                                   self.rect.y + (tileSize_y["empty"] / tile_factor_size) / 2 -
                                   int(self.rect.width * 0.1 / 2),

                                   int(self.rect.width * 0.7),

                                   int(self.rect.width * 0.1)]
            pygame.draw.rect(surface, background_color, background_progress)

            progress_percent = self.cnt_construct / (construction_time[self.type] / FPS)

            progress = [self.rect.x + self.rect.width / 2 -
                        int(self.rect.width * 0.7 / 2),

                        self.rect.y + (tileSize_y["empty"] / tile_factor_size) / 2 -
                        int(self.rect.width * 0.1 / 2),

                        int(self.rect.width * progress_percent * 0.7),

                        int(self.rect.width * 0.1)]
            pygame.draw.rect(surface, progress_color, progress)

        else:
            self.cnt_construct = 0

    def show_information(self, pos, window_width, surface):

        self.show_information_enable = True

        # Background
        info_background_color = (128, 128, 128)
        info_size = (200, 300)

        if pos:
            right = False
            down = True
            if pos[0] < (window_width - info_size[0]):
                right = True

            if pos[1] > info_size[1]:
                down = False

            if right:
                pos_x = pos[0]
            else:
                pos_x = pos[0] - info_size[0]

            if down:
                pos_y = pos[1]
            else:
                pos_y = pos[1] - info_size[1]

            self.info_position = [pos_x, pos_y, info_size[0], info_size[1]]
        pygame.draw.rect(surface, info_background_color, self.info_position)

        # Write information
        # Name
        name = GameInfoFont.render(self.type.upper(), False, (0, 0, 0))
        name_rect = name.get_rect()
        name_rect.x = self.info_position[0] + info_size[0] / 2 - name_rect.width / 2
        name_rect.y = self.info_position[1]
        surface.blit(name, name_rect)
        offset = name_rect.height + 5

        if not self.construct:
            construct = GameCommentFont.render("Construction in progress", False, (0, 0, 0))
            construct_rect = construct.get_rect()
            construct_rect.x = self.info_position[0] + info_size[0] / 2 - construct_rect.width / 2
            construct_rect.y = self.info_position[1] + offset
            surface.blit(construct, construct_rect)
            offset += construct_rect.height + 5

        # Production
        prod_title = GameInfoFont.render("Prod / day: ", False, (0, 0, 0))
        prod_title_rect = prod_title.get_rect()
        prod_title_rect.x = self.info_position[0] + 5
        prod_title_rect.y = self.info_position[1] + offset
        surface.blit(prod_title, prod_title_rect)
        offset += prod_title_rect.height

        cnt_prod = 0
        for prod in self.production:
            if self.production[prod] > 0:
                image = resource["hud_res_" + prod]
                image = pygame.transform.scale(image, (int(Mousse_icon_size / 2), int(Mousse_icon_size / 2)))
                image_rect = image.get_rect()

                prod_name = GameInfoFont.render(str(self.production[prod]), False, (0, 0, 0))
                prod_name_rect = prod_name.get_rect()

                image_rect.x = self.info_position[0] + cnt_prod * (image_rect.width + prod_name_rect.width + 10)
                image_rect.y = self.info_position[1] + offset

                prod_name_rect.x = self.info_position[0] + image_rect.width + 5 + cnt_prod * (image_rect.width +
                                                                                              prod_name_rect.width + 10)
                prod_name_rect.y = self.info_position[1] + offset

                surface.blit(image, image_rect)
                surface.blit(prod_name, prod_name_rect)

                cnt_prod += 1

        if cnt_prod == 0:
            prod_name = GameInfoFont.render("   None", False, (0, 0, 0))
            prod_name_rect = prod_name.get_rect()
            prod_name_rect.x = self.info_position[0] + 5
            prod_name_rect.y = self.info_position[1] + offset
            surface.blit(prod_name, prod_name_rect)
            cnt_prod += 1

        offset += prod_title_rect.height + 5

        # Cost
        cost_title = GameInfoFont.render("Cost / day: ", False, (0, 0, 0))
        cost_title_rect = cost_title.get_rect()
        cost_title_rect.x = self.info_position[0] + 5
        cost_title_rect.y = self.info_position[1] + offset
        surface.blit(cost_title, cost_title_rect)

        offset += cost_title_rect.height

        cnt = 0
        for cost in self.cost:
            if self.cost[cost] > 0:
                image = resource["hud_res_" + cost]
                image = pygame.transform.scale(image, (int(Mousse_icon_size / 2), int(Mousse_icon_size / 2)))
                image_rect = image.get_rect()

                cost_name = GameInfoFont.render(str(self.cost[cost]), False, (0, 0, 0))
                cost_name_rect = cost_name.get_rect()

                image_rect.x = self.info_position[0] + cnt * (image_rect.width + cost_name_rect.width + 10)
                image_rect.y = self.info_position[1] + offset

                cost_name_rect.x = self.info_position[0] + image_rect.width + 5 + cnt * (image_rect.width +
                                                                                         cost_name_rect.width + 10)
                cost_name_rect.y = self.info_position[1] + offset

                surface.blit(image, image_rect)
                surface.blit(cost_name, cost_name_rect)

                cnt += 1

        if cnt == 0:
            cost_name = GameInfoFont.render("   None", False, (0, 0, 0))
            cost_name_rect = cost_name.get_rect()
            cost_name_rect.x = self.info_position[0] + 5
            cost_name_rect.y = self.info_position[1] + offset
            surface.blit(cost_name, cost_name_rect)

        offset += cost_title_rect.height + 5

        # Remove
        if self.type != "empty" and self.construct:
            self.remove_button_rect.x = self.info_position[0] + 5
            self.remove_button_rect.y = self.info_position[1] + info_size[1] - self.remove_button_rect.height
            surface.blit(self.remove_button, self.remove_button_rect)
