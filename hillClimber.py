import random

def hillClimber(iterations, houseList, batteryList):

	for i in range(iterations):
		
		# Randomly pick a house and assign to another battery
		house1 = random.choice(houseList)
		house2 = random.choice(houseList)
		battery1 = 0
		battery2 = 0
		#overcapacitated or not

		battery1OverCapacitated = True
		battery2OverCapacitated = True

		# Check to which battery the houses are linked
		for i in range (len(batteryList)):
			if batteryList[i].assignedHouses[house1.name][1]:
				battery1 = batterylist[i]
			if batteryList[i].assignedHouses[house2.name][1]:
				battery2 = batterylist[i]

		# Update current capacity used for each battery
		battery1.update()
		battery2.update()

		# Check whether one or both batteries are overcapacitated
		if battery1.overCapacitated or battery2.overCapacitated:
			overCapacitated(battery1, battery2, house1, house2)

		# If none are overcapacitated, the swap is accepted if the total costs (in euro's) are lower afterwards
		else:
			costBefore = cost(n_batteries, houseList, wireCost, batteryCost)

			# Swap batteries
			battery1.assignedhouse[house1.name][1] = False
			battery1.assignedhouse[house2.name][1] = True
			battery2.assignedhouse[house1.name][1] = True
			battery2.assignedhouse[house2.name][1] = False

			costAfter = cost(n_batteries, houseList, wireCost, batteryCost)

			if costBefore < costAfter:
				# Swap back
				battery1.assignedhouse[house1.name][1] = True
				battery1.assignedhouse[house2.name][1] = False
				battery2.assignedhouse[house1.name][1] = False
				battery2.assignedhouse[house2.name][1] = True



	totalOvercap = totalOvercapacity(batteryList)
	# return final cost, hoe veel overcapaciteit er nog is
	return max(costAfter,costBefore), totalOvercap

def overCapacitated(battery1, battery2, house1, house2):

	# If both are overcapacitated, swap is always accepted
	if battery1.overCapacitated and battery2.overCapacitated == True:
		battery1.assignedhouse[house1.name][1] = False
		battery1.assignedhouse[house2.name][1] = True
		battery2.assignedhouse[house1.name][1] = True
		battery2.assignedhouse[house2.name][1] = False

	# If one is overcapacitated, the swap is accepted if it is less overcapacitated afterwards
	if battery1.overCapacitated == True and battery2.overCapacitated == False:

		# Overcapacity is the the total capacity - capacity used (so a negative number if there is overcapacity)
		overcapacityBefore = battery1.capacityLeft

		# Swap
		battery1.assignedhouse[house1.name][1] = False
		battery1.assignedhouse[house2.name][1] = True
		battery2.assignedhouse[house1.name][1] = True
		battery2.assignedhouse[house2.name][1] = False

		overcapacityAfter = battery1.capacityLeft

		if overcapacityBefore > overcapacityAfter:
			# Swap Back
			battery1.assignedhouse[house1.name][1] = True
			battery1.assignedhouse[house2.name][1] = False
			battery2.assignedhouse[house1.name][1] = False
			battery2.assignedhouse[house2.name][1] = True

	# If Two is overcapacitated, the swap is accepted if it is less overcapacitated afterwards
	if battery1.overCapacitated == False and battery2.overCapacitated == True:

		# Overcapacity is the the total capacity - capacity used (so a negative number if there is overcapacity)
		overcapacityBefore = battery2.capacityLeft

		# Swap
		battery1.assignedhouse[house1.name][1] = False
		battery1.assignedhouse[house2.name][1] = True
		battery2.assignedhouse[house1.name][1] = True
		battery2.assignedhouse[house2.name][1] = False

		overcapacityAfter = battery2.capacityLeft

		if overcapacityBefore > overcapacityAfter:
			# Swap Back
			battery1.assignedhouse[house1.name][1] = True
			battery1.assignedhouse[house2.name][1] = False
			battery2.assignedhouse[house1.name][1] = False
			battery2.assignedhouse[house2.name][1] = True

def totalOvercapacity(batteryList):
	overcap = 0

	for i in range (len(batteryList)):
		overcap += batteryList[i].capacityLeft

	return overcap
