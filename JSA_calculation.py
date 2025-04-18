import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation
import csv
import os

from tqdm import tqdm

pwd = os.path.realpath(__file__)
fig = plt.figure(num=1, figsize=(13, 4))
grids = gridspec.GridSpecFromSubplotSpec(nrows=1, ncols=4, width_ratios=[10, 10, 10, 0.5], subplot_spec=gridspec.GridSpec(nrows=1, ncols=1)[0], wspace=0.05)

temperature = 109.0

domain = (785, 835)
step = 300
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
        n = n + T*dn
        return  n
    else:
        dn = ((-0.5523*np.reciprocal(wavelength_mat)) + 3.3920 - (1.7101*wavelength_mat) + (0.3424*np.pow(wavelength_mat, 2))) * 1e-5
        n = n + T*dn
        return n

def n_z(wavelength_mat, _temp):
    _wavelength_mat = wavelength_mat * 1e-3           # micrometer
    squared_wavelength_mat = np.pow(_wavelength_mat, 2)
    n_z_mat = np.pow(4.59423 + (0.06206*np.reciprocal(squared_wavelength_mat - 0.04763)) + (110.80672*np.reciprocal(squared_wavelength_mat - 86.12171)), 1/2)
    n_z_mat = dn_z_dt(n_z_mat, _temp, _wavelength_mat)
    return n_z_mat

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

_wavelength_pump = float(input("Wavelength of Pump (nm) :") or val[0])                               # nanometer
bandwidth_pump = float(input("Gaussian distributed Pump spectrum bandwidth (nm) :") or val[1])      # nanometer
poling_period = float(input("Poling period of the SPDC crystal (㎛) :") or val[2]) * 1e3             # nanometer
L = float(input("length of the SPDC crystal (mm) :") or val[3]) * 1e6                               # nanometer

print("starting value :", [_wavelength_pump, bandwidth_pump, poling_period*1e-3, L*1e-6])

frames = []

wavelength_pump_list = np.linspace(_wavelength_pump, _wavelength_pump+0.001, 12)
_phase_matching_amplitude = []
for wavelength_pump in tqdm(wavelength_pump_list, ascii=" ▖▘▝▗▚▞█", bar_format='{l_bar}{bar:100}{r_bar}{bar:-100b}'):
    frequency_signal = np.reciprocal(wavelength_signal) * (2*np.pi*c)           # radian per second (angular frequency)
    frequency_idler = np.reciprocal(wavelength_idler) * (2*np.pi*c)             # radian per second (angular frequency)
    frequency_pump =  (2*np.pi*c)/wavelength_pump                               # radian per second (angular frequency)

    amplitude_X, amplitude_Y = np.meshgrid(frequency_signal, frequency_idler)       # 2-dimensional, radian per second  (angular frequency space)

    amplitude = np.exp(-1 * np.pow((amplitude_X + amplitude_Y - frequency_pump)/(2*np.pi*c/bandwidth_pump), 2))


    wavenumber_signal = np.reciprocal(wavelength_signal*n_z(wavelength_signal, temperature)) * (2*np.pi)    # inverse nanometer (wave number)
    wavenumber_idler = np.reciprocal(wavelength_idler*n_z(wavelength_idler, temperature)) * (2*np.pi)      # inverse nanometer (wave number)
    wavenumber_pump = (2*np.pi)/(wavelength_pump*n_z(wavelength_pump, temperature))                         # inverse nanometer (wave number)

    PMA_X, PMA_Y = np.meshgrid(wavenumber_signal, wavenumber_idler)

    phase_mismatch = wavenumber_pump - PMA_X - PMA_Y + (2*np.pi/poling_period)
    phase_matching_amplitude = np.sinc(phase_mismatch*L/2)

    if wavelength_pump == _wavelength_pump:
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

        _phase_matching_amplitude = phase_matching_amplitude

    frames.append([amplitude*phase_matching_amplitude, wavelength_pump])

fig2, ax = plt.subplots()
im = ax.pcolor(frames[0][0])
title = ax.text(0.5,0.95, "Pump wavelength = %4.4f"%_wavelength_pump, bbox={'facecolor':'w', 'alpha':0.5, 'pad':5}, transform=ax.transAxes, ha="center")

def update(data):
    frame = data[0]
    _title = data[1]
    im.set_array(frame)
    title.set_text("Pump wavelength = %4.4f"%_title)
    return im, title,

ani = animation.FuncAnimation(fig, update, frames=frames, interval=120, blit=True, )
ticks, labels = tick_setter(_ticks=figure_ticks, axis_data=wavelength_signal)
plt.xticks(ticks=ticks, labels=labels)
ticks, labels = tick_setter(_ticks=figure_ticks, axis_data=wavelength_idler)
plt.yticks(ticks=ticks, labels=labels)
plt.xlabel("Signal wavelength (nm)")

frames_CP = []

temp_list = np.linspace(temperature, temperature+1, 30)
global tau_list
for temp in tqdm(temp_list, ascii=" ▖▘▝▗▚▞█", bar_format='{l_bar}{bar:100}{r_bar}{bar:-50b}'):
    tau_list = np.linspace(-10, 10 ,200)
    t_idx = 0
    Coincidence_probability = tau_list
    for tau in tau_list:
        tau = tau * 1e-12
        wavelength_pump = _wavelength_pump
        frequency_signal = np.reciprocal(wavelength_signal) * (2 * np.pi * c)  # radian per second (angular frequency)
        frequency_idler = np.reciprocal(wavelength_idler) * (2 * np.pi * c)  # radian per second (angular frequency)
        frequency_pump = (2 * np.pi * c) / wavelength_pump  # radian per second (angular frequency)

        amplitude_X, amplitude_Y = np.meshgrid(frequency_signal, frequency_idler)  # 2-dimensional, radian per second  (angular frequency space)

        amplitude = np.exp(-1 * np.pow((amplitude_X + amplitude_Y - frequency_pump) / (2 * np.pi * c / bandwidth_pump), 2))

        wavenumber_signal = np.reciprocal(wavelength_signal * n_z(wavelength_signal, temp)) * (2 * np.pi)  # inverse nanometer (wave number)
        wavenumber_idler = np.reciprocal(wavelength_idler * n_z(wavelength_idler, temp)) * (2 * np.pi)  # inverse nanometer (wave number)
        wavenumber_pump = (2 * np.pi) / (wavelength_pump * n_z(wavelength_pump, temp))  # inverse nanometer (wave number)

        PMA_X, PMA_Y = np.meshgrid(wavenumber_signal, wavenumber_idler)

        phase_mismatch = wavenumber_pump - PMA_X - PMA_Y + (2 * np.pi / poling_period)
        phase_matching_amplitude = np.sinc(phase_mismatch * L / 2)

        f = amplitude*phase_matching_amplitude
        integrated = f-np.transpose(f)*np.exp(-1j*(amplitude_Y-amplitude_X)*tau)
        p_tau = (1/4)*(np.sum(np.square(integrated)))

        Coincidence_probability[t_idx] = p_tau
        t_idx += 1
    frames_CP.append([Coincidence_probability, temp])

new_img = []
for idx in range(np.shape(temp_list)[0]):
    new_img.append(frames_CP[idx][0])

plt.figure(3)
plt.pcolor(new_img)
ticks, labels = tick_setter(_ticks=5, axis_data=tau_list)
plt.xticks(ticks=ticks, labels=labels)
plt.xlabel("Delay (ps)")
plt.colorbar()

plt.show()
