import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
import numpy as np




class plotter:
	def __init__(self):
		pass

	def walkPlot(self, walk, method=None):

		if method == None:
			plt.plot(range(len(walk)),walk)
			plt.show()
		else:
			fig = plt.figure()
			ax = fig.add_subplot(111, projection='3d')
			sq = math.sqrt(len(walk))
			Z = np.reshape(walk, (sq,sq))
			X = np.arange(0, sq, 1)
			Y = np.arange(0, sq, 1)
			X, Y = np.meshgrid(X, Y)
			ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
			plt.show()

	def plotGrid(self, houseList, batteryList, boardLength, boardHeight, method = "A"):
		""" plots the grid """

		fig, ax = plt.subplots()
		for house in houseList:
			colorNow = ""
			if (method == "A"):
				colorNow = "r"
			else:
				colorNow = house.batteryAssignment.color
			plt.plot([house.position[0]],[house.position[1]],  'ro', color=colorNow)

		for battery in batteryList:
			plt.plot([battery.position[0]],[battery.position[1]],  '^', color=battery.color)


		major_ticks = np.arange(0, boardLength+1, 10)                                              
		minor_ticks = np.arange(0, boardHeight+1, 1)                                               

		ax.set_xticks(major_ticks)                                                       
		ax.set_xticks(minor_ticks, minor=True)                                           
		ax.set_yticks(major_ticks)                                                       
		ax.set_yticks(minor_ticks, minor=True)                                           

		# and a corresponding grid                                                       

		ax.grid(which='both')                                                            

		# or if you want differnet settings for the grids:                               
		ax.grid(which='minor', alpha=0.2)                                                
		ax.grid(which='major', alpha=0.5)

		plt.grid()
		plt.show()

	def plotPicture(self, houseList, batteryList, boardLength, boardHeight):
		x = []
		y = []
		for house in houseList:
			x.append(house.position[0])
			y.append(house.position[1])
		ind = np.argsort(y)[::-1]
		xnew = []
		ynew = []
		for i in ind:
			ynew.append(y[i])
			xnew.append(x[i])
		image_path = "huis.png"
		fig, ax = plt.subplots()
		self.imscatter(xnew, ynew, image_path, zoom=0.1, ax=ax)
		x = []
		y = []
		for battery in batteryList:
			x.append(battery.position[0])
			y.append(battery.position[1])
		image_path = "battery.png"
		self.imscatter(x, y, image_path, zoom=0.1, ax=ax)
		
		major_ticks = np.arange(0, boardLength+1, 10)                                              
		minor_ticks = np.arange(0, boardHeight+1, 1)                                               

		ax.set_xticks(major_ticks)                                                       
		ax.set_xticks(minor_ticks, minor=True)                                           
		ax.set_yticks(major_ticks)                                                       
		ax.set_yticks(minor_ticks, minor=True)                                           

		# and a corresponding grid                                                       

		ax.grid(which='both')                                                            

		# or if you want differnet settings for the grids:                               
		ax.grid(which='minor', alpha=0.2)                                                
		ax.grid(which='major', alpha=0.5)
		plt.show()


	def imscatter(self, x, y, image, ax=None, zoom=1):
		if ax is None:
			ax = plt.gca()
		try:
			image = plt.imread(image)
		except TypeError:
			# Likely already an array...
			pass
		im = OffsetImage(image, zoom=zoom)
		x, y = np.atleast_1d(x, y)
		artists = []
		for x0, y0 in zip(x, y):
			ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
			artists.append(ax.add_artist(ab))
		ax.update_datalim(np.column_stack([x, y]))
		ax.autoscale()
		return artists




