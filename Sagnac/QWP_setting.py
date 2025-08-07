import matplotlib.pyplot as plt
import numpy as np

from scipy.optimize import minimize
from pylablib.devices import Thorlabs
from TimeTagger import Coincidences, Counter, Resolution_Standard, createTimeTagger, freeTimeTagger

import time


std_member = []

H1 = Thorlabs.KinesisMotor(conn='83854766', scale='stage', default_channel=1)
H2 = Thorlabs.KinesisMotor(conn='83836223', scale='stage', default_channel=1)
Q1 = Thorlabs.KinesisMotor(conn='83857392', scale='stage', default_channel=1)
Q2 = Thorlabs.KinesisMotor(conn='83836935', scale='stage', default_channel=1)
stages = [H1, Q1, H2, Q2]

start_point = 0.0175
end_point = 0.0195
data_num = 50
binwidth = 100
n_value = 2
delay = [350, 0]
cw = 500

# device connecting
device_list = Thorlabs.list_kinesis_devices()
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

# breakpoint()

for stage in stages:
    stage.setup_velocity(max_velocity=15, acceleration=15)


def is_moving(arr, keys):
    val = False
    for item in arr:
        for key in keys:
            if item == key:
                val = True
    return val


def detect(path, qwp_angle):
    H = stages[2*path]
    Q = stages[1 + 2*path]
    Q.move_to(qwp_angle)
    output = []
    while is_moving(arr=Q.get_status(channel=1), keys=["moving_fw", "moving_bk"]):
        time.sleep(0.01)
    H.move_by(180)
    while is_moving(arr=H.get_status(channel=1), keys=["moving_fw", "moving_bk"]):
        if n_value != 1:
            val = counter.getData()[path].sum()
        else:
            val = counter.getData()[path][0]
        output.append(val)
    return output


def obj_func(obj_x, obj_path):
    output = np.std(detect(path=obj_path, qwp_angle=obj_x))
    std_member.append(output)
    return output


if __name__=="__main__":
    option = 0
    angle_list = [16.385, 272.1]
    model = minimize(
        obj_func,
        x0=[angle_list[option]],
        args=option,
        method='COBYLA'
    )
    print(model)

    plt.plot(std_member)
    plt.show()
    for stage in stages:
        stage.close()

    freeTimeTagger(tagger=tagger)
    breakpoint()
