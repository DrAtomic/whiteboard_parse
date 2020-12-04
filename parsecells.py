import numpy as np
import cv2 
import os
import csv
from imageparse import display_image

def cell_to_csv(path_to_csv, path_to_image_dir, character):
    """takes a directory of files and appends the images to a csv

    Args:
       path_to_csv: the data for the images
       path_to_image_dir: files to be parsed
       character: the label for the dataset
    
    
    """
    path = str(path_to_image_dir)
    count = 0
    for filename in os.listdir(path):
        im = cv2.imread(os.path.join(path,filename))
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        blurred = cv2.blur(gray,(3,3))
        thresh, black_white = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        
        edges = cv2.Canny(black_white,100,200)
        pts = np.argwhere(edges > 0)
        y1,x1 = pts.min(axis=0)
        y2,x2 = pts.max(axis=0)
        cropped = black_white[y1:y2, x1:x2]
        
        cropped = cv2.resize(cropped, (28,28))
       
        temp = [item for sublist in cropped for item in sublist]
        temp.insert(0,character)
        
        with open(path_to_csv + '/gathered_data.csv', 'a', newline='',encoding='utf-8') as fd:
            writer = csv.writer(fd)
            writer.writerow(temp)
        
#pwd = os.getcwd()

#cell_to_csv(pwd +'/data/', pwd + '/cell_images','(')
