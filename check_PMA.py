import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv
import os

pwd = os.path.realpath(__file__)
fig = plt.figure(num=1, figsize=(13, 4))
grids = gridspec.GridSpecFromSubplotSpec(nrows=1, ncols=4, width_ratios=[10, 10, 10, 0.5], subplot_spec=gridspec.GridSpec(nrows=1, ncols=1)[0], wspace=0.05)

temperature = 109
domain = (700, 920)
step = 500
figure_ticks = 4


def tick_setter(_ticks, axis_data):
    length = len(axis_data)
    arrange = np.arange(length//(2*_ticks), length, length//_ticks)
    return arrange, axis_data[arrange].astype(np.float16)


def n_z(wavelength_nm: np.ndarray, _temp: float) -> np.ndarray:
    wavelength_um = wavelength_nm / 1000.0
    ΔT = _temp - 25.0

    A0, A1 = 1.14886, 1e-4
    B0, B1 = 5.69293, 1e-3
    C0, C1 = -2.42924, 1e-3

    A = A0 + A1 * ΔT
    B = B0 + B1 * ΔT
    C = C0 + C1 * ΔT

    λ2 = wavelength_um**2
    n_squared = A + B / (λ2 - C)
    return np.sqrt(n_squared)



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

amplitude = np.exp(-1 * np.pow((amplitude_X + amplitude_Y - frequency_pump)/(c/bandwidth_pump), 2))


wavenumber_signal = np.reciprocal(wavelength_signal*n_z(wavelength_signal, temperature)) * (2*np.pi)    # inverse nanometer (wave number)
wavenumber_idler = np.reciprocal(wavelength_idler*n_z(wavelength_idler, temperature)) * (2*np.pi)       # inverse nanometer (wave number)
wavenumber_pump = (2*np.pi)/(wavelength_pump*n_z(wavelength_pump, temperature))                         # inverse nanometer (wave number)

PMA_X, PMA_Y = np.meshgrid(wavenumber_signal, wavenumber_idler)

phase_mismatch = -wavenumber_pump - PMA_X + PMA_Y + (2*np.pi/poling_period)
phase_matching_amplitude = np.sinc(phase_mismatch*L/2)

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
