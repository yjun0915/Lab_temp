import numpy as np
import serial
import time
import csv
from datetime import datetime

# 07/03, 13:14~, dt=2s
ser = serial.Serial('COM14', 9600)
time.sleep(2)  # 보드 초기화 대기

with open('env_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Temperature', 'Humidity'])

    holder = 30
    cache = np.zeros(shape=[2, holder])
    counter = 0
    try:
        while True:
            line = ser.readline().decode().strip()
            if ',' in line:
                temp, humi = line.split(',')
                cache[0][counter] = temp
                cache[1][counter] = humi
                cache += 1
                if cache == holder:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ave_temp = np.sum(cache[0][:])/holder
                    ave_humi = np.sum(cache[1][:])/holder
                    writer.writerow([timestamp, ave_temp, ave_humi])
                    cache = np.zeros(shape=[2, holder])
                    counter = 0
                print(f"{timestamp} | Temp: {temp}°C, Humidity: {humi}%")
    except KeyboardInterrupt: # 콘솔 좌상단 정지 버튼만 작동함
        print("데이터 저장 종료")
    finally:
        ser.close()
