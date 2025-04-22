import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv
import os

pwd = os.path.realpath(__file__)
fig = plt.figure(num=1, figsize=(13, 4))
grids = gridspec.GridSpecFromSubplotSpec(nrows=1, ncols=4, width_ratios=[10, 10, 10, 0.5], subplot_spec=gridspec.GridSpec(nrows=1, ncols=1)[0], wspace=0.05)

temperature = 19

domain = (620, 1000)
step = 1000
figure_ticks = 4

def tick_setter(_ticks, axis_data):
    length = len(axis_data)
    arrange = np.arange(length//(2*_ticks), length, length//_ticks)
    # arrange = np.append(arrange, [int(length/2)])
    return arrange, axis_data[arrange].astype(np.float16)

def dn_z_dt(n, T, wavelength_mat):
    if np.average(wavelength_mat) < 0.53:
        return  n
    elif (np.average(wavelength_mat) >= 0.53) and (np.average(wavelength_mat) <= 1.445):
        dn = ((0.9221*np.reciprocal(np.pow(wavelength_mat, 3))) - (2.9220*np.reciprocal(np.pow(wavelength_mat, 2))) + (3.6677*np.reciprocal(wavelength_mat)) - 0.1897) * 1e-5
        n = n
        return  n
    else:
        dn = ((-0.5523*np.reciprocal(wavelength_mat)) + 3.3920 - (1.7101*wavelength_mat) + (0.3424*np.pow(wavelength_mat, 2))) * 1e-5
        n = n
        return n

def n_z(wavelength_mat, _temp):
    _wavelength_mat = wavelength_mat * 1e-3           # micrometer
    squared_wavelength_mat = np.pow(_wavelength_mat, 2)
#    n_z_mat = np.pow(4.59423 + (0.06206*np.reciprocal(squared_wavelength_mat - 0.04763)) + (110.80672*np.reciprocal(squared_wavelength_mat - 86.12171)), 1/2)
    n_z_mat = np.pow(2.12725 + (1.18431*np.reciprocal(1-0.0514852*np.reciprocal(squared_wavelength_mat))) + (0.6603*np.reciprocal(1-100.00507*np.reciprocal(squared_wavelength_mat))) - 0.00968956*squared_wavelength_mat, 1/2)
    n_z_mat = dn_z_dt(n_z_mat, _temp, _wavelength_mat)
    return n_z_mat * 1e3

c = 299792458 * 1e9         # nanometer per second

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

wavelength_pump = float(input("Wavelength of Pump (nm) :") or val[0])                               # nanometer
bandwidth_pump = float(input("Gaussian distributed Pump spectrum bandwidth (nm) :") or val[1])      # nanometer
poling_period = float(input("Poling period of the SPDC crystal (㎛) :") or val[2]) * 1e3             # nanometer
L = float(input("length of the SPDC crystal (mm) :") or val[3]) * 1e6                               # nanometer

print("start calculation with value :", [wavelength_pump, bandwidth_pump, poling_period*1e-3, L*1e-6])


frequency_signal = np.reciprocal(wavelength_signal) * (2*np.pi*c)           # radian per second (angular frequency)
frequency_idler = np.reciprocal(wavelength_idler) * (2*np.pi*c)             # radian per second (angular frequency)
frequency_pump =  (2*np.pi*c)/wavelength_pump                               # radian per second (angular frequency)

amplitude_X, amplitude_Y = np.meshgrid(frequency_signal, frequency_idler)       # 2-dimensional, radian per second  (angular frequency space)

amplitude = np.exp(-1 * np.pow((amplitude_X + amplitude_Y - frequency_pump)/(2*np.pi*c/bandwidth_pump), 2))


wavenumber_signal = np.reciprocal(wavelength_signal*n_z(wavelength_signal, temperature)) * (2*np.pi)    # inverse nanometer (wave number)
wavenumber_idler = np.reciprocal(wavelength_idler*n_z(wavelength_idler, temperature)) * (2*np.pi)       # inverse nanometer (wave number)
wavenumber_pump = (2*np.pi)/(wavelength_pump*n_z(wavelength_pump, temperature))                         # inverse nanometer (wave number)

PMA_X, PMA_Y = np.meshgrid(wavenumber_signal, wavenumber_idler)

phase_mismatch = -wavenumber_pump - PMA_X + PMA_Y + (2*np.pi/poling_period)
phase_matching_amplitude = np.sinc(phase_mismatch*L/2 - 3158)

ax1 = fig.add_subplot(grids[0])
plt.pcolor(amplitude)
ticks, labels = tick_setter(_ticks=figure_ticks, axis_data=wavelength_signal)
plt.xticks(ticks=ticks, labels=labels)
ticks, labels = tick_setter(_ticks=figure_ticks, axis_data=wavelength_idler)
plt.yticks(ticks=ticks, labels=labels)
plt.xlabel("Signal wavelength (nm)")
plt.ylabel("Idler wavelength (nm)")
ax1.set_title("Pump envelop amplitude")

ax2 = fig.add_subplot(grids[1])
plt.pcolor(phase_matching_amplitude)
ticks, labels = tick_setter(_ticks=figure_ticks, axis_data=wavelength_signal)
plt.xticks(ticks=ticks, labels=labels)
plt.xlabel("Signal wavelength (nm)")
plt.yticks([])
ax2.set_title("Phase matching amplitude")

ax3 = fig.add_subplot(grids[2])
plt.pcolor(amplitude * phase_matching_amplitude)
ticks, labels = tick_setter(_ticks=figure_ticks, axis_data=wavelength_signal)
plt.xticks(ticks=ticks, labels=labels)
plt.xlabel("Signal wavelength (nm)")
plt.yticks([])
ax3.set_title("Joint spectral amplitude")

color_axis = fig.add_subplot(grids[3])
plt.colorbar(cax=color_axis)


plt.figure(2)

plt.plot(phase_mismatch[:][int(step/2)]*L/2)
ticks, labels = tick_setter(_ticks=figure_ticks, axis_data=wavelength_signal)
plt.xticks(ticks=ticks, labels=labels)
plt.title("phase mismatch (    )")

plt.show()
