# batteryList = []
# n_batteries = 5
# totalCapacity = 1000
# batteryPositionList = [10,10],[40,40],[25,25],[10,40],[40,10]
capacityList = [100,200,300,350,50]
allBatteries = False

class battery(object):

	def __init__(self, batteryNumber, capacity, housingList, overCapacitated, position = [0,0]):
		self.position = position
		self.batteryNumber = batteryNumber
		#self.batteryType = batteryType
		self.capacity = capacity
		self.overCapacitated = overCapacitated #boolean
		self.assignedHouses = {}
		for house in housingList:
			self.assignedHouses[house.name] = (house, False)

	def update(self):
		capacityUsed = 0
		for houseName in self.assignedHouses:
			houseTuple = self.assignedHouses[houseName]
			if houseTuple[1] == True:
				capacityUsed += houseTuple[0].netto
		if capacityUsed > self.capacity:
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

# createBatteries(n_batteries,totalCapacity, batteryPositionList, capacityList)
# print batteryList

# batteryInformation(False,2)


