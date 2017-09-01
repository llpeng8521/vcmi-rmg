# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-09-01

from mapgenerator import CMapGenOptions
from mapgenerator import CMapGenerator
from storage import CRmgTemplateStorage
from storage import CObjectTemplateStorage

g_Vcmi = None


class CVCMI(object):
	def __init__(self):
		self.m_MapTemplateStorage = CRmgTemplateStorage()
		self.m_ObjTemplateStorage = CObjectTemplateStorage()

	def GetMapTemplates(self):
		return self.m_MapTemplateStorage.GetTemplates()

	def GetObjTemplates(self):
		return self.m_ObjTemplateStorage.GetTemplates()


def main():
	global g_Vcmi
	g_Vcmi = CVCMI()

	MAP_SIZE_SMALL = 36
	MAP_SIZE_MIDDLE = 72
	MAP_SIZE_LARGE = 108
	MAP_SIZE_XLARGE = 144

	TEST_RANDOM_SEED = 1337

	oMapOption = CMapGenOptions(g_Vcmi)
	oMapOption.SetWidth(MAP_SIZE_MIDDLE)
	oMapOption.SetHeight(MAP_SIZE_MIDDLE)

	oMapGen = CMapGenerator()
	oMap = oMapGen.Generate(oMapOption, TEST_RANDOM_SEED)


if __name__ == '__main__':
	main()
