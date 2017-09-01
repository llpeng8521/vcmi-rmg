# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-09-01

"""数据仓库"""

import os
import json

from rmgtemplate import CRmgTemplate

PJ = os.path.join

TEMPLATE_PATH = "template"


class CStorage(object):
	m_Templates = None  # 模板映射

	def __init__(self):
		self.m_Templates = {}  # {sName: CRmgTemplate}
		self.LoadTemplate()

	def LoadTemplate(self):
		"""加载模板数据，json文件"""
		for root, dirs, files in os.walk(TEMPLATE_PATH):
			for sFile in files:
				print sFile
				if sFile.endswith(".json") or sFile.endswith(".JSON"):
					print sFile, PJ(root, sFile)
					with open(PJ(root, sFile), "r") as f:
						data = json.load(f)
						oTempl = self.createTemplate(data)
						self.m_Templates[oTempl.GetName()] = oTempl

	def GetTemplates(self):
		return self.m_Templates.values()

	def createTemplate(self, dDate):
		pass


class CRmgTemplateStorage(CStorage):
	"""地图模板列表"""

	def createTemplate(self, dDate):
		oTempl = CRmgTemplate()
		oTempl.ParseData(dDate)
		return oTempl


class CObjectTemplateStorage(CStorage):
	"""物品模板列表"""

	def LoadTemplate(self):
		pass
