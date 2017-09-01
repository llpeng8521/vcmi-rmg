# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-09-01

"""随机地图产生器"""

import sys
import random
import weakref
from util import Matrix
from rmgtemplate import CSize
from rmgtemplatezone import CTileInfo
from zoneplacer import CZonePlacer

class CRandomGenerator(object):
	def SetSeed(self, seed):
		random.seed(seed)

	def NextInt(self, lower=None, upper=None):
		if upper is None and lower is None:
			return random.randint(0, sys.maxint)
		if upper is None:
			return random.randint(0, lower) if lower else 0
		return random.randint(lower, upper)

	def NextDouble(self, lower=None, upper=None):
		if upper is None and lower is None:
			return random.uniform(0, sys.maxint)
		if upper is None:
			return random.uniform(0, lower) if lower else 0.0
		return random.uniform(lower, upper)

	def NextItem(self, container):
		return container[self.NextInt(len(container)-1)]

	def RandomShuffle(self, container):
		return random.shuffle(container)


class CMapGenOptions(object):
	m_Width = 0
	m_Height = 0
	m_MapTemplate = None  # 地图模板

	def __init__(self, oVcmi):
		self.m_Vcmi = weakref.ref(oVcmi)

	def InitMapTempl(self, oRandGen):
		lTemplate = self.m_Vcmi().GetMapTemplates()
		lAvailable = []
		for oTempl in lTemplate:
			oSize = CSize(self.m_Width, self.m_Height)
			if oSize >= oTempl.GetMinSize() and oSize <= oTempl.GetMaxSize():
				lAvailable.append(oTempl)

		if not lAvailable:
			raise "Map Template are all not available!"
		else:
			self.m_MapTemplate = oRandGen.NextItem(lAvailable)

	def GetMapTemplate(self):
		return self.m_MapTemplate

	def GetWidth(self):
		return self.m_Width

	def GetHeight(self):
		return self.m_Height

	def SetWidth(self, value):
		self.m_Width = value

	def SetHeight(self, value):
		self.m_Height = value


class CMapGenerator(object):
	m_MapGenOption = None  # 地图配置
	m_Map = None  # 地图对象

	m_RandGen = None  # 随机数据产生器
	m_RandomSeed = 0  # 随机种子

	m_Zones = None  # 区域连通
	m_Tiles = None

	m_ZoneColouring = None

	def __init__(self):
		self.m_RandGen = CRandomGenerator()
		self.m_Zones = {}
		self.m_Tiles = []

		import mapobject
		self.m_Map = mapobject.CMap()

	def Generate(self, oMapOption, randomSeed):
		self.m_RandomSeed = randomSeed
		self.m_RandGen.SetSeed(randomSeed)

		self.m_MapGenOption = oMapOption
		self.m_MapGenOption.InitMapTempl(self.m_RandGen)

		# 初始化地图数据
		self.m_Map.InitHeaderInfo(oMapOption)

		# 初始化格子信息
		self.InitTiles()

		# 产生地图区域
		self.GenZones()

	def InitTiles(self):
		"""初始化格子"""
		self.m_Map.InitTerrain()
		nWidth = self.m_Map.GetWidth()
		nHeight = self.m_Map.GetHeight()
		self.m_Tiles = Matrix(nWidth, nHeight, None)
		for i in xrange(nWidth):
			for j in xrange(nHeight):
				self.m_Tiles[i][j] = CTileInfo()

		self.m_ZoneColouring = Matrix(nWidth, nHeight, None)

	def GenZones(self):
		"""产生地图区域"""
		oTmpl = self.m_MapGenOption.GetMapTemplate()
		self.m_Zones = oTmpl.GetZones()

		oZonePlacer = CZonePlacer(self)
		# oZonePlacer.PlaceZones(self.m_MapGenOption, self.m_RandGen)
		# oZonePlacer.AssignZones(self.m_MapGenOption)
		print "Zones generated successfully"


	# ==========================================
	# 地图数据处理
	# ==========================================
	def checkIsOnMap(self, tile):
		if not self.m_Map.IsInTheMap(tile):
			raise "Tile %s is outside the map" % str(tile)

	def SetZoneID(self, tile, zoneId):
		self.checkIsOnMap(tile)
		self.m_ZoneColouring[tile.x][tile.y] = zoneId
