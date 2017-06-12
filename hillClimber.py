import random
import Battery

def hillClimber(iterations, houseList, batteryList):

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

		swap(battery1, battery2, house1, house2)

		battery1.update()
		battery2.update()

		overCapacityAfter = -(battery1.capacityLeft + battery2.capacityLeft)

		# als een van de twee overcapacitated is, dan wil je dat eerst fixen, anders ga je score optimaliseren
		if (battery1.overCapacitated or battery2.overCapacitated) and (overCapacityAfter >= overCapacityBefore):
			swap(battery1, battery2, house1, house2)
			nothingChanged += 1
		else:
			costAfter = cost(batteryList, houseList, wireCost, batteryCost)
			if costBefore < costAfter:
			# Swap back
				nothingChanged += 1
				swap(battery1, battery2, house1, house2)
			else:
				nothingChanged = 0



	totalOvercap = totalOvercapacity(batteryList)
	# return final cost, hoe veel overcapaciteit er nog is
	return min(costAfter,costBefore), totalOvercap, iterating

def overCapacitated(battery1, battery2, house1, house2):

	# If both are overcapacitated, swap is always accepted
	if (battery1.overCapacitated and battery2.overCapacitated):
		swap(battery1, battery2, house1, house2)

	# If one is overcapacitated, the swap is accepted if it is less overcapacitated afterwards
	elif (battery1.overCapacitated and not battery2.overCapacitated == False):

		# Overcapacity is the the total capacity - capacity used (so a negative number if there is overcapacity)
		overcapacityBefore = battery1.capacityLeft

		# Swap
		battery1.assignedHouses[house1.name][1] = False
		battery1.assignedHouses[house2.name][1] = True
		battery2.assignedHouses[house1.name][1] = True
		battery2.assignedHouses[house2.name][1] = False

		overcapacityAfter = battery1.capacityLeft

		if overcapacityBefore > overcapacityAfter:
			# Swap Back
			battery1.assignedHouses[house1.name][1] = True
			battery1.assignedHouses[house2.name][1] = False
			battery2.assignedHouses[house1.name][1] = False
			battery2.assignedHouses[house2.name][1] = True

	# If Two is overcapacitated, the swap is accepted if it is less overcapacitated afterwards
	elif battery1.overCapacitated == False and battery2.overCapacitated == True:

		# Overcapacity is the the total capacity - capacity used (so a negative number if there is overcapacity)
		overcapacityBefore = battery2.capacityLeft

		# Swap
		battery1.assignedHouses[house1.name][1] = False
		battery1.assignedHouses[house2.name][1] = True
		battery2.assignedHouses[house1.name][1] = True
		battery2.assignedHouses[house2.name][1] = False

		overcapacityAfter = battery2.capacityLeft

		if overcapacityBefore > overcapacityAfter:
			# Swap Back
			battery1.assignedHouses[house1.name][1] = True
			battery1.assignedHouses[house2.name][1] = False
			battery2.assignedHouses[house1.name][1] = False
			battery2.assignedHouses[house2.name][1] = True


def swap(battery1, battery2, house1, house2):
	battery1.assignedHouses[house1.name][1] = not battery1.assignedHouses[house1.name][1]
	battery1.assignedHouses[house2.name][1] = not battery1.assignedHouses[house2.name][1]
	battery2.assignedHouses[house1.name][1] = not battery2.assignedHouses[house1.name][1]
	battery2.assignedHouses[house2.name][1] = not battery2.assignedHouses[house2.name][1]

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