import serial
import time

ser = serial.Serial(
    port='COM5',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

ser.write(b'READ_TEMP\n\r')
res = ser.readline().decode('utf-8')
print(ser.open())
