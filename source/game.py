import pygame
from HUD import HUD
from tile import Tile
from mousseIcon import MousseIcon
from envVar import *


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
                self.tiles[str(y * nb_tile_x + x)] = Tile(self.start_game_zone["x"] + x * tileSize,
                                                          self.start_game_zone["y"] + y * tileSize)
                print(str(int((y * nb_tile_x + x) / (nb_tile_x * nb_tile_y) * 100)) + "%")

        # HUD
        self.hud = HUD()

        # Mousse icon
        self.mousseIcon = MousseIcon()

    def move(self):

        right = pygame.mouse.get_pos()[0] > windowSize - windowBoarder
        left = pygame.mouse.get_pos()[0] < windowBoarder
        up = pygame.mouse.get_pos()[1] < windowBoarder
        down = pygame.mouse.get_pos()[1] > windowSize - windowBoarder - HUD_size

        if right and self.cam_pos["x"] < self.start_game_zone["x"] - windowBoarder:
            right = False
        if left and self.cam_pos["x"] > self.end_game_zone["x"] + windowBoarder:
            left = False

        if down and self.cam_pos["y"] < self.start_game_zone["y"] - HUD_size:
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
        # TODO: To optimized
        for tileName in self.tiles:
            # Farm produce only if the city have money
            if self.tiles[tileName].type == "farm":
                if self.hud.po >= self.tiles[tileName].poProduction["farm"]:
                    self.hud.po -= self.tiles[tileName].poProduction["farm"]
                    self.hud.food += self.tiles[tileName].foodProduction["farm"]

            # Market gain money only if food is available
            elif self.tiles[tileName].type == "market":
                if self.hud.food >= self.tiles[tileName].foodProduction["market"]:
                    self.hud.po += self.tiles[tileName].poProduction["market"]
                    self.hud.food -= self.tiles[tileName].foodProduction["market"]
