import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def line(x, a, b):
    return a*x + b

tags = pd.read_csv(filepath_or_buffer="./datetime.csv", sep=',', index_col=0)

selection = int(input(tags))
tag = tags.loc[selection]["datetime"].astype(str)
print(tag)

measurement = pd.read_csv(filepath_or_buffer="./measurement_"+tag+".csv", sep=',', index_col=0)
position_log = pd.read_csv(filepath_or_buffer="./position_log_"+tag+".csv", sep=',', index_col=0)

new_row = measurement['coincidence counts'].div(np.sqrt(measurement['A channel counts'].mul(measurement['B channel counts'])))

fig, ax = plt.subplots(3)
measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax[0], s=1)
new_row.plot(kind='line', ax=ax[1])
position_log.plot(kind='line', y='position', ax=ax[2], lw=0.5)
position_log.reset_index().plot(kind='scatter', x='index', y='position', ax=ax[2], s=0.1)

p0 = [0, 0]

coeff, var_matrix = curve_fit(f=line,
                              xdata=pd.concat([measurement['position'][0:49], measurement['position'][-50:-1]]),
                              ydata=pd.concat([measurement['coincidence counts'][0:49], measurement['coincidence counts'][-50:-1]]),
                              p0=p0)

fitting = pd.DataFrame(data={'x':measurement['position'], 'y':(measurement['position'].mul(coeff[0]).add(coeff[1]))})

fitting.plot(kind='line', x='x', y='y', ax=ax[0], lw=0.5, color='r')

# visibility = 1 - (/)

plt.show()
