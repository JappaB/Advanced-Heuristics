import pickle
import solarHouse
import Battery
import hillClimberB as hillB
import hillClimber as hillOld
from random import randint
import matplotlib.pyplot as plt
import time
import Board
import numpy as np
import random
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm

def solverB(houseList, batteryList, boardLength, boardHeight):

	# House to battery assignment
	for house in houseList:
		battery = random.choice(batteryList)
		battery.assignedHouses[house.name][1] = True
		# house.batteryAssignment = battery

	# battery positioning random
	batteryPositionList =[]
	for x in range(len(batteryList)):

		newPosition = [randint(0,boardLength), randint(0,boardHeight)]
		for j in batteryPositionList:
			if (tuple(j) == tuple(newPosition)):
				newPosition[0] = (newPosition[0] + 1) % boardLength
				newPosition[1] = (newPosition[1] + 1) % boardHeight

		batteryPositionList.append(newPosition)
	

	print batteryPositionList
	i = 0
	for battery in batteryList:
		print i
		battery.position = batteryPositionList[i]
		i += 1


	iterations = 0
	somethingChanged = True
	while(somethingChanged):

		


		cost, reset, itt = hillB.hillClimber(1000, houseList, batteryList)

		
		iterations += 1 + itt
		# print iterations
		changedlist = []
		for battery in batteryList:
			# save old location
			oldPosition = tuple(battery.position)
			# print "oldposition", oldPosition
			
			# initiate values for new battery-position
			n = 0
			positionSum = np.array([0,0])

			# check per house if it is assignet to current battery
			for houseKey in battery.assignedHouses:
				# if so, count its position in
				if (battery.assignedHouses[houseKey][1]):
					n += 1
					positionSum += battery.assignedHouses[houseKey][0].position
			battery.position = list(positionSum/n)

			# print "newposition", battery.position

			# save wether the battery moved since last time
			if (tuple(battery.position) == oldPosition):
				changedlist.append(False)
			else:
				changedlist.append(True)

		print changedlist
		# stop if no battery changed
		if (all(i == False for i in changedlist)):
			somethingChanged = False
		# print somethingChanged

	cost, reset, itt = hillB.hillClimber(1000, houseList, batteryList)

	totalcap = 0
	for battery in batteryList:
		battery.update()
		if (battery.overCapacitated):
			totalcap -= battery.capacityLeft

			
	finalCost = hillB.cost2(batteryList, houseList)

	return totalcap, finalCost, iterations



