""" 

BoardClass for smartgrid case, not submitted for grading
Stijn Verdenius, Jasper Bakker 2017

"""

class board:
	def __init__(self):
		self.height = 0
		self.width = 0
		self.n_houses = 0
		self.n_batteries = 0
		self.houseList =  []
		self.batteryList = []