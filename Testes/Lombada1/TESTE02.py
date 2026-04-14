import cv2
import numpy as np
from datetime import datetime

# Configurações iniciais
conf = {
    "max_disappear": 10,
    "distância_máxima": 175,
    "objeto_de_trilha": 4,
    "confiança": 0.4,
    "largura_do_quadro": 400,
    "zona_de_estimativa_de_velocidade": {"A": 120, "B": 160, "C": 200, "D": 240},
    "distância": 16,  # distância real em metros
    "limite_de_velocidade": 15  # em MPH
}

# Função para calcular a velocidade média
def calculate_speed(speeds):
    if len(speeds) > 0:
        return sum(speeds) / len(speeds)
    return 0

# Função para registrar a velocidade em um arquivo de log
def log_speed(speed):
    with open("speed_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: {speed:.2f} MPH\n")

# Função para inicializar a câmera
def initialize_camera(video_source):
    vs = cv2.VideoCapture(video_source)
    if not vs.isOpened():
        raise ValueError("Não foi possível abrir a câmera.")
    return vs

# Função para processar o quadro e desenhar o retângulo
def process_frame(frame, trackableObjects, bg_subtractor, metroPorPixel):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    fg_mask = bg_subtractor.apply(frame)
    blurred = cv2.GaussianBlur(fg_mask, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)

    # Dilatação para preencher pequenos buracos
    thresh = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    objects = {}

    # Calculando a área da imagem para filtrar contornos
    frame_height, frame_width = frame.shape[:2]
    min_area = (frame_height * frame_width) * 0.01  # 1% da área total

    for c in contours:
        if cv2.contourArea(c) < min_area:  # Filtrando pequenos objetos/ruído
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        centroid = (int(x + w // 2), int(y + h // 2))
        objectID = len(objects) + 1
        objects[objectID] = centroid

        to = trackableObjects.get(objectID, None)
        if to is None:
            to = TrackableObject(objectID, centroid)

        # Estimativa de velocidade
        if to.lastPoint and not to.estimated:
            speeds = []
            for i, j in [("A", "B"), ("B", "C"), ("C", "D")]:
                d = to.position[j] - to.position[i]
                distanceInPixels = abs(d)
                if distanceInPixels == 0:
                    continue
                t = to.timestamp[j] - to.timestamp[i]
                timeInSeconds = abs(t.total_seconds())
                if timeInSeconds > 0:  # Prevenir divisão por zero
                    distanceInMeters = distanceInPixels * metroPorPixel
                    speed = (distanceInMeters / timeInSeconds) * 2.23694  # Convertendo para MPH
                    speeds.append(speed)

            to.speedMPH = calculate_speed(speeds)
            log_speed(to.speedMPH)  # Logar a velocidade
            to.estimated = True
            print(f"[INFO] Velocidade do veículo que acabou de passar é: {to.speedMPH:.2f} MPH")
            if to.speedMPH > conf["limite_de_velocidade"]:
                print(f"[ALERT] Velocidade acima do limite: {to.speedMPH:.2f} MPH")

        trackableObjects[objectID] = to

        # Desenhar retângulo ao redor do objeto
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Desenhar o ID do objeto e o centroide
        text = f"ID {objectID}"
        cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        # Exibir status de velocidade
        status_text = "Acima do limite" if to.speedMPH > conf["limite_de_velocidade"] else "Dentro do limite"
        cv2.putText(frame, f"Status: {status_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    return frame

# Classe para objetos rastreáveis
class TrackableObject:
    def __init__(self, objectID, centroid):
        self.objectID = objectID
        self.centroids = [centroid]
        self.timestamp = {"A": datetime.now(), "B": datetime.now(), "C": datetime.now(), "D": datetime.now()}
        self.position = {"A": 0, "B": 0, "C": 0, "D": 0}
        self.direction = None
        self.lastPoint = False
        self.estimated = False
        self.speedMPH = 0.0
        self.logged = False

# Função principal
def main():
    # Inicializando configurações e inputs
    try:
        conf["limite_de_velocidade"] = float(input("Digite o limite de velocidade em MPH: "))
        metroPorPixel = float(input("Digite a conversão de pixels para metros: "))
        camera_type = input("Digite '0' para câmera padrão ou o caminho da câmera USB: ")
        video_source = int(camera_type) if camera_type.isdigit() else camera_type
        vs = initialize_camera(video_source)
        trackableObjects = {}
        bg_subtractor = cv2.createBackgroundSubtractorMOG2()
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    contador_frames = 0  # Contador de frames

    # Loop principal
    while True:
        ret, frame = vs.read()
        if not ret:
            break

        frame = process_frame(frame, trackableObjects, bg_subtractor, metroPorPixel)

        # Exibição do quadro processado
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        contador_frames += 1  # Incrementar contador de frames

    # Finalizando
    cv2.destroyAllWindows()
    vs.release()APS

if __name__ == "__main__":
    main()

