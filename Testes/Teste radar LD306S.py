import serial
#115200

def receber_dados_serial(porta, baudrate):

    ser = serial.Serial(porta, baudrate)
    dados = ser.read(size=12)  # Lê 14 bytes (tamanho do array de exemplo)
    ser.close()
    print('.')
    return dados

def processar_dados(dados):

    #dados = ser.read(14)  # Lê 14 bytes
    array = [int(x) for x in dados]
    print(array)
    #hex_dados = [hex(dado) for dado in dados]
    #print(array[8])
    # if (array[8] <100):
    #     print(array[8])
   
    
if __name__ == "__main__":
    porta_serial = "COM6"
    baudrate = 9600
    while True:
        dados_recebidos = receber_dados_serial(porta_serial, baudrate)
        processar_dados(dados_recebidos)