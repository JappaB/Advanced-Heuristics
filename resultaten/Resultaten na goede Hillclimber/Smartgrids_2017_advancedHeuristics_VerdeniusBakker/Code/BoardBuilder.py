""" 

BoardbuilderClass for smartgrid case, not submitted for grading
In here are the basic tools for building a new board
Stijn Verdenius, Jasper Bakker 2017

"""


import pickle
import solarHouse
import Battery
import hillClimber as hillClimber
from random import randint
import matplotlib.pyplot as plt
import time
import Board
import numpy as np
import random

class boardBuilder:
	def __init__(self):
		pass

	def saveBoards(self, n, boardLength, boardHeight, n_houses, n_batteries):
		for i in range(n):
			houseList, batteryList = self.createBoard(boardLength, boardHeight, n_houses, n_batteries)
			self.saveBoard(houseList, batteryList, "board"+str(i), boardLength, boardHeight)
		return True


	def saveBoard(self, houseList, batteryList, boardName, width, height):
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

	def loadBoard(self, boardName):
		""" loads board with name """

		with open(boardName+'.pkl', 'rb') as input:
			inputPickle = pickle.load(input)
			houseList = inputPickle.houseList
			batteryList = inputPickle.batteryList
		return houseList, batteryList

	def manhattenDistance(self, position, goal):
		""" calculates the minimal length of the wire from base to goal """

		return sum(abs(a-b) for a,b in zip(position,goal))

	def cost(self, n_batteries, houseList, wireCost, batteryCost):
		""" calculates the cost of a setup of batteries and houses """

		cost = 0
		cost += n_batteries*batteryCost
		for house in houseList:
			cost += self.manhattenDistance(house.position, house.batteryAssignment.position)*wireCost
		return cost

	def createBoard(self, boardLength, boardHeight, n_houses, n_batteries):
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
		Battery.createBatteries(n_batteries, 1000, batteryPositionList, [], batteryList, houseList)
			# batteryList.append(Battery.battery( position = [randint(0, boardLength), randint(0, boardHeight)] , "A", 500, [], False))

		return houseList, batteryList


