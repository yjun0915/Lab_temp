import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def line(x, a, b):
    return a*x + b

tags = pd.read_csv(filepath_or_buffer="./datetime.csv", sep=',', index_col=0)
fig, ax = plt.subplots(1)

for idx in range(44, 47, 1):
    selection = idx
    tag = tags.loc[selection]["datetime"].astype(str)

    measurement = pd.read_csv(filepath_or_buffer="./measurement_"+tag+".csv", sep=',', index_col=0)

    measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax, s=2.5)
    measurement.plot(kind='line', x='position', y='coincidence counts', ax=ax)

plt.ylim(ymin=0)
plt.show()
