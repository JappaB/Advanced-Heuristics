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

def solverC(houseList, boardLength, boardHeight, wirePrice, batteryOptions, batterycosts, batteryConfiguration):
	
	# new configuration to be checked
	readableConfiguration = countBatteries(batteryConfiguration, batteryOptions)
	wireCost = 0
	batteryCost = 0
	# calculate wirecost
	wireCost = wireCost1(100, batteryConfiguration, boardLength,boardHeight, houseList, wirePrice, 0, readableConfiguration)
	# calculate batterycost
	batteryCost = batteryCost1(batteryOptions, batterycosts, batteryConfiguration)
	# calculate total costafter
	cost = wireCost + batteryCost

	return cost, batteryCost

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
		print ('solver b : found samples [%d%%]\r'%len(wireCosts)),
		batteryList = createBatteryList(batteryConfiguration,boardLength,boardHeight, houseList)
		cap, wireLength, itt = SolverB.solverB(houseList, batteryList,boardLength,boardHeight)
		if (cap == 0):
			wireCosts.append(wireLength*wirePrice)
			tries = 0
		tries += 1
	wireCost = np.mean(wireCosts)

	return wireCost