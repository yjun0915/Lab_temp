from pylablib.devices import Thorlabs


device_list = Thorlabs.list_kinesis_devices()

selection = device_list[int(input(device_list))][0]

stage = Thorlabs.KinesisMotor(selection)

print(stage.get_stage())
print(stage.get_position(channel=1, scale=True))
stage.blink(channel=1, dest="host")

stage.close()
