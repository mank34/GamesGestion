import pygame

# Name
GameName = 'City Game'

# Windows configuration
windowBoarder = 50

# Game configuration
FPS_available = [25, 30, 45, 60, 75]
resolution_available = ["720x480", "1280x720", "1920x1080", "Full screen"]

nb_tile_x = 1
nb_tile_y = 1

default_res = dict(po=500,
                   food=0,
                   wood=10)

# Tile configuration
tileSize_x = 127
tileSize_base = 64
tileSize_y = dict(empty=63,
                  farm=79)

citizen_size_x = 12
citizen_size_y = 24

# HUD configuration
HUD_size = 50
HUD_margin = 5
HUD_size_button = HUD_size - 3 * HUD_margin
Info_text_size = 100

# Mousse configuration
Mousse_icon_size = 30

# HUD
ConstructionButton = "../asset/HUD/construction.png"
Gold_Icon = "../asset/HUD/gold.png"
Food_Icon = "../asset/HUD/food.png"
Wood_Icon = "../asset/HUD/wood.png"

HUD_main_menu = ["hud_construct"]

HUD_resource = ["hud_res_po", "hud_res_food", "hud_res_wood"]

HUD_construct_menu = ["hud_construct_farm", "hud_construct_market"]

# Background
BGpath = "../asset/bg.jpg"

# Empty
EmptyTile = "../asset/tile/empty.png"

# Farm
FarmTile = "../asset/tile/farm.png"
MousseFarm = "../asset/mousseIcon/farm.png"

# Market
MarketTile = "../asset/tile/market.png"
MousseMarket = "../asset/mousseIcon/market.png"

# Load resource
resource = dict(empty=pygame.image.load(EmptyTile),
                farm=pygame.image.load(FarmTile),
                market=pygame.image.load(MarketTile),
                hud_construct=pygame.image.load(ConstructionButton),
                hud_construct_farm=pygame.image.load(MousseFarm),
                hud_construct_market=pygame.image.load(MousseMarket),
                hud_res_po=pygame.image.load(Gold_Icon),
                hud_res_food=pygame.image.load(Food_Icon),
                hud_res_wood=pygame.image.load(Wood_Icon))

# Production
po_production = dict(farm=0,
                     empty=0,
                     market=5)

food_production = dict(empty=0,
                       farm=5,
                       market=0)

wood_production = dict(empty=0,
                       farm=0,
                       market=0)

# Cost
po_cost = dict(empty=0,
               farm=5,
               market=0)

food_cost = dict(empty=0,
                 farm=0,
                 market=5)

wood_cost = dict(empty=0,
                 farm=0,
                 market=0)

day_duration = 30000

# Construction time
construction_time = dict(empty=day_duration*0,
                         farm=day_duration * 3,
                         market=day_duration * 3)

# Font
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', int((HUD_size - 2 * HUD_margin) / 2))
GameNameFont = pygame.font.SysFont('Comic Sans MS', 50)
GameMenuFont = pygame.font.SysFont('Comic Sans MS', 25)
GameInfoFont = pygame.font.SysFont('Comic Sans MS', 20)
GameCommentFont = pygame.font.SysFont('Comic Sans MS', 15)

# Debug
showFPS = False
showLoading = False
