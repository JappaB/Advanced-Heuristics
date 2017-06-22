import pickle
import solarHouse
import Battery
import hillClimber
from random import randint
import matplotlib.pyplot as plt
import time
import Board
import numpy as np
import SolverB



def main():
	boardNames = ["finalBoard1", "finalBoard2", "finalBoard3"]
	for board in boardNames[1:3]:
		# f = open(board+"opdrachtBResults_versie1.csv", "w")
		capacities = []
		costs = []
		comptime = []
		totalcap = 1.0
		n = 1
		while(totalcap >0.0):
			houseList, batteryList = loadBoard(board)
			totalcap, finalCost, iterations = SolverB.solverB(houseList, batteryList,50,50)
			# capacities.append(totalcap)
			# costs.append(finalCost)
			# comptime.append(iterations)

			print n, " :anus ", totalcap, finalCost, iterations
			n += 1
			# f.write(str(totalcap)+","+ str(finalCost)+","+ str(iterations)+"\n")

		# plt.plot(range(100),capacities)
		# plt.show()
		# plt.plot(range(100),costs)
		# plt.show()
		# plt.plot(range(100),comptime)
		# plt.show()

		plotGrid(houseList, batteryList)



def loadBoard(boardName):
	""" loads board with name """

	with open(boardName+'.pkl', 'rb') as input:
		inputPickle = pickle.load(input)
		houseList = inputPickle.houseList
		batteryList = inputPickle.batteryList
	return houseList, batteryList


def plotGrid(houseList, batteryList):
	""" plots the grid """

	for house in houseList:
		colorNow = 0
		for battery in batteryList:
			if (battery.assignedHouses[house.name][1]):
				colorNow = battery.color
		plt.plot([house.position[0]],[house.position[1]],  'ro', color=colorNow)

	for battery in batteryList:
		plt.plot([battery.position[0]],[battery.position[1]],  '^', color=battery.color)

	plt.grid()
	plt.show()

def changeCapacity(batteryList, factor):
	for battery in batteryList:
		battery.capacity = int(battery.capacity*factor)

### RUN PROGRAM ###
if __name__ == '__main__':
	main()

