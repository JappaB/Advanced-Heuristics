# check = []
# 		for i in range(len(houseList)):
# 			check.append(0)
# 			house = houseList[i]
# 			for battery in batteryList:
# 				if (battery.assignedHouses[house.name][1]):
# 					check[i] += 1

# 		print "before ", check.count(1)

import time

for i in range(100):
    time.sleep(0.1)
    print 'Downloading File FooFile.txt [%d%%]\r'%i,