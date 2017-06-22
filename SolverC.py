import pickle
import solarHouse
import Battery
import SolverB
from random import randint
import matplotlib.pyplot as plt
import time
import Board
import numpy as np
import random
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
from copy import deepcopy

def solverC(houseList, boardLength, boardHeight, wireCost):
	batteryOptions = [450,900,1800]
	batterycosts = [900,1350,1800]
	
	# precalculate capacity
	totalCapacity = 0
	for house in houseList:
		totalCapacity += house.netto

	# make inital configuration
	batteryConfiguration = []
	while(sum(batteryConfiguration)<(totalCapacity*1.13)):
		batteryConfiguration.append(random.choice(batteryOptions))

	# calculate initial cost
	batteryCost = 0
	for i in range(len(batteryOptions)):
		batteryCost += batteryConfiguration.count(batteryOptions[i])*batterycosts[i]
	
	#create batteryList
	batteryList = []
	number = 0
	for batterycap in batteryConfiguration:
		# newpos = [randint(0,boardLength), randint(0,boardHeight)]
		Battery.battery(number, batterycap, houseList, False, position = [25,25])
		number += 1

	Wirecost = 0
	cap = 1
	while(cap > 0):
		cap, wireLength, itt = SolverB.solverB(houseList, batteryList,50,50)
	costBefore = batteryCost + wireLength*wireCost

	# do until converge
	nothingChanged = 0
	while(nothingChanged < 50):

		# change something
		oldConfiguration = deepcopy(batteryConfiguration)
		choice = random.choice(range(4))
		oldbattery = 0 
		if (choice < 2):
			# swap
			batteryConfiguration.pop(randint(0,len(batteryConfiguration)))
			batteryConfiguration.append(random.choice(batteryOptions))
		elif (choice == 2):
			# remove
			batteryConfiguration.pop(randint(0,len(batteryConfiguration)))
		else:
			# add
			batteryConfiguration.append(random.choice(batteryOptions))



		# if capacity is too high or low try something else
		if((sum(batteryConfiguration)>(totalCapacity*1.13)) and (sum(batteryConfiguration)<=(totalCapacity))):
			batteryConfiguration = oldConfiguration
			continue

		print oldConfiguration, batteryConfiguration

		#create batteryList
		batteryList = []
		number = 0
		for batterycap in batteryConfiguration:
			Battery.battery(number, batterycap, houseList, False, position = [randint(0,boardLength), randint(0,boardHeight)])
			number += 1

		# calculate cost after
		wireCosts = []
		for x in range(5):
			print "solver b itt:",x
			cap, wireLength, itt = solverB.solverB(houseList, batteryList,50,50)
			if (cap == 0):
				wireCosts.append(wireLength*wireCost)
		batteryCost = 0
		for i in range(len(batteryOptions)):
			batteryCost += batteryConfiguration.count(batteryOptions[i])*batterycosts[i]
		costAfter = np.mean(wireCosts) + batteryCost

		print costAfter, costBefore

		# if no improvement, swap back, else keep change
		if (costAfter >= costBefore):
			batteryConfiguration = oldConfiguration
			nothingChanged += 1
		else:
			costBefore = costAfter
			nothingChanged = 0

	return batteryConfiguration