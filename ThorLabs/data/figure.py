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

fig, ax = plt.subplots(1)
measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax, s=5)
measurement.plot(kind='line', x='position', y='coincidence counts', ax=ax)
#new_row.plot(kind='line', ax=ax[1])
#position_log.plot(kind='line', y='position', ax=ax[2], lw=0.5)
#position_log.reset_index().plot(kind='scatter', x='index', y='position', ax=ax[2], s=0.1)

p0 = [0, 0]

coeff, var_matrix = curve_fit(f=line,
                              xdata=pd.concat([measurement['position'][0:3], measurement['position'][-4:-1]]),
                              ydata=pd.concat([measurement['coincidence counts'][0:3], measurement['coincidence counts'][-4:-1]]),
                              p0=p0)

fitting = pd.DataFrame(data={'x':measurement['position'], 'y':(measurement['position'].mul(coeff[0]).add(coeff[1]))})

#fitting.plot(kind='line', x='x', y='y', ax=ax, lw=0.5, color='r')

min_idx = measurement['coincidence counts'].idxmin()

visibility = 1 - (measurement['coincidence counts'][min_idx]/(measurement['position'][min_idx]*coeff[0] + coeff[1]))

visibility_spot = pd.DataFrame(data={
    'position':[measurement['position'][min_idx], measurement['position'][min_idx]],
    'coincidence counts':[measurement['coincidence counts'][min_idx], (measurement['position'][min_idx]*coeff[0] + coeff[1])]
})
#visibility_spot.plot(kind='scatter', x='position', y='coincidence counts', ax=ax, s=3, color='r')

print("Visibility of this data is %.2f"%(visibility*100)+"%")

plt.ylim(ymin=0)
plt.show()
