"""
Course: CMPS 4883
Assignemt: A08
Date: 03/26/2019
Github username: briceallard
Repo url: https://github.com/briceallard/4883-SWTools-Allard
Name: Brice Allard
Description: 
    Using an image dataset, create an image mosaic (image made of other images)
    Gathers screen shots of a downloaded youtube clip and resizes them all to
    the center block in a square dimension
"""

import os
import sys
import time
import string
import getopt
import ffmpy
from pytube import YouTube
from sklearn.cluster import KMeans
from PIL import Image, ImageDraw, ImageMath

VIDEO_ID = ''
SAVE_PATH = ''
TITLE = ''
SS_INTERVAL = 0
SS_SIZE = 256


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


def download_video():
    """
    Name:
        download_video
    Description:
        Given a YouTube video ID, downloads the video in the 
        highest quality and in .mp4 format
    Params:
        None
    Returns:
        None
    """
    global VIDEO_ID
    global SAVE_PATH
    global TITLE

    try:
        print('Attemping connection to: https://www.youtube.com/watch?v=' + VIDEO_ID)
        yt = YouTube('https://www.youtube.com/watch?v=' + VIDEO_ID)
    except:
        print("Connection Error!")

    TITLE = ''.join(e for e in yt.title if e.isalnum())

    print('Downloading: ' + TITLE)
    yt.streams.first().download(output_path=SAVE_PATH, filename=TITLE)

    # Screen shot frame by frame every i (Interval)
    ss_frames()


def ss_frames():
    """
    Name:
        ss_frames
    Description:
        Given a video, captures a screen shot of a frame each second
        and stores it as .jpg format
    Params:
        None
    Returns:
        None
    """
    global SAVE_PATH
    global SS_INTERVAL
    global TITLE

    save_format = './frame_captures/' + TITLE + '%03' + 'd'

    print('Capturing frames ...')
    os.system('ffmpeg -i {0} -vf fps={1} {2}.jpg'
              .format(SAVE_PATH + TITLE + '.mp4',
                      str(SS_INTERVAL),
                      save_format))


def crop_center(img, width, height):
    """
    Name:
        crop_center
    Description:
        Crops to the center of the image given the width and height
    Params:
        None
    Returns:
        cwd
    """
    w, h = img.size

    left = (w - width) / 2
    top = (h - height) / 2
    right = (w + height) / 2
    bottom = (h + height) / 2

    try:
        img = img.crop((left, top, right, bottom))
    except:
        print('Error cropping to the size requested!')

    return img


def resize(img, width):
    """
    Name:
        resize
    Description:
        Resizes the image to passed in width value while maintaining aspect ratio
    Params:
        img - the image being resized
        width - designated width (height will be resized to keep aspect ratio)
    Returns:
        img
    """

    wpercent = float(width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((width, hsize), Image.ANTIALIAS)

    return img


def resize_and_crop():
    count = 0

    for filename in os.listdir('./frame_captures/'):
        with Image.open('./frame_captures/' + filename) as image:
            os.remove('./frame_captures/' + filename)
            image = resize(image, SS_SIZE)
            min_dimension = min(image.size)
            image = crop_center(image, min_dimension, min_dimension)
            image.save('./frame_captures/' + TITLE + '_' + str(count) + '.jpg')
            image.close()
            count += 1


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

    print("python3 images_from_yt.py [options] [--id | --dir | --seconds\n")
    print("--id [-i]\t: URL to YouTube Video to download.")
    print("--dir [-d]\t: PATH to save the video")
    print("--sec [-s]\t: Interval between screenshot capture")
    print("Ex: python3 images_from_yt.py --id=eOrNdBpGMv8 --dir=/output_folder/ --second=5")
    print("Ex: python3 images_from_yt.py -i eOrNdBpGMv8 -d /output_folder/ -s 5\n")


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

    global VIDEO_ID
    global SAVE_PATH
    global SS_INTERVAL

    # Get user arguments
    # --i, --input: the YouTube URL of the video to download
    # --o, --output: The PATH to save the video
    # --s, --seconds: Interval between screenshot capture
    if not argv:
        usage()
        sys.exit(2)
    # otherwise default values used
    else:
        try:
            opts, args = getopt.getopt(
                argv, 'i:d:s:', ['id=', 'dir=', 'seconds='])

            for opt, arg in opts:
                if opt in ('-i', '--id'):
                    print("Setting --id = %s" % arg)
                    VIDEO_ID = arg
                elif opt in ('-d', '--dir'):
                    print("Setting --dir = %s" % arg)
                    SAVE_PATH = get_CWD() + arg
                elif opt in ('-s', '--sec'):
                    print("Setting --sec = %s" % arg)
                    SS_INTERVAL = arg
        except getopt.GetoptError:
            usage()
            sys.exit(2)


if __name__ == '__main__':
    # Get arguments from terminal and assign them
    handle_args(sys.argv[1:])

    download_video()

    time.sleep(5)

    resize_and_crop()
