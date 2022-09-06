import os
import cv2
import sys
import json
import math
import string
import getopt
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
from sklearn.cluster import KMeans
from PIL import Image, ImageDraw, ImageMath


COUNT = 0
SAVE_NAME = ''
SAVE_PATH = ''
DATA_PATH = ''
DOMINANT_DATA = {}


def get_CWD():
    """
    Name:
        get_CWD
    Description:
        Finds the current working directory
    Params:
        None
    Returns:
        cwd
    """
    return os.path.dirname(os.path.abspath(__file__))


def usage():
    """
    Name:
        usage
    Description:
        Displays instructional data for user
    Params:
        None
    Returns:
        None
    """

    print("python3 images_from_yt.py [options] [--i | --o\n")
    print("--id [-i]\t: PATH of input file used for conversion")
    print("--dir [-d]\t: PATH to save the video")
    print("Ex: python3 images_from_yt.py --i=/input_folder/ --o=/output_folder/")
    print("Ex: python3 images_from_yt.py -i /input_folder/ -o /output_folder/\n")


def handle_args(argv):
    """
    Name:
        handle_args
    Description:
        Gets user arguments from command line and associates with:
            - DOWNLOAD_URL
            - SAVE_PATH
    Params:
        argv: the arguments being passed in from command line
    Returns:
        None
    """

    global DATA_PATH
    global SAVE_NAME
    global SAVE_PATH

    # Get user arguments
    # --i, --input: the image path used for conversion
    # --o, --output: The PATH to save the video
    if not argv:
        usage()
        sys.exit(2)
    # otherwise default values used
    else:
        try:
            opts, args = getopt.getopt(
                argv, 'i:o:', ['in=', 'out='])

            for opt, arg in opts:
                if opt in ('-i', '--in'):
                    print("Setting --in = %s" % arg)
                    DATA_PATH = arg
                elif opt in ('-o', '--out'):
                    print("Setting --out = %s" % arg)
                    SAVE_NAME = arg + '.json'
                    SAVE_PATH = get_CWD() + '/dominant_data/' + arg + '/'

        except getopt.GetoptError:
            usage()
            sys.exit(2)


def extract_cluster_color_values(hist, centroids, ignore_background=False):
    """Get the dominant colors of an image.

    Arguments:
        hist        -- [numpy.ndarray]
        centroids   -- [numpy.ndarray] 
    Returns:
        dictionary of color values
    Used By:
        get_dominant_colors
    """

    colors = []

    for (percent, color) in zip(hist, centroids):
        rgb = []
        total = 0
        for c in color:
            c = round(float(c))
            total += c
            rgb.append(c)
        if ignore_background:
            if total > 15 and total < 750:
                colors.append(
                    {'percent': round(float(percent), 2), 'rgb': rgb})
        else:
            colors.append({'percent': round(float(percent), 2), 'rgb': rgb})

    return sorted(colors, key=lambda i: i['percent'], reverse=True)


def find_histogram(clt):
    """ Create a histogram with k clusters
    Arguments:
        :param: clt
        :return:hist
    Used By:
        get_dominant_colors
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist


def plot_colors(hist, centroids):
    """Get the dominant colors of an image.

    Arguments:
        hist        -- [numpy.ndarray]
        centroids   -- [numpy.ndarray] 
    Returns:
        plot image
    """
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar


def get_dominant_color(img, k=3):
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = img.reshape((img.shape[0] * img.shape[1], 3))

    clt = KMeans(n_clusters=k)
    clt.fit(img)

    hist = find_histogram(clt)
    colors = extract_cluster_color_values(hist, clt.cluster_centers_)

    return colors[0]['rgb']

    # Display most dominant color
    # new_image = Image.new('RGB', (500, 500), (r, g, b))
    # draw_image = ImageDraw.Draw(new_image)
    # new_image.show()

    # Display top 3 most dominant colors by percentage
    # bar = plot_colors(hist, clt.cluster_centers_)
    # plt.axis("off")
    # plt.imshow(bar)
    # plt.show()


def process_dataset(files):
    count = 0
    total = len([f for f in os.listdir(DATA_PATH) if os.path.isfile(os.path.join(DATA_PATH, f))])
    dominant_dataset = {}

    print('Processing dataset ...')

    if os.path.isdir(files):
        for filename in os.listdir(files):
            dominant_dataset[filename] = get_dominant_color(files + filename)
            count += 1
            
            print("{0} of {1} - {2}%".format(count, total, math.trunc(count / total * 100)))
    else:
        print('Invalid dataset loaded!')

    print('{0} images processed successfully'.format(count))

    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)

    with open(SAVE_PATH + SAVE_NAME, 'w+') as f:
        json.dump(dominant_dataset, f)


if __name__ == '__main__':
    # Get arguments from terminal and assign them
    handle_args(sys.argv[1:])

    process_dataset(DATA_PATH)
