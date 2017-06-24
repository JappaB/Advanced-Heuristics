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
	boardNames = ["small_test_board20x20_24h"]#["finalBoard1", "finalBoard2", "finalBoard3"]
	for board in boardNames:
		f = open(board+"_C_5tot15_10keer50exitc.csv", "w")
		for wirecost in [100,0]:
			results = [[],[],[]]
			for i in range(1):
				print "wirecost: ", wirecost, "itteratie : ", i
				houseList, batteryList = loadBoard(board)
				# print houseList
				batteryOptions = [450,900,1800]
				batteryOptions = [72,288]
				batterycosts = [900,1800]
				# import cProfile, pstats, StringIO
				# pr = cProfile.Profile()
				# pr.enable()
				confList = SolverC.solverC(houseList,20,20,wirecost,batteryOptions,1.5, batterycosts  )
				# pr.disable()
				# s = StringIO.StringIO()
				# sortby = 'cumulative'
				# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
				# ps.print_stats() # TODO
				# print s.getvalue()
				# return
				results[0].append(confList[0])
				results[1].append(confList[1])
				results[2].append(confList[2])
			stri = str(wirecost)+","
			for res in results:
				stri = stri+str(np.mean(res))+","
			stri = stri+"\n"



def loadBoard(boardName):
	""" loads board with name """

	with open(boardName+'.pkl', 'rb') as input:
		inputPickle = pickle.load(input)
		houseList = inputPickle.houseList
		batteryList = inputPickle.batteryList
	return houseList, batteryList





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

