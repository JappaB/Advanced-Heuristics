import Battery
import solarHouse
import numpy as np
import random
from random import randint
import matplotlib.pyplot as plt

def manhattenDistance(position, goal):
	""" calculates the minimal length of the wire from base to goal """

	return sum(abs(a-b) for a,b in zip(position,goal))

def cost(n_batteries, houseList, wireCost, batteryCost):
	""" calculates the cost of a setup of batteries and houses """

	cost = 0
	cost += n_batteries*batteryCost
	for house in houseList:
		cost += manhattenDistance(house.position, house.batteryAssignment.position)*wireCost
	return cost

def k_means(n_Batteries, n_Houses, boardLength, boardHeight):
	
	# initiation
	somethingChanged = True
	houseList = []
	batteryList = []

	# build batteries
	for x in xrange(n_Batteries):
		newBatt = Battery.battery()
		newBatt.name = 'Battery : '+str(x)
		newBatt.position = [randint(boardLength/4, 3*(boardLength/4)), randint(boardHeight/4, 3*(boardHeight/4))]
		batteryList.append(newBatt)

	# build houses
	for x in xrange(n_Houses):
		newHouse = solarHouse.solarpanelHouse()
		newHouse.position = [randint(0, boardLength), randint(0, boardHeight)]
		houseList.append(newHouse)

	it = 0
	while(somethingChanged):
		it += 1
		
		# assignment of houses
		for house in houseList:
			distances = []
			for battery in batteryList:
				distances.append(manhattenDistance(battery.position,house.position))
			index = np.argmin(distances)
			house.batteryAssignment = batteryList[index]

		# relocating batteries
		changedlist = []
		for battery in batteryList:
			
			# save old location
			oldPosition = tuple(battery.position)
			
			# initiate values for new battery-position
			n = 0
			positionSum = np.array([0,0])

			# check per house if it is assignet to current battery
			for house in houseList:
				# if so, count its position in
				if (house.batteryAssignment == battery):
					n += 1
					positionSum += house.position
			battery.position = list(positionSum/n)
			
			# save wether the battery moved since last time
			if (tuple(battery.position) == oldPosition):
				changedlist.append(True)
			else:
				changedlist.append(False)

		# stop if no battery changed
		if (all(i == True for i in changedlist)):
			somethingChanged = False
			print it
	return houseList, batteryList


def plotGrid(houseList, batteryList):
	""" plots the grid """

	for house in houseList:
		colorNow = house.batteryAssignment.color
		plt.plot([house.position[0]],[house.position[1]],  'ro', color=colorNow)

	for battery in batteryList:
		plt.plot([battery.position[0]],[battery.position[1]],  '^', color=battery.color)

	plt.grid()
	plt.show()



import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()
a,b = k_means(10,4000,1000,1000)
pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats() # TODO
print s.getvalue()
plotGrid(a,b)
