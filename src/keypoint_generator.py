from pathlib import Path
import cv2
import numpy as np


def generate():
	content = []
	orb = cv2.ORB_create()

	print('Generating database..')

	current_folder = ""
	keypoints = []

	for path in Path('../landmarks/').rglob('*.*'):

		extention = path.name[-3 : len(path.name)]

		if extention != "jpg" and extention != "JPG":
			continue

		sub_folder = path.name[0:3]	
		if current_folder != sub_folder:
			current_folder = sub_folder
			print("New subfolder: " + current_folder)

		img = cv2.imread('../landmarks/{0}/{1}'.format(sub_folder, path.name))
		kp, des = orb.detectAndCompute(img, None)

		string_representation = np.array2string(des,threshold=np.size(des))[2 : -2]
		string_representation = string_representation.replace("]\n [", ";").replace("\n", "")
		keypoints.append([path.name, des])
	
		content.append('{0}:{1}'.format(path.name, string_representation))

	file = open("../keypoint_data.txt", "w+")
	file.write("|".join(content))
	file.close()
	return keypoints
