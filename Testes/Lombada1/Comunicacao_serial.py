import serial

velocidade = "36 km"

try:

    conexao = serial.Serial("COM3", 9600, timeout=0.5)
    print(conexao)
    print("Conecxao na porta", conexao.portstr)
except serial.SerialException:
    print("nao conectado")
    pass

while True:
    serialstring = ""
    ##velocidade = input("Digite o comando ")

    conexao.write(velocidade.encode(encoding='ascii', errors='strict'))
    
    #conexao.write(b"teste")
    # if comando == "l":
    #     conexao.write(b'1')
    # else: 
    #     conexao.write(b'0')

    if  input("Continue?").upper()=="N":
         break

conexao.close()
print("Conecao fechada")