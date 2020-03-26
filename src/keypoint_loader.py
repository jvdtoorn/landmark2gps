import numpy as np


def load():
	try:
		with open("../keypoint_data.txt", "r") as file:
			content = file.read()
			file.close()
			strings = content.split("|")
			keypoints = []

			print('Loading database..')

			for data in strings:
				meta_data, keypoint_string = data.split(":")
				keypoint_data = np.matrix(keypoint_string)
				keypoints.append([meta_data, keypoint_data])

			return keypoints
	except IOError:
		return -1
		
