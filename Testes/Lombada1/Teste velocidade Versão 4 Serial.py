import cv2
import numpy as np
import os
from datetime import datetime

# Configurações iniciais
conf = {
    "max_disappear": 10,
    "distância_máxima": 175,
    "objeto_de_trilha": 4,
    "confiança": 0.9,
    "largura_do_quadro": 400,
    "zona_de_estimativa_de_velocidade": {"A": 120, "B": 160, "C": 200, "D": 240},
    "distância_real": 14,  # distância real em metros entre os pontos
    "limite_de_velocidade": 10  # em MPH
}

mode = "v" #Digite 'c' para usar a câmera ou 'v' para usar um vídeo: 
video_path = r"Amostras\Carros_passando.mp4"  # Caminho do vídeo de teste
conf["limite_de_velocidade"] = float = 20 #Digite a conversão de pixels para metros:
metroPorPixel = float = 20 #(input("Digite a conversão de pixels para metros: "))


# Caminho fixo para salvar o log e imagens
log_path = r"imagens_Carros"  # Coloque aqui o caminho da pasta que deseja salvar

# Função para criar a pasta, se não existir
def create_directory(path):
    os.makedirs(path, exist_ok=True)

# Função para calcular a velocidade com base na distância e tempo
def calculate_speed_by_distance_time(start_time, end_time, distancia_real):
    time_elapsed = (end_time - start_time).total_seconds()
    if time_elapsed > 0:
        velocidade_mps = distancia_real / time_elapsed  # Velocidade em metros por segundo
        velocidade_mph = velocidade_mps * 2.23694  # Conversão para MPH
        return velocidade_mph
    return 0

# Função para converter MPH para KM/H
def convert_mph_to_kmh(speed_mph):
    return speed_mph * 1.60934  # 1 MPH = 1.60934 KM/H

# Função para registrar a velocidade em um arquivo de log na pasta especificada
def log_speed(speed):
    log_file_path = os.path.join(log_path, "speed_log.txt")
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{datetime.now()}: {speed:.2f} MPH\n")

# Função para tirar print e salvar a imagem quando o carro ultrapassar a velocidade limite
def save_snapshot(frame, objectID, speed):
    snapshot_filename = f"carro_{objectID}_speed_{speed:.2f}_MPH_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    snapshot_path = os.path.join(log_path, snapshot_filename)
    cv2.imwrite(snapshot_path, frame)
    print(f"[INFO] Imagem salva: {snapshot_path}")

# Função para inicializar a câmera
def initialize_camera():
    vs = cv2.VideoCapture(0)  # Webcam padrão
    if not vs.isOpened():
        raise ValueError("Não foi possível abrir a câmera. Verifique se está conectada corretamente.")
    return vs

# Função para inicializar o vídeo de teste
def initialize_video(video_path):
    vs = cv2.VideoCapture(video_path)
    if not vs.isOpened():
        raise ValueError("Não foi possível abrir o vídeo. Verifique se o caminho está correto.")
    return vs

# Função para processar o quadro
def process_frame(frame, trackableObjects, bg_subtractor, metroPorPixel):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    fg_mask = bg_subtractor.apply(frame)
    blurred = cv2.GaussianBlur(fg_mask, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    objects = {}

    frame_height, frame_width = frame.shape[:2]
    min_area = (frame_height * frame_width) * 0.01

    for c in contours:
        if cv2.contourArea(c) < min_area:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        centroid = (int(x + w // 2), int(y + h // 2))
        objectID = len(objects) + 1
        objects[objectID] = centroid

        to = trackableObjects.get(objectID, None)
        if to is None:
            to = TrackableObject(objectID, centroid)
            to.timestamp['A'] = datetime.now()

        to.centroids.append(centroid)

        # Se o objeto se moveu de um ponto "A" até um ponto "B"
        if len(to.centroids) >= 2 and to.crossed_A_B(conf['zona_de_estimativa_de_velocidade']):
            start_time = to.timestamp['A']
            end_time = datetime.now()
            speed_mph = calculate_speed_by_distance_time(start_time, end_time, conf['distância_real'])
            speed_kmh = convert_mph_to_kmh(speed_mph)
            
            to.speedMPH = speed_mph
            log_speed(to.speedMPH)  # Log na pasta especificada
            to.timestamp['D'] = end_time
            print(f"[INFO] Velocidade do veículo: {to.speedMPH:.2f} MPH | {speed_kmh:.2f} KM/H")
            if to.speedMPH > conf["limite_de_velocidade"]:
                print(f"[ALERT] Velocidade acima do limite: {to.speedMPH:.2f} MPH")
                save_snapshot(frame, to.objectID, to.speedMPH)  # Salvar o print do carro

        trackableObjects[objectID] = to
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = f"ID {objectID}"
        cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

    return frame

# Função para checar se o carro cruzou a zona de estimativa de velocidade
class TrackableObject:
    def __init__(self, objectID, centroid):
        self.objectID = objectID
        self.centroids = [centroid]
        self.timestamp = {"A": datetime.now(), "B": datetime.now(), "C": datetime.now(), "D": datetime.now()}
        self.lastPoint = False
        self.estimated = False
        self.speedMPH = 0.0

    def crossed_A_B(self, zona):
        # Checa se o carro cruzou de uma zona "A" para uma zona "B"
        if (self.centroids[-1][1] > zona["A"] and self.centroids[-1][1] < zona["B"]):
            self.timestamp['B'] = datetime.now()
            return True
        return False

# Função principal
def main():
    #video_path = r"Amostras\Carros_passando.mp4"  # Caminho do vídeo de teste
    #mode = input("Digite 'c' para usar a câmera ou 'v' para usar um vídeo: ")


    try:
        create_directory(log_path)  # Criando pasta para salvar o log de velocidades
        #conf["limite_de_velocidade"] = float(input("Digite o limite de velocidade em MPH: "))
        #metroPorPixel = float(input("Digite a conversão de pixels para metros: "))
        
        if mode.lower() == 'c':
            print("[INFO] Inicializando webcam...")
            vs = initialize_camera()
        elif mode.lower() == 'v':
            print("[INFO] Inicializando vídeo de teste...")
            vs = initialize_video(video_path)
        else:
            raise ValueError("Modo inválido. Digite 'c' para câmera ou 'v' para vídeo.")
        
        trackableObjects = {}
        bg_subtractor = cv2.createBackgroundSubtractorMOG2()
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    while True:
        ret, frame = vs.read()
        if not ret:
            print("[WARNING] O vídeo terminou ou não pode ser lido.")
            break

        frame = process_frame(frame, trackableObjects, bg_subtractor, metroPorPixel)
        cv2.imshow("Detecção de Velocidade", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    vs.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
