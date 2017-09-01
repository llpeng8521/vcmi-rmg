# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-09-01

"""模板区域"""

from constant import ETileType
from constant import ETerrainType
from constant import ERoadType


class CTileInfo(object):
	"""格子(瓦片)信息"""
	m_NearestObjectDistance = 0

	m_TileType = None
	m_Terrain = None
	m_RoadType = None

	def __init__(self):
		self.m_TileType = ETileType.POSSIBLE
		self.m_Terrain = ETerrainType.WRONG
		self.m_RoadType = ERoadType.NO_ROAD

	def GetNearestObjectDistance(self):
		return self.m_NearestObjectDistance

	def SetNearestObjectDistance(self, value):
		self.m_NearestObjectDistance = value

	def ShouldBeBlocked(self):
		return self.m_TileType == ETileType.BLOCKED

	def IsBlocked(self):
		return self.m_TileType in (ETileType.BLOCKED, ETileType.USED)

	def IsPossible(self):
		return self.m_TileType == ETileType.POSSIBLE

	def IsFree(self):
		return self.m_TileType == ETileType.FREE

	def IsUsed(self):
		return self.m_TileType == ETileType.USED

	def IsRoad(self):
		return self.m_RoadType != ERoadType.NO_ROAD

	def SetOccupied(self, nType):
		self.m_TileType = nType

	def SetTileTyp(self, nType):
		self.m_TileType = nType

	def GetTileType(self):
		return self.m_TileType

	def SetTerrainType(self, nType):
		self.m_Terrain = nType

	def GetTerrainType(self):
		return self.m_Terrain

	def SetRoadType(self, nType):
		self.m_RoadType = nType


class CTreasureInfo(object):
	"""宝物信息"""
	m_Min = 0
	m_Max = 0
	m_Density = 0


class CObjectInfo(object):
	"""物品信息"""
	m_Templ = None  # 物品模板
	m_Value = 0  # 物品价值
	m_Probability = 0  # 物品产生的概率
	m_MaxPerZone = 0  # 物品在一个区域的最大数量

	m_GenerateObject = None  # 产生物品的函数


class CTreasurePileInfo(object):
	"""宝物堆"""
	m_VisitableFromBottomPositions = set()
	m_VisitableFromTopPositions = set()
	m_BlockedPositions = set()
	m_OccupiedPositions = set()

	m_NextTreasurePos = ()


class CTownInfo(object):
	m_TownCount = 0
	m_CastleCount = 0
	m_TownDensity = 0
	m_CastleDensity = 0


class CRmgTemplateZone(object):
	"""地图区域"""
	m_Id = 0
	m_Type = 0
	m_Size = 0  # 区域大小
	m_Owner = 0

	# 城镇信息
	m_PlayerTowns = None
	m_NeutralTowns = None
	m_bTownsAreSameType = False
	m_TownTypes = set()
	m_MonsterTypes = set()
	m_bMatchTerrainToTown = True
	m_TerrainTypes = set()
	m_Mines = {}

	m_TownType = 0
	m_TerrainType = 0
	m_QuestArtZone = None

	# 物品信息
	m_TerrainInfo = []
	m_possibleObjects = []

	m_RequiredObjects = []
	m_CloseObjects = []

	# 地图信息
	m_Pos = None
	m_Center = None
	m_TileInfo = None
	m_PossibleTiles = None
	m_FreePaths = None
	m_Connections = None

	m_RoadNodes = None
	m_Roads = None
	m_TilesToConnectLater = None

	def __init__(self):
		self.m_TerrainTypes = []

	# ==========================================
	# 解析逻辑
	# ==========================================
	def ParseData(self, nZoneId, dZoneInfo):
		self.m_Id = nZoneId
		self.m_Type = str(dZoneInfo["type"])
		self.m_Size = dZoneInfo["size"]

		self.m_PlayerTowns = self._parseTemplateZoneTowns(dZoneInfo.get("playerTowns", {}))
		self.m_NeutralTowns = self._parseTemplateZoneTowns(dZoneInfo.get("neutralTowns", {}))

		defaultTerTypes = ETerrainType.Default
		self.m_TerrainTypes = self._parseTerrainType(dZoneInfo.get("terrainTypes", []), defaultTerTypes)

	def _parseTemplateZoneTowns(self, dDate):
		oTown = CTownInfo()
		oTown.m_TownCount = dDate.get("towns", 0)
		oTown.m_CastleCount = dDate.get("castles", 0)
		oTown.m_TownDensity = dDate.get("townDensity", 0)
		oTown.m_CastleDensity = dDate.get("castleDensity", 0)
		return oTown

	def _parseTerrainType(self, lTerTypeStrings, defaultTerTypes):
		if not lTerTypeStrings:
			return defaultTerTypes
		setTerTypes = set()
		for sTer in lTerTypeStrings:
			if sTer == "all":
				return defaultTerTypes
			setTerTypes.add(ETerrainType.Map[sTer])
		return setTerTypes
