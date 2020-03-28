# External dependencies
from img_index import load_img_index
import progressbar
import numpy as np
import os.path
import cv2

def load_orb_index(img_index):
    repo_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    # If ORB index already exists, return it
    if os.path.isfile(os.path.join(repo_path, 'index/orb_index.db')):
        return np.memmap(os.path.join(repo_path, 'index/orb_index.db'), dtype='float32', mode='r+', shape=(len(img_index['path']), 256, 32))

    # Create the ORB index: for each image, calculate its ORB descriptors
    print("Creating ORB database...")
    orb_index = np.memmap(os.path.join(repo_path, 'index/orb_index.db'), dtype='float32', mode='w+', shape=(len(img_index['path']), 256, 32))
    orb = cv2.ORB_create(256)
    bar = progressbar.ProgressBar(maxval=len(img_index['path']), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]).start()
    for i in range(len(img_index['path'])):
        bar.update(i)
        db_img = cv2.imread(img_index['path'][i], 0)
        _, db_desc = orb.detectAndCompute(db_img, None)
        if db_desc is None:
            print("ERROR: No descriptors found ({})".format(img_index['path'][i]))
            continue
        if len(db_desc) < 256: db_desc = np.vstack((db_desc, np.zeros((256 - len(db_desc), 32))))
        orb_index[i] = db_desc
    bar.finish()

    return orb_index

if __name__ == "__main__":
    img_index = load_img_index()
    orb_index = load_orb_index(img_index)
    print("Loaded orb index! [{}]".format(orb_index.shape))
