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
from copy import deepcopy


def main222():

	# with open("finalBoard3_CanalyseConstructiefJasperr.csv", "r") as f:
	# 	f.readline()
	# 	for line in f:
	# 		print line
	# 		[float(x) for x in line.split(",")[1:]]

	# cs1 = np.genfromtxt("finalBoard1_CanalyseConstructiefJasper.csv", delimiter=",", dtype=None)
	cs2 = np.loadtxt("finalBoard2_CanalysePartThree9&10ConstructiefStijn.csv",dtype=float,delimiter=',',skiprows=1,usecols=(1,2))
	cs3 = np.loadtxt("finalBoard3_CanalysePartThree9&10ConstructiefStijn.csv",dtype=float,delimiter=',',skiprows=1,usecols=(1,2))

	cs1 = np.loadtxt("finalBoard1_CanalysePartThree9&10ConstructiefStijn.csv",dtype=float,delimiter=',',skiprows=1,usecols=(1,2))
	conf = np.loadtxt("finalBoard3_CanalysePartThree9&10ConstructiefStijn.csv",dtype="str",delimiter=',',skiprows=1,usecols=(0))
	results = []
	# for c in conf:
	# print cs2

	# print len(conf), 46
	for i in range(len(cs1[0])):
		score1 = np.argsort(-1*cs1[:,i])
		score2 = np.argsort(-1*cs2[:,i])
		score3 = np.argsort(-1*cs3[:,i])
		scoretotal = [0 for x in range(len(score1))]
		# print score1

		for j in range(len(score1)):

			scoretotal[score1[j]] += j
			scoretotal[score2[j]] += j
			scoretotal[score3[j]] += j

		scoretotal = np.array(scoretotal)/3
		results.append(scoretotal)
		# print scoretotal


	# # print np.array(results).T
	# ratios = [conf,[],[]]
	# for c in conf:
	# 	ratio1 = 0
	# 	ratio1 = (float(c[-1]))/(int(c[0])+int(c[-1]))
	# 	ratio2 = (float(c[-1])*1800)/((int(c[0])*450)+(int(c[-1])*1800))
	# 	ratios[1].append(ratio1)
	# 	ratios[2].append(ratio2)

	output = results

	output =  np.array(output).T
	g = open("wireLengthResultsPartThree.csv", "w")
	g.write("9,10\n")
	for y in output:
		stri = ""
		for x in y:
			stri = stri + str(x) + ","
		stri = stri + "\n"
		g.write(stri)



def main():
	# boardNames = ["small_test_board20x20_24h"]#["finalBoard1", "finalBoard2", "finalBoard3"]
	boardNames = ["finalBoard1", "finalBoard2", "finalBoard3"]

	for board in boardNames[:]:
		f = open(board+"_CanalysePartFour9&10ConstructiefJasperDonderdag.csv", "w")
		f.write("conf,9,10,11,batterycost\n")
		houseList, batteryList = loadBoard(board)
		batteryOptions = [450,900,1800]
		batterycosts = [900,1350,1800]
		possibleConfigurations = precalculateCapacities(houseList, batteryOptions)
		print len(possibleConfigurations)
		for conf in possibleConfigurations:
			# print countBatteries(conf, batteryOptions)
			stri = str(countBatteries(conf, batteryOptions)[0])+" | "+str(countBatteries(conf, batteryOptions)[1])+" | "+str(countBatteries(conf, batteryOptions)[2])+","
			batterycost = 0
			for wirecost in [9,10,11]:
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

	for x in range(36):
		for y in range(18):
			for z in range(9):
				cap = x*batteryOptions[0] + y*batteryOptions[1] + z*batteryOptions[2]
				if (cap == 9000):#(cap >totalCapacity*1.005) and (cap < totalCapacity*1.5):
					confList = [batteryOptions[0] for i in range(x)] + [batteryOptions[1] for j in range(y)] + [batteryOptions[2] for j in range(z)]
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

