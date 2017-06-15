import random
import Battery

def hillClimber(iterations, houseList, batteryList):

	# House to battery assignment
	for house in houseList:
		battery = random.choice(batteryList)
		battery.assignedHouses[house.name][1] = True

	# Battery.batteryInformation(True,0,batteryList)

	n_batteries = len(batteryList)
	wireCost = 1
	batteryCost = 100

	nothingChanged = 0

	iterating = 0

	while(nothingChanged < iterations):


		iterating += 1

		# print nothingChanged
		
		# Randomly pick a house and assign to another battery
		house1 = random.choice(houseList)
		house2 = random.choice(houseList)
		battery1 = 0
		battery2 = 0
		#overcapacitated or not

		battery1OverCapacitated = True
		battery2OverCapacitated = True

		# Check to which battery the houses are linked
		for battery in batteryList:
			# print battery.assignedHouses[house1.name]
			# print battery.assignedHouses[house2.name], "\n"
			if battery.assignedHouses[house1.name][1]:
				battery1 = battery
				# print battery1.batteryNumber
			if battery.assignedHouses[house2.name][1]:
				battery2 = battery
				# print battery2.batteryNumber

		# Update current capacity used for each battery
		# try:
		battery1.update()
		battery2.update()
		

		# If none are overcapacitated, the swap is accepted if the total costs (in euro's) are lower afterwards
		
		costBefore = cost(batteryList, houseList, wireCost, batteryCost)
		overCapacityBefore = 0
		if (battery1.overCapacitated or battery2.overCapacitated):
			overCapacityBefore = -( battery1.capacityLeft + battery2.capacityLeft)

		assigned = True
		if (((not battery1.overCapacitated) and (not battery2.overCapacitated)) or (battery1.capacityLeft == battery2.capacityLeft)):
			swap(battery1, battery2, house1, house2)
			assigned = False
		else:
			assignedHouse = house1
			if(battery1.capacityLeft < battery2.capacityLeft):
				assignedHouse = house1
			elif(battery1.capacityLeft > battery2.capacityLeft):
				assignedHouse = house2
			assignment(battery1,battery2,assignedHouse)

		battery1.update()
		battery2.update()

		overCapacityAfter = -(battery1.capacityLeft + battery2.capacityLeft)

		# als een van de twee overcapacitated is, dan wil je dat eerst fixen, anders ga je score optimaliseren
		if (battery1.overCapacitated or battery2.overCapacitated) and (overCapacityAfter >= overCapacityBefore):
			if (assigned):
				assignment(battery1,battery2,assignedHouse)
			else:
				swap(battery1, battery2, house1, house2)
			nothingChanged += 1
			costAfter = costBefore
		else:
			costAfter = cost(batteryList, houseList, wireCost, batteryCost)
			if costBefore < costAfter:
			# Swap back
				nothingChanged += 1
				if (assigned):
					assignment(battery1,battery2,assignedHouse)
				else:
					swap(battery1, battery2, house1, house2)
			else:
				nothingChanged = 0


	for battery in batteryList:
		battery.update()
	totalOvercap = totalOvercapacity(batteryList)
	# return final cost, hoe veel overcapaciteit er nog is
	return min(costAfter,costBefore), -totalOvercap, iterating

def swap(battery1, battery2, house1, house2):
	#50/50 chance to either swap between two houses or to assign one house to a new battery
	# swapBool =random.choice([0, 1])

	battery1.assignedHouses[house1.name][1] = not battery1.assignedHouses[house1.name][1]
	battery1.assignedHouses[house2.name][1] = not battery1.assignedHouses[house2.name][1]
	battery2.assignedHouses[house1.name][1] = not battery2.assignedHouses[house1.name][1]
	battery2.assignedHouses[house2.name][1] = not battery2.assignedHouses[house2.name][1]


def assignment(battery1, battery2, house1):
	battery1.assignedHouses[house1.name][1] = not battery1.assignedHouses[house1.name][1]
	battery2.assignedHouses[house1.name][1] = not battery2.assignedHouses[house1.name][1]





	# if ((battery1.capacityLeft >0) and ( battery2.capacityLeft > 0)):
	# 	battery1.assignedHouses[house1.name][1] = not battery1.assignedHouses[house1.name][1]
	# 	battery1.assignedHouses[house2.name][1] = not battery1.assignedHouses[house2.name][1]
	# 	battery2.assignedHouses[house1.name][1] = not battery2.assignedHouses[house1.name][1]
	# 	battery2.assignedHouses[house2.name][1] = not battery2.assignedHouses[house2.name][1]
	# else:
	# 	if (battery1.capacityLeft < battery2.capacityLeft):
	# 		battery1.assignedHouses[house1.name][1] = not battery1.assignedHouses[house1.name][1]
	# 		battery2.assignedHouses[house1.name][1] = not battery2.assignedHouses[house1.name][1]
	# 	elif(battery1.capacityLeft > battery2.capacityLeft):
	# 		battery1.assignedHouses[house2.name][1] = not battery1.assignedHouses[house2.name][1]
	# 		battery2.assignedHouses[house2.name][1] = not battery2.assignedHouses[house2.name][1]
	# 	else:
	# 		battery1.assignedHouses[house1.name][1] = not battery1.assignedHouses[house1.name][1]
	# 		battery1.assignedHouses[house2.name][1] = not battery1.assignedHouses[house2.name][1]
	# 		battery2.assignedHouses[house1.name][1] = not battery2.assignedHouses[house1.name][1]
	# 		battery2.assignedHouses[house2.name][1] = not battery2.assignedHouses[house2.name][1]

def totalOvercapacity(batteryList):
	overcap = 0

	for i in range (len(batteryList)):
		overcap += batteryList[i].capacityLeft

	return overcap

def cost(batteryList, houseList, wireCost, batteryCost):
	""" calculates the cost of a setup of batteries and houses """

	cost = 0
	cost += len(batteryList)*batteryCost
	for battery in batteryList:
		for houseKey in battery.assignedHouses:
			if (battery.assignedHouses[houseKey][1]):
				cost += manhattenDistance(battery.assignedHouses[houseKey][0].position, battery.position)*wireCost
	return cost

def manhattenDistance(position, goal):
	""" calculates the minimal length of the wire from base to goal """

	return sum(abs(a-b) for a,b in zip(position,goal))