import pickle
import solarHouse
import Battery
import hillClimber
from random import randint
import matplotlib.pyplot as plt
import time
import Board
import numpy as np
import random


# batteryPositionList = [10,10],[40,40],[25,25],[10,40],[40,10]

capacityListOriginal = [100,200,300,350,50]
capacityList = capacityListOriginal

totalCapacity = 1000

def main():
	boardNames = ["board0", "board1", "board2", "board3", "board4"]
	for board in boardNames[0:1]:
		f = open(board+"Stijn_findSigmoidDeviation1_24_batt500_capacity_2500.csv", "w")
		results2 = []
		for x in range(1,6):
			results1 = [[],[],[]]
			temp = 0
			for i in range(1):
				start_time = time.time()
				deviation = x*0.5
				newCapacities = [500,500,500,500,500]
				houseList, batteryList = loadBoard(board)
				changeCapacityTo(batteryList, newCapacities)
				# changeCapacity(batteryList, newCapacities)
				changeDeviation(houseList, deviation, 13, 2500)

				cost, overCapacity, itt = hillClimber.hillClimber(50, houseList, batteryList )
				results1[0].append(cost)
				results1[1].append(overCapacity)
				results1[2].append(itt)
				solveableCheck = True
				for battery in batteryList:
					if (battery.overCapacitated == True):
						solveableCheck = False

				for battery in batteryList:
					print battery.capacityLeft
					print battery.capacity
					print battery.overCapacitated
					print ""

				print overCapacity

				return


				if solveableCheck:
					temp += 1

				Elapsed = (time.time() - start_time)
				print "working on #",x, "\% cost : ", cost, " overCapacity : ", overCapacity, " iterations : ", itt, " in ", Elapsed

			results2.append(temp)

			f.write(str(np.mean(results1[0]))+","+str(np.mean(results1[1]))+","+str(np.mean(results1[2]))+"\n")
		
		print results2
		plt.plot(range(len(results2)),results2)
		plt.show()






def main1():
	# saveBoards(5, 50, 50, 150, 5)
	boardNames = ["board0", "board1", "board2", "board3", "board4"]
	for board in boardNames[4:5]:
		f = open(board+"Jasper105-115-40it-sample100cap100_200_300_350_50.csv", "w")
		for x in range(105,115):
			for i in range(100):
				
				houseList, batteryList = loadBoard(board)
				changeCapacity(batteryList, x*0.01)
				start_time = time.time()
				cost, overCapacity, itt = hillClimber.hillClimber(40, houseList, batteryList )
				Elapsed = (time.time() - start_time)
				print "working on #",x, " cost : ", cost, " overCapacity : ", overCapacity, " iterations : ", itt, " in ", Elapsed
				results[0].append(cost)
				results[1].append(overCapacity)
				results[2].append(Elapsed)
				results[3].append(itt)
			# f.write(str(cost)+","+str(overCapacity)+","+str(Elapsed)+","+str(itt)+"\n")
			f.write(str(np.mean(results[0]))+","+str(np.mean(results[1]))+","+str(np.mean(results[2]))+","+str(np.mean(results[3]))+"\n")



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




### RUN PROGRAM ###
if __name__ == '__main__':
	main()

