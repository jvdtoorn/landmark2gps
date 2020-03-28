# External dependencies
import cv2
import os.path
import numpy as np
import progressbar
from LatLon import *
from img_index import load_img_index
from orb_index import load_orb_index

# Configures the amount of frames processed from the input video
USE_KEYPOINTS = 2

def gps_str(latitude, longitude):
	location = LatLon(latitude, longitude)
	pp_loc_pt = location.to_string('d%|%m%|%S%|%H')
	res = []
	for cor in pp_loc_pt:
		part = cor.split('|')
		res.append(part[0] + u'\u00b0' + part[1].zfill(2) + '\'' + part[2] + '"' + part[3])
	return res[0] + " " + res[1]

def landmark2gps():

	# Load index
	img_index = load_img_index()
	orb_index = load_orb_index(img_index)

	# Ask for input video
	print("Please provide a query video.")
	video_path = raw_input("Video path: ")
	while not os.path.isfile(video_path):
		print("This video does not exist. Please check your spelling.")
		video_path = raw_input("Video path: ")

	# Calculate ORB descriptors of query video
	orb = cv2.ORB_create(256)
	cap = cv2.VideoCapture(video_path)
	q_orb_index = np.empty((USE_KEYPOINTS, 256, 32), dtype='float32')
	for i, frame_frct in np.ndenumerate(np.linspace(0.0, 1.0, USE_KEYPOINTS + 2)[1:-1]):
		cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_frct * cap.get(cv2.CAP_PROP_FRAME_COUNT)))
		_, frame = cap.read()
		_, q_desc = orb.detectAndCompute(frame, None)
		if len(q_desc) < 256: q_desc = np.vstack((q_desc, np.zeros((256 - len(q_desc), 32))))
		q_orb_index[i] = q_desc

	# Find best match
	print("Finding match in dataset...")
	highest_match_cnt = 0; highest_match_ind = -1
	flann = cv2.FlannBasedMatcher(dict(algorithm=0, trees=5), dict(checks=50))
	bar = progressbar.ProgressBar(maxval=orb_index.shape[0], widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]).start()
	for db_i in range(orb_index.shape[0]):
		bar.update(db_i)
		for q_i in range(q_orb_index.shape[0]):
			matches = flann.knnMatch(orb_index[db_i], q_orb_index[q_i], k=2)
			match_count = 0
			for m, n in matches:
				if m.distance < 0.7 * n.distance: match_count += 1
			if match_count > highest_match_cnt:
				highest_match_cnt = match_count
				highest_match_ind = db_i
	bar.finish()

	# Output the result
	print("Your input video closely resembled the landmark '{}'.".format(img_index['path'][highest_match_ind].split('_')[-1].split('.')[0]))
	print("Coordinates: " + gps_str(img_index['lat'][highest_match_ind], img_index['long'][highest_match_ind]))

if __name__ == "__main__": landmark2gps()
