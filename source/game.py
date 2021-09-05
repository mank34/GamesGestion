import pygame
from HUD import HUD
from tile import Tile
from mousseIcon import MousseIcon
from envVar import *


def move_cam(game):
    right = False
    left = False
    up = False
    down = False

    if (pygame.mouse.get_pos()[0]) > windowSize - windowBoarder:
        right = True
    elif (pygame.mouse.get_pos()[0]) < windowBoarder:
        left = True

    if (pygame.mouse.get_pos()[1]) > windowSize - windowBoarder:
        down = True
    elif (pygame.mouse.get_pos()[1]) < windowBoarder:
        up = True

    game.move(right, left, up, down)


# Class game
class Game:
    def __init__(self):

        # Camera configuration
        self.cam_velocity = 2

        self.cam_pos = {
            "x": 0,
            "y": 0
        }

        # Define the game zone
        self.start_game_zone = {
            "x": int(-nb_tile_x / 2 * tileSize) + windowSize / 2,
            "y": int(-nb_tile_y / 2 * tileSize) + windowSize / 2
        }
        self.end_game_zone = {
            "x": int(nb_tile_x / 2 * tileSize) - windowSize / 2,
            "y": int(nb_tile_y / 2 * tileSize) - windowSize / 2
        }

        # Generate all the tiles
        self.tiles = {}

        for y in range(nb_tile_y):
            for x in range(nb_tile_x):
                self.tiles[str(y * nb_tile_x + x)] = Tile("empty_" + str(y * nb_tile_x + x),
                                                          self.start_game_zone["x"] + x * tileSize,
                                                          self.start_game_zone["y"] + y * tileSize)
                print(str(int((y * nb_tile_x + x) / (nb_tile_x * nb_tile_y) * 100)) + "%")

        # HUD
        self.hud = HUD()

        # Mousse icon
        self.mousseIcon = MousseIcon()

    def move(self, right, left, up, down):

        if right and self.cam_pos["x"] < self.start_game_zone["x"] - windowBoarder:
            right = False
        if left and self.cam_pos["x"] > self.end_game_zone["x"] + windowBoarder:
            left = False

        if down and self.cam_pos["y"] < self.start_game_zone["y"] - windowBoarder:
            down = False
        if up and self.cam_pos["y"] > self.end_game_zone["y"] + windowBoarder:
            up = False

        for tileName in self.tiles:
            self.tiles[tileName].rect.x += self.cam_velocity * left
            self.tiles[tileName].rect.x -= self.cam_velocity * right
            self.tiles[tileName].rect.y += self.cam_velocity * up
            self.tiles[tileName].rect.y -= self.cam_velocity * down

        self.cam_pos["x"] += self.cam_velocity * left
        self.cam_pos["x"] -= self.cam_velocity * right
        self.cam_pos["y"] += self.cam_velocity * up
        self.cam_pos["y"] -= self.cam_velocity * down

    def update_prod_value(self):

        for tileName in self.tiles:
            # Farm produce only if the city have money
            if self.tiles[tileName].type == "farm":
                if self.hud.po >= self.tiles[tileName].poProduction:
                    self.hud.po -= self.tiles[tileName].poProduction
                    self.hud.food += self.tiles[tileName].foodProduction

            # Market gain money only if food is available
            elif self.tiles[tileName].type == "market":
                if self.hud.food >= self.tiles[tileName].foodProduction:
                    self.hud.po += self.tiles[tileName].poProduction
                    self.hud.food -= self.tiles[tileName].foodProduction

