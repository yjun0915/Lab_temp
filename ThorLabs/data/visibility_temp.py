import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def line(x, a, b):
    return a*x + b

file = pd.read_csv(filepath_or_buffer="./visibility_temp_data_shortrange.txt", sep=',', index_col=0)

fig, ax = plt.subplots(1)
file.plot(kind='line', x='temp', y='visibility', ax=ax)
file.plot(kind='scatter', x='temp', y='visibility', s=5, ax=ax)

plt.show()
