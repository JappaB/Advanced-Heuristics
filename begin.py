import numpy as np
from random import randint
import individualClass as ind
import math
import math
import netlists
import firstSolution
from random import shuffle
from copy import deepcopy
from numpy.random import choice
import multiprocessing
import threading
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random


class Fitting:

	def guidedWirelength(self, pathList):
		""" calculates the distance of a path """

		return len(pathList)-1

	def manhattenDistance(self, position, goal):
		""" calculates the minimal length of the wire from base to goal """

		return sum(abs(a-b) for a,b in zip(position,goal))


	def possibleMoves(self, position, boardHeight, boardLength):
		""" evaluates possible moves in the grid """

		unityVectors = [[1,0,0],[0,1,0],[0,0,1],[-1,0,0],[0,-1,0],[0,0,-1]]
		posList = []

		# add all unityvectors to the current position
		for vector in unityVectors:
			newVector = list((a+b) for a,b in zip(position,vector))

			# don't add it if it's going off board
			if ((newVector[1] > boardHeight) or (newVector[0] > boardLength) or (any(i < 0 for i in newVector)) or (newVector[2] > 7)):
				continue
			else:
				posList.append(newVector)
		return posList


	def aStar(self, position, target, evaluatedStates, genome, board):
		""" recreates a path from position to target, evading the occupied slots """

		# add the origin to visited states
		evaluatedStates.add(tuple(position))

		# initiation the walkedpath library
		camefrom = {}

		# start with the startposition
		openStates = [(np.array(position),0,0)]

		# simultaniously keep track of a scorelist
		scoreList = [0]

		# caculate the onionrings around the target
		aroundTarget = []
		if (genome[2] > 0 or genome[3] > 0):
			aroundTarget = list(self.netlistObject.possibleMoves(np.array(target), board))

		# initiate amount of iterationscounter
		i = 0

		# while the path is not found or end of the state space reached 
		while(openStates):
			
			# find the state with the lowest score
			leastIndex = np.argmin(scoreList)
			currentState = openStates.pop(leastIndex)
			scoreList.pop(leastIndex)

			# if the goal is reached, recreate the path and return
			if (np.array_equal(currentState[0], target)):
				# print "found in ", i , " steps"
				return self.printcame(camefrom, target)

			# expand possiblemoves
			for possible in self.possibleMoves(currentState[0], genome, board):

				
				possibleTuple = tuple(possible)

				# if the new possible is the target, return the path
				if (possibleTuple == target):
					camefrom[str(possible)] = currentState
					return self.printcame(camefrom, target)

				# if the new possible is already evaluated, skip it
				elif (possibleTuple in evaluatedStates):
					continue

				else:
					# calculate scores
					newF = self.stepWeight(possibleTuple, aroundTarget, genome, board)
					newH = self.manhattenDistance(possible, target)
					f_score = currentState[2] + newF
					h_score = newH
					totalscore = h_score + f_score

					# add scores
					scoreList.append(totalscore)
					openStates.append((possible,h_score,f_score))

					# save where the state came from
					camefrom[str(possible)] = currentState

					# add the state to already evaluated
					evaluatedStates.add(possibleTuple)
			i += 1

	def stepWeight(self, position, target, genome, board):
		""" calculates the Astar movementcost """

		# initialcost is 1
		cost = 1

		# add heatvalue if applicable
		if (genome[4] > 0):
			try: 
				cost = self.netlistObject.heatValue(position, genome[4], genome[1], board)
			except: 
				print genome, "heatmap is still off"
				return 'error'

		# add onions if applicable
		if ((genome[2] > 0 or genome[3] > 0) and position[2] < 3):
			highcostlist1, highcostlist2 = self.netlistObject.costlyPositions1_2, self.netlistObject.costlyPositions2_2
			aroundTarget1, aroundTarget2  = target[0], target[1]
			# line can only come near net if it is the targetnet
			if (position in aroundTarget1):
				cost += genome[2]
			elif (position in aroundTarget2):
				cost += genome[3]
			elif (position in highcostlist2):
				cost += 9999999999999*genome[3]
			elif (position in highcostlist1):
				cost += 9999999999999999999999*genome[2]
		return cost


	def printcame(self, dicti, start):
		""" recreates the path walked from base to target """

		Walklist = []
		temp = list(start)
		for n in dicti:
			Walklist.append(list(temp))
			try:
				temp = dicti[str(temp)][0]
			except:
				return Walklist

	def testAstar(self, start = [5,5,5], goal=[1,1,1], obstructed = set()):
		""" testing aStar method """

		a = set()
		pathlist = self.aStar(tuple(start),tuple(goal), a, [0,0,0,0,0], self.netlistObject.board1)
		print pathlist