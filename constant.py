# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-09-01

"""常量枚举"""

class EMapSize:
	MAP_SIZE_SMALL = 36
	MAP_SIZE_MIDDLE = 72
	MAP_SIZE_LARGE = 108
	MAP_SIZE_XLARGE = 144

	Map = {
		"s": MAP_SIZE_SMALL,
		"m": MAP_SIZE_MIDDLE,
		"x": MAP_SIZE_LARGE,
		"xl": MAP_SIZE_XLARGE,
	}


class ETileType:
	FREE = 0
	POSSIBLE = 1
	BLOCKED = 2
	USED = 3


class ETerrainType:
	WRONG = -2
	BORDER = -1
	DIRT = 0
	SAND = 1
	GRASS = 2
	SNOW = 3
	SWAMP = 4
	ROUGH = 5
	SUBTERRANEAN = 6
	LAVA = 7
	WATER = 8
	ROCK = 9

	All = set([DIRT, SAND, GRASS, SNOW, SWAMP, ROUGH, SUBTERRANEAN, LAVA, WATER, ROCK])
	Default = set([DIRT, SAND, GRASS, SNOW, SWAMP, ROUGH, SUBTERRANEAN, LAVA])
	Map = {
		"dirt": DIRT,
		"sand": SAND,
		"grass": GRASS,
		"snow": SNOW,
		"swamp": ROUGH,
		"rough": ROUGH,
		"subterra": SUBTERRANEAN,
		"lava": LAVA,
		"water": WATER,
		"rock": ROCK,
	}


class ERoadType:
	NO_ROAD = 0
	DIRT_ROAD = 1
	GRAVEL_ROAD = 2
	COBBLESTONE_ROAD = 3


class ERiverType:
	NO_RIVER = 0
	CLEAR_RIVER = 1
	ICY_RIVER = 2
	MUDDY_RIVER = 3
	LAVA_RIVER = 4


class ETemplateZoneType:
	PLAYER_START = 0
	CPU_START = 1
	TREASURE = 2
	JUNCTION = 3