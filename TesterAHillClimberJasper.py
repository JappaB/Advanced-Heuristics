import pickle
import solarHouse
import Battery
import hillClimber as hillClimber
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
builder = BoardBuilder.boardBuilder()
plot = Plotter.plotter()


def main():
	boardNames = ["finalBoard1", "finalBoard2", "finalBoard3"]
	for board in boardNames[2:3]:

		'''Vul hier in hoe je de data wilt verkrijgen, hoeveel iteraties per bord/stddev combinatie, etc.'''
		ITERATIONS = 100
		EXITHC = 23000
		
		'''Hieronder wordt het bord doorgelopen voor een batterijcapaciteit die steeds 2.5 percent
		omhoog gaat. Van 502.5 tot 520. De st. dev output verandert nog steeds op dezelfde manier.'''
		f = open(board+"Final results- "+str(ITERATIONS)+" -ExitHC - "+str(EXITHC)+" -.csv", "w")
		f.write("Cost,Reset,Iterations,Solved,TimeInHC,Dev,Batterycap\n")
		results2 = []
		results1 = [[],[],[],[],[]]
		solved = 0
		for j in range(ITERATIONS):

			houseList, batteryList = loadBoard(board)

			start_time = time.time()
			cost, reset, itt = hillClimber.hillClimber(EXITHC, houseList, batteryList)
			TimeInHC = (time.time() - start_time)
			results1[0].append(cost)
			results1[1].append(reset)
			results1[2].append(itt)
			results1[3].append(TimeInHC)

			solveableCheck = True
			TotalOvercap = 0
			for battery in batteryList:
				if (battery.overCapacitated == True):
					# print battery.overCapacitated
					solveableCheck = False
					TotalOvercap -= battery.capacityLeft
					results1[4].append(TotalOvercap)

			if solveableCheck:
				solved += 1


			print "Working on: ",board, ", cost: ", cost,", resets: ", reset, ", itt: " , itt, ", TimeInHC, ", TimeInHC, " solveable : ", solved,"/",j , " TotalOvercap: ", TotalOvercap, "\n"

		results2.append(solved)
		print "percentage : ", float((solved/ITERATIONS)*100.0), "%"

		f.write(str(np.mean(results1[0]))+","+str(np.mean(results1[1]))+","+str(np.mean(results1[2]))+","+str(solved)+","+str(np.mean(results1[3]))+","+str(np.mean(results1[4]))+","+str(board)+"\n")




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


def randomWalker(houseList, batteryList, iterations):
	# House to battery assignment
	for house in houseList:
		battery = random.choice(batteryList)
		battery.assignedHouses[house.name][1] = True

	scoreList = []
	for i in range(iterations):
		swapBool =random.choice([True, True])
		house1 = random.choice(houseList)
		house2 = random.choice(houseList)
		battery1 = 0
		battery2 = 0
		for battery in batteryList:
			if battery.assignedHouses[house1.name][1]:
				battery1 = battery
			if battery.assignedHouses[house2.name][1]:
				battery2 = battery
		if (swapBool):
			swap(battery1, battery2, house1, house2)
		else:
			assignment(battery1,battery2,house1)

		battery1.update()
		battery2.update()
		score = 0
		for battery in batteryList:
			if battery.capacityLeft < 0:
				score -= battery.capacityLeft
		scoreList.append(score)

	return scoreList


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

