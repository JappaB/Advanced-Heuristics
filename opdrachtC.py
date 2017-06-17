import Battery
import solarHouse
import random
import HousingBlocks as blocks
import Board




def main:




def createHousesBoardC(boardLength, boardHeight, n_houses):
	""" """

	houseList = []
	houseCounter = 0
	

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

	return houseList

def plotGrid(houseList, batteryList):
	""" plots the grid """

	for house in houseList:
		# colorNow = house.batteryAssignment.color
		plt.plot([house.position[0]],[house.position[1]],  'ro', color="r")

	for battery in batteryList:
		plt.plot([battery.position[0]],[battery.position[1]],  '^', color=battery.color)

	plt.grid()
	plt.show()

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

