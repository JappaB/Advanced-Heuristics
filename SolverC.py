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

def solverC(houseList, boardLength, boardHeight, wireCost, method = "A"):
	batteryOptions = [450,900,1800]
	batterycosts = [900,1350,1800]
	
	# precalculate capacity
	totalCapacity = 0
	for house in houseList:
		totalCapacity += house.netto

	# make inital configuration
	batteryConfiguration = []
	
	if (method == "A"):
		while(sum(batteryConfiguration)<(totalCapacity*1.01)):
			batteryConfiguration.append(random.choice(batteryOptions))
	else:
		batteryConfiguration = [450,450,450,900,900,900,1800,1800]

	

	# calculate initial cost
	batteryCost = 0
	for i in range(len(batteryOptions)):
		batteryCost += batteryConfiguration.count(batteryOptions[i])*batterycosts[i]

	# print "batteryConfiguration, sum(batteryConfiguration), batteryCost :", batteryConfiguration, sum(batteryConfiguration), batteryCost
	
	batteryList = createBatteryList(batteryConfiguration,50,50, houseList)

	# print batteryList

	Wirecost = 0
	cap = 1
	while(cap > 0):
		cap, wireLength, itt = SolverB.solverB(houseList, batteryList,50,50)
	costBefore = batteryCost + wireLength*wireCost

	# do until converge
	nothingChanged = 0
	while(nothingChanged < 10):
		# print "NothingChanged since : ", nothingChanged

		# change something
		oldConfiguration = deepcopy(batteryConfiguration)
		choice = random.choice(range(4))
		oldbattery = 0 
		if (choice < 2):
			# swap
			batteryConfiguration.pop(randint(0,len(batteryConfiguration)-1))
			batteryConfiguration.append(random.choice(batteryOptions))
		elif (choice == 2):
			# remove
			batteryConfiguration.pop(randint(0,len(batteryConfiguration)-1))
		else:
			# add
			batteryConfiguration.append(random.choice(batteryOptions))



		# if capacity is too high or low try something else
		if((sum(batteryConfiguration)>(totalCapacity*1.13)) or (sum(batteryConfiguration)<=(totalCapacity))):
			batteryConfiguration = oldConfiguration
			continue

		# print oldConfiguration, batteryConfiguration

		countlist = []
		for i in range(len(batteryOptions)):
			countlist.append(batteryConfiguration.count(batteryOptions[i]))

		# calculate cost after
		wireCosts = []
		for x in range(5):
			print "solver b itt:",x, "nothing canged ", nothingChanged, " batteries : ", countlist
			batteryList = createBatteryList(batteryConfiguration,50,50, houseList)
			cap, wireLength, itt = SolverB.solverB(houseList, batteryList,50,50)
			if (cap == 0):
				wireCosts.append(wireLength*wireCost)
		batteryCost = 0
		for i in range(len(batteryOptions)):
			batteryCost += batteryConfiguration.count(batteryOptions[i])*batterycosts[i]
		costAfter = np.mean(wireCosts) + batteryCost

		# print costAfter, costBefore

		# if no improvement, swap back, else keep change
		if (costAfter >= costBefore):
			print "worse"
			batteryConfiguration = oldConfiguration
			nothingChanged += 1
		else:
			print "better"
			costBefore = costAfter
			nothingChanged = 0

	countlist = []
	for i in range(len(batteryOptions)):
		countlist.append(batteryConfiguration.count(batteryOptions[i]))

	return countlist

def createBatteryList(configuration, l, h, houseList):
	#create batteryList
	batteryList = []
	number = 0
	for batterycap in configuration:
		x = randint(0,l)
		y = randint(0,h)
		newpos = [x,y]
		newbat = Battery.battery(number, batterycap, houseList, False, position = newpos)
		number += 1
		batteryList.append(newbat)
	return batteryList