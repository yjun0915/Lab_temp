from pylablib.devices import Thorlabs

from actions import Function
from home import FastAxis
from qst import QST
from TimeTagger import Coincidences, Counter, Resolution_Standard, createTimeTagger, freeTimeTagger

import pandas as pd


binwidth, n_value, cw = 1000.0, 1, 1000
delay = [0, 132]

devices = Thorlabs.list_kinesis_devices()
print("[Devices]: ", devices)

stages = pd.DataFrame(data={
    "H1":[Thorlabs.KinesisMotor(conn='83854766', scale='stage', default_channel=1)],
    "Q1":[Thorlabs.KinesisMotor(conn='83857392', scale='stage', default_channel=1)],
    "H2":[Thorlabs.KinesisMotor(conn='83836223', scale='stage', default_channel=1)],
    "Q2":[Thorlabs.KinesisMotor(conn='83836935', scale='stage', default_channel=1)]
})

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

counter.start()

func = Function(stages)
go_fast_axis = FastAxis(stages, counter)

if __name__ == "__main__":
    # data = go_fast_axis.excute([43, 16.8, 7.9, 26.8])
    # print(data)
    # offset = data.x - [0, 0, 45, 0]
    qst = QST(stages, counter, [35.5, 39.51, 7.9, 276.61], 2)
    P = qst.measure()
    P.to_csv(path_or_buf="./QST_data.csv", sep = ',')
