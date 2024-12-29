import pygame, pickle
from enum import Enum
import game_data
from item import Item
from managers import EntityManager

WORLD_SIZE_X = 0
WORLD_SIZE_Y = 0

world = None

terrain_surface = pygame.Surface((0, 0))
border_down = 0
border_up = 0
border_left = 0
border_right = 0

biome_border_x_1 = 0
biome_border_x_2 = 0

WORLD_NAME = ""

grass_grow_delay = 2.5
grass_grow_tick = grass_grow_delay

structure_rects = []


class WorldSize(Enum):
    TINY = 0
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class WorldType(Enum):
    PASSIVE = 0
    NORMAL = 1
    EXPERT = 2


class WorldGenType(Enum):
    DEFAULT = 0
    SUPERFLAT = 1
    ICE_CAVES = 2


class MaskType(Enum):
    TOP_MID = 0
    LEFT_MID = 1
    BOT_MID = 2
    RIGHT_MID = 3
    SINGLE_VERTICAL_MID = 4
    SINGLE_HORIZONTAL_MID = 5
    SINGLE_VERTICAL_TOP = 6
    SINGLE_VERTICAL_BOT = 7
    SINGLE_HORIZONTAL_LEFT = 8
    SINGLE_HORIZONTAL_RIGHT = 9
    SINGLE = 10
    CORNER_TOP_LEFT = 11
    CORNER_TOP_RIGHT = 12
    CORNER_BOT_LEFT = 13
    CORNER_BOT_RIGHT = 14
    MIDDLE = 15


class World:
    def __init__(self):
        self.name = ""
        self.creation_date = None
        self.last_played_date = None
        self.size = WorldSize.TINY
        self.type = WorldType.NORMAL
        self.gen_type = WorldGenType.DEFAULT
        self.state_flags = {}
        self.play_time = 0
        self.spawn_position = (0, 0)
        self.chest_data = []
        self.tile_data = []
        self.tile_mask_data = []

    def get_creation_date_string(self):
        return str(str(self.creation_date)[:19])

    def get_last_played_date_string(self):
        return str(str(self.last_played_date)[:19])
    
    def save(self):
        # Save chest data using a better format
        formatted_chest_data = [[] for _ in range(len(self.chest_data))]
        for chest_data_index in range(len(self.chest_data)):
            chest_data_at_index = self.chest_data[chest_data_index]
            formatted_chest_data[chest_data_index] = [chest_data_at_index[0], []]
            for chest_item_index in range(len(chest_data_at_index[1])):
                item = chest_data_at_index[1][chest_item_index]
                if item is not None:
                    if item.prefix_data is None:
                        formatted_chest_data[chest_data_index][1].append([chest_item_index, item.get_id_str(), item.amnt, None])
                    else:
                        formatted_chest_data[chest_data_index][1].append([chest_item_index, item.get_id_str(), item.amnt, item.get_prefix_name()])

        save_map = {
            "name": self.name,
            "creation_date": self.creation_date,
            "last_played_date": self.last_played_date,
            "size": self.size,
            "type": self.type,
            "gen_type": self.gen_type,
            "state_flags": self.state_flags,
            "play_time": self.play_time,
            "spawn_position": self.spawn_position,
            "chest_data": formatted_chest_data,
            "tile_id_str_lookup": game_data.get_current_tile_id_str_lookup(),
            "wall_id_str_lookup": game_data.get_current_wall_id_str_lookup(),
        }

        pickle.dump(save_map, open("res/worlds/" + str(self.name) + ".dat", "wb"))  # save dat
        pickle.dump(self.tile_data, open("res/worlds/" + str(self.name) + ".wrld", "wb"))  # save wrld
    
    def load(self, world_name, load_all=True):
        save_map = pickle.load(open("res/worlds/" + world_name + ".dat", "rb"))  # open selected save dat file

        self.name = save_map["name"]
        self.creation_date = save_map["creation_date"]
        self.size = save_map["size"]
        self.gen_type = save_map["gen_type"]
        self.play_time = save_map["play_time"]
        self.spawn_position = save_map["spawn_position"]
        formatted_chest_data = save_map["chest_data"]

        if load_all:
            self.chest_data = [[(0, 0), [None for _ in range(20)]] for _ in range(len(formatted_chest_data))]

            for chest_data_index in range(len(formatted_chest_data)):
                formatted_chest_data_at_index = formatted_chest_data[chest_data_index]
                self.chest_data[chest_data_index][0] = formatted_chest_data_at_index[0]
                for item_data_index in range(len(formatted_chest_data_at_index[1])):
                    loaded_item_data = formatted_chest_data_at_index[1][item_data_index]
                    item = Item(game_data.get_item_id_by_id_str(loaded_item_data[1]), loaded_item_data[2])
                    item.assign_prefix(loaded_item_data[3])
                    self.chest_data[chest_data_index][1][loaded_item_data[0]] = item

            # Open selected save wrld file
            self.tile_data = pickle.load(open("res/worlds/" + world_name + ".wrld", "rb"))

            # And replace the tile and wall values with updated ones
            tile_id_str_lookup = save_map["tile_id_str_lookup"]
            wall_id_str_lookup = save_map["wall_id_str_lookup"]

            for tile_column_index in range(len(self.tile_data)):
                for tile_row_index in range(len(self.tile_data[tile_column_index])):
                    existing_tile_id_str = tile_id_str_lookup[self.tile_data[tile_column_index][tile_row_index][0]]
                    self.tile_data[tile_column_index][tile_row_index][0] = game_data.get_tile_id_by_id_str(existing_tile_id_str)

                    existing_wall_id_str = wall_id_str_lookup[self.tile_data[tile_column_index][tile_row_index][1]]
                    self.tile_data[tile_column_index][tile_row_index][1] = game_data.get_wall_id_by_id_str(existing_wall_id_str)
