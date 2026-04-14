import serial
import serial.tools.list_ports
import time
import os
import cv2
import datetime
import csv
##############################################################################################################################
#webcam =  cv2.VideoCapture( r'rtsp://admin:Revlo123@192.168.15.150:554/cam/realmonitor?channel=1&subtype=0')
webcam = cv2.VideoCapture(0)

agora = datetime.datetime.now()
hora = agora.time()
nome_arquivo = "Registro.csv"

contador = 0
excesso = 30
Velo_max = 0
vel = 0

##############################################################################################################################
def registro():
    agora = datetime.datetime.now()
    data_hora_formatada = agora.strftime("%H:%M:%S")
    cabecario = ["Hora","Contador","Velocidade"]
    with open(nome_arquivo, 'a', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow([data_hora_formatada, contador, vel])


##############################################################################################################################
try:
    # ports = serial.tools.list_ports.comports()
    # ports
    # print(ports)
    # [port.manufacturer for port in ports]
    # port = ports[0].device
    # arduino = serial.Serial(port, baudrate=115200, timeout=0.5)

    arduino = serial.Serial("COM14", 11520000, timeout=0.5)
    arduino.reset_input_buffer()
    arduino.close()
    arduino.open()
    print("conetado")
    time.sleep(.3)
except:
    print("dispositivo nao encontrado")
    pass

##############################################################################################################################

while True:
     if arduino.in_waiting > 0 :
        handshake_message = arduino.read_until()     
        #print("message: " + handshake_message.decode())
        raw = handshake_message.decode()
        try:
            t, periodo, V = raw.rstrip().split(",")
        except:
            print("NAO CONECTADO")
            pass   
        #int(t), int(periodo), int(V)
        vel = int(t) 
        print(vel)
        arduino.reset_input_buffer()
        
     if webcam.isOpened():
        validacao, frame = webcam.read()
    
        cv2.imshow("Video da Webcam {vel}", frame)
        if (vel > 0) and (vel <  excesso) :
            contador =  contador + 1
            cv2.imwrite(f"{contador} - {vel}Km .png", frame)           
            print(f"Imagem salva {contador} - {vel}km")
            registro()
            vel = 0            
            time.sleep(1.5)
        elif vel > Velo_max :
            excesso =  excesso + 1
            cv2.imwrite(f"{contador} excesso {vel}Km .png", frame) 
            print(f"Imagem salva {contador} excesso {vel}km")
            vel = 0
            time.sleep(1.5)   
            
        key = cv2.waitKey(5)
        if key == 27: # ESC
            webcam.release()
            cv2.destroyAllWindows()
            arduino.close()
            print("Encerrado")
            break
        
        