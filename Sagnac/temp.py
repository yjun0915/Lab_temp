import serial
import time
import csv

import actions
from pylablib.devices import Thorlabs
from TimeTagger import Coincidences, Counter, Resolution_Standard, createTimeTagger, freeTimeTagger
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Kinesis serial
ports = {
    "H1": '83854766',
    "H2": '83836223',
    "Q1": '83857392',
    "Q2": '83836935'
}
arr = ["H1", "H2", "Q1", "Q2"]

now = 1
start = 0
end = 16

binwidth, n_value, cw = 1000.0, 10, 1000
delay = [0, 132]


def is_stable(_stage):
    state = _stage.get_status(channel=1)
    keys = ["moving_fw", "moving_bk"]
    var = True
    for item in state:
        for key in keys:
            if item == key:
                var = False
    return var

tagger = createTimeTagger(resolution=Resolution_Standard)
coincidences = Coincidences(
    tagger=tagger,
    coincidenceGroups=[[1, 2]],
    coincidenceWindow=cw,
)
counter = Counter(
    tagger=tagger,
    channels=[1, 2, list(coincidences.getChannels())[0]],
    binwidth=binwidth * 1e9,
    n_values=n_value,
)
tagger.setInputDelay(channel=1, delay=delay[0])
tagger.setInputDelay(channel=2, delay=delay[1])

stage = Thorlabs.KinesisMotor(conn=ports[arr[now]], scale='stage', default_channel=1)
Thorlabs.KinesisMotor(conn='83857392', scale='stage', default_channel=1).move_to(35)
Thorlabs.KinesisMotor(conn='83836935', scale='stage', default_channel=1).move_to(24.6)

marker = ['\\', '|', '/', '--']
with open(arr[now]+'.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['degree', 'single count', 'coincidence count'])

for idx in range(start, end+1):
    stage.move_to(idx)
    mark=0
    while not is_stable(stage):
        print("\r["+str(idx)+"] Moving..."+marker[int(mark)%4]+"  ", end='')
        mark+=0.75
        time.sleep(0.1)
    mark=0
    for sle in range(int(binwidth*n_value/10)):
        print("\r["+str(idx)+"] Reading..."+marker[int(mark)%4]+"  ", end='')
        mark+=0.01
        time.sleep(1e-2)
    count_data = counter.getData()
    A_channel_counts = np.sum(a=count_data, axis=1)[0]
    B_channel_counts = np.sum(a=count_data, axis=1)[1]
    coincidence_data = np.sum(a=count_data, axis=1)[2]

    single_count = A_channel_counts
    if now == 0 or now == 2:
        single_count = B_channel_counts

    with open(arr[now]+'.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([idx, single_count/n_value, coincidence_data/n_value])

data = pd.read_csv(filepath_or_buffer='./'+arr[now]+'.csv', sep=',', index_col=0)
max_idx = data.idxmax()

start = (max_idx.iloc[0] - 1) * 10
end = (max_idx.iloc[0] + 1)*10

for idx in range(start, end+1):
    idx = idx/10
    stage.move_to(idx)
    mark=0
    while not is_stable(stage):
        print("\r["+str(idx)+"] Moving..."+marker[int(mark)%4], end='')
        mark+=0.75
        time.sleep(0.1)
    mark=0
    for sle in range(int(binwidth*n_value/10)):
        print("\r["+str(idx)+"] Reading..."+marker[int(mark)%4]+"  ", end='')
        mark+=0.01
        time.sleep(1e-2)
    count_data = counter.getData()
    A_channel_counts = np.sum(a=count_data, axis=1)[0]
    B_channel_counts = np.sum(a=count_data, axis=1)[1]
    coincidence_data = np.sum(a=count_data, axis=1)[2]

    single_count = A_channel_counts
    if now == 0 or now == 2:
        single_count = B_channel_counts

    with open(arr[now]+'.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([idx, single_count/n_value, coincidence_data/n_value])

data = pd.read_csv(filepath_or_buffer='./'+arr[now]+'.csv', sep=',')
data = data.sort_values(by='degree')
data.plot(x='degree', y='single count')
plt.show()
