# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-09-01

"""地图对象"""

from constant import ERoadType
from constant import ERiverType
from constant import ETerrainType
from util import Matrix

class CTerrainTile(object):
	"""地图格子的地形"""
	m_TerType = ETerrainType.BORDER
	m_TerView = None
	m_RiverType = ERiverType.NO_RIVER
	m_RiverView = None
	m_RoadType = ERoadType.NO_ROAD
	m_RoadView = None

	m_bVisitable = False
	m_bBlocked = False

class CMapHeader(object):
	m_Width = 72
	m_Height = 72
	m_Name = ""
	m_Description = ""
	m_Difficulty = 1
	m_LevelLimit = 0
	m_TriggeredEvents = None

	def InitHeaderInfo(self, oMapOption):
		self.m_Height = oMapOption.GetHeight()
		self.m_Width = oMapOption.GetWidth()

	def GetWidth(self):
		return self.m_Width

	def GetHeight(self):
		return self.m_Height


class CMap(CMapHeader):
	"""地图对象"""
	m_Objects = None
	m_Towns = None
	m_Terrain = None

	def __init__(self):
		super(CMap, self).__init__()
		self.m_Objects = []
		self.m_Towns = []
		self.m_Terrain = []

	def InitTerrain(self):
		"""初始化地形格子"""
		self.m_Terrain = Matrix(self.m_Width, self.m_Height, None)
		for i in xrange(self.m_Width):
			for j in xrange(self.m_Height):
				self.m_Terrain[i][j] = CTerrainTile()

	def IsInTheMap(self, pos):
		return pos.x < 0 or pos.y < 0 or pos.z < 0 or \
			pos.x > self.m_Width or pos.y > self.m_Height or pos.z != 0
