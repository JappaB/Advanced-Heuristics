import Battery
import solarHouse
import random
import HousingBlocks as blocks
import Board
import hillClimber
from random import randint
import matplotlib.pyplot as plt
import time
import numpy as np
# import SolverC as SolverB
import SolverB
import SolverC
import pickle




def main():
	# boardNames = ["small_test_board20x20_24h"]#["finalBoard1", "finalBoard2", "finalBoard3"]
	boardNames = ["finalBoard1", "finalBoard2", "finalBoard3"]

	for board in boardNames[:]:
		f = open(board+"_CanalysePartTwo75-90ConstructiefJasperrr.csv", "w")
		f.write("conf,7.5,7.75,8.25,8.5,8.75,batterycost\n")
		houseList, batteryList = loadBoard(board)
		batteryOptions = [450,1800]
		batterycosts = [900,1800]
		possibleConfigurations = precalculateCapacities(houseList, batteryOptions)
		for conf in possibleConfigurations:
			stri = str(countBatteries(conf, batteryOptions)[0])+" | "+str(countBatteries(conf, batteryOptions)[1])+","
			batterycost = 0
			for wirecost in [7.5,7.75,8.25,8.5,8.75]:
				print board, "  | configuration : ", countBatteries(conf, batteryOptions), " wirecost : ", wirecost
				houseList, batteryList = loadBoard(board)
				cost, batterycost = SolverC.solverC(houseList,50,50,wirecost,batteryOptions, batterycosts, conf)
				stri = stri + str(cost)+ ","
			stri = stri + str(batterycost) +"\n"
			f.write(stri)	

def precalculateCapacities(houseList,batteryOptions):
	totalCapacity = 0
	for house in houseList:
		totalCapacity += house.netto

	print totalCapacity

	possibleConfigurations = []

	for x in range(34):
		for y in range(9):
			cap = x*batteryOptions[0] + y*batteryOptions[1]
			if (cap >totalCapacity*1.005) and (cap < totalCapacity*1.5):
				confList = [batteryOptions[0] for i in range(x)] + [batteryOptions[1] for j in range(y)]
				possibleConfigurations.append(confList)
	return possibleConfigurations

def loadBoard(boardName):
	""" loads board with name """

	with open(boardName+'.pkl', 'rb') as input:
		inputPickle = pickle.load(input)
		houseList = inputPickle.houseList
		batteryList = inputPickle.batteryList
	return houseList, batteryList


def countBatteries(batteryConfiguration, batteryOptions):
	countlist = []
	for i in range(len(batteryOptions)):
		countlist.append(batteryConfiguration.count(batteryOptions[i]))

	return countlist


# def createHousesBoardC(boardLength, boardHeight, n_houses):
# 	""" """

# 	houseList = []
# 	houseCounter = 0
	

# 	housePositionList = []
# 	for x in range(n_houses):
# 		newPosition = [randint(0,boardLength), randint(0,boardHeight)]
# 		for x in housePositionList:
# 			if (tuple(x) == tuple(newPosition)):
# 				newPosition[0] = (newPosition[0] + randint(-2,2)) % boardLength
# 				newPosition[1] = (newPosition[1] + randint(-2,2)) % boardHeight
# 		housePositionList.append(newPosition)
# 	for x in range(n_houses):
# 		houseList.append(solarHouse.solarpanelHouse("house" + str(x), randint(5,10), position = housePositionList[x]))

# 	return houseList


### RUN PROGRAM ###
if __name__ == '__main__':
	main()

