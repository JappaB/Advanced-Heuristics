import pickle
import solarHouse
import Battery
import SolutionCounterHillclimber as hillClimber
from random import randint
import matplotlib.pyplot as plt
import time
import Board
import numpy as np
import random
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
import Plotter
import BoardBuilder
import copy
builder = BoardBuilder.boardBuilder()
plot = Plotter.plotter()


def main():
	boardNames = ["finalBoard1", "finalBoard2", "finalBoard3"]
	for board in boardNames[:]:

		f = open(board+'randomwalkSolutionCounter.csv', "w")

		uniquesolutions = set()

		for j in range(5000):

			houseList, batteryList = loadBoard(board)

			res = randomWalker(houseList, batteryList,10000,uniquesolutions)
			print j, "  : ", res[1], "/",res[0] 
			print len(uniquesolutions)
			f.write(str(res[0])+","+str(res[1])+"\n")
			



def loadBoard(boardName):
	""" loads board with name """

	with open(boardName+'.pkl', 'rb') as input:
		inputPickle = pickle.load(input)
		houseList = inputPickle.houseList
		batteryList = inputPickle.batteryList
	return houseList, batteryList


def changeCapacity(batteryList, factor):
	for battery in batteryList:
		battery.capacity = int(battery.capacity*factor)

def changeCapacityTo(batteryList, capacityList):
	for i in range(len(batteryList)):
		batteryList[i].capacity = capacityList[i]

def changeDeviation(houseList, deviation, median, totalCapacity):
	randoms = []
	total = 0.0
	for i in range(len(houseList)):
		newRandom = random.uniform(median-deviation,median+deviation)
		total += newRandom
		randoms.append(newRandom)

	scale = totalCapacity/total

	for i in range(len(houseList)):
		houseList[i].netto = randoms[i]*scale


def randomWalker(houseList, batteryList, iterations,uniquesolutions):
	# House to battery assignment
	for house in houseList:
		battery = random.choice(batteryList)
		battery.assignedHouses[house.name][1] = True

	scoreCount = 0
	beforeHand = len(uniquesolutions)
	for i in range(iterations):
		swapBool =random.choice([True, False])
		house1 = random.choice(houseList)
		house2 = random.choice(houseList)
		battery1 = 0
		battery2 = 0
		found_one = False
		found_two = False
		for battery in batteryList:
			if battery.assignedHouses[house1.name][1]:
				battery1 = battery
				found_one = True
			if battery.assignedHouses[house2.name][1]:
				battery2 = battery
				found_two = True
			if (found_two):
				if (found_one):
					break
		if (swapBool):
			swap(battery1, battery2, house1, house2)
			battery1.capacityLeft += (house1.netto - house2.netto)
			battery2.capacityLeft += (house2.netto - house1.netto)
		else:
			assignment(battery1,battery2,house1)
			battery2.capacityLeft -=  house1.netto
			battery1.capacityLeft +=  house1.netto

		battery1.checkOvercapacity()
		battery2.checkOvercapacity()
		score = True
		for battery in batteryList:
			if battery.overCapacitated:
				score = False
				


		if (score):
			scoreCount += 1
			solution = []
			#create list for all the houses
			for house in houseList:
				solution.append(0)
			# add batterynumber to list of houses
			for battery in batteryList:
				for key in battery.assignedHouses:
					house = battery.assignedHouses[key]
					if house[1] == True:
						solution[int(house[0].name[5:])] = battery.batteryNumber
			uniquesolutions.add(tuple(solution))
	return scoreCount, (len(uniquesolutions)-beforeHand)


def swap(battery1, battery2, house1, house2):
	#50/50 chance to either swap between two houses or to assign one house to a new battery
	# swapBool =random.choice([0, 1])

	battery1.assignedHouses[house1.name][1] = not battery1.assignedHouses[house1.name][1]
	battery1.assignedHouses[house2.name][1] = not battery1.assignedHouses[house2.name][1]
	battery2.assignedHouses[house1.name][1] = not battery2.assignedHouses[house1.name][1]
	battery2.assignedHouses[house2.name][1] = not battery2.assignedHouses[house2.name][1]


def assignment(battery1, battery2, house1):
	battery1.assignedHouses[house1.name][1] = not battery1.assignedHouses[house1.name][1]
	battery2.assignedHouses[house1.name][1] = not battery2.assignedHouses[house1.name][1]




### RUN PROGRAM ###
if __name__ == '__main__':
	main()

