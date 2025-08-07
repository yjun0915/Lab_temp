import asyncio
import numpy as np
import pandas as pd
from pylablib.devices import Thorlabs
from TimeTagger import Coincidences, Counter, Resolution_Standard, createTimeTagger, freeTimeTagger
from tqdm import tqdm
from datetime import datetime

select=False

class Experiment:
    def __init__(self, inputs, desc):
        self.start_point = inputs[0]
        self.end_point = inputs[1]
        self.data_num = int(inputs[2])
        self.binwidth = inputs[3]
        self.n_value = int(inputs[4])
        self.delay = [inputs[5], inputs[6]]
        self.desc = desc
        self.cw = 500

        # device connecting
        device_list = Thorlabs.list_kinesis_devices()
        self.tagger = createTimeTagger(resolution=Resolution_Standard)
        self.coincidences = Coincidences(
            tagger=self.tagger,
            coincidenceGroups=[[1, 2]],
            coincidenceWindow=self.cw,
        )
        self.counter = Counter(
            tagger=self.tagger,
            channels= [1, 2, list(self.coincidences.getChannels())[0]],
            binwidth=self.binwidth * 1e9,
            n_values=self.n_value,
        )
        self.tagger.setInputDelay(channel=1, delay=self.delay[0])
        self.tagger.setInputDelay(channel=2, delay=self.delay[1])

        if select:
            selection = device_list[int(input(device_list) or 0)][0]
        else:
            selection = '27007111'

        self.stage = Thorlabs.KinesisMotor(conn=selection, scale="stage", default_channel=1)
        self.stage.setup_velocity(max_velocity=0.001, acceleration=0.002)
        # device initializing
        self.counter.start()
        self.move_kinesis(sub_stage=self.stage, pos = self.start_point)


    def __del__(self):
        self.stage.close()
        freeTimeTagger(tagger=self.tagger)


    def checkstr(self, arr, keys):
        val = False
        for item in arr:
            for key in keys:
                if item == key:
                    val = True
        return val


    def move_kinesis(self, sub_stage, pos, log=[]):
        sub_stage.move_to(position=pos, channel=1, scale=True)
        while self.checkstr(arr=sub_stage.get_status(channel=1), keys=["moving_fw", "moving_bk"]):
            if log:
                log.append(sub_stage.get_position(channel=1, scale=True))


    async def execute(self):
        steps = np.linspace(start=self.start_point, stop=self.end_point, num=self.data_num, endpoint=True)

        position_tracking = [self.stage.get_position(channel=1, scale=True)]
        A_channel_counts = []
        B_channel_counts = []
        coincidence_data = []

        for step in tqdm(steps, ascii=" ▖▘▝▗▚▞█", bar_format='{l_bar}{bar:100}{r_bar}{bar:-100b}'):
            self.move_kinesis(sub_stage=self.stage, pos=step, log=position_tracking)
            count_data = self.counter.getData()
            A_channel_counts.append(np.sum(a=count_data, axis=1)[0])
            B_channel_counts.append(np.sum(a=count_data, axis=1)[1])
            coincidence_data.append(np.sum(a=count_data, axis=1)[2])
            await asyncio.sleep(self.binwidth*self.n_value*1e-3)
            coincidence_data[-1] -= A_channel_counts[-1]*B_channel_counts[-1]*self.cw*1e-12

        result = pd.DataFrame(
            data={'position':(steps-np.average(steps)),
                  'A channel counts':A_channel_counts,
                  'B channel counts':B_channel_counts,
                  'coincidence counts':coincidence_data}
        )
        position_log = pd.DataFrame(data={'position':position_tracking})

        tag = datetime.today().strftime("%Y%m%d%H%M")
        tags = pd.read_csv(filepath_or_buffer="./data/datetime.csv", sep=',', index_col=0)
        tags = pd.concat(objs=[tags, pd.DataFrame(data={'datetime':[tag], 'description':[self.desc]})], ignore_index=True)
        tags.to_csv(path_or_buf="./data/datetime.csv")

        result.to_csv(path_or_buf=("./data/measurement_"+tag+".csv"))
        position_log.to_csv(path_or_buf=("./data/position_log_"+tag+".csv"))

        self.stage.blink(channel=1)
