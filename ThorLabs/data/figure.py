import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def line(x, a, b):
    return a*x + b

tags = pd.read_csv(filepath_or_buffer="./datetime.csv", sep=',')

selection = int(input(tags["datetime"]))
tag = tags.loc[selection]["datetime"].astype(str)
print(tag)

measurement = pd.read_csv(filepath_or_buffer="./measurement_"+tag+".csv", sep=',')
position_log = pd.read_csv(filepath_or_buffer="./position_log_"+tag+".csv", sep=',')

print(position_log)

fig, ax = plt.subplots(2)
measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax[0], s=1)
position_log.plot(kind='line', x=0, y='position', ax=ax[1], lw=0.5)
position_log.plot(kind='scatter', x=0, y='position', ax=ax[1], s=0.1)

p0 = [0, 0]

coeff, var_matrix = curve_fit(f=line, xdata=measurement['position'], ydata=measurement['coincidence counts'], p0=p0)

fitting = pd.DataFrame(data={'x':measurement['position'], 'y':(measurement['position'].mul(coeff[0]).add(coeff[1]))})

fitting.plot(kind='line', x='x', y='y', ax=ax[0], lw=0.5, color='r')

# visibility = 1 - (/)

plt.show()
