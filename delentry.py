import pandas as pd
import os

pwd = os.getcwd()
x = pd.read_csv(pwd + "/data/gathered_data.csv")


x = x[0:-100]


x.to_csv(pwd + "/data/gathered_data.csv", index=False)
