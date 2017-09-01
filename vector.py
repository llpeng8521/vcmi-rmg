# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-09-01

"""定义向量"""

import math

class Vec3(object):
	x = 0
	y = 0
	z = 0

	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		return "({0},{1},{2})".format(self.x, self.y, self.z)

	def __eq__(self, v):
		return self.x == v.x and self.y == v.y and self.z == v.z

	def __ne__(self, v):
		return self.x != v.x or self.y != v.y or self.z != v.z

	def __add__(self, v):
		if isinstance(v, Vec3):
			return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)
		else:
			return Vec3(self.x + v, self.y + v, self.z + v)

	def __sub__(self, v):
		if isinstance(v, Vec3):
			return Vec3(self.x - v.x, self.y - v.y, self.z - v.z)
		else:
			return Vec3(self.x - v, self.y - v, self.z - v)

	def __neg__(self):
		return Vec3(-self.x, -self.y, -self.z)

	def __mul__(self, v):
		if isinstance(v, Vec3):
			return Vec3(self.x * v.x, self.y * v.y, self.z * v.z)
		else:
			return Vec3(self.x * v, self.y * v, self.z * v)

	def __div__(self, v):
		if isinstance(v, Vec3):
			assert v.x != 0 and v.y != 0 and v.z != 0
			return Vec3(self.x / v.x, self.y / v.y, self.z / v.z)
		else:
			assert v != 0
			return Vec3(self.x / v, self.y / v, self.z / v)

	def __lt__(self, v):
		if self.z < v.z:
			return True
		if self.z > v.z:
			return False
		if self.y < v.y:
			return True
		if self.y > v.y:
			return False
		if self.x < v.x:
			return True
		if self.x > v.x:
			return False
		return False

	def dist2d(self, v):
		dx = self.x - v.x
		dy = self.y - v.y
		return dx * dx + dy * dy

	def dist2dSQ(self, v):
		return math.sqrt(self.dist2d(v))

	def areNeighbours(self, v):
		return self.dist2dSQ(v) < 4 and self.z == v.z


class Float3(Vec3):
	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)

	def mag(self):
		return math.sqrt(self.x * self.x + self.y * self.y)

	def unitVector(self):
		return Float3(self.x, self.y, self.z) / self.mag()


class Int3(Vec3):
	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.x = int(x)
		self.y = int(y)
		self.z = int(z)

	def mandist2d(self, v):
		return abs(self.x - v.x) + abs(self.y - v.y)
