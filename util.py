# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-09-01

"""
辅助接口/函数
"""

def Matrix(row, col, val=0):
	"""
	Create a Matrix of row x col with value = val
	"""
	return [[val for _j in xrange(col)] for _i in xrange(row)]
