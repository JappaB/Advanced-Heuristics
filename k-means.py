import Battery
import solarHouse
import numpy as np
import random
from random import randint
import matplotlib.pyplot as plt

def manhattenDistance(position, goal):
	""" calculates the minimal length of the wire from base to goal """

	return sum(abs(a-b) for a,b in zip(position,goal))

def cost(n_batteries, houseList, wirecost, batterycost):
	cost = 0
	cost += n_batteries*batterycost
	for house in houseList:
		cost += manhattenDistance(house.position, house.batteryAssignment.position)*wirecost

	return cost


somethingChanged = True

results = []
n_tries = 4
houseList = []
batteryList = []
for n_Batteries in range(3,n_tries):
	# batteryList = []
	# houseList = []
	# n_Batteries = 2
	n_Houses = 400
	boardLength = 100
	boardHeight = 100

	for x in xrange(n_Batteries):
		newBatt = Battery.battery()
		newBatt.name = 'Battery : '+str(x)
		newBatt.position = [randint(boardLength/4, 3*(boardLength/4)), randint(boardHeight/4, 3*(boardHeight/4))]
		batteryList.append(newBatt)
		# print newBatt.name, newBatt.position, newBatt.color


	for x in xrange(n_Houses):
		newHouse = solarHouse.solarpanelHouse()
		newHouse.position = [randint(0, boardLength), randint(0, boardHeight)]
		houseList.append(newHouse)
		# print newHouse.position


	print "start", n_Batteries


	z = 0
	while(z < 1000):
		z += 1
		# assignment
		for house in houseList:
			distances = []
			for battery in batteryList:
				distances.append(manhattenDistance(battery.position,house.position))
			index = np.argmin(distances)
			house.batteryAssignment = batteryList[index]
			# print house.position, house.batteryAssignment.name


		# relocating 
		for battery in batteryList:
			n = 0
			positionSum = np.array([0,0])
			for house in houseList:
				if (house.batteryAssignment == battery):
					n += 1
					positionSum += house.position
			battery.position = list(positionSum/n)
			# print battery.name, battery.position, n

	results.append(cost(n_Batteries,houseList,3,40))
	# for house in houseList:
	# 	print house.position, house.batteryAssignment.name

	# print ""


# plt.plot(xrange(1,n_tries), results)
	
for house in houseList:
	# print house.position, house.batteryAssignment.name
	colorNow = house.batteryAssignment.color
	plt.plot([house.position[0]],[house.position[1]],  'ro', color=colorNow)

for battery in batteryList:
	plt.plot([battery.position[0]],[battery.position[1]],  '^', color=battery.color)

plt.grid()
plt.show()



