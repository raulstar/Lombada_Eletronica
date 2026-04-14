import cv2  # Importa a biblioteca OpenCV
from tracker import EuclideanDistTracker, inicio_max, inicio_mim, final_max, final_mim 
import numpy as np  
import math
import time


tracker = EuclideanDistTracker()


cap = cv2.VideoCapture(r"C:\Users\Raulstar\Meu Drive (autorobotica.sp@gmail.com)\Lombada eletronica\edicaoTester\teste\Testando\20241023_091252.mp4")


if not cap.isOpened():

    print("Erro ao carregar o vídeo. Verifique o caminho do arquivo.")
    exit()

f = 30  
w = int(1000 / (f - 1)) 

# Configuração de detecção de objetos
object_detector = cv2.createBackgroundSubtractorMOG2(history=None, varThreshold=None)

# Kernels para operações morfológicas
kernalOp = np.ones((3, 3), np.uint8)
kernalCl = np.ones((11, 11), np.uint8)
cap = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
kernal_e = np.ones((5, 5), np.uint8)


def ajuste_tela():
    print("Escolha a resolução da câmera e pressione o Enter por favor:")
    print("1. 320x240")
    print("2. 640x480")
    print("3. 720x480")
    print("4. 1280x720")
    print("5. 1920x1080")
    print("6. Personalizar resolução")

    try:
        escolha = int(input("Digite o número correspondente à sua escolha: "))

        if escolha == 1:
            largura, altura = 320, 240
        elif escolha == 2:
            largura, altura = 640, 480
        elif escolha == 3:
            largura, altura = 720, 480
        elif escolha == 4:
            largura, altura = 1280, 720
        elif escolha == 5:
            largura, altura = 1920, 1080
        elif escolha == 6:
            largura = int(input("Digite a largura da resolução (x): "))
            altura = int(input("Digite a altura da resolução (y): "))
        else:
            print("Escolha inválida. Por favor, tente novamente.")
            return ajuste_tela()

        # Ajuste a janela com a resolução escolhida
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Frame", largura, altura)
        print(f"Resolução ajustada para {largura}x{altura}.")
        return largura, altura

    except ValueError:
        print("Erro: Por favor, insira um número válido.")
        return ajuste_tela()
