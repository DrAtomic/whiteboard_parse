from imageparse import display_image
import numpy as np
import pandas as pd
import os
from random import randint


pwd = os.getcwd() + '/data/gathered_data.csv'

x = pd.read_csv(pwd)

# get random row
x1 = x.iloc[randint(0,len(x))]

#remove label
x1 = x1[1:]
data = x1.to_numpy()

pixels = data
pixels = np.array(pixels, dtype='uint8')
pixels = pixels.reshape((28,28))


display_image(pixels)
