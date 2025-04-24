from pylablib.devices import Thorlabs

device_list = Thorlabs.list_kinesis_devices()

selection = device_list[int(input(device_list))][0]

stage = Thorlabs.KinesisMotor(selection)



stage.close()
