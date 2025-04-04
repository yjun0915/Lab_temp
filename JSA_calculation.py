import numpy as np
import matplotlib.pyplot as plt

temperature = 20

domain = (750, 810)
step = 200
figure_ticks = 4

def tick_setter(_ticks, axis_data):
    length = len(axis_data)
    arrange = np.arange(length//(2*_ticks), length, length//_ticks)
    return arrange, axis_data[arrange].astype(np.float16)

n = 1
c = 299792458 * 1e9 / n

wavelength_signal = np.linspace(start=domain[0], stop=domain[1], num=step)
wavelength_idler = np.linspace(start=domain[0], stop=domain[1], num=step)

wavelength_pump = float(input("Wavelength of Pump (nm) :"))
bandwidth_pump = float(input("Gaussian distributed Pump spectrum bandwidth (nm) :"))
poling_period = float(input("Poling period of the SPDC crystal (㎛) :")) * 1e3
L = float(input("length of the SPDC crystal (mm) :")) * 1e6

frequency_signal = np.reciprocal(wavelength_signal) * (2*np.pi*c)
frequency_idler = np.reciprocal(wavelength_idler) * (2*np.pi*c)
frequency_pump =  (2*np.pi*c)/wavelength_pump

X, Y = np.meshgrid(frequency_signal, frequency_idler)
amplitude = np.exp(-1 * np.pow((X + Y - frequency_pump)/bandwidth_pump, 2))

delta_k = ((frequency_pump - X - Y)/c) + (2*np.pi/poling_period)
phase_matching_amplitude = np.sinc(delta_k*L/2)

plt.pcolor(amplitude*phase_matching_amplitude)
ticks, labels = tick_setter(_ticks=figure_ticks, axis_data=wavelength_signal)
plt.xticks(ticks=ticks, labels=labels)
ticks, labels = tick_setter(_ticks=figure_ticks, axis_data=wavelength_idler)
plt.yticks(ticks=ticks, labels=labels)
plt.xlabel("Signal wavelength (nm)")
plt.ylabel("Idler wavelength (nm)")
plt.clim(0., 0.1)
plt.colorbar()

plt.show()
