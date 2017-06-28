import cv2
import numpy as np
stri = [250]
for x in range(10):
	newstri = []
	for i in range(len(stri)):
		letter = stri[i]
		if letter == 250:
			newstri = newstri + [250,250,0,0]
			# stri = stri[:i] + [250,0] + stri[1+i:]
		elif letter == 0:
			newstri = newstri + [250,250]
			# stri = stri[:i] + [250] + stri[1+i:]
		# print stri
	stri = newstri


while(np.sqrt(len(stri))%1 > 0.0):
	stri.append(0)

# print stri


stri = np.array(stri)/255.0
stri = np.matrix(stri.reshape((int(np.sqrt(len(stri))),int(np.sqrt(len(stri))))))

# print type(stri)
# # mat_array = cv2.fromarray(stri)
cv2.imshow("ba", stri)
cv2.waitKey(0)