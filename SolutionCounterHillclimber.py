import random
import Battery
# import 

def hillClimber(iterations, houseList, batteryList):

	# print "running hillclimber b"

	nothingChanged = 0
	iterating = 0
	reset = 0

	while(nothingChanged < iterations):
		# print nothingChanged

		# print "\n", cost2(batteryList, houseList), "\n"

		iterating += 1
		
		# Randomly pick a house and assign to another battery
		house1 = random.choice(houseList)
		house2 = random.choice(houseList)
		battery1 = 0
		battery2 = 0
		# battery1 = house1.batteryAssignment
		# battery2 = house2.batteryAssignment

		# print house1.name, house1.batteryAssignment.batteryNumber, battery1.batteryNumber
		# print house2.name, house2.batteryAssignment.batteryNumber, battery2.batteryNumber
		# # Check to which battery the houses are linked
		for battery in batteryList:
			if battery.assignedHouses[house1.name][1]:
				battery1 = battery
			if battery.assignedHouses[house2.name][1]:
				battery2 = battery

		# Update current capacity used for each battery
		# try:
		battery1.checkOvercapacity()
		battery2.checkOvercapacity()


		# before swap calculations of the wireCost
		costBefore = manhattenDistance(battery1.position,house1.position)+manhattenDistance(battery2.position,house2.position) #cost2(batteryList,houseList)
		# two_housesBefore = wireDifference(0, [house1,house2])

		overCapacityBefore = 0
		if (battery1.overCapacitated): 
			overCapacityBefore -= ( battery1.capacityLeft)
		if (battery2.overCapacitated):
			overCapacityBefore -= (battery2.capacityLeft)

		# swap itself
		assigned = True
		if (((not battery1.overCapacitated) and (not battery2.overCapacitated)) or (battery1.capacityLeft == battery2.capacityLeft)):
			swap(battery1, battery2, house1, house2)
			battery1.capacityLeft += (house1.netto - house2.netto)
			battery2.capacityLeft += (house2.netto - house1.netto)
			assigned = False
		else:
			assignedHouse = house1
			if(battery1.capacityLeft > battery2.capacityLeft):
				assignedHouse = house2
				battery2.capacityLeft +=  house2.netto
				battery1.capacityLeft -=  house2.netto
			else:
				battery2.capacityLeft -=  house1.netto
				battery1.capacityLeft +=  house1.netto
			assignment(battery1,battery2,assignedHouse)

		# update 
		battery1.checkOvercapacity()
		battery2.checkOvercapacity()

		# after swap calculations of overcapacity
		# try to get overcapacity from a positive number to zero
		overCapacityAfter = 0
		if (battery1.overCapacitated):
			overCapacityAfter -= ( battery1.capacityLeft)
		if (battery2.overCapacitated):
			overCapacityAfter -= (battery2.capacityLeft)

		# als een van de twee overcapacitated is, dan wil je dat eerst fixen, anders ga je score optimaliseren
		if (battery1.overCapacitated or battery2.overCapacitated) and (overCapacityAfter > overCapacityBefore):
			if (assigned):
				assignment(battery1,battery2,assignedHouse)
				if (assignedHouse == house1):
					battery2.capacityLeft +=  house1.netto
					battery1.capacityLeft -=  house1.netto
				else:
					battery2.capacityLeft -=  house2.netto
					battery1.capacityLeft +=  house2.netto
			else:
				swap(battery1, battery2, house1, house2)
				battery1.capacityLeft += -(house1.netto - house2.netto)
				battery2.capacityLeft += -(house2.netto - house1.netto)
			nothingChanged += 1
			costAfter = costBefore
		else:
			costAfter = 0#cost2(batteryList,houseList)
			if (assigned):
				for battery in batteryList:
					for house in [house1,house2]:
						if battery.assignedHouses[house.name][1]:
							costAfter += manhattenDistance(battery.assignedHouses[house.name][0].position,battery.position)
			else:
				costAfter = manhattenDistance(battery1.position,house2.position)+manhattenDistance(battery2.position,house1.position)

			if (costBefore <= costAfter):
			# Swap back
				nothingChanged += 1
				if (assigned):
					assignment(battery1,battery2,assignedHouse)
					if (assignedHouse == house1):
						battery2.capacityLeft +=  house1.netto
						battery1.capacityLeft -=  house1.netto
					else:
						battery2.capacityLeft -=  house2.netto
						battery1.capacityLeft +=  house2.netto
				else:
					swap(battery1, battery2, house1, house2)
					battery1.capacityLeft += -(house1.netto - house2.netto)
					battery2.capacityLeft += -(house2.netto - house1.netto)
			else:
				reset += 1
				# print reset
				nothingChanged = 0
		


	for battery in batteryList:
		battery.update()
	# return final cost, hoe veel overcapaciteit er nog is
	return cost2(batteryList, houseList), reset, iterating

def swap(battery1, battery2, house1, house2):
	#50/50 chance to either swap between two houses or to assign one house to a new battery
	# swapBool =random.choice([0, 1])

	# print house1.name, house1.batteryAssignment.batteryNumber, battery1.batteryNumber, battery1.assignedHouses[house1.name][1] ,battery1.assignedHouses[house2.name][1]
	# print house2.name, house2.batteryAssignment.batteryNumber, battery2.batteryNumber, battery2.assignedHouses[house1.name][1] ,battery2.assignedHouses[house2.name][1]

	


	battery1.assignedHouses[house1.name][1] = not battery1.assignedHouses[house1.name][1]
	battery1.assignedHouses[house2.name][1] = not battery1.assignedHouses[house2.name][1]
	battery2.assignedHouses[house1.name][1] = not battery2.assignedHouses[house1.name][1]
	battery2.assignedHouses[house2.name][1] = not battery2.assignedHouses[house2.name][1]
	# house1.batteryAssignment = battery2
	# house2.batteryAssignment = battery1
	


def assignment(battery1, battery2, house1):
	battery1.assignedHouses[house1.name][1] = not battery1.assignedHouses[house1.name][1]
	battery2.assignedHouses[house1.name][1] = not battery2.assignedHouses[house1.name][1]
	# house1.batteryAssignment = battery2


# def totalOvercapacity(batteryList):
# 	overcap = 0

# 	for i in range (len(batteryList)):
# 		overcap += batteryList[i].capacityLeft

# 	return -overcap

def cost2(batteryList, houseList):
	""" calculates the cost of a setup of batteries and houses """

	cost = 0
	for battery in batteryList:
		for houseKey in battery.assignedHouses:
			if (battery.assignedHouses[houseKey][1]):
				cost += manhattenDistance(battery.assignedHouses[houseKey][0].position,battery.position)
	return cost

def manhattenDistance(position, goal):
	""" calculates the minimal length of the wire from base to goal """

	return sum(abs(a-b) for a,b in zip(position,goal))

def cost(batteryList, houseList):
	"""Calculates total wirecost for before"""
	wireLength = 0
	for house in houseList:
		position = house.position 
		goal = house.batteryAssignment.position
		wireLength += manhattenDistance(position, goal)
	return wireLength

# def wireDifference(distanceBefore, housesNow):
# 	cost = 0
# 	for house in housesNow: #new distance house 1
# 		position = house.position 
# 		goal = house.batteryAssignment.position
# 		cost += manhattenDistance(position, goal)
# 	costDifference = cost - distanceBefore
# 	return costDifference

