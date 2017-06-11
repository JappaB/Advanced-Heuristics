import pickle
import solarHouse
import Battery


batteryPositionList = [10,10],[40,40],[25,25],[10,40],[40,10]
capacityList = [100,200,300,350,50]
batteryList = []
houseList = []
totalCapacity = 1000

def main():
	pass

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

def createBoard(boardLength, boardHeight, n_houses, n_batteries):
	""" """



	for x in range(n_batteries):
		batteryList.append(Battery.battery( position = [randint(0, boardLength), randint(0, boardHeight)] , "A", 500, [], False))

	for x in range(n_houses):
		houseList.append(solarHouse.solarpanelHouse(position = [randint(0, boardLength), randint(0, boardHeight)]))

	return houseList, batteryList

def saveBoards(n, boardLength, boardHeight, n_houses, n_batteries):
	for i in range(n):
		houseList, batteryList = createBoard(boardLength, boardHeight, n_houses, n_batteries)
		saveBoard(houseList, batteryList, "board"+str(i))
	return True

# def OpdrachtA(board):
	

### RUN PROGRAM ###
if __name__ == '__main__':
	main()