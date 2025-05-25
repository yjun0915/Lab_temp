import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def v_line(x, a, b, c, d, h):
    output_list = []
    for pos in x:
        output_list.append(min(a*pos + b, abs(c*pos + d) + h))
    return output_list

measurement = pd.read_csv(filepath_or_buffer="./data/measurement_202505251639.csv", sep=',', index_col=0)

fig, ax = plt.subplots()
ax.set_xlim(xmin=measurement['position'].min(), xmax=measurement['position'].max())
ax.set_xticks(
    ticks=np.concatenate([measurement['position'][
                          int(measurement['position'].shape[0] / 2):0:-int(measurement['position'].shape[0] / 5)],
                          measurement['position'][
                          int(measurement['position'].shape[0] / 2):-1:int(measurement['position'].shape[0] / 5)]],
                         0),
    labels=(1e3) * np.round(
        np.concatenate([measurement['position'][int(measurement['position'].shape[0] / 2):0:-int(
            measurement['position'].shape[0] / 5)], measurement['position'][
                                                    int(measurement['position'].shape[0] / 2):-1:int(
                                                        measurement['position'].shape[0] / 5)]], 0), 4)

)

p0 = [0, measurement['coincidence counts'].max(), 1, 0, measurement['coincidence counts'].min()]
coeff, var_matrix = curve_fit(f=v_line, xdata=measurement['position'], ydata=measurement['coincidence counts'], p0=p0)
coeff[0] = 0

fitting_position = np.linspace(start=measurement['position'].min(), stop=measurement['position'].max(), num=1000)
fitting = pd.DataFrame(data={'x':fitting_position, 'y':v_line(fitting_position, coeff[0], coeff[1], coeff[2], coeff[3], coeff[4])})

min_idx = fitting['y'].idxmin()

visibility = 1 - (fitting['y'][min_idx])/(coeff[1] + coeff[0]*fitting['x'][min_idx])
print(visibility)

measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax, s=5)
fitting.plot(kind='line', x='x', y='y', ax=ax, color='r', legend=False)

ax.axis('on')
ax.set_ylabel("coincidence counts")
ax.set_xlabel("position (mm)")
ax.set_ylim(ymin=0)

plt.show()
