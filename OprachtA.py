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
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


# batteryPositionList = [10,10],[40,40],[25,25],[10,40],[40,10]

capacityListOriginal = [100,200,300,350,50]
capacityList = capacityListOriginal

totalCapacity = 1000


def main3():
	saveBoards(3,50,50,150,5)
	boardNames = ["board0", "board1", "board2"]
	deviations = [12,10,6]
	capacities = [520,515,505]

	for i in range(len(boardNames)):
		board = boardNames[i]
		houseList, batteryList = loadBoard(board)
		newCapacities = [capacities[i] for x in range(5)]
		changeCapacityTo(batteryList, newCapacities)
		deviation = deviations[i]
		changeDeviation(houseList, deviation, 13, 2500)

		newBoard = Board.board()

		newBoard.height = 50
		newBoard.width = 50
		newBoard.n_houses = 150
		newBoard.n_batteries = 5
		newBoard.houseList =  houseList
		newBoard.batteryList = batteryList

		with open(boardName+'_walk.pkl', 'wb') as output:
			pickle.dump(newBoard, output, pickle.HIGHEST_PROTOCOL)







def main():
	boardNames = ["board0", "board1", "board2"]
	for board in boardNames[0:1]:
		

		walks = {}
		walks['mean'] = []
		walks['median'] = []
		walks['solutions'] = []
		walks['dev'] = []
		for i in range(100):
			print "walk ", i
			houseList, batteryList = loadBoard(board)
			newCapacities = [505 for x in range(5)]
			changeCapacityTo(batteryList, newCapacities)
			changeDeviation(houseList, 4, 13, 2500)
			# a,b,c,walk = hillClimber.hillClimber(100,houseList,batteryList) #
			walk = randomWalker(houseList, batteryList, 10000)
			walks['mean'].append(np.mean(walk))
			walks['median'].append(np.median(walk))
			walks['dev'].append(np.std(walk))
			counter = 0
			for w in walk:
				if w == 0:
					counter += 1
			walks['solutions'].append(counter)

		with open(board+'cap505dev5_walk.pkl', 'wb') as output:
			pickle.dump(walks, output, pickle.HIGHEST_PROTOCOL)

		print "mean ", np.mean(walks['mean']) ," median ", np.mean(walks['median']), " max solutions per walk : ", max(walks['solutions']), " mean solutions per walk : ",np.mean(walks['solutions']), " amount of walks without solution : ", walks['solutions'].count(0) , " dev gem ", np.mean(walks['dev'])
		# print walks
		# Z = np.reshape(walk, (1000,1000))
		# X = np.arange(0, 1000, 1)
		# Y = np.arange(0, 1000, 1)
		# X, Y = np.meshgrid(X, Y)


		# ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
		# plt.show()

		# plt.plot(range(len(walk)),walk)

		# plt.show()




def main2():
	boardNames = ["board0", "board1", "board2", "board3", "board4"]
	for board in boardNames[0:1]:
	# saveBoards(5,50,50,150,5)
		f = open(board+"Stijn_sneller520_findSigmoidDeviation1_24_batt500_capacity_2500.csv", "w")
		results2 = []
		for x in range(1,24):
			results1 = [[],[],[]]
			temp = 0
			for i in range(100):
				start_time = time.time()
				deviation = x*0.5
				newCapacities = [520,520,520,520,520]
				houseList, batteryList = loadBoard(board)
				changeCapacityTo(batteryList, newCapacities)
				# changeCapacity(batteryList, newCapacities)
				changeDeviation(houseList, deviation, 13, 2500)

				cost, overCapacity, itt = hillClimber.hillClimber(100, houseList, batteryList )
				results1[0].append(cost)
				results1[1].append(overCapacity)
				results1[2].append(itt)
				solveableCheck = True
				for battery in batteryList:
					if (battery.overCapacitated == True):
						solveableCheck = False

				# for battery in batteryList:
				# 	print battery.capacityLeft
				# 	print battery.capacity
				# 	print battery.overCapacitated
				# 	print ""

				# print overCapacity

				# return


				if solveableCheck:
					temp += 1

				Elapsed = (time.time() - start_time)
				print "working on #",str(x/2.0), "% cost : ", cost, " overCapacity : ", overCapacity, " iterations : ", itt, " in ", Elapsed, " solveable : ", solveableCheck

			results2.append(temp)
			print "percentage : ", temp, "%"

			f.write(str(np.mean(results1[0]))+","+str(np.mean(results1[1]))+","+str(np.mean(results1[2]))+","+str(temp)+"\n")
		
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

