import pickle
import solarHouse

def saveBoard(houseList, batteryList, boardName):
	""" saves board with name """

	with open(boardName+'.pkl', 'wb') as output:
		pickle.dump(houseList, output, pickle.HIGHEST_PROTOCOL)
		pickle.dump(batteryList, output, pickle.HIGHEST_PROTOCOL)
	return True

def loadBoard(boardName):
	""" loads board with name """

	with open(boardName+'.pkl', 'rb') as input:
		houseList = pickle.load(input)
		batteryList = pickle.load(input)
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

