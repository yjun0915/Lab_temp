import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import pause
from pylablib.devices import Thorlabs
from TimeTagger import Coincidences, Counter, Resolution_Standard, createTimeTagger, freeTimeTagger


def checkstr(arr, keys):
    val = False
    for item in arr:
        for key in keys:
            if item == key:
                val = True
    return val

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
    binwidth=100.0 * 1e9,
    n_values=20,
)

selection = device_list[int(input(device_list))][0]
stage = Thorlabs.KinesisMotor(conn=selection, scale="stage", default_channel=1)

# device initializing
counter.start()
stage.move_to(position=0.000, channel=1, scale=True)

while checkstr(arr=stage.get_status(channel=1), keys=["moving_fw", "moving_bk"]):
    pause(0.001)

print("start detecting")


if __name__ == '__main__':

    steps = np.linspace(start=0, stop=0.002, num=5, endpoint=True)

    position_tracking = []
    for step in steps:
        stage.move_to(position=step, channel=1, scale=True)
        pos_now = stage.get_position(channel=1, scale=True)
        pos_before = -1
        while not checkstr(stage.get_status(), "settled"):
            print(stage.get_status(channel=1))
        position_tracking.append(0)

    plt.plot(position_tracking)
    plt.show()

    stage.close()
    freeTimeTagger(tagger=tagger)
