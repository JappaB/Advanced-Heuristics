""" 

BatteryClass for smartgrid case, not submitted for grading
Stijn Verdenius, Jasper Bakker 2017

"""



import random

allBatteries = False

class battery(object):

	def __init__(self, batteryNumber, capacity, housingList, overCapacitated, position = [0,0]):
		self.position = position
		self.batteryNumber = batteryNumber
		self.capacityLeft = capacity
		#self.batteryType = batteryType
		self.capacity = capacity
		self.overCapacitated = overCapacitated #boolean
		self.assignedHouses = {}
		self.color = "#%06x" % random.randint(0, 0xFFFFFF)
		for house in housingList:
			self.assignedHouses[house.name] = [house, False, manhattenDistance(self.position,house.position)]

	def update(self):
		self.capacityLeft = self.capacity
		for houseName in self.assignedHouses:
			houseTuple = self.assignedHouses[houseName]
			if (houseTuple[1] == True):
				self.capacityLeft -= houseTuple[0].netto
		if (self.capacityLeft < 0):
			self.overCapacitated = True
		else:
			self.overCapacitated = False


	def checkOvercapacity(self):
		if (self.capacityLeft < 0):
			self.overCapacitated = True
		else:
			self.overCapacitated = False


def createBatteries(n_batteries, totalCapacity, batteryPositionList, capacityList, batteryList, houseList):

	# print n_batteries, totalCapacity, batteryPositionList, capacityList
	for i in range(n_batteries):
		batteries = battery(i, capacityList[i], houseList, False, position = batteryPositionList[i])
		batteryList.append(batteries)

def batteryInformation(batteryList):


	for i in range (len(batteryList)):
		for attr, value in batteryList[i].__dict__.iteritems():
			print "this is "+attr+" of battery number "+str(i)
			print "value: " + str(value)

def houseInformation(houseList):

	for i in range (len(houseList)):
		for attr, value in houseList[i].__dict__.iteritems():
			print "this is "+attr+" of house number "+str(i)
			print "value: " + str(value)
	




def manhattenDistance(position, goal):
	""" calculates the minimal length of the wire from base to goal """

	return sum(abs(a-b) for a,b in zip(position,goal))