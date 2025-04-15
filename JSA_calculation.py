import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv
import os

pwd = os.path.realpath(__file__)
fig = plt.figure(num=1, figsize=(13, 4))
grids = gridspec.GridSpecFromSubplotSpec(nrows=1, ncols=4, width_ratios=[10, 10, 10, 0.5], subplot_spec=gridspec.GridSpec(nrows=1, ncols=1)[0], wspace=0.05)

temperature = 20

domain = (1950, 2000)
step = 500
figure_ticks = 4

def tick_setter(_ticks, axis_data):
    length = len(axis_data)
    arrange = np.arange(length//(2*_ticks), length, length//_ticks)
    return arrange, axis_data[arrange].astype(np.float16)

n = 1               # non-dimension
c = 299792458 / n   # meter per second

wavelength_signal = np.linspace(start=domain[0], stop=domain[1], num=step)
wavelength_idler = np.linspace(start=domain[0], stop=domain[1], num=step)

val = [0, 0, 0, 0]

if os.path.isfile('setting_info.csv'):
    with open('setting_info.csv', 'r', encoding='cp949') as file:
        csv_reader = csv.reader(file)
        idx = 0
        for row in csv_reader:
            val[idx] = float(row[1])
            idx += 1

wavelength_pump = float(input("Wavelength of Pump (nm) :") or val[0]) * 1e-9                            # meter
bandwidth_pump = float(input("Gaussian distributed Pump spectrum bandwidth (nm) :") or val[1]) * 1e-9   # meter
poling_period = float(input("Poling period of the SPDC crystal (㎛) :") or val[2]) * 1e-6                # meter
L = float(input("length of the SPDC crystal (mm) :") or val[3]) * 1e-3                                  # meter

print(val)

frequency_signal = np.reciprocal(wavelength_signal) * (2*np.pi*c)           # radian per second (angular frequency)
frequency_idler = np.reciprocal(wavelength_idler) * (2*np.pi*c)             # radian per second (angular frequency)
frequency_pump =  (2*np.pi*c)/wavelength_pump                               # radian per second (angular frequency)

X, Y = np.meshgrid(frequency_signal, frequency_idler)       # 2-dimensional, radian per second  (angular frequency space)
amplitude = np.exp(-1 * np.pow((X + Y - frequency_pump)/(bandwidth_pump), 2))

delta_k = ((frequency_pump - X - Y)/(2*np.pi*c)) + (2*np.pi/poling_period)
phase_matching_amplitude = np.sinc(delta_k*L/2)

ax1 = fig.add_subplot(grids[0])
plt.pcolor(amplitude)
ticks, labels = tick_setter(_ticks=figure_ticks, axis_data=wavelength_signal)
plt.xticks(ticks=ticks, labels=labels)
ticks, labels = tick_setter(_ticks=figure_ticks, axis_data=wavelength_idler)
plt.yticks(ticks=ticks, labels=labels)
plt.xlabel("Signal wavelength (nm)")
plt.ylabel("Idler wavelength (nm)")

ax2 = fig.add_subplot(grids[1])
plt.pcolor(phase_matching_amplitude)
ticks, labels = tick_setter(_ticks=figure_ticks, axis_data=wavelength_signal)
plt.xticks(ticks=ticks, labels=labels)
plt.xlabel("Signal wavelength (nm)")
plt.yticks([])

ax3 = fig.add_subplot(grids[2])
plt.pcolor(amplitude*phase_matching_amplitude)
ticks, labels = tick_setter(_ticks=figure_ticks, axis_data=wavelength_signal)
plt.xticks(ticks=ticks, labels=labels)
plt.xlabel("Signal wavelength (nm)")
plt.yticks([])

color_axis = fig.add_subplot(grids[3])
plt.colorbar(cax=color_axis)
fig.tight_layout()

plt.show()
