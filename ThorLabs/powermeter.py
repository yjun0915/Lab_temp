import pyvisa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ThorlabsPM100 import ThorlabsPM100

# ---------------setting constants---------------
low_bound = 0.000001
choose_device = False
data_num = -10000

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 256,
        }

fig = plt.figure(1)
rm = pyvisa.ResourceManager()
# print(rm)

device = ''

if choose_device:
    device_idx = input(f"choose index: {rm.list_resources()}")
    device = rm.list_resources()[int(device_idx)-1]
else:
    device = 'USB0::0x1313::0x8078::P0042685::INSTR'

device_address = device

global inst

try:
    inst = rm.open_resource(device_address, timeout=5000)
    print("장치 연결 성공:", device_address)

except Exception as e:
    print("장치 연결 실패:", e)

power_meter = ThorlabsPM100(inst=inst)

# ---------------data prepare---------------
data = np.array([power_meter.read])
visibility = np.array([0])
max_idx = 0
min_idx = 0

# ---------------measurement---------------
while True:
    power = power_meter.read
    data = np.append(data, np.array([power]))
    if data[-1] <= low_bound:
        data = data[0:-1]
        df = pd.DataFrame(data[data_num:-1])
        df.to_csv('ND_visibility_97.csv', index=False)
        break
    Imax = float(data[data_num: -1].max())
    Imin = float(data[data_num: -1].min())
    if data[max_idx] < Imax:
        max_idx = len(data)-2
    if data[min_idx] > Imin:
        min_idx = len(data)-2

    if len(data) > (-1*data_num):
        max_idx = max_idx - 1
        min_idx = min_idx - 1

    visibility = np.append(visibility, [(Imax-Imin)/(Imax+Imin)])
    #print(visibility[-1])

    fig.clf()
    ax1 =  fig.add_subplot(211)
    plt.text(y=0.1, x=0, s=("%f3" % float(visibility[-1])), fontdict=font)
    plt.axis('off')

    ax2 = fig.add_subplot(212)
    plt.plot(data[data_num:-1])
    plt.scatter(x=max_idx, y=data[max_idx], marker="^", color='r', s=200)
    plt.scatter(x=min_idx, y=data[min_idx], marker="v", color='b', s=200)
    #plt.ylim([0, 0.002])
    plt.pause(0.000001)

#plt.plot(data)
#plt.plot(visibility)

