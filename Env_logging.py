import serial
import time
import csv

# 07/03, 13:14~, dt=2s
ser = serial.Serial('COM14', 9600)
time.sleep(2)  # 보드 초기화 대기

with open('env_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Temperature (C)', 'Humidity (%)'])

    try:
        while True:
            line = ser.readline().decode().strip()
            if ',' in line:
                temp, humi = line.split(',')
                writer.writerow([temp, humi])
                print(f"Saved: {temp}°C, {humi}%")
    except KeyboardInterrupt: # 콘솔 좌상단 정지 버튼만 작동함
        print("데이터 저장 종료")
    finally:
        ser.close()
