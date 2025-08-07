import serial
import time
from pylablib.devices import Thorlabs

# Kinesis 장비 초기화
H1 = Thorlabs.KinesisMotor(conn='83854766', scale='stage', default_channel=1)
H2 = Thorlabs.KinesisMotor(conn='83836223', scale='stage', default_channel=1)
Q1 = Thorlabs.KinesisMotor(conn='83857392', scale='stage', default_channel=1)
Q2 = Thorlabs.KinesisMotor(conn='83836935', scale='stage', default_channel=1)

H1.home()
H2.home()
Q1.home()
Q2.home()

Q1.move_to(128.885)
Q2.move_to(204.6)
# Q1.move_to(39.51)
# Q2.move_to(276.61)

def move_H1_H2(pos1, pos2):
    H1.move_to(pos1)
    H2.move_to(pos2)
    while H1.is_moving() or H2.is_moving():
        time.sleep(0.1)
    print(f"Moved to H1: {pos1}°, H2: {pos2}°")

# 시리얼 포트 연결 (아두이노 COM 포트 확인 필요)
ser = serial.Serial('COM14', 9600, timeout=1)  # COM 포트는 환경에 따라 조정

print("Listening to Arduino...")

try:
    while True:
        if ser.in_waiting > 0:
            command = ser.readline().decode().strip()
            if command == "H":
                move_H1_H2(35.5000, 52.9000)
            elif command == "V":
                move_H1_H2(80.5000, 7.9000)
            elif command == "D":
                move_H1_H2(58.0000, 30.4000)
            elif command == "A":
                move_H1_H2(13.0000, -14.6000)
            else:
                print(f"[Unknown Command]: {command}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    ser.close()
