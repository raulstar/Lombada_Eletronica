import serial
import time

porta_serial = "COM13"
baudrate = 9600

while True:
    try:
        ser = serial.Serial(porta_serial, baudrate)
        dados = ser.read(size=12)
        ser.close()
        print('.')
        array_int = [int(x) for x in dados]
        array_hex = [hex(x) for x in dados]
        print(f"Decimal: {array_int}")
        print(f"Hexadecimal: {array_hex}")
    except serial.SerialException as e:
        #exit()
         print('falha')
    time.sleep(0.5)

#Decimal: [85, 165, 10, 211, 0, 0, 0, 0, 0, 0, 0, 0]
#Hexadecimal: ['0x55', '0xa5', '0xa', '0xd3', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0']    