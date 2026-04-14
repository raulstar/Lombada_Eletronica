import cv2
import math
import time
import numpy as np
import os

# Configurações de limite de velocidade
limit = 30  # km/h
traffic_record_folder_name = "TrafficRecord"
distance_between_points = 5.0  # Distância entre os pontos em metros

# Criação da pasta para salvar os registros, se não existir
if not os.path.exists(traffic_record_folder_name):
    os.makedirs(traffic_record_folder_name)
    os.makedirs(traffic_record_folder_name + "//exceeded")

# Caminho para o arquivo de registro de velocidade
speed_record_file_location = traffic_record_folder_name + "//SpeedRecord.txt"
file = open(speed_record_file_location, "w")
file.write("ID \t SPEED\n------\t-------\n")
file.close()

# Classe para controle de detecção e velocidade
class EuclideanDistTracker:
    def __init__(self):
        self.center_points = {}
        self.id_count = 0
        self.time_entered = {}
        self.speed_records = {}
        self.count = 0
        self.exceeded = 0

    def update(self, objects_rect):
        objects_bbs_ids = []
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            same_object_detected = False

            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 70:
                    self.center_points[id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True

                    # Marca o tempo de entrada do objeto
                    if id not in self.time_entered:
                        self.time_entered[id] = time.time()

                    # Calcula a velocidade quando o objeto ultrapassa a linha
                    if y < 235:  # Linha de detecção
                        time_now = time.time()
                        time_passed = time_now - self.time_entered[id]
                        if time_passed > 0:  # Evitar divisão por zero
                            speed = (distance_between_points / time_passed) * 3.6  # Converte para km/h
                            self.speed_records[id] = speed
                            self.capture(x, y, h, w, speed, id)

                    # Remove o ID se o objeto já não estiver mais na tela
                    if y > 540:  # Ajuste conforme a altura do vídeo
                        del self.center_points[id]
                        del self.time_entered[id]

            if not same_object_detected:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        return objects_bbs_ids

    def capture(self, x, y, h, w, sp, id):
        # Certificando-se de que a ROI está correta para captura
        if y - 5 >= 0 and y + h + 5 <= roi.shape[0] and x - 5 >= 0 and x + w + 5 <= roi.shape[1]:
            crop_img = roi[y - 5:y + h + 5, x - 5:x + w + 5]
            n = str(id) + "_speed_" + str(int(sp))
            file = traffic_record_folder_name + '//' + n + '.jpg'
            cv2.imwrite(file, crop_img)
            self.count += 1
            filet = open(speed_record_file_location, "a")
            if sp > limit:
                file2 = traffic_record_folder_name + '//exceeded//' + n + '.jpg'
                cv2.imwrite(file2, crop_img)
                filet.write(str(id) + " \t " + str(int(sp)) + "<---exceeded\n")
                self.exceeded += 1
            else:
                filet.write(str(id) + " \t " + str(int(sp)) + "\n")
            filet.close()

            # Registro da velocidade no prompt de comando
            print(f"ID {id}: Speed = {int(sp)} km/h")

    def end(self):
        file = open(speed_record_file_location, "a")
        file.write("\n-------------\n")
        file.write("-------------\n")
        file.write("SUMMARY\n")
        file.write("-------------\n")
        file.write("Total Vehicles :\t" + str(self.count) + "\n")
        file.write("Exceeded speed limit :\t" + str(self.exceeded))
        file.close()

# Inicializando o rastreador
tracker = EuclideanDistTracker()

# Captura de vídeo
cap = cv2.VideoCapture(r"Lombada-eletronica\20241023_091252.mp4")
f = 25
w = int(1000 / (f - 1))

# Detector de objetos
object_detector = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

# KERNAL para operações morfológicas
kernalOp = np.ones((3, 3), np.uint8)
kernalCl = np.ones((11, 11), np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, None, fx=1.0, fy=1.0)  # Aumenta a escala para o dobro
    height, width, _ = frame.shape

    # Região de interesse
    roi = frame[50:540, 200:960]

    # Aplicação de máscara
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)

    fgmask = object_detector.apply(roi)
    ret, imBin = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    mask1 = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernalOp)
    mask2 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernalCl)

    contours, _ = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 4000:  # Ajustar o limite da área
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = w / h  # Proporção largura/altura
            if 1.2 < aspect_ratio < 3.0:  # Verifica se a proporção está dentro do intervalo (ajustar conforme necessário)
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)  # Desenha retângulo verde
                detections.append([x, y, w, h])

    # Rastreamento de objetos
    boxes_ids = tracker.update(detections)

    # Linhas de referência
    cv2.line(roi, (0, 410), (960, 410), (0, 0, 255), 2)
    cv2.line(roi, (0, 235), (960, 235), (0, 255, 255), 2)

    cv2.imshow("ROI", roi)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

tracker.end()
cap.release()
cv2.destroyAllWindows()
