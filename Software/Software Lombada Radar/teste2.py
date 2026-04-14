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

if webcam.isOpened():
    validacao, frame = webcam.read()
    while validacao:
        validacao, frame = webcam.read()
        cv2.imshow("Video da Webcam", frame)
        key = cv2.waitKey(5)
        RX  = conexao.readline()    
        line = RX.decode("utf-8")
        print(line)
        if (line > 0) :
            print(line)
    
        if key == 27: # ESC
            break
    cv2.imwrite("FotoLira.png", frame)

webcam.release()
cv2.destroyAllWindows()