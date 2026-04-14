import serial
import time
import os
import cv2

webcam = cv2.VideoCapture(0)

try:
    conexao = serial.Serial("COM14", 9600, timeout=0.5)  #Porta serial atribuídaao dispositivo de acionamento
    time.sleep(2)
    print(conexao)
    print("")
    print("Dispositivo conectado na porta ", conexao.portstr)
  

except serial.SerialException:
    print("Dispositivo de acionamento nao encontrado:")

while True:
    
    RX  = conexao.readline(1)
    #print(RX)
    line = RX.decode("utf-8")
    limpo = line.strip()
    print(int(limpo))
    #print(int(limpo.strip()))
    #print(type(line))
    #velo = int(line)      
    conexao.flush()
    
    time.sleep(.5)