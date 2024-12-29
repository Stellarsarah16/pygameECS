
import pygame
from collections import OrderedDict
from enum import Enum
from settings import *
import random

class ItemTag(Enum):
    TILE = 0
    WALL = 1
    MATERIAL = 2
    WEAPON = 3
    TOOL = 4
    MELEE = 5
    RANGED = 6
    MAGICAL = 7
    AMMO = 8
    PICKAXE = 9
    AXE = 10
    HAMMER = 11
    GRAPPLE = 12
    COIN = 13

class ItemPrefixGroup(Enum):
    UNIVERSAL = 0
    COMMON = 1
    MELEE = 2
    RANGED = 3
    MAGICAL = 4

class TileTag(Enum):
    TRANSPARENT = 0
    NODRAW = 1
    NOCOLLIDE = 2
    MULTITILE = 3
    CYCLABLE = 4
    CHEST = 5
    BREAKABLE = 6
    CRAFTINGTABLE = 7
    PLATFORM = 8
    DAMAGING = 9

class TileStrengthType(Enum):
    PICKAXE = 0
    HAMMER = 1
    AXE = 2
    DAMAGE = 3


class TileMaskType(Enum):
    NONE = 0
    NOISY = 1


def make_item_tag_list(item_tags_str):
    str_list = item_tags_str.split(",")
    enum_list = []
    for string in str_list:
        for tag in ItemTag:
            if tag.name.lower() == string:
                enum_list.append(tag)
                break
    return enum_list

def make_item_prefix_list(item_prefixes_str):
    str_list = item_prefixes_str.split(",")
    enum_list = []
    for string in str_list:
        for prefix in ItemPrefixGroup:
            if prefix.name.lower() == string:
                enum_list.append(prefix)
                break
    return enum_list


def make_tile_tag_list(tile_tags_str):
    str_list = tile_tags_str.split(",")
    enum_list = []
    for string in str_list:
        for tag in TileTag:
            if tag.name.lower() == string:
                enum_list.append(tag)
                break
    return enum_list