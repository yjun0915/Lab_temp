import pyvisa
import serial
import time


class OC2Controller:
    def __init__(self, visa_address='ASRL5::INSTR', serial_port='COM5', baudrate=9600, timeout=1):
        self.connected = False
        self.mode = None  # 'visa' or 'serial'

        # 1. 시도: VISA 방식 연결
        try:
            rm = pyvisa.ResourceManager()
            self.device = rm.open_resource(visa_address)
            self.device.baud_rate = baudrate
            self.device.timeout = timeout * 1000  # pyvisa는 ms 단위
            self.mode = 'visa'
            self.connected = True
            print("[✓] pyVISA로 연결 성공:", visa_address)
        except Exception as e:
            print("[!] pyVISA 연결 실패:", e)

        # 2. 백업: Serial 방식 연결 (쓰기 전용 예상)
        if not self.connected:
            try:
                self.device = serial.Serial(port=serial_port, baudrate=baudrate, timeout=timeout)
                self.mode = 'serial'
                self.connected = True
                print("[!] VISA 실패, Serial로 연결 성공:", serial_port)
            except Exception as e:
                print("[✗] serial 연결 실패:", e)

    def checksum_writer(self, command: str) -> bytes:
        ascii_array = [1] + [ord(c) for c in command]
        checksum = sum(ascii_array) % 256
        full_command = chr(1) + command + format(checksum, '02X')
        return full_command.encode('ascii')

    def formatter(self, values, formats):
        return [fmt % float(val) for val, fmt in zip(values, formats)]

    def write_command(self, command: str):
        cmd = self.checksum_writer(command)
        if self.mode == 'visa':
            self.device.write_raw(cmd)
        elif self.mode == 'serial':
            self.device.write(cmd)
        time.sleep(5)

    def read_response(self) -> str:
        if self.mode == 'visa':
            try:
                response = self.device.read().strip()
                return response
            except:
                return ""
        elif self.mode == 'serial':
            try:
                response = self.device.readline().decode('ascii', errors='ignore').strip()
                return response
            except:
                return ""

    def change_control_params(self, control_params):
        formatted = self.formatter(control_params, ["%i", "%.3f", "%.3f", "%.3f", "%.3f", "%.3f"])
        cmd_str = ";".join(formatted) + ";1;"  # 루프 enable 포함
        cmd = 'a' + str(len(cmd_str)) + cmd_str
        print(f"[제어 파라미터] {cmd}")
        self.write_command(cmd)

    def change_setpoint_params(self, setpoint_params):
        formatted = self.formatter(setpoint_params, ["%.3f", "%.3f", "%.3f", "%i", "%.2f", "%.2f"])
        cmd_str = "1;" + ";".join(formatted) + ";"  # 채널 번호 포함
        cmd = 'i' + str(len(cmd_str)) + cmd_str
        print(f"[세트포인트] {cmd}")
        self.write_command(cmd)

    def read_temperature(self):
        cmd = 'r3;'
        print(f"[온도 요청]: {cmd}")
        self.write_command(cmd)
        response = self.read_response()
        print(f"[온도 응답]: {response}")
        return response

    def close(self):
        self.device.close()
        print("[✓] 연결 종료됨.")


if __name__ == '__main__':
    controller = OC2Controller(visa_address='ASRL5::INSTR', serial_port='COM5')

    if controller.connected:
        controller.change_setpoint_params([45.0, 60.0, 40.0, 1, 0.5, 5.0])
        temp = controller.read_temperature()
        print("현재 온도:", temp)
        controller.close()
    else:
        print("장치 연결 실패. pyvisa 또는 시리얼 확인 요망.")

