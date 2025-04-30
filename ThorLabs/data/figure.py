import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

range = 16

def line(x, a, b):
    return a*x + b

def v_line(x, a, b, h):
    return abs(a*x + b) + h

tags = pd.read_csv(filepath_or_buffer="./datetime.csv", sep=',', index_col=0)

selection = int(input(tags))
tag = tags.loc[selection]["datetime"].astype(str)
print(tag)

measurement = pd.read_csv(filepath_or_buffer="./measurement_"+tag+".csv", sep=',', index_col=0)
position_log = pd.read_csv(filepath_or_buffer="./position_log_"+tag+".csv", sep=',', index_col=0)

new_row = measurement['coincidence counts'].div(np.sqrt(measurement['A channel counts'].mul(measurement['B channel counts'])))

fig01, ax01 = plt.subplots(1)
measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax01, s=5)
measurement.plot(kind='line', x='position', y='coincidence counts', ax=ax01)

fig02, ax02 = plt.subplots(3)
measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax02[0], s=5)
new_row.plot(kind='line', ax=ax02[1])
position_log.plot(kind='line', y='position', ax=ax02[2], lw=0.5)
position_log.reset_index().plot(kind='scatter', x='index', y='position', ax=ax02[2], s=0.1)

len = int(measurement.shape[0]*range/100)
range_list = [len, -len-1, len+1, measurement.shape[0]-len-1]
print(range_list)
p0 = [0, 0]
coeff01, var_matrix01 = curve_fit(f=line,
                              xdata=pd.concat([measurement['position'][0:range_list[0]], measurement['position'][range_list[1]:-1]]),
                              ydata=pd.concat([measurement['coincidence counts'][0:range_list[0]], measurement['coincidence counts'][range_list[1]:-1]]),
                              p0=p0)

p1 = [0, 0, 0]
coeff02, var_matrix02 = curve_fit(f=v_line,
                              xdata=measurement['position'][range_list[2]:range_list[3]],
                              ydata=measurement['coincidence counts'][range_list[2]:range_list[3]],
                              p0=p1)

range_list = [len+1, -len-1, len, measurement.shape[0]-len]
fitting01 = pd.DataFrame(data={
    'x':measurement['position'][0:range_list[0]],
    'y':(measurement['position'][0:range_list[0]].mul(coeff01[0]).add(coeff01[1]))
})
fitting01.plot(kind='line', x='x', y='y', ax=ax02[0], color='r', legend=False)
fitting02 = pd.DataFrame(data={
    'x':measurement['position'][range_list[1]:-1],
    'y':(measurement['position'][range_list[1]:-1].mul(coeff01[0]).add(coeff01[1]))
})
fitting02.plot(kind='line', x='x', y='y', ax=ax02[0], color='r', legend=False)
fitting03 = pd.DataFrame(data={
    'x':measurement['position'][range_list[2]:range_list[3]],
    'y':(abs(measurement['position'][range_list[2]:range_list[3]].mul(coeff02[0]).add(coeff02[1]))+coeff02[2])
})
fitting03.plot(kind='line', x='x', y='y', ax=ax02[0], color='r', legend=False)


min_idx = measurement['coincidence counts'].idxmin()

visibility = 1 - (measurement['coincidence counts'][min_idx]/(measurement['position'][min_idx]*coeff01[0] + coeff01[1]))

visibility_spot = pd.DataFrame(data={
    'position':[measurement['position'][min_idx], measurement['position'][min_idx]],
    'coincidence counts':[measurement['coincidence counts'][min_idx], (measurement['position'][min_idx]*coeff01[0] + coeff01[1])]
})
visibility_spot.plot(kind='scatter', x='position', y='coincidence counts', ax=ax02[0], s=3, color='r')

print("Visibility of this data is %.2f"%(visibility*100)+"%")

ax01.set_ylim(ymin=0)
plt.show()
