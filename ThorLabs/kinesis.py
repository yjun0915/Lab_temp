import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylablib.devices import Thorlabs
from TimeTagger import Coincidences, Counter, Resolution_Standard, createTimeTagger, freeTimeTagger
from tqdm import tqdm
from datetime import datetime

start_point = 0.021550
end_point = 0.023550
data_num = 35
binwidth = 100.0
n_value = 2
select=False

def checkstr(arr, keys):
    val = False
    for item in arr:
        for key in keys:
            if item == key:
                val = True
    return val

def move_kinesis(sub_stage, pos, log=[]):
    sub_stage.move_to(position=pos, channel=1, scale=True)
    while checkstr(arr=sub_stage.get_status(channel=1), keys=["moving_fw", "moving_bk"]):
        if log:
            log.append(sub_stage.get_position(channel=1, scale=True))

# device connecting
device_list = Thorlabs.list_kinesis_devices()
tagger = createTimeTagger(resolution=Resolution_Standard)
coincidences = Coincidences(
    tagger=tagger,
    coincidenceGroups=[[1, 2]],
    coincidenceWindow=1000,
)
counter = Counter(
    tagger=tagger,
    channels= [1, 2] + list(coincidences.getChannels()),
    binwidth=binwidth * 1e9,
    n_values=n_value,
)
tagger.setInputDelay(channel=1, delay=0)
tagger.setInputDelay(channel=2, delay=24)

selection = '11111111'

if select:
    selection = device_list[int(input(device_list) or 0)][0]
else:
    selection = '27266188'

stage = Thorlabs.KinesisMotor(conn=selection, scale="stage", default_channel=1)

# device initializing
counter.start()
move_kinesis(sub_stage=stage, pos = start_point)


if __name__ == '__main__':

    steps = np.linspace(start=start_point, stop=end_point, num=data_num, endpoint=True)

    position_tracking = [stage.get_position(channel=1, scale=True)]
    A_channel_counts = []
    B_channel_counts = []
    coincidence_data = []

    for step in tqdm(steps, ascii=" ▖▘▝▗▚▞█", bar_format='{l_bar}{bar:100}{r_bar}{bar:-100b}'):
        move_kinesis(sub_stage=stage, pos=step, log=position_tracking)
        count_data = counter.getData()
        A_channel_counts.append(np.sum(a=count_data, axis=1)[0])
        B_channel_counts.append(np.sum(a=count_data, axis=1)[1])
        coincidence_data.append(np.sum(a=count_data, axis=1)[2])
        plt.pause(binwidth*n_value*1e-3)

    result = pd.DataFrame(
        data={'position':(steps-np.average(steps)),
              'A channel counts':A_channel_counts,
              'B channel counts':B_channel_counts,
              'coincidence counts':coincidence_data}
    )
    position_log = pd.DataFrame(data={'position':position_tracking})

    tag = datetime.today().strftime("%Y%m%d%H%M")
    tags = pd.read_csv(filepath_or_buffer="./data/datetime.csv", sep=',', index_col=0)
    tags = pd.concat(objs=[tags, pd.DataFrame(data={'datetime':[tag]})], ignore_index=True)
    tags.to_csv(path_or_buf="./data/datetime.csv")

    result.to_csv(path_or_buf=("./data/measurement_"+tag+".csv"))
    position_log.to_csv(path_or_buf=("./data/position_log_"+tag+".csv"))

    fig, ax = plt.subplots(2)
    result.plot(kind='line', x='position', y='coincidence counts', ax=ax[0])
    position_log.plot(kind='line', ax=ax[1])

    stage.blink(channel=1)

    stage.close()
    freeTimeTagger(tagger=tagger)

    plt.show()

