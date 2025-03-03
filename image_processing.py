import os
import cv2 as cv
import argparse
from PIL import Image

def rename_frames(folder_target):
    count = 0
    for filename in os.listdir(folder_target):
        new_filename = "frame" + f"{count:06}" + ".png"
        if (filename != new_filename):
            os.rename(folder_target + filename, folder_target + new_filename)
        count += 1

def create_mask(folder):
    img = cv.imread(folder + '/masks/frame000000.png')
    assert img is not None, "file could not be read, check with os.path.exists()"
    
    gray = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
    ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    cv.imwrite(folder + "/masks/frame000000.png", thresh)
    
    filename = folder + "/masks/frame000000.png"
    # Open an image file
    image = Image.open(filename).convert('P')

    image.putpalette([  0,   0,   0,         # Background - Black
                     255,   0,   0,         # Class 1 - Red
                       ])

    # Save the grayscale image
    image.save(filename)

        
        
        
        

def main():
    parser = argparse.ArgumentParser(description="A basic argparse example")
    parser.add_argument('action', help='name of action')
    parser.add_argument('folder', help='folder')
    parser.add_argument('sf', help='subfolder')
    
    # Parse the arguments
    args = parser.parse_args()
    
    folder = args.folder + "/" + args.sf + "/"

    if (args.action == "rename"):
        rename_frames(folder)
    elif (args.action == "segment"):
        create_mask(args.folder)
        

if __name__ == "__main__":
    main()
