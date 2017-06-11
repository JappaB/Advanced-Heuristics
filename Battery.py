import random
capacityList = [100,200,300,350,50]
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
			self.assignedHouses[house.name] = (house, False)

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


def createBatteries(n_batteries, totalCapacity, batteryPositionList, capacityList, batteryList, houseList):

	for i in range(n_batteries):
		batteries = battery(i, capacityList[i], houseList, False, position = batteryPositionList[i])
		batteryList.append(batteries)

def batteryInformation(allBatteries, number, batteryList):

	if allBatteries == True:
		for i in range (len(batteryList)):
			for attr, value in batteryList[i].__dict__.iteritems():
				print "this is "+attr+" of battery number "+str(i)
				print "value: " + str(value)
	else:
		for attr, value in batteryList[number].__dict__.iteritems():
			print "this is "+attr+" of battery number "+str(number)
			print "value: "+ str(value)

def houseInformation(houseList):

	for i in range (len(houseList)):
		for attr, value in houseList[i].__dict__.iteritems():
			print "this is "+attr+" of house number "+str(i)
			print "value: " + str(value)
	




