# External dependencies
import matplotlib.pyplot as plt
from GPSPhoto import gpsphoto
import progressbar
import os.path
import imutils
import pickle
import glob
import cv2

# Setting this flag to 'True' will only index images with known GPS coordinates
SKIP_UNKNOWN_GEO = False

def get_meta_gps(img_path):
    try: gps_data = gpsphoto.getGPSData(img_path)
    except: return None, None
    # If GPS coordinates are in metadata, use those
    if gps_data is not None and 'Latitude' in gps_data and 'Longitude' in gps_data:
        return gps_data['Latitude'], gps_data['Longitude']
    return None, None

def get_hardcoded_gps(img_name):
    # For the Oude Jan, Nieuwe Kerk and Raadhuis we already know the coordinates
    name_parts = img_name.split('_')
    loc_code = None
    if len(name_parts) > 3: loc_code = name_parts[2]
    # Oude Jan
    if loc_code == 'oj': return 52.012755, 4.355959
    # Nieuwe Kerk
    elif loc_code == 'nk': return 52.012517, 4.360909
    # Raadhuis
    elif loc_code == 'rh': return 52.011461, 4.358469
    return None, None

def get_input_gps():
    gps_input = raw_input("[LATITUDE LONGITUDE]: ")
    parts = gps_input.split(' ')
    if len(parts) != 2: return None, None
    try: float(parts[0])
    except ValueError: return None, None
    try: float(parts[1])
    except ValueError: return None, None
    return float(parts[0]), float(parts[1])

def load_img_index():

    # If image index already exists, return it
    if os.path.isfile('img_index.db'):
        with open('img_index.db', 'rb') as handle:
            return pickle.load(handle)

    # Create the image index:
    # - if metadata contains GPS: use those coordinates
    # - if image is taken at Oude Jan, Nieuwe Kerk or Raadhuis: use hardcoded coordinates
    # - otherwise, ask the user to provide GPS coordinates
    print("Indexing images...")
    img_files = glob.glob("../landmarks/*/*.*")
    img_index = {'path': [], 'lat': [], 'long': []}
    if SKIP_UNKNOWN_GEO: bar = progressbar.ProgressBar(maxval=len(img_files), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]); bar.start()
    for i in range(len(img_files)):
        if False and i > 0: print("[path: {}, lat: {}, long: {}]".format(img_index['path'][i-1], img_index['lat'][i-1], img_index['long'][i-1]))
        if SKIP_UNKNOWN_GEO: bar.update(i)

        # Try getting GPS from metadata
        lat, lon = get_meta_gps(img_files[i])
        if lat is not None and lon is not None:
            img_index['path'].append(img_files[i])
            img_index['lat'].append(lat)
            img_index['long'].append(lon)
            continue

        # Try getting hardcoded GPS from file name
        lat, lon = get_hardcoded_gps(img_files[i].split('/')[-1])
        if lat is not None and lon is not None:
            img_index['path'].append(img_files[i])
            img_index['lat'].append(lat)
            img_index['long'].append(lon)
            continue

        if SKIP_UNKNOWN_GEO: continue
        # If those didn't work, ask user for the coordinates
        print("Where is the following picture taken? (see external window)")
        print("Name: '{}'".format(img_files[i].split('/')[-1]))
        img = imutils.resize(cv2.cvtColor(cv2.imread(img_files[i]), cv2.COLOR_BGR2RGB), width=900)
        plt.imshow(img); plt.show(block=False); plt.pause(0.001)
        lat, lon = get_input_gps()
        while lat is None and lon is None:
            print("Invalid coordinates format, please try again.")
            lat, lon = get_input_gps()
        plt.close('all')

        img_index['path'].append(img_files[i])
        img_index['lat'].append(lat)
        img_index['long'].append(lon)
    if SKIP_UNKNOWN_GEO: bar.finish()

    # Store and return the image index
    with open('img_index.db', 'wb') as handle: pickle.dump(img_index, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return img_index

if __name__ == "__main__": load_img_index()
