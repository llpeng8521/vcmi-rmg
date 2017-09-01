# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-09-01

"""区域划分"""

import math

from vector import Int3
from vector import Float3

MAX_ITERATIONS = 100
CREATE_FULL_UNDERGROUND = True

class CZonePlacer(object):
	"""处理区域划分逻辑"""
	m_Width = 0
	m_Height = 0
	m_ScaleX = 0
	m_ScaleY = 0
	m_MapSize = 0

	m_GravityConstant = 0
	m_StiffnessConstant = 0

	m_MapGen = None

	def __init__(self, oMapGen):
		self.m_MapGen = oMapGen

	def PlaceZones(self, oMapOption, oRandGen):
		print "Starting zone placement"
		self.m_Width = oMapOption.GetWidth()
		self.m_Height = oMapOption.GetHeight()

		zones = self.m_MapGen.GetZones()

		# gravity-based algorithm
		# let's assume we try to fit N circular zones with radius = size on a map

		self.m_GravityConstant = 4e-3
		self.m_StiffnessConstant = 4e-3

		zonesVector = zones.values()
		zonesVector = oRandGen.RandomShuffle(zonesVector)

		# 0. set zone sizes and surface / underground level
		self.prepareZones(zones, zonesVector, oRandGen)

		# gravity-based algorithm. connected zones attract, intersceting zones and map boundaries push back

		# remember best solution
		bestTotalDistance = 1e10
		bestTotalOverlap = 1e10

		bestSolution = {}  # {CRmgTemplateZone: float3}
		forces = {}  # {CRmgTemplateZone: float3}
		totalForces = {}  # {CRmgTemplateZone: float3}
		distances = {}  # {CRmgTemplateZone: float}
		overlaps = {}  # {CRmgTemplateZone: float}

		for i in xrange(100):
			# 1. attract connected zones
			self.attractConnectedZones(zones, forces, distances)
			for zone, distance in forces.items():
				zone.SetCenter(zone.GetCenter() + distance)
				totalForces[zone] = distance

			# 2. separate overlapping zones
			self.separateOverlappingZones(zones, forces, overlaps)
			for zone, distance in forces.items():
				zone.SetCenter(zone.GetCenter() + distance)
				totalForces[zone] = distance

			# 3. now perform drastic movement of zone that is completely not linked
			self.moveOneZone(zones, totalForces, distances, overlaps)

			# 4. NOW after everything was moved, re-evaluate zone positions
			self.attractConnectedZones(zones, forces, distances)
			self.separateOverlappingZones(zones, forces, overlaps)

			totalDistance = sum(distances.values())
			totalOverlap = sum(overlaps.values())

			# check fitness function
			improvement = False
			if bestTotalDistance > 0 and bestTotalOverlap > 0:
				# multiplication is better for auto-scaling, but stops working if one factor is 0
				if totalDistance * totalOverlap < bestTotalDistance * bestTotalOverlap:
					improvement = True
			else:
				if totalDistance + totalOverlap < bestTotalDistance + bestTotalOverlap:
					improvement = True

			print "Total distance between zones after this iteration: %2.4f, Total overlap: %2.4f, Improved: %s" % \
				(totalDistance, totalOverlap, improvement)

			# save best solution
			if improvement:
				bestTotalDistance = totalDistance
				bestTotalOverlap = totalOverlap
				for zone in zones.values():
					bestSolution[zone] = zone.GetCenter()

		print "Best fitness reached: total distance %2.4f, total overlap %2.4f" % (bestTotalDistance, bestTotalOverlap)
		for zone in zone.values():
			zone.SetPos(self.cords(bestSolution[zone]))

	def prepareZones(self, zones, zonesVector, oRandGen):
		# make sure that sum of zone sizes on surface match size of the map
		totalSize = 0

		radius = 0.4
		pi2 = 6.28

		zonesToPlace = []
		for zone in zonesVector:
			totalSize += zone.GetSize() * zone.GetSize()
			randomAngle = oRandGen.NextDouble(0, pi2)
			# place zones around circle
			x = 0.5 + radius * math.sin(randomAngle)
			y = 0.5 + radius * math.cos(randomAngle)
			zone.SetCenter(Float3(x, y, 0))

		"""
		prescale zones
		formula: sum((prescaler*n)^2)*pi = WH
		prescaler = sqrt((WH)/(sum(n^2)*pi))
		"""
		self.m_MapSize = math.sqrt(self.m_Width * self.m_Height)
		prescaler = self.m_MapSize / (totalSize * 3.14)
		for zone in zones.values():
			zone.SetSize(zone.GetSize() * prescaler)

	def attractConnectedZones(self, zones, forces, distances):
		for zone in zones.values():
			forceVector = Float3()
			pos = zone.GetCenter()

			totalDistance = 0

			for otherZone in zone.GetConnections():
				otherZoneCenter = otherZone.GetCenter()
				distance = pos.dist2d(otherZoneCenter)
				minDistance = 0

				if pos.z != otherZoneCenter.z:
					minDistance = 0
				else:
					minDistance = (zone.GetSize() + otherZone.GetSize()) / self.m_MapSize

				if distance > minDistance:
					if pos.z != otherZoneCenter.z:
						overlapMultiplier = 1.0
					else:
						overlapMultiplier = minDistance / distance
					forceVector += (((otherZoneCenter - pos)* overlapMultiplier / self.GetDistance(distance))) * self.m_GravityConstant
					totalDistance += (distance - minDistance)

			distances[zone] = totalDistance
			forceVector.z = 0
			forces[zone] = forceVector

	def separateOverlappingZones(self, zones, forces, overlaps):
		for zone in zones.values():
			forceVector = Float3()
			pos = zone.GetCenter()

			overlap = 0
			for otherZone in zones.values():
				otherZoneCenter = otherZone.GetCenter()

				if zone == otherZone or pos.z != otherZoneCenter.z:
					continue
				distance = pos.dist2d(otherZoneCenter)
				minDistance = (zone.GetSize() + otherZone.GetSize()) / self.m_MapSize
				if distance < minDistance:
					distance = distance if distance else 1e-3
					forceVector -= (((otherZoneCenter - pos) * (minDistance / distance)) / self.GetDistance(distance)) * self.m_StiffnessConstant
					# overlapping of small zones hurts us more
					overlap += (minDistance - distance)

			# move zones away from boundaries
			# do not scale boundary distance - zones tend to get squashed
			size = zone.GetSize() / self.m_MapSize
			if pos.x < size:
				overlap, forceVector = self.pushAwayFromBoundary(0, pos.y, pos, size, overlap, forceVector)
			if pos.x > 1 - size:
				overlap, forceVector = self.pushAwayFromBoundary(1, pos.y, pos, size, overlap, forceVector)
			if pos.y < size:
				overlap, forceVector = self.pushAwayFromBoundary(pos.x, 0, pos, size, overlap, forceVector)
			if pos.y > 1 - size:
				overlap, forceVector = self.pushAwayFromBoundary(pos.x, 1, pos, size, overlap, forceVector)
			overlaps[zone] = overlap
			forceVector.z = 0
			forces[zone] = forceVector

	def pushAwayFromBoundary(self, x, y, pos, size, overlap, forceVector):
		boundary = Float3(x, y, pos.z);
		distance = pos.dist2d(boundary);
		# check if we're closer to map boundary than value of zone size
		overlap = overlap + max(0, distance - size)
		forceVector = forceVector - (boundary - pos) * (size - distance) / self.GetDistance(distance) * self.m_StiffnessConstant
		return overlap, forceVector

	def moveOneZone(self, zones, totalForces, distances, overlaps):
		maxRatio = 0
		# experimental - the more zones, the greater total distance expected
		maxDistanceMovementRatio = len(zones) * len(zones)
		misplacedZone = None

		totalDistance = sum(distances.values())
		totalOverlap = sum(overlaps.values())

		# find most misplaced zone
		for zone in zones.values():
			distance = distances[zone]
			overlap = overlaps[zone]

			# if distance to actual movement is long, the zone is misplaced
			ratio = (distance + overlap) / totalForces[zone].mag()
			if ratio > maxRatio:
				maxRatio = ratio
				misplacedZone = zone
		print "Worst misplacement/movement ratio: %3.2f" % maxRatio

		if maxRatio < maxDistanceMovementRatio or not misplacedZone:
			return

		targetZone = None
		ourCenter = misplacedZone.GetCenter()
		ourSize = misplacedZone.GetSize()
		if totalDistance > totalOverlap:
			# find most distant zone that should be attracted and move inside it
			maxDistance = 0
			for otherZone in misplacedZone.GetConnections():
				distance = otherZone.GetCenter().dist2dSQ(ourCenter)
				if distance > maxDistance:
					maxDistance = distance
					targetZone = otherZone
			if targetZone:
				center = targetZone.GetCenter()
				size = targetZone.GetSize()
				vec = center - ourCenter
				newDistanceBetweenZones = max(ourSize, size) / self.m_MapSize
				print "Trying to move zone %d %s towards %d %s. Old distance %f" % \
						(misplacedZone.GetId(), str(ourCenter), targetZone.getId(), str(center), maxDistance)
				print "direction is %s" % str(vec)

				misplacedZone.SetCenter(center - vec.unitVector() * newDistanceBetweenZones)
				print "New distance %f" % center.dist2d(misplacedZone.GetCenter())
		else:
			maxOverlap = 0
			for otherZone in zones.values():
				otherZoneCenter = otherZone.GetCenter()
				if otherZone.second == misplacedZone or otherZoneCenter.z != ourCenter.z:
					continue
				distance = otherZoneCenter.dist2dSQ(ourCenter)
				if distance > maxOverlap:
					maxOverlap = distance
					targetZone = otherZone

			if targetZone:
				center = targetZone.GetCenter()
				size = targetZone.GetSize()
				newDistanceBetweenZones = (ourSize + size) / self.m_MapSize
				print "Trying to move zone %d %s towards %d %s. Old distance %f" % \
						(misplacedZone.GetId(), str(ourCenter), targetZone.getId(), str(center), maxOverlap)
				print "direction is %s", str(center - ourCenter)

				misplacedZone.SetCenter(center + vec.unitVector() * newDistanceBetweenZones)
				print "New distance %f" % center.dist2d(misplacedZone.GetCenter())

	def cords(self, float3):
		return Int3(max(0, (float3.x * self.m_Width)-1), max(0, (float3.y * self.m_Height-1)), float3.z)

	def GetDistance(self, distance):
		return distance * distance if distance else 1e-6

	def AssignZones(self, oMapOption):
		print "Starting zone colouring"
		width = oMapOption.GetWidth()
		height = oMapOption.GetHeight()

		# scale to Medium map to ensure smooth results
		self.m_ScaleX = 72.0 / width
		self.m_ScaleY = 72.0 / height

		zones = self.m_MapGen.GetZones()
		distances = []  # [(CRmgTemplateZone, float),]

		"""
		1. Create Voronoi diagram
		2. find current center of mass for each zone. Move zone to that center to balance zones sizes
		"""
		for i in xrange(width):
			for j in xrange(height):
				distances = []
				pos = Int3(i, j, 0)
				for zone in zones.values():
					distances.append((zone, pos.dist2dSQ(zone.GetPos())))
				closestZone = self.getClosestTile(distances)
				closestZone.AddTile(pos)

		for zone in zones.values():
			self.moveZoneToCenterOfMass(zone)

		# assign actual tiles to each zone using nonlinear norm for fine edges
		for zone in zones.values():
			zone.ClearTiles() # now populate them again

		for i in xrange(width):
			for j in xrange(height):
				distances = []
				pos = Int3(i, j, 0)
				for zone in zones.values():
					distances.append((zone, self.metric(pos, zone.GetPos())))
				closestZone = self.getClosestTile(distances)
				closestZone.AddTile(pos)
				self.m_MapGen.SetZoneID(pos, zone.GetId())

		# set position (town position) to center of mass of irregular zone
		for zone in zones.values():
			self.moveZoneToCenterOfMass(zone)

		print "Finished zone colouring"

	def getClosestTile(self, distances):
		distanceBySize = []
		for zone, distance in distances:
			distanceBySize.append(distance / zone.GetSize())
		minDistance = min(distanceBySize)
		index = distanceBySize.index(minDistance)
		return distances[index][0]

	def compareByDistance(self, lhs, rhs):
		return lhs[1] / lhs[0].GetSize() < rhs[1] / rhs[0].GetSize()

	def moveZoneToCenterOfMass(self, zone):
		total = Int3()
		tiles = zone.GetTileInfo()
		for tile in tiles:
			total += tile
		size = len(tiles)
		zone.SetPos(Int3(total.x / size, total.y / size, total.z / size))

	def metric(self, int3A, int3B):
		"""
		Matlab code
		dx = abs(A(1) - B(1)); %distance must be symmetric
		dy = abs(A(2) - B(2));
		d = 0.01 * dx^3 - 0.1618 * dx^2 + 1 * dx + ...
			0.01618 * dy^3 + 0.1 * dy^2 + 0.168 * dy;
		"""
		dx = abs(int3A.x - int3B.x) * self.m_ScaleX
		dy = abs(int3A.y - int3B.y) * self.m_ScaleY
		return dx * (1 + dx * (0.1 + dx * 0.01)) + \
			dy * (1.618 + dy * (-0.1618 + dy * 0.01618))
