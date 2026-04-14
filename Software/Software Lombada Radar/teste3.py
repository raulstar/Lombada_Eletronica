import serial
import serial.tools.list_ports
import time
import os
import cv2

webcam =  cv2.VideoCapture( r'rtsp://admin:Revlo123@192.168.15.150:554/cam/realmonitor?channel=1&subtype=0')

#webcam = cv2.VideoCapture(0)
ports = serial.tools.list_ports.comports()
contador = 0
excesso = 30
Velo_max = 0
vel = 0
ports
print(ports)

"""Identificação do dispositivo em cada porta"""

[port.manufacturer for port in ports]

"""Descobre o string da porta associada"""

port = ports[0].device

arduino = serial.Serial(port, baudrate=115200, timeout=1)

arduino.close()
arduino.open()
print("conetado" ,port)

time.sleep(.5)

while True:
     if arduino.in_waiting > 0 :
        handshake_message = arduino.read_until()     
        #print("message: " + handshake_message.decode())
        raw = handshake_message.decode()
        try:
            t, periodo, V = raw.rstrip().split(",")
        except:
            pass   
        #int(t), int(periodo), int(V)
        vel = int(t) 
        #print(type(vel))
        arduino.flush()

     if webcam.isOpened():
        validacao, frame = webcam.read()
    
       #`` cv2.imshow("Video da Webcam {vel}", frame)
        if (vel > 0) and (vel <  excesso) :
            contador =  contador + 1
            cv2.imwrite(f"Velocidade {vel}Km {contador}.png", frame)
            print(vel)
            print("contador", contador)
            vel = 0
            time.sleep(1)
        if vel > Velo_max :
            excesso =  excesso + 1
            cv2.imwrite(f"Velo Excesso {vel}Km {excesso}.png", frame)
            print(vel)
            print("excesso", excesso)
            time.sleep(1)   
        key = cv2.waitKey(5)
        if key == 27: # ESC
            webcam.release()
            cv2.destroyAllWindows()
            break
        
        