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
		self.housingList = housingList
		self.overCapacitated = overCapacitated #boolean

	



def createBatteries(n_batteries, totalCapacity, batteryPositionList, capacityList):

	for i in range(n_batteries):
		batteries = battery(i, capacityList[i], [], False, batteryPositionList[i])
		batteryList.append(batteries)

def batteryInformation(allBatteries, number):

	if allBatteries == True:
		for i in range (len(batteryList)):
			for attr, value in batteryList[i].__dict__.iteritems():
				print "this is "+attr+" of battery number "+str(i)
				print "value: " + str(value)
	else:
		for attr, value in batteryList[number].__dict__.iteritems():
			print "this is "+attr+" of battery number "+str(number)
			print "value: "+ str(value)

createBatteries(n_batteries,totalCapacity, batteryPositionList, capacityList)
print batteryList

batteryInformation(False,2)


