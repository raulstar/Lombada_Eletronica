import cv2
import time
import os
from datetime import datetime

# Carrega o classificador
classifier_path = r"Lombada-eletronica\cars.xml"
classifier = cv2.CascadeClassifier(classifier_path)

# Distância conhecida em metros entre dois pontos de referência (ex: linha na pista)
distancia_real = 2  # Ajuste conforme necessário
velocidade_limite = 20  # Limite de velocidade em KM/H
log_path = r"Lombada-eletronica\imagens_acima_limite"

# Função para criar pasta se não existir
def create_directory(path):
    os.makedirs(path, exist_ok=True)

def detecta_objetos(frame):
    """Detecta objetos em um frame e retorna suas posições."""
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Converte o frame para escala de cinza
    objetos = classifier.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))  
    return objetos

def calcular_velocidade(distancia_pixels, tempo):
    """Calcula a velocidade em KM/H dado a distância em pixels e o tempo em segundos."""
    if distancia_pixels > 0 and tempo > 0:
        # Calcula a velocidade em metros por segundo
        velocidade_mps = (distancia_real / tempo)  # Metros por segundo
        velocidade_kmh = velocidade_mps * 3.6  # Converte para km/h
        return velocidade_kmh
    return 0

def save_snapshot(frame, objectID, speed):
    """Salva uma imagem quando o objeto ultrapassa o limite de velocidade."""
    snapshot_filename = f"objeto_{objectID}_speed_{speed:.2f}KMH_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    snapshot_path = os.path.join(log_path, snapshot_filename)
    cv2.imwrite(snapshot_path, frame)
    print(f"[INFO] Imagem salva: {snapshot_path}")

def simulator(video):
    """Executa a simulação da detecção de objetos em um vídeo."""
    if not video.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    create_directory(log_path)

    objectID = 0  # Identificador único para o objeto
    fps = video.get(cv2.CAP_PROP_FPS)  # Pega o FPS do vídeo
    print(f"[INFO] FPS do vídeo: {fps}")

    objetos_detectados = {}  # Armazena objetos detectados e suas informações

    while True:
        ret, frame = video.read()
        if not ret:
            print("Fim do vídeo ou erro ao ler o frame.")
            break

        # Detecta objetos
        objetos = detecta_objetos(frame)
        print(f"[DEBUG] Objetos detectados: {len(objetos)}")

        for (x, y, w, h) in objetos:
            # Desenha o retângulo verde ao redor do objeto detectado
            cv2.rectangle(frame, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)

            # Marca o objeto como detectado
            if objectID not in objetos_detectados:
                # Adiciona objeto a lista de objetos detectados
                objetos_detectados[objectID] = {
                    "posicao_inicial": x,  # Posição inicial do objeto
                    "tempo_inicial": time.time(),  # Tempo em que o objeto foi detectado
                    "velocidade_calculada": False,  # Flag para indicar se a velocidade foi calculada
                }
            else:
                # Se o objeto já foi detectado e ele saiu do frame
                if x + w < 0 and not objetos_detectados[objectID]["velocidade_calculada"]:
                    tempo_decorrido = time.time() - objetos_detectados[objectID]["tempo_inicial"]
                    distancia_pixels = abs(objetos_detectados[objectID]["posicao_inicial"] - (x + w))

                    velocidade_kmh = calcular_velocidade(distancia_pixels, tempo_decorrido)
                    if velocidade_kmh > 0:  # Verifica se a velocidade é válida
                        print(f"Objeto {objectID} - Velocidade: {velocidade_kmh:.2f} KM/H")

                        # Salva uma imagem se a velocidade ultrapassar o limite
                        if velocidade_kmh > velocidade_limite:
                            save_snapshot(frame, objectID, velocidade_kmh)

                    # Marca que a velocidade foi calculada
                    objetos_detectados[objectID]["velocidade_calculada"] = True
            
            # Se o objeto sair da área, reseta as informações para o próximo objeto
            if x + w < 0:  # Se o objeto já saiu do frame
                del objetos_detectados[objectID]  # Remove o objeto da lista de objetos detectados
                objectID += 1  # Incrementa o ID do objeto detectado

        # Mostra o frame com as detecções e retângulos verdes
        cv2.imshow('Detecção de Objetos', frame)

        if cv2.waitKey(1) == ord('q'):  # Pressione 'q' para sair
            break

    video.release()
    cv2.destroyAllWindows()

# Inicia a captura de vídeo
def main():
    mode = input("Digite 'c' para usar a câmera ou 'v' para usar um vídeo: ")
    
    try:
        if mode.lower() == 'c':
            video = cv2.VideoCapture(0)  # Webcam padrão
            print("[INFO] Inicializando webcam...")
        elif mode.lower() == 'v':
            video_path = r"Lombada-eletronica\20241023_091252.mp4"
            video = cv2.VideoCapture(video_path)
            print("[INFO] Inicializando vídeo de teste...")
        else:
            raise ValueError("Modo inválido. Digite 'c' para câmera ou 'v' para vídeo.")

        simulator(video)

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
