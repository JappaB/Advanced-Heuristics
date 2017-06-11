def hillClimber(iterations, houseList):

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
			if house1 == batteryList[i].assignedHouses[house.name]:
				battery1 = batterylist[i]
			elif house2 == batterylist[i].assignedHouses[house.name]:
				battery2 = batterylist[i]

		# Update current capacity used for each battery
		battery1.update()
		battery2.update()

		# Check whether one or both batteries are overcapacitated
		if battery1.overCapacitated or battery2.overCapacitated == True:
			overCapacitated(battery1, battery2, house1, house2)

		# If none are overcapacitated, the swap is accepted if the total costs are lower afterwards
		else:
			costBefore = cost(n_batteries, houseList, wireCost, batteryCost)

			# Swap batteries
			battery1.assignedhouse[house1] = False
			battery1.assignedhouse[house2] = True
			battery2.assignedhouse[house1] = True
			battery2.assignedhouse[house2] = False

			costAfter = cost(n_batteries, houseList, wireCost, batteryCost)

			if costBefore < costAfter:
				# Swap back
				battery1.assignedhouse[house1] = True
				battery1.assignedhouse[house2] = False
				battery2.assignedhouse[house1] = False
				battery2.assignedhouse[house2] = True


def overCapacitated(battery1, battery2, house1, house2):

	# If both are overcapacitated, swap is always accepted
	if battery1.overCapacitated and battery2.overCapacitated == True:
		battery1.assignedhouse[house1] = False
		battery1.assignedhouse[house2] = True
		battery2.assignedhouse[house1] = True
		battery2.assignedhouse[house2] = False

	# If one is overcapacitated, the swap is accepted if it is less overcapacitated afterwards
	if battery1.overCapacitated == True and battery2.overCapacitated == False:
		


