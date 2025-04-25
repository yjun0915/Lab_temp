import pyvisa

rm = pyvisa.ResourceManager()
print(rm.list_resources())

instrument = rm.open_resource('ASRL4::INSTR')

instrument.write('SET:TEMP 100')


current_temp = instrument.query('READ:TEMP?')
print(f"현재 온도: {current_temp}°C")