class EuclideanDistTracker:
    def __init__(self):
      
        self.center_points = {}

        self.id_count = 0
        self.et = 0
        self.s1 = np.zeros((1, 1000))  
        self.s2 = np.zeros((1, 1000))  
        self.f = np.zeros(1000)     
        self.count = 0
        self.exceeded = 0

       
        self.distancia_metros = 10  

    def update(self, objects_rect):
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # CHECK IF OBJECT IS DETECTED ALREADY
            same_object_detected = False

            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 60:  # Distância máxima para considerar o mesmo objeto
                    self.center_points[id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True

                    # START TIMER: Quando o objeto cruza a primeira linha
                    if inicio_max <= y <= inicio_mim:  # Ajuste os valores de ROI corretamente
                        if self.s1[0, id] == 0:  # Apenas marque uma vez
                            self.s1[0, id] = time.time()

                    # STOP TIMER: Quando o objeto cruza a segunda linha
                    if final_max <= y <= final_mim:  # Ajuste os valores de ROI corretamente
                        if self.s2[0, id] == 0:  # Apenas marque uma vez
                            self.s2[0, id] = time.time()
                            self.s[0, id] = self.s2[0, id] - self.s1[0, id]

                    # CAPTURE FLAG: Marca para captura adicional
                    if y < 235:  # Ajuste com base no seu ROI
                        self.f[id] = 1

            # NEW OBJECT DETECTION
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1
                self.s[0, self.id_count] = 0
                self.s1[0, self.id_count] = 0
                self.s2[0, self.id_count] = 0

        # ASSIGN NEW ID to OBJECT
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        self.center_points = new_center_points.copy()
        return objects_bbs_ids

    # CALCULATE SPEED
    def getsp(self, id):
        if self.s[0, id] != 0:
            # Verifica se o tempo é válido para evitar divisões por números pequenos
            tempo = self.s[0, id]
            if tempo > 0.1:  # Apenas considere valores significativos
                velocidade = self.distancia_metros / tempo  # m/s
                velocidade_kmh = velocidade *3.6 # Converte para km/h
            else:
                velocidade_kmh = 0
        else:
            velocidade_kmh = 0

        return round(velocidade_kmh, 2)
    










def configurar_fps():
    print("Escolha o FPS desejado antes de iniciar o vídeo:")
    print("1. 30 FPS")
    print("2. 60 FPS")
    print("3. 75 FPS")
    print("4. 144 FPS")
    print("5. 180 FPS")
    print("6. 240 FPS")
    print("7. Personalizado (Digite o valor desejado, LEMBRANDO QUE ISSO DEPENDE DA MÁQUINA USADA, SENDO ELA PC, CÂMERA OU ARDUÍNOS PARA TRANSMITIREM IMAGEM)")

    try:
        escolha = int(input("Digite o número correspondente à sua escolha: "))
        if escolha == 1:
            fps = 30
        elif escolha == 2:
            fps = 60
        elif escolha == 3:
            fps = 75
        elif escolha == 4:
            fps = 144
        elif escolha == 5:
            fps = 180
        elif escolha == 6:
            fps = 240
        elif escolha == 7:
            fps = int(input("Digite o FPS desejado (máximo depende do hardware): "))
            if fps < 1 or fps > 1000:  
                print("FPS inválido. Configurando para 30 FPS.")
                fps = 30
        else:
            print("Escolha inválida. Configurando para 30 FPS por padrão.")
            fps = 30
        print(f"FPS configurado para {fps}.")
        return fps
    except ValueError:
        print("Erro: Entrada inválida. Configurando para 30 FPS por padrão.")
        return 30

# Função para capturar vídeo de uma câmera ou arquivo
def capturar_video(fps):
    cap = cv2.VideoCapture(0)  # Mude para o índice correto ou caminho do vídeo
    if not cap.isOpened():
        print("Erro ao abrir a câmera ou o vídeo.")
        return

    # Calcula o intervalo entre os frames com base no FPS
    intervalo = int(1000 / fps)  # Em milissegundos

    print(f"Capturando vídeo a {fps} FPS. Pressione 'ESC' para sair.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fim do vídeo ou erro na captura.")
            break

        # Mostra o frame na tela
        cv2.imshow("Vídeo", frame)

        # Aguarda o tempo correto entre frames
        key = cv2.waitKey(intervalo)
        if key == 27:  # Tecla ESC para sair
            print("Finalizando...")
            break

    cap.release()
    cv2.destroyAllWindows()


fps = configurar_fps()  
capturar_video(fps)    













def ajuste_area_interesse(height):
    print("Escolha a área de interesse e pressione Enter:")
    print("1. Parte de cima da tela")
    print("2. Parte de baixo da tela")
    print("3. Parte do centro")
    print("4. Personalize sua área de interesse")

    try:
        escolha = int(input("Digite o número correspondente à sua escolha: "))

        if escolha == 1:
            inicio_max = int(height * 0.1)  # 10% da altura da tela
            inicio_mim = int(height * 0.15)  # 15% da altura da tela
            final_max = int(height * 0.2)  # 20% da altura da tela
            final_mim = int(height * 0.25)  # 25% da altura da tela
            print("Área de interesse ajustada para a parte superior da tela.")

        elif escolha == 2:
            inicio_max = int(height * 0.4)  # 40% da altura da tela (antes: 50%)
            inicio_mim = int(height * 0.5) # 60% da altura da tela (antes: 75%)
            final_max = int(height * 0.60) # 65% da altura da tela (antes: 80%)
            final_mim = int(height * 0.7)  # 70% da altura da tela (antes: 85%)

            print("Área de interesse ajustada para a parte inferior da tela.")

        elif escolha == 3:
            inicio_max = int(height * 0.4)  # 40% da altura da tela
            inicio_mim = int(height * 0.45)  # 45% da altura da tela
            final_max = int(height * 0.5)  # 50% da altura da tela
            final_mim = int(height * 0.55)  # 55% da altura da tela
            print("Área de interesse ajustada para a área central da tela.")

        elif escolha == 4:
            print("Personalize sua área de interesse:")
            inicio_max = int(input("Digite a posição (em pixels) da linha superior: "))
            inicio_mim = int(input("Digite a posição (em pixels) da linha inferior: "))
            final_max = int(input("Digite a posição (em pixels) da segunda linha superior: "))
            final_mim = int(input("Digite a posição (em pixels) da segunda linha inferior: "))
            print("Área de interesse personalizada definida.")

        else:
            print("Escolha inválida. Por favor, tente novamente.")
            return ajuste_area_interesse(height)

        return inicio_max, inicio_mim, final_max, final_mim

    except ValueError:
        print("Erro: Por favor, insira um número válido.")
        return ajuste_area_interesse(height)






# Chamar o ajuste de tela antes de iniciar o loop principal
largura, altura = ajuste_tela()
inicio_max, inicio_mim, final_max, final_mim = ajuste_area_interesse(altura)
while True:
    
    ret, frame = cap.read()
    if not ret:
        print("Fim do vídeo ou erro ao ler o frame.")
        break

    # Redimensionar o frame para a resolução escolhida
    frame = cv2.resize(frame, (largura, altura))
    height, width, _ = frame.shape

    # Método de mascaramento (análise do frame completo)
    fgmask = fgbg.apply(frame)
    ret, imBin = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    mask1 = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernalOp)
    mask2 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernalCl)
    e_img = cv2.erode(mask2, kernal_e)

    # Encontra contornos na máscara processada
    contours, _ = cv2.findContours(e_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []

    # Filtrar contornos que estão abaixo da linha de interesse
       # Filtrar contornos que estão abaixo da linha de interesse
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:  # Ajuste a área mínima para ignorar objetos irrelevantes
            x, y, w, h = cv2.boundingRect(cnt)

            # Adicione um filtro para tamanho mínimo do contorno
            if w > 30 and h > 30 and y > int(height * inicio_mim / 720):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                detections.append([x, y, w, h])

    # Dentro do loop principal
        # Rastreamento de objetos (mova esta linha para antes do uso de boxes_ids)
    boxes_ids = tracker.update(detections)

    # Dentro do loop principal
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        velocidade = tracker.getsp(id)

        if y >= int(height * inicio_mim / 720):
            if velocidade < tracker.limit():
                cv2.putText(frame, f"{id} {velocidade} km/h", (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            else:
                cv2.putText(frame, f"{id} {velocidade} km/h", (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 3)

            if tracker.f[id] == 1 and velocidade != 0:
                tracker.capture(frame, x, y, h, w, velocidade, id)


    # Rastreamento de objetos
    boxes_ids = tracker.update(detections)

    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        velocidade = tracker.getsp(id)

        if y >= int(height * inicio_mim / 720):
            if velocidade < tracker.limit():
                cv2.putText(frame, f"{id} {velocidade}", (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            else:
                cv2.putText(frame, f"{id} {velocidade}", (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 3)

            if tracker.f[id] == 1 and velocidade != 0:
                tracker.capture(frame, x, y, h, w, velocidade, id)

    
    cv2.line(frame, (0, inicio_max), (width, inicio_max), (0, 0, 255), 2)
    cv2.line(frame, (0, inicio_mim), (width, inicio_mim), (0, 0, 255), 2)
    cv2.line(frame, (0, final_max), (width, final_max), (0, 0, 255), 2)
    cv2.line(frame, (0, final_mim), (width, final_mim), (0, 255, 255), 2)


    # Exibe o frame na janela redimensionada
    cv2.imshow("Frame", frame)

    # Controle de execução
    key = cv2.waitKey(w - 10)
    if key == 27:  # Tecla ESC para sair
        tracker.end()
        break


# Finaliza

tracker.end()
cap.release()
cv2.destroyAllWindows()
