# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-09-01


"""随机地图模板"""

from constant import EMapSize
from rmgtemplatezone import CRmgTemplateZone

class CRmgTemplate(object):
	"""随机地图模板"""
	m_Name = ""
	m_MinSize = None
	m_MaxSize = None

	m_Zones = None
	m_Connections = None

	def __init__(self):
		self.m_Zones = {}  # {ZoneId: CRmgTemplateZone}
		self.m_Connections = []  # [CRmgTemplateZoneConnection]

	def ParseData(self, dData):
		for sName, dInfo in dData.items():
			self.m_Name = str(sName)
			self.m_MinSize = self._parseMapSize(dInfo["minSize"])
			self.m_MaxSize = self._parseMapSize(dInfo["maxSize"])

			# 区域信息
			for nZoneId, dZoneInfo in dInfo["zones"].items():
				nZoneId = str(nZoneId)
				oZone = CRmgTemplateZone()
				oZone.ParseData(nZoneId, dZoneInfo)
				self.m_Zones[nZoneId] = oZone

			# 连通信息
			for dConnect in dInfo["connections"]:
				oConnect = CRmgTemplateZoneConnection()
				oConnect.ParseData(dConnect, self.m_Zones)
				self.m_Connections.append(oConnect)

			break

	def GetName(self):
		return self.m_Name

	def GetZones(self):
		return self.m_Zones

	def GetMinSize(self):
		return self.m_MinSize

	def GetMaxSize(self):
		return self.m_MaxSize

	def _parseMapSize(self, s):
		nSize = EMapSize.Map[s]
		oSize = CSize(nSize, nSize)
		return oSize


class CRmgTemplateZoneConnection(object):
	"""模板连通区域"""
	m_ZoneA = None
	m_ZoneB = None
	m_GuardStrength = 0  # 怪物强度

	def ParseData(self, dConnect, dZones):
		nZoneAId = str(dConnect["a"])
		nZoneBId = str(dConnect["b"])
		self.m_ZoneA = dZones[nZoneAId]
		self.m_ZoneB = dZones[nZoneBId]
		self.m_GuardStrength = dConnect["guard"]

	def GetZoneA(self):
		return self.m_ZoneA

	def GetZoneB(self):
		return self.m_ZoneB

	def GetGuardStrength(self):
		return self.m_GuardStrength


class CSize(object):
	"""地图大小"""
	m_Width = 0
	m_Height = 0

	def __init__(self, nWidth=0, nHeight=0):
		self.m_Width = nWidth
		self.m_Height = nHeight

	def __le__(self, size):
		"""小于等于"""
		return self.m_Width <= size.m_Width and self.m_Height <= size.m_Height

	def __ge__(self, size):
		"""大于等于"""
		return self.m_Width >= size.m_Width and self.m_Height >= size.m_Height

	def GetWidth(self):
		return self.m_Width

	def GetHeight(self):
		return self.m_Height

	def SetWidth(self, value):
		self.m_Width = value

	def SetHeight(self, value):
		self.m_Height = value

	def GetSize(self):
		return (self.m_Width, self.m_Height)