import glob
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

def get_GPS_from_exif(img_path):
    pass

if __name__ == "__main__":
    files = glob.glob("../landmarks/*/*.jpg")
    orb = cv2.ORB_create()

    # print(files)
    print(len(files))

    query_im = cv2.imread('../queries/frame.png')
    query_im = cv2.cvtColor(query_im, cv2.COLOR_RGB2GRAY)
    print("Shape: {}".format(query_im.shape))

    s_t = time.time()
    q_kp, q_d = orb.detectAndCompute(query_im, None)

    print('Keypoint calc. took {0:.2f} ms'.format((time.time() - s_t) * 1000))

    query_im_cp_1 = np.copy(query_im)
    query_im_cp_2 = np.copy(query_im)
    cv2.drawKeypoints(query_im, q_kp, query_im_cp_1, color=(0, 255, 0))
    cv2.drawKeypoints(query_im, q_kp, query_im_cp_2, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    print("KP: {}".format(q_kp))
    # Display image with and without keypoints size
    fx, plots = plt.subplots(1, 2, figsize=(20, 10))

    plots[0].set_title("Train keypoints With Size")
    plots[0].imshow(query_im_cp_1, cmap='gray')

    plots[1].set_title("Train keypoints Without Size")
    plots[1].imshow(query_im_cp_2, cmap='gray')

    plt.show()
    #cv2.imshow('kp', query_im)
    #cv2.waitKey(0)
