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

def solverC(houseList, boardLength, boardHeight, wirePrice, batteryOptions, maxOvercapacity,batterycosts, method = "A"):
	
	checked = set()
	
	# precalculate capacity
	totalCapacity = 0
	for house in houseList:
		totalCapacity += house.netto

	possibleConfigurations = []

	for x in range(34):
		for y in range(9):
			cap = x*batteryOptions[0] + y*batteryOptions[1]
			if (cap >totalCapacity*1.4) and (cap < totalCapacity*1.5):
				confList = [batteryOptions[0] for i in range(x)] + [batteryOptions[1] for j in range(y)]
				possibleConfigurations.append(confList)

	
	# make inital configuration
	# batteryConfiguration = initialConfiguration(method, totalCapacity, maxOvercapacity, batteryOptions)
	
	# calculate initial cost
	# batteryCost = batteryCost1(batteryOptions, batterycosts, batteryConfiguration)
	# wireLength = 0
	# cap = 1
	# while(cap > 0):
	# 	print "initiation try"
	# 	batteryList = createBatteryList(batteryConfiguration,boardLength,boardHeight, houseList)
	# 	cap, wireLength, itt = SolverB.solverB(houseList, batteryList,boardLength,boardHeight)
	# costBefore = batteryCost + wireLength*wirePrice 
	# print "initiation confirmed : ", countBatteries(batteryConfiguration, batteryOptions), len(batteryConfiguration)
	results = {}

	# do until converge
	# nothingChanged = 0
	# while(nothingChanged < 10):
	for batteryConfiguration in possibleConfigurations:

		# change something
		# oldConfiguration = deepcopy(batteryConfiguration)
		# batteryConfiguration = changeConfiguration(batteryConfiguration, batteryOptions)

		# if capacity is too high or low try something else
		# if((sum(batteryConfiguration)>(totalCapacity*maxOvercapacity*1.1)) or (sum(batteryConfiguration)<=(totalCapacity)) or (tuple(countBatteries(batteryConfiguration, batteryOptions)) in checked)):
		# 	batteryConfiguration = oldConfiguration
		# 	continue

		# new configuration to be checked
		readableConfiguration = countBatteries(batteryConfiguration, batteryOptions)
		# checked.add(tuple(readableConfiguration))
		# print readableConfiguration, len(batteryConfiguration)

		wireCost = 0
		batteryCost = 0
		# costAfter = 0
		# calculate cost after
		# calculate wirecost
		wireCost = wireCost1(25, batteryConfiguration, boardLength,boardHeight, houseList, wirePrice, 0, readableConfiguration)
		# calculate batterycost
		batteryCost = batteryCost1(batteryOptions, batterycosts, batteryConfiguration)
		# calculate total costafter
		cost = wireCost + batteryCost

		results[str(readableConfiguration)] = cost
		
		# print costBefore- costAfter

		# if no improvement, swap back, else keep change
		# if (costAfter >= costBefore):
		# 	print "worse so restore:", countBatteries(oldConfiguration, batteryOptions)
		# 	batteryConfiguration = oldConfiguration
		# 	nothingChanged += 1
		# else:
		# 	print "better so use : ", readableConfiguration
		# 	costBefore = costAfter
		# 	nothingChanged = 0
	return results

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


def countBatteries(batteryConfiguration, batteryOptions):
	countlist = []
	for i in range(len(batteryOptions)):
		countlist.append(batteryConfiguration.count(batteryOptions[i]))

	return countlist

def initialConfiguration(method, totalCapacity, maxOvercapacity, batteryOptions):
	batteryConfiguration = []
	if (method == "A"):
		while(sum(batteryConfiguration)<(totalCapacity*maxOvercapacity)):
			batteryConfiguration.append(random.choice(batteryOptions))
	else:
		batteryConfiguration = [450,450,450,900,900,900,1800,1800]

	return batteryConfiguration

def batteryCost1(batteryOptions, batterycosts, batteryConfiguration):
	batteryCost = 0
	for i in range(len(batteryOptions)):
		batteryCost += batteryConfiguration.count(batteryOptions[i])*batterycosts[i]

	return batteryCost

def changeConfiguration(batteryConfiguration, batteryOptions):
	choice = random.choice(range(4))
	if (choice < 2):
		batteryConfiguration.pop(randint(0,len(batteryConfiguration)-1))
		batteryConfiguration.append(random.choice(batteryOptions))
	elif (choice == 2):
		batteryConfiguration.pop(randint(0,len(batteryConfiguration)-1))
	else:
		batteryConfiguration.append(random.choice(batteryOptions))
	return batteryConfiguration

def wireCost1(iterations, batteryConfiguration, boardLength,boardHeight, houseList, wirePrice, nothingChanged, countlist):
	wireCost = 0
	tries = 0
	wireCosts = []
	while(len(wireCosts) < iterations):
		if (tries > 200):
			return 1000000000000000000000
		print "solver b", "nothing canged ", len(wireCosts), " batteries : ", countlist
		batteryList = createBatteryList(batteryConfiguration,boardLength,boardHeight, houseList)
		cap, wireLength, itt = SolverB.solverB(houseList, batteryList,boardLength,boardHeight)
		if (cap == 0):
			wireCosts.append(wireLength*wirePrice)
	wireCost = np.mean(wireCosts)

	print "in formula", wireCost
	return wireCost