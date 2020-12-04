from imageparse import display_image
import numpy as np
import pandas as pd
import os
from random import randint


pwd = os.getcwd() + '/data/gathered_data.csv'

x = pd.read_csv(pwd)

cell = randint(0,len(x)-1)
# get random row
x1 = x.iloc[cell]

#remove label
x1 = x1[1:]
data = x1.to_numpy()

pixels = data
pixels = np.array(pixels, dtype='uint8')
pixels = pixels.reshape((28,28))

print("row " + str(cell))
display_image(pixels)

