import numpy as np
import pandas as pd
import os
import cv2


pwd = os.getcwd() + '/data/gathered_data.csv'

x = pd.read_csv(pwd)

# get first row
x = x.iloc[0]

#remove label
x = x[1:]
data = x.to_numpy()

pixels = data
pixels = np.array(pixels, dtype='uint8')
pixels = pixels.reshape((28,28))



def display_image(img):
    """displays an image
    
    Args:
       img: image to be displayed
    
    
    """
    
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


display_image(pixels)
