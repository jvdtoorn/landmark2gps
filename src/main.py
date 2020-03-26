import numpy as np
import cv2
import matplotlib.pyplot as plt
from video_tools import *
import feature_extraction as ft
from scikits.talkbox.features import mfcc
import scipy.io.wavfile as wav

if __name__ == "__main__": 
	S = 0
	E = 3

	video = '../Videos/VIDEO0191.3gp'

	frame_count = get_frame_count(video) + 1
	frame_rate = get_frame_rate(video)

	cap = cv2.VideoCapture(video)

	prev_frame = None

	cap.set(cv2.CAP_PROP_POS_MSEC, S * 1000)

	orb = cv2.ORB_create()

	while (cap.isOpened() and cap.get(cv2.CAP_PROP_POS_MSEC) < (E * 1000)):

		retVal, frame = cap.read()

		if retVal == False:
			break

		cv2.imshow('Video', frame)

		kp = orb.detect(frame, None)
		kp, des = orb.compute(frame, kp)

		img2 = cv2.drawKeypoints(frame, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

		#plt.imshow(img2)
		#plt.show()

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

    	prev_frame = frame

	cap.release()
	cv2.destroyAllWindows()
