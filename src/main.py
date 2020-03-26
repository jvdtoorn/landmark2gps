import numpy as np
import cv2
from video_tools import *
import glob
import feature_extraction as ft
from scikits.talkbox.features import mfcc
import scipy.io.wavfile as wav
import time
import calendar

if __name__ == "__main__": 
	S = 0
	E = 3

	video_files = glob.glob("../queries/*.3gp")

	video = video_files[0]

	frame_count = get_frame_count(video) + 1
	frame_rate = get_frame_rate(video)

	cap = cv2.VideoCapture(video)

	prev_frame = None

	cap.set(cv2.CAP_PROP_POS_MSEC, S * 1000)

	orb = cv2.ORB_create()
	matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

	while (cap.isOpened() and cap.get(cv2.CAP_PROP_POS_MSEC) < (E * 1000)):

		retVal, frame = cap.read()

		if retVal == False:
			break

		cv2.imshow('Video', frame)

		kp1, des1 = orb.detectAndCompute(frame, None)			
		kp2, des2 = orb.detectAndCompute(frame, None)

		start = time.time()
		matches = matcher.match(des1, des2)
		matches = sorted(matches, key = lambda x:x.distance)
		end = time.time()

		print('Total time: {0}'.format(end - start))
	
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		prev_frame = frame

	cap.release()
	cv2.destroyAllWindows()
