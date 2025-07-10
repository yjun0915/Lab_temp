from pylablib.devices import Thorlabs

from actions import Function
from home import FastAxis
from qst import QST
from TimeTagger import Coincidences, Counter, Resolution_Standard, createTimeTagger, freeTimeTagger

import pandas as pd


binwidth, n_value, cw = 500.0, 2, 1000
delay = [0, 132]

devices = Thorlabs.list_kinesis_devices()
print("[Devices]: ", devices)

stages = pd.DataFrame(data={
    "H1":[Thorlabs.KinesisMotor(conn='83854766', scale='stage', default_channel=1)],
    "V1":[Thorlabs.KinesisMotor(conn='83857392', scale='stage', default_channel=1)],
    "H2":[Thorlabs.KinesisMotor(conn='83836223', scale='stage', default_channel=1)],
    "V2":[Thorlabs.KinesisMotor(conn='83836935', scale='stage', default_channel=1)]
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
    data = go_fast_axis.excute([217.2535, 218.0520, 143.0710, 208.9197])
    print(data)
    offset = data.x - [0, 0, 45, 0]
    # qst = QST(stages, counter, [213.7, 222.6, 96.8, 203.0])
    # P = qst.measure()
    # print(P)
    # P.to_csv(path_or_buf="QST_data.csv", sep = ',')
