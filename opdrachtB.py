import pickle
import solarHouse
import Battery
import hillClimber
from random import randint
import matplotlib.pyplot as plt
import time
import Board
import numpy as np


# batteryPositionList = [10,10],[40,40],[25,25],[10,40],[40,10]

capacityListOriginal = [1000,1000,1000,1000,1000]
capacityList = capacityListOriginal

totalCapacity = 1000

def main():
	boardNames = ["board0", "board1", "board2", "board3", "board4"]
	for board in boardNames[0:1]:
		f = open(board+"JasperOpdrachtB-Board0-bestScoreEachCentroid.csv", "w")
		for i in range(100):
			start_time = time.time()
			# deviation = x*0.5
			newCapacities = [515,515,515,515,515]
			houseList, batteryList = loadBoard(board)
			changeCapacityTo(batteryList, newCapacities)
			# changeCapacity(batteryList, newCapacities)
			changeDeviation(houseList, deviation, 13, 2500)

			cost, overCapacity, itt = hillClimber.hillClimber(100, houseList, batteryLists)
			results1[0].append(cost)
			results1[1].append(overCapacity)
			results1[2].append(itt)
			solveableCheck = True
			for battery in batteryList:
				if (battery.overCapacitated == True):
					solveableCheck = False

			if solveableCheck:
				temp += 1

			Elapsed = (time.time() - start_time)
			print "working on #",x, "\% cost : ", cost, " overCapacity : ", overCapacity, " iterations : ", itt, " in ", Elapsed, " Solved =  ", solveableCheck

		results2.append(temp)

		f.write(str(np.mean(results1[0]))+","+str(np.mean(results1[1]))+","+str(np.mean(results1[2]))+","+str(temp)+"\n")
		
		print results2
		plt.plot(range(len(results2)),results2)
		plt.show()
	



def saveBoard(houseList, batteryList, boardName, width, height):
	""" saves board with name """

	board = Board.board()
	board.batteryList = batteryList
	board.houseList = houseList
	board.height = height
	board.width = width
	board.n_houses = len(houseList)
	board.n_batteries = len(batteryList)
	with open(boardName+'.pkl', 'wb') as output:
		pickle.dump(board, output, pickle.HIGHEST_PROTOCOL)
		# pickle.dump(batteryList, output, pickle.HIGHEST_PROTOCOL)
	return True

def loadBoard(boardName):
	""" loads board with name """

	with open(boardName+'.pkl', 'rb') as input:
		inputPickle = pickle.load(input)
		houseList = inputPickle.houseList
		batteryList = inputPickle.batteryList
	return houseList, batteryList

def manhattenDistance(position, goal):
	""" calculates the minimal length of the wire from base to goal """

	return sum(abs(a-b) for a,b in zip(position,goal))

def cost(n_batteries, houseList, wireCost, batteryCost):
	""" calculates the cost of a setup of batteries and houses """

	cost = 0
	cost += n_batteries*batteryCost
	for house in houseList:
		cost += manhattenDistance(house.position, house.batteryAssignment.position)*wireCost
	return cost

def createBoard(boardLength, boardHeight, n_houses, n_batteries):
	""" """

	batteryList = []
	houseList = []

	housePositionList = []
	for x in range(n_houses):
		newPosition = [randint(0,boardLength), randint(0,boardHeight)]
		for x in housePositionList:
			if (tuple(x) == tuple(newPosition)):
				newPosition[0] = (newPosition[0] + randint(-2,2)) % boardLength
				newPosition[1] = (newPosition[1] + randint(-2,2)) % boardHeight
		housePositionList.append(newPosition)
	for x in range(n_houses):
		houseList.append(solarHouse.solarpanelHouse("house" + str(x), randint(5,10), position = housePositionList[x]))

	batteryPositionList =[]
	for x in range(n_batteries):
		newPosition = [randint(0,boardLength), randint(0,boardHeight)]
		for x in batteryPositionList:
			if (tuple(x) == tuple(newPosition)):
				newPosition[0] = (newPosition[0] + 1) % boardLength
				newPosition[1] = (newPosition[1] + 1) % boardHeight
		for x in housePositionList:
			if (tuple(x) == tuple(newPosition)):
				newPosition[0] = (newPosition[0] + randint(-2,2)) % boardLength
				newPosition[1] = (newPosition[1] + randint(-2,2)) % boardHeight
		batteryPositionList.append(newPosition)
	Battery.createBatteries(n_batteries, 1000, batteryPositionList, capacityList, batteryList, houseList)
		# batteryList.append(Battery.battery( position = [randint(0, boardLength), randint(0, boardHeight)] , "A", 500, [], False))

	return houseList, batteryList

def saveBoards(n, boardLength, boardHeight, n_houses, n_batteries):
	for i in range(n):
		houseList, batteryList = createBoard(boardLength, boardHeight, n_houses, n_batteries)
		saveBoard(houseList, batteryList, "board"+str(i), boardLength, boardHeight)
	return True

def plotGrid(houseList, batteryList):
	""" plots the grid """

	for house in houseList:
		# colorNow = house.batteryAssignment.color
		plt.plot([house.position[0]],[house.position[1]],  'ro', color="r")

	for battery in batteryList:
		plt.plot([battery.position[0]],[battery.position[1]],  '^', color=battery.color)

	plt.grid()
	plt.show()

def changeCapacity(batteryList, factor):
	for battery in batteryList:
		battery.capacity = int(battery.capacity*factor)

def randomBatteryPositions(batteryList):

	for battery in batteryList:
		battery.position = ([random.choice([0,Board.board.width]),random.choice([0,Board.board.height])])


### RUN PROGRAM ###
if __name__ == '__main__':
	main()

