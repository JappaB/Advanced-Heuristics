""" 

HouseClass for smartgrid case, not submitted for grading
Stijn Verdenius, Jasper Bakker 2017

"""

class solarpanelHouse:

	def __init__(self, name, netto = 0, position = [0,0]):
		self.name = name
		self.netto = netto
		self.position = position
		self.batteryAssignment = None