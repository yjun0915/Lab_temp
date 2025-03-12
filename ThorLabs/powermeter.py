import pyvisa
from ThorlabsPM100 import ThorlabsPM100
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import pause

low_bound = 0.000001
choose_device = False
data_num = -100

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 256,
        }
fig1 = plt.figure(1)
fig2 = plt.figure(2)
rm = pyvisa.ResourceManager()
print(rm)

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

data = np.array([power_meter.read])
visibility = np.array([0])
while True:
    power = power_meter.read
    data = np.append(data, np.array([power]))
    if data[-1] <= low_bound:
        data = data[data_num:-1]
        break
    Imax = float(data[data_num: -1].max()) * 1000
    Imin = float(data[data_num: -1].min()) * 1000
    visibility = np.append(visibility, [(Imax-Imin)/(Imax+Imin)])
    print(visibility[-1])
    plt.clf()
    plt.text(y=0, x=0, s=("%f3" % float(visibility[-1])), fontdict=font)
    plt.axis('off')
    pause(0.0001)

#plt.plot(data)
#plt.plot(visibility)

