import pygame

GameName = 'GestionGame'

black = (128, 128, 128)
boarderSize = 1
tileSize = 25
windowBoarder = 20
windowSize = 400
maxFPS = 60  # TODO: Conf
nb_tile_x = 25  # TODO: Conf
nb_tile_y = 25  # TODO: Conf

HUD_size = 50
HUD_margin = 5
HUD_size_button = HUD_size - 3 * HUD_margin

Mousse_icon_size = 30

Info_text_size = 100

Nb_tick_day = 30000 / maxFPS

BGpath = "../asset/bg.jpg"

EmptyTile = "../asset/tile/empty.jpg"
FarmTile = "../asset/tile/farm.png"
MarketTile = "../asset/tile/market.png"

MousseFarm = "../asset/mousseIcon/farm.png"
MousseMarket = "../asset/mousseIcon/market.png"

ConstructionButton = "../asset/HUD/construction.png"
Gold_Icon = "../asset/HUD/gold.png"
Food_Icon = "../asset/HUD/food.png"

construct = {"farm", "market"}

# Load resource
resource = {
    "empty": pygame.image.load(EmptyTile),
    "farm": pygame.image.load(FarmTile),
    "market": pygame.image.load(MarketTile)
}

# Font
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', int((HUD_size - 2 * HUD_margin) / 2))

