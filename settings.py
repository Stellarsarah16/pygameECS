import os, math, pygame, pathlib

os.environ['SDL_VIDEO_WINDOW_POS'] = '10,20'

game_events = {
    "ENEMY_DESTROYED_EVENT": pygame.USEREVENT + 10,
    "TAKE_DAMAGE_EVENT": pygame.USEREVENT + 20,
    "BULLET_HIT_EVENT": pygame.USEREVENT + 200
}

BASE_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent
font_dir: str = str(BASE_DIR.joinpath("Stellaria","res", "fonts"))

# screen setup
WIDTH = 1080
HEIGHT: float = WIDTH * (3/4)
CENTER_SCREEN = (WIDTH // 2, HEIGHT // 2)


print("Font Directory:", font_dir)
FONTS = {
    "font1" : font_dir +"\\font1.ttf", 
    "font2" : font_dir + "\\font2.ttf",
    "font3" : font_dir + "\\font3.ttf",
    "font4" : font_dir + "\\font4.ttf",
    "font5" : font_dir + "\\font5.ttf"
}

# game setup
FPS = 60
TILESIZE = 16
PLAYERSIZEX = 48
PLAYERSIZEY = 32
ITEM_OFFSET = 33
GRAVITY = 40
TERMINAL_VELOCITY = 10

# Define Player Settings
JUMP_POWER = 10
PLAYER_SPEED = 10

# Define Colors
COLORS = {
    "grass": (0, 255, 0),
    "ground": (200, 220, 60),
    "water": (80, 160, 255),
    "stone": (150, 150, 150),
    "dirt": (100, 50, 0),
    "sand": (255, 200, 100),
    "sky": (150, 200, 255), 
    "darksky": (100, 140, 200),
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "gray": (128, 128, 128),
    "green": (0, 255, 0),
    "blueblack": (0, 0, 20)
}