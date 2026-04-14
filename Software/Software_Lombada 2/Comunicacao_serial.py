import serial
import time

try:
    conexao = serial.Serial("COM7", 9600, timeout=0.5)
    conexao.write(2)
    print("Conectado na porta", conexao.portstr)
    
except serial.SerialException:
    print("Porta serial nao conectado")
    comunicacao = 0
    pass


def envia(numero):
    if comunicacao == 1:
        time.sleep(1)   
        conexao.write(numero.encode(encoding='ascii', errors='strict'))
        conexao.flush()
        print("enviado " + numero)
    else:
        print("Não enviado pela serial") 


