import pyvisa as visa
import usbtmc
from ThorlabsPM100 import ThorlabsPM100
import time

# VISA 리소스 매니저 초기화
rm = visa.ResourceManager()
print(rm.list_resources())
# # 장치 연결
# # 여기서 'TCPIP0::192.168.1.100::inst0::INSTR'은 연결된 장치의 VISA 주소입니다.
# # 실제 IP 주소를 입력해야 합니다.
# power_meter = rm.open_resource('TCPIP0::192.168.1.100::inst0::INSTR')
#
# # 장치 초기화
# power_meter.write('*RST')  # 장치 초기화 (옵션# )
#
# # 측정 모드 설정 (예: 파워 측정)
# power_meter.write('MEASU:FUNC:RESOLU HIGH')  # 해상도 설정 (옵션)
# power_meter.write('MEASU:CHAN1:WAV:SOUR1:POW')  # 파워 측정 채널 선택 (옵션)
#
# # 측정 시작 (1초 대기 후 측정)
# time.sleep(1)
#
# # 측정값 읽기
# power_value = power_meter.query('MEASU:POW:DC?')  # DC 파워 값 요청
#
# # 출력
# print(f"측정된 파워: {power_value} W")
#
# # 연결 종료
# power_meter.close()
