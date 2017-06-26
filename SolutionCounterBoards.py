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

		'''Vul hier in hoe je de data wilt verkrijgen, hoeveel iteraties per bord/stddev combinatie, etc.'''
		ITERATIONS = 500
		EXITHC = 23000
		
		'''Hieronder wordt het bord doorgelopen voor een batterijcapaciteit die steeds 2.5 percent
		omhoog gaat. Van 502.5 tot 520. De st. dev output verandert nog steeds op dezelfde manier.'''
		f = open(board+"Unique solutioncounter - Iterations - "+str(ITERATIONS)+" -ExitHC - "+str(EXITHC)+" -.csv", "w")
		f.write("Cost,Reset,Iterations,Solved,TimeInHC,TotalOvercap,board,uniqueSolutions\n")
		results1 = [[],[],[],[],[],[]]
		solved = 0
		uniqueSolutions = set()
		firstSolution = True

		for j in range(ITERATIONS):

			houseList, batteryList = loadBoard(board)

			# House to battery assignment
			for house in houseList:
				battery = random.choice(batteryList)
				battery.assignedHouses[house.name][1] = True


			start_time = time.time()
			cost, reset, itt = hillClimber.hillClimber(EXITHC, houseList, batteryList)
			TimeInHC = (time.time() - start_time)
			results1[0].append(cost)
			results1[1].append(reset)
			results1[2].append(itt)
			results1[3].append(TimeInHC)

			solveableCheck = True
			TotalOvercap = 0


			if (battery.overCapacitated == True):
				# print battery.overCapacitated
				solveableCheck = False
				TotalOvercap -= battery.capacityLeft
				results1[4].append(TotalOvercap)


			if solveableCheck:
				solved += 1
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


				#Turn  list of houses to tuple and put in set of uniquesolutions


				solutionTuple = tuple(solution)
				for i in range(10):
					uniqueSolutions.add(solutionTuple)



			# if solveableCheck:
			# 	solved += 1
			# 	solution = []
			# 	if firstSolution:
			# 		# create a list of assigned houses per battery and put in 'solution'
			# 		for battery in batteryList:
			# 			housesInBat = []
			# 			for house in battery.assignedHouses:
			# 				if house[1] == True:
			# 					housesInBat.append(house)
			# 			solution.append(housesInBat)
			# 		uniqueSolutions.append(solution)
			# 		print solution		
			# 		firstSolution = False

			# 	if firstSolution == False:
			# 		# create a list of assigned houses per battery and put in 'solution'
			# 		for battery in batteryList:
			# 			housesInBat = []
			# 			for house in battery.assignedHouses:
			# 				if house[1] == True:
			# 					housesInBat.append(house)
			# 			solution.append(housesInBat)

			# 		for i in range(len(uniqueSolutions)):
			# 			batteryIsSame = 0
			# 			for batterySolList in uniqueSolutions[i]:
			# 				for batr in range(len(batterySolList)):
			# 					print "len battery solution list", len(batterySolList)
								# compare = set(batterySolList).difference(solution[batr])
								# # print compare
								# # print bool(compare)
								# # return
			# 					if bool(compare) == False:
			# 						batteryIsSame += 1
			# 						# uniqueSolution = True
			# 					print "solution number: ", "solution nr", i,"batterynumber",batr, batteryIsSame
			# 		if batteryIsSame == 5:
			# 			print batteryIsSame
			# 			print "no new solution"
			# 		else:
			# 			print batteryIsSame
			# 			print "new solution"
			# 			uniqueSolutions.append(solution)
			# 			break








			




			numberOfUniqueSolutions = len(uniqueSolutions)

			print "Working on: ",board, ", cost: ", cost,", resets: ", reset, ", itt: " , itt, ", TimeInHC, ", TimeInHC, " solveable : ", solved,"/",j+1,"unique",numberOfUniqueSolutions,"/",solved , " TotalOvercap: ", TotalOvercap, "\n"





		f.write(str(np.mean(results1[0]))+","+str(np.mean(results1[1]))+","+str(np.mean(results1[2]))+","+str(solved)+","+str(np.mean(results1[3]))+","+str(np.mean(results1[4]))+","+str(board)+","+str(numberOfUniqueSolutions)+"\n")




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

