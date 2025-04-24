from pylablib.devices import Thorlabs

'''
Important prechanges
.venv/Lib/site-packages/ft232/__init__.py [line 19~21] : .d2xx -> d2xx
.venv/Lib/site-packages/pylablib/devices/Thorlabs/kinesis.py [line 101] : FT232DeviceBackend -> HIDeviceBackend
'''

device_list = Thorlabs.list_kinesis_devices()

selection = device_list[int(input(device_list))][0]

stage = Thorlabs.KinesisMotor(selection)



stage.close()
