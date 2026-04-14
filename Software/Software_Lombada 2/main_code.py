############################################
# BIBLIOTECAS
############################################
from deep_sort_realtime.deepsort_tracker import DeepSort
from ultralytics import YOLO
import cv2

from utils import *
from velocidade_utils import *
#from tracker import *
from Comunicacao_serial import*

import logging
logging.getLogger("ultralytics").setLevel(logging.CRITICAL)


############################################
# CONFIGURAÇÕES
############################################
# Se quiser *manualmente* setar as linhas A e B, defina aqui:
# k_A1 = None
# k_A2 = None
# k_B1 = None
# k_B2 = None

# Exemplo de valores fixos (descomente se quiser testar):
k_A1 = (415, 271)
k_A2 = (722, 240)
k_B1 = (1052, 437)
k_B2 = (500, 454)

video_path = 'videos/video (4).mp4'
# output_path = 'saida.mp4'
model_path = './model/yolov8n.pt'


DISTANCIA_LINHAS_METROS = 5.0
FRAME_SKIP = 6


CLASSES_INTERESSE = ["car", "motorbike", "bus", "truck"]
INFERENCE_SCALE = 0.5

area_points = []
track_states = {}
object_count = {
    "car": 0,
    "motorbike": 0,
    "bus": 0,
    "truck": 0
}


############################################
# FUNÇÃO DE CLIQUES NA TELA SE NECESSÁRIO
############################################
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(area_points) < 4:
        area_points.append((x, y))
        print(f"Clique {len(area_points)}: ({x}, {y})")
        if len(area_points) == 4:
            print("Polígono definido:", area_points)
            

