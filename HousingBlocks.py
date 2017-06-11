from random import randint
import solarHouse
import numpy as np

class housingBlockA :

	def __init__(self, postion):

		self.boundaryX = 3
		self.boundaryY = 5

		self.house1 = solarHouse.solarpanelHouse(list(np.array([1,1])+ position))
		self.house2 = solarHouse.solarpanelHouse(list(np.array([1,2])+ position))
		self.house3 = solarHouse.solarpanelHouse(list(np.array([1,3])+ position))
		self.house4 = solarHouse.solarpanelHouse(list(np.array([1,4])+ position))
		self.house5 = solarHouse.solarpanelHouse(list(np.array([2,1])+ position))
		self.house6 = solarHouse.solarpanelHouse(list(np.array([2,2])+ position))
		self.house7 = solarHouse.solarpanelHouse(list(np.array([2,3])+ position))
		self.house8 = solarHouse.solarpanelHouse(list(np.array([2,4])+ position))


class housingBlockB :

	def __init__(self, postion):

		self.boundaryX = 5
		self.boundaryY = 3

		self.house1 = solarHouse.solarpanelHouse(list(np.array([1,1])+ position))
		self.house2 = solarHouse.solarpanelHouse(list(np.array([2,1])+ position))
		self.house3 = solarHouse.solarpanelHouse(list(np.array([3,1])+ position))
		self.house4 = solarHouse.solarpanelHouse(list(np.array([4,1])+ position))
		self.house5 = solarHouse.solarpanelHouse(list(np.array([1,2])+ position))
		self.house6 = solarHouse.solarpanelHouse(list(np.array([2,2])+ position))
		self.house7 = solarHouse.solarpanelHouse(list(np.array([3,2])+ position))
		self.house8 = solarHouse.solarpanelHouse(list(np.array([4,2])+ position))