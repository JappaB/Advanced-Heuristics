import random

class battery:

	def __init__(self):
		self.position = [0,0]
		self.name = ""
		self.color = "#%06x" % random.randint(0, 0xFFFFFF)