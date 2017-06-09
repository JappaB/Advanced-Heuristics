batteryList = []
n_batteries = 5
totalCapacity = 1000
batteryPositionList = [[10,10],[40,40],[25,25],[10,40],[40,10]]
capacityLists = [[100,200,300,350,50]]

class battery(object):

	def __init__(self, batteryNumber, position = [0,0], capacity, housingList, overCapacitated):
		self.position = position
		self.batteryNumber = batteryNumber
		#self.batteryType = batteryType
		self.capacity = capacity
		self.housingList = housingList
		self.overCapacitated = overCapacitated #boolean

def createBatteries(n_batteries, totalCapacity, batteryPositionList, capacitydistribution):

	capacityList

	for i in range(n_batteries):
		battery = battery(i, batteryPositionList[i], capacityList[i], housingList, overCapacitated
		batteryList.append(battery)


createBatteries(n_batteries,totalCapacity)
print batteryList