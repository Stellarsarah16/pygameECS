from settings import *

block_path = "res/sprite_maps/block_sheet.png"
block_atlas = {
    "grass" : {"type":"block", "size" : (TILESIZE, TILESIZE), "position": (0, 0)},
    "dirt" : {"type":"block", "size" : (TILESIZE, TILESIZE), "position": (0, 1)},
    "stone" : {"type":"block", "size" : (TILESIZE, TILESIZE), "position": (0, 2)},
    "mud" : {"type":"block", "size" : (TILESIZE, TILESIZE), "position": (2, 1)},
    "gravel" : {"type":"block", "size" : (TILESIZE, TILESIZE), "position": (0, 7)}
}

PLAYER_PATH = "res/sprite_maps/characters1.png"
PLAYER_ATLAS = {
    "idle": [
        {"type": "player", "size": (PLAYERSIZEX, PLAYERSIZEY), "position": (0, 0)}
    ],
    "walk": [
        {"type": "player", "size": (PLAYERSIZEX, PLAYERSIZEY), "position": (1 * PLAYERSIZEX, 0)},
        {"type": "player", "size": (PLAYERSIZEX, PLAYERSIZEY), "position": (2 * PLAYERSIZEX, 0)},
        {"type": "player", "size": (PLAYERSIZEX, PLAYERSIZEY), "position": (3 * PLAYERSIZEX, 0)},
    ]
}


solo_textures = {
    "idle" : {"type":"player", "file_path":"res/idle.png", "size": (PLAYERSIZEX, PLAYERSIZEY)}
}