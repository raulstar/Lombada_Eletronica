import cv2
import numpy as np
import os
from datetime import datetime
import serial


# Configurações iniciais
conf = {
    "distância_real": 14,  # distância real em metros entre os pontos
    "limite_de_velocidade": 10,  # em MPH
    "ponto_A": 120,  # Ponto inicial para cálculo de velocidade (coordenada Y)
    "ponto_B": 160,  # Ponto final para cálculo de velocidade (coordenada Y)
}

# Caminho fixo para salvar o log e imagens
log_path_base = r"Lombada-eletronica\imagens_acima_limite"

# Carregar o modelo Haar Cascade
car_cascade = cv2.CascadeClassifier(r"Lombada-eletronica/cars.xml")

# Função para criar subpastas diárias
def create_directory(path):
    os.makedirs(path, exist_ok=True)

def get_log_path():
    date_str = datetime.now().strftime('%Y%m%d')
    log_path = os.path.join(log_path_base, date_str)
    create_directory(log_path)
    return log_path

# Função para calcular a velocidade com base na distância e tempo
def calculate_speed_by_distance_time(start_time, end_time, distancia_real):
    time_elapsed = (end_time - start_time).total_seconds()
    if time_elapsed > 0:
        velocidade_mps = distancia_real / time_elapsed
        velocidade_mph = velocidade_mps * 2.23694  # Conversão para MPH
        return velocidade_mph
    return 0

# Função para registrar a velocidade em um arquivo de log na pasta especificada
def log_speed(speed):
    log_path = get_log_path()
    log_file_path = os.path.join(log_path, f"speed_log_{datetime.now().strftime('%Y%m%d')}.txt")
    velocidade_kmh = speed * 1.60934  # Conversão de MPH para KM/H
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{datetime.now()}: {speed:.2f} MPH ({velocidade_kmh:.2f} KM/H)\n")

# Função para tirar print e salvar a imagem quando o carro ultrapassar a velocidade limite
def save_snapshot(frame, objectID, speed):
    log_path = get_log_path()
    snapshot_filename = f"carro_{objectID}_speed_{speed:.2f}_MPH_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    snapshot_path = os.path.join(log_path, snapshot_filename)
    cv2.imwrite(snapshot_path, frame)
    print(f"[INFO] Imagem salva: {snapshot_path}")

# Função para inicializar a câmera
def initialize_camera():
    vs = cv2.VideoCapture(0)
    if not vs.isOpened():
        raise ValueError("Não foi possível abrir a câmera. Verifique se está conectada corretamente.")
    return vs

# Função para inicializar o vídeo de teste
def initialize_video(video_path):
    vs = cv2.VideoCapture(video_path)
    if not vs.isOpened():
        raise ValueError("Não foi possível abrir o vídeo. Verifique se o caminho está correto.")
    return vs

# Função para processar o quadro com Haar Cascade
def process_frame_with_cascade(frame, trackableObjects, bg_subtractor):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    objects = {}
    frame_height, frame_width = frame.shape[:2]
    min_area = (frame_height * frame_width) * 0.01

    for (x, y, w, h) in cars:
        if w * h < min_area:
            continue

        centroid = (int(x + w // 2), int(y + h // 2))
        objectID = len(objects) + 1
        objects[objectID] = centroid

        to = trackableObjects.get(objectID, None)
        if to is None:
            to = TrackableObject(objectID, centroid)
            to.timestamp['A'] = datetime.now()

        to.centroids.append(centroid)

        # Se o objeto se moveu de um ponto "A" até um ponto "B"
        if len(to.centroids) >= 2 and to.crossed_A_B(conf["ponto_A"], conf["ponto_B"]):
            start_time = to.timestamp['A']
            end_time = datetime.now()
            speed_mph = calculate_speed_by_distance_time(start_time, end_time, conf["distância_real"])

            to.speedMPH = speed_mph
            log_speed(to.speedMPH)
            print(f"[INFO] Velocidade do veículo: {to.speedMPH:.2f} MPH")
            if to.speedMPH > conf["limite_de_velocidade"]:
                print(f"[ALERT] Velocidade acima do limite: {to.speedMPH:.2f} MPH")
                save_snapshot(frame, to.objectID, to.speedMPH)

        trackableObjects[objectID] = to
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = f"ID {objectID} | Speed: {to.speedMPH:.2f} MPH"
        cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

# Classe TrackableObject
class TrackableObject:
    def __init__(self, objectID, centroid):
        self.objectID = objectID
        self.centroids = [centroid]
        self.timestamp = {"A": datetime.now(), "B": datetime.now()}
        self.speedMPH = 0.0

    def crossed_A_B(self, ponto_A, ponto_B):
        if ponto_A < self.centroids[-1][1] < ponto_B:
            self.timestamp['B'] = datetime.now()
            return True
        return False

# Função principal
def main():
    video_path = r"Lombada-eletronica\imagens_Carros\Video veiculo.mp4"
    mode = input("Digite 'c' para usar a câmera ou 'v' para usar um vídeo: ")

    try:
        create_directory(log_path_base)
        conf["limite_de_velocidade"] = float(input("Digite o limite de velocidade em MPH: "))
        
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

        frame = cv2.resize(frame, (640, 480))  # Reduzir resolução para melhorar performance
        frame = process_frame_with_cascade(frame, trackableObjects, bg_subtractor)
        cv2.imshow("Detecção de Velocidade", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    vs.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
