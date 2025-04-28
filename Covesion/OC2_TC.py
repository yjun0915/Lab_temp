import serial
import time

# 1. 시리얼 포트 설정
ser = serial.Serial(
    port='COM5',      # <- 여기를 본인 컴퓨터 COM 포트에 맞게 수정
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1         # 1초 기다림 (응답 받을 때)
)

# 2. 장치가 준비될 때까지 약간 기다리기
time.sleep(2)

# 3. 명령어 보내기 (예: 현재 온도 읽기)
ser.write(b'TEMP?\n')

# 4. 응답 읽기
response = ser.readline()
print(response.decode().strip())

# 5. 연결 종료
ser.close()
