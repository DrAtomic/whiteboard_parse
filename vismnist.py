from imageparse import display_image
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


display_image(pixels)
