import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from scipy.optimize import curve_fit



def v_line(x, a, b, c, d, h):
    output_list = []
    for pos in x:
        output_list.append(min(a*pos + b, abs(c*pos + d) + h))
    return output_list


H_data = pd.read_csv(filepath_or_buffer="../ThorLabs/Hong_Ou_Mandel/data/measurement_202508111507.csv", sep=',', index_col=0)
V_data = pd.read_csv(filepath_or_buffer="../ThorLabs/Hong_Ou_Mandel/data/measurement_202508111509.csv", sep=',', index_col=0)

fig, ax = plt.subplots()

# H_data.plot(kind='scatter', x='position', y='coincidence counts', ax=ax, s=5)

p0 = [0, H_data['coincidence counts'].max(), 1, 0, H_data['coincidence counts'].min()]
coeff, var_matrix = curve_fit(f=v_line, xdata=H_data['position'], ydata=H_data['coincidence counts'], p0=p0)
coeff[0] = 0

fitting_position = np.linspace(start=H_data['position'].min(), stop=H_data['position'].max(), num=1000)
fitting = pd.DataFrame(
    data={'x': fitting_position, 'y': v_line(fitting_position, coeff[0], coeff[1], coeff[2], coeff[3], coeff[4])})
fitting.plot(kind='line', x='x', y='y', ax=ax, legend=False)

print(-1000*coeff[3]/coeff[2])
# V_data.plot(kind='scatter', x='position', y='coincidence counts', ax=ax, s=5, color='r')

p0 = [0, V_data['coincidence counts'].max(), 1, 0, V_data['coincidence counts'].min()]
coeff, var_matrix = curve_fit(f=v_line, xdata=V_data['position'], ydata=V_data['coincidence counts'], p0=p0)
coeff[0] = 0

fitting_position = np.linspace(start=V_data['position'].min(), stop=V_data['position'].max(), num=1000)
fitting = pd.DataFrame(
    data={'x': fitting_position, 'y': v_line(fitting_position, coeff[0], coeff[1], coeff[2], coeff[3], coeff[4])})
fitting.plot(kind='line', x='x', y='y', ax=ax, color='r', legend=False)
ax.set_xticks([-0.001, -0.0005, 0, 0.0005, 0.001], [-1, -0.5, 0, 0.5, 1])
ax.set_xlabel('position (mm)')
print(-1000*coeff[3]/coeff[2])


plt.show()
