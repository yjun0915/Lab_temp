import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

range = 16

def v_line(x, a, b, c, d, h):
    output_list = []
    for pos in x:
        print(pos)
        output_list.append(min(a*pos + b, abs(c*pos + d) + h))
    print(output_list)
    return output_list

tags = pd.read_csv(filepath_or_buffer="./datetime.csv", sep=',', index_col=0)

selection = int(input(tags))
tag = tags.loc[selection]["datetime"].astype(str)
print(tag)

measurement = pd.read_csv(filepath_or_buffer="./measurement_"+tag+".csv", sep=',', index_col=0)
position_log = pd.read_csv(filepath_or_buffer="./position_log_"+tag+".csv", sep=',', index_col=0)

new_row = measurement['coincidence counts'].div(np.sqrt(measurement['A channel counts'].mul(measurement['B channel counts'])))

fig01, ax01 = plt.subplots(1)
measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax01, s=5)

fig02, ax02 = plt.subplots(3)
measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax02[0], s=5)
new_row.plot(kind='line', ax=ax02[1])
position_log.plot(kind='line', y='position', ax=ax02[2], lw=0.5)
position_log.reset_index().plot(kind='scatter', x='index', y='position', ax=ax02[2], s=0.1)

p0 = [0, 100, 0, 0, 0]
coeff02, var_matrix02 = curve_fit(f=v_line, xdata=measurement['position'], ydata=measurement['coincidence counts'], p0=p0)

fitting = pd.DataFrame(data={'x':measurement['position'], 'y':v_line(measurement['position'], coeff02[0], coeff02[1], coeff02[2], coeff02[3], coeff02[4])})
fitting.plot(kind='line', x='x', y='y', ax=ax02[0], color='r', legend=False)

# min_idx = measurement['coincidence counts'].idxmin()
#
# visibility = 1 - (measurement['coincidence counts'][min_idx]/(measurement['position'][min_idx]*coeff01[0] + coeff01[1]))
#
# visibility_spot = pd.DataFrame(data={
#     'position':[measurement['position'][min_idx], measurement['position'][min_idx]],
#     'coincidence counts':[measurement['coincidence counts'][min_idx], (measurement['position'][min_idx]*coeff01[0] + coeff01[1])]
# })
# visibility_spot.plot(kind='scatter', x='position', y='coincidence counts', ax=ax02[0], s=3, color='r')
#
# print("Visibility of this data is %.2f"%(visibility*100)+"%")

ax01.set_ylim(ymin=0)
plt.show()
