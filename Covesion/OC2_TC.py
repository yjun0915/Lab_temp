import pyvisa

rm = pyvisa.ResourceManager('@py')
try:
    inst = rm.open_resource('ASRL4::INSTR')  # COM3에 해당
    inst.baud_rate = 9600
    inst.timeout = 2000

    inst.write("*IDN?")
    response = inst.read()
    print("장비 응답:", response)

except Exception as e:
    print("에러 발생:", e)