############################################
# MAIN
############################################
def main():
    global area_points, k_A1, k_A2, k_B1, k_B2
    
    
    
    if (k_A1 is not None and k_A2 is not None and 
        k_B1 is not None and k_B2 is not None):
        # Define area_points a partir dessas variáveis
        area_points = [k_A1, k_A2, k_B1, k_B2]
        print("Usando coordenadas fixas:")
        print("Line A:", k_A1, k_A2)
        print("Line B:", k_B1, k_B2)
    else:
        print("Clique 4 pontos na janela (2 p/ Linha A e 2 p/ Linha B).")
        
    
    
    # MODELO YOLO
    model = YOLO(f"{model_path}", verbose=False)
    
    # DEEPSORT
    deepsort = DeepSort(
        max_age=30,
        n_init=8,
        nms_max_overlap=0.8,
        max_cosine_distance=0.3,
        nn_budget=8,
        embedder="mobilenet",
        embedder_gpu=False
    )
    
    

    # CONFIGURAÇÕES VÍDEO
    cap = cv2.VideoCapture(f"{video_path}")
    if not cap.isOpened():
        print("Erro ao abrir vídeo.")
        return
    

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
    
    if len(area_points) < 4:
        cv2.setMouseCallback("Video", mouse_callback)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # CASO QUISER SALVAR O VIDEO DETECTADO, DESCOMENTE ESSA LINHA E TUDO QUE TIVER out
    # out = cv2.VideoWriter(f"{output_path}", fourcc, fps, (width, height))

    
    frame_count = 0
    
    
    while True:
        
        speed = None

        ret, frame = cap.read()
        if not ret:
            break

        frame_limpo = frame.copy()
        frame_count += 1
        current_time = frame_count / fps

        draw_polygon_and_lines(frame, area_points)

        # Pular frames
        if frame_count % FRAME_SKIP != 0:
            continue
        
        # --------------------------------------------------------------------
        # 1) Reduza o frame apenas para detecção (YOLO/DeepSort)
        # --------------------------------------------------------------------
        orig_h, orig_w = frame.shape[:2]
        inf_w = int(orig_w * INFERENCE_SCALE)
        inf_h = int(orig_h * INFERENCE_SCALE)
    
        # Crie um frame menor
        frame_inference = cv2.resize(frame, (inf_w, inf_h), interpolation=cv2.INTER_LINEAR)

        # YOLO
        results = model(frame_inference, stream=True)
        dets = []
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                coords = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = map(int, coords)

                if model.names[cls_id] in CLASSES_INTERESSE:
                    w = x2 - x1
                    h = y2 - y1
                    dets.append([(x1, y1, w, h), conf, cls_id])

        tracks = deepsort.update_tracks(dets, frame=frame_inference)

        if len(area_points) == 4:
            A1, A2 = area_points[0], area_points[1]  # Linha A
            B1, B2 = area_points[2], area_points[3]  # Linha B

        for track in tracks:
            if not track.is_confirmed() or track.time_since_update > 0:
                continue

            # Este 'ltrb' está em coordenadas do frame_inference
            l_in, t_in, r_in, b_in = map(int, track.to_ltrb())
    
            # Precisamos ESCALAR de volta para o tamanho original
            # Para isso, dividimos pelo INFERENCE_SCALE
            # Exemplo: x_original = x_inferencia / scale
            l = int(l_in / INFERENCE_SCALE)
            t = int(t_in / INFERENCE_SCALE)
            r = int(r_in / INFERENCE_SCALE)
            b = int(b_in / INFERENCE_SCALE)
            
            
            cls_id = track.det_class
            class_name = model.names[cls_id] if cls_id is not None else "desconhecido"

            track_id = track.track_id
            if track_id not in track_states:
                track_states[track_id] = {
                    "active": False,
                    "time_A": None,
                    "time_B": None,
                    "speed": None,
                    "has_crossed_B": False,
                    "finish": False,
                    "entrou_mais_proximo_de": None,
                    "saiu_mais_proximo_de": None
                }
                
            
            
            # print(track_states[track_id]["entrou_mais_proximo_de"])
            # ------------------------------------------------
            # 1) Se ao menos 1 canto do BBox está no polígono => active = True
            #    Se 'active' ficar True e time_A for None, definimos time_A = current_time
            # ------------------------------------------------
            if not track_states[track_id]["active"]:
                if len(area_points) == 4:
                    inside_poly = any_corner_in_polygon(l, t, r, b, area_points)
                    if inside_poly:
                        track_states[track_id]["active"] = True
                        
                        
                        if track_states[track_id]["entrou_mais_proximo_de"] is None:
                            # >>> CÁLCULO: entrou_mais_proximo_de <<<
                            cx = (l + r) // 2
                            cy = (t + b) // 2
                            distA = distance_point_to_line(cx, cy, A1[0], A1[1], A2[0], A2[1])
                            distB = distance_point_to_line(cx, cy, B1[0], B1[1], B2[0], B2[1])
                            
                            if distA < distB:
                                track_states[track_id]["entrou_mais_proximo_de"] = "A"
                            else:
                                track_states[track_id]["entrou_mais_proximo_de"] = "B"
                                
                        # Definir time_A se ainda for None
                        if track_states[track_id]["time_A"] is None:
                            track_states[track_id]["time_A"] = current_time





            # Se já estiver ativo
            if track_states[track_id]["active"]:
                box_p1 = (l, b)
                box_p2 = (r, b)

                # # 2) Se ainda não temos time_A e a aresta inferior cruzar A, setar time_A
                # if track_states[track_id]["time_A"] is None and len(area_points) == 4:
                #     if lines_intersect(A1, A2, box_p1, box_p2):
                #         registrar_entrada(track_id, current_time, track_states)
                        

                # 3) Se ainda não cruzou B, verificar se cruza B ou sai do polígono
                if track_states[track_id]["entrou_mais_proximo_de"] != "B" and len(area_points) == 4:
                # if not track_states[track_id]["has_crossed_B"] and len(area_points) == 4:
                    # crossed_B = lines_intersect(B1, B2, box_p1, box_p2)

                    inside_now = any_corner_in_polygon(l, t, r, b, area_points)
                    # if crossed_B or not inside_now:
                    if not inside_now:
                        
                        # 4) INCREMENTA O CONTADOR
                        #    (Só quando o carro finaliza)
                        if class_name in object_count:
                            object_count[class_name] += 1
                           
                           
                        # Finaliza => registrar saida
                        registrar_saida(track_id, current_time, track_states, DISTANCIA_LINHAS_METROS)
                        speed = track_states[track_id]["speed"]
                        vtxt = f"{speed:}kmh" if speed else "None"
                        #vtxt = f"{speed:.2f}kmh" if speed else "None"
                        nome = f"{class_name}_ID{track_id}_{vtxt}"
                        salvar_veiculo(frame_limpo, l, t, r, b, nome)
                        
                        track_states[track_id]["finish"] = True
                        
                elif track_states[track_id]["entrou_mais_proximo_de"] == "B":
                    track_states[track_id]["finish"] = True
                        
                
                if track_states[track_id]["finish"]:
                    pass
                
                # 4) Se ainda está ativo, desenha
                elif track_states[track_id]["active"]:
                    cv2.rectangle(frame, (l, t), (r, b), (0,255,0), 2)
                    texto = f"ID {track_id} | {class_name}"
                    cv2.putText(frame, texto, (l, t - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

                    # spd = track_states[track_id]["speed"]
                    # if spd is not None:
                    #     cv2.putText(frame, f"{spd:.2f} km/h", (l, t - 30),
                    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)





        # 5) EXIBIR A CONTAGEM
        for i, (cname, count_val) in enumerate(object_count.items()):
            texto = f"{cname}: {count_val}"
            x = 10
            y = 30 + i * 30
            cv2.putText(frame, texto, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (255, 255, 255), 2, cv2.LINE_AA)
            
        
        
        if speed != None:
            print(int(speed))
            envia(str(int(speed)))
            
            
            
        # out.write(frame)
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    # out.release()
    cv2.destroyAllWindows()
    print("Finalizado.")
    end()                                                        # Termina o rastreamento
    end = 1 
    
    
    
############################################
if __name__ == "__main__":
    main()
