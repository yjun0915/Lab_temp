import pyvisa
import pandas as pd
from ThorlabsPM100 import ThorlabsPM100
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import pause

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 256,
        }
fig1 = plt.figure(1)
range = -100
rm = pyvisa.ResourceManager()

device = 'USB0::0x1313::0x8078::P0042685::INSTR'

device_address = device

inst = rm.open_resource(device_address, timeout=5000)

power_meter = ThorlabsPM100(inst=inst)

data = np.array([power_meter.read])
visibility = np.array([0])

while True:
    power = power_meter.read
    data = np.append(data, np.array([power]))
    if data[-1] <= 0.00010:
        data = data[0:-1]
        df = pd.DataFrame(data[range:-1])
        df.to_csv('visibility_90.csv', index=False)
        break
    Imax = float(data[range: -1].max()) * 1000
    Imin = float(data[range: -1].min()) * 1000
    visibility = np.append(visibility, [(Imax-Imin)/(Imax+Imin)])
    print(visibility[-1])

    fig1.clf()
    fig1.text(y=0.1, x=0, s=("%f3" % float(visibility[-1])), fontdict=font)

    pause(0.0001)

