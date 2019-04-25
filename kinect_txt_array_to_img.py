#!/usr/bin/python3
import os
import sys
import cv2 # pylint: disable-all
import numpy as np
import imageio

# PICTURE_DIR = "/path/to/files/"
PICTURE_DIR = sys.argv[1]


def save_bw(in_data, save_path):
    """
    Save grayscale jpg image from depth camera
    """
    depth_img = np.dstack((in_data, in_data, in_data)).astype(np.uint8)
    if depth_img.shape[0] == 480 and depth_img.shape[1] > 640:
        print(save_path)
        cv2.imwrite(save_path, depth_img)
    else:
        raise IOError

def get_txt_files(picture_dir):
    res = [os.path.join(dp, f) for dp, dn, filenames in os.walk(picture_dir)
           for f in filenames if os.path.splitext(f)[1] == '.txt']
    return res


def get_txt_filename(file_path):
    return file_path.split(os.path.sep)[-1]


def create_output_path(file_path, filename):
    pth = file_path.split(os.path.sep)
    pth = pth[:-1]
    pth = os.path.join('/', *pth)
    if not os.path.exists(pth):
        os.makedirs(pth, exist_ok=True)
    filename = filename.strip(".txt")
    filename = filename.replace('R', 'D')
    return os.path.join(pth, filename + '.jpg')


def main():

    if not os.path.exists(PICTURE_DIR):
        exit("Could not find specified folder: %s" % PICTURE_DIR)

    res = get_txt_files(PICTURE_DIR)
    
    for r in res:
        txt_filename = get_txt_filename(r)
        raw = np.genfromtxt(r, delimiter="\t")
        path = create_output_path(r, txt_filename)
        if not os.path.exists(path):
            try:
                save_bw(raw, path)
                print("Exported .jpg image from %s" % txt_filename)
            except IOError:
                print("Not a valid .txt format in %s" % txt_filename)
                continue


if __name__ == "__main__":
    main()
