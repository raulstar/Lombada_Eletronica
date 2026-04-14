import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import easyocr
import time
import tkinter.font as tkfont


# Variáveis globais
cap = None
reader = easyocr.Reader(['pt'])
placas_registradas = []
limite_velocidade = 60.0
camera_address = 0

# Caminho do classificador Haar Cascade para carros
car_cascade_path = "cars.xml"
car_cascade = cv2.CascadeClassifier(car_cascade_path)

if car_cascade.empty():
    print("Erro: Não foi possível carregar o classificador Haar Cascade para carros.")
    exit()

# Definição dos pontos do delimitador (quadrado)
ponto_inferior_esquerdo = (50, 250)  # Aumentei para capturar melhor
ponto_superior_direito = (900, 550)

# Inicializa o dicionário de detecção de carros
carros_deteccao = {}

def calcular_velocidade(tempo_inicio, tempo_fim, posicao_inicial, posicao_final):
    distancia = posicao_final - posicao_inicial
    tempo = tempo_fim - tempo_inicio
    if tempo > 0:
        velocidade = (distancia / tempo) * 3.6  # De m/s para km/h
        return velocidade
    return 0

def limpar_carros_deteccao():
    tempo_atual = time.time()
    for carro in list(carros_deteccao.keys()):
        if tempo_atual - carros_deteccao[carro]['tempo_inicio'] > 10:
            del carros_deteccao[carro]

def carregar_camera():
    global cap
    cap = cv2.VideoCapture(camera_address)

    if not cap.isOpened():
        messagebox.showerror("Erro", "Falha ao acessar a câmera.")
        return

    with open("placas_detectadas.txt", "w") as f:
        f.write("Placas Detectadas:\n")

    with open("velocidades_registradas.txt", "w") as v:
        v.write("Velocidades Registradas:\n")

    last_frame_time = time.time()

    def reproduzir_camera():
        nonlocal last_frame_time
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (root.winfo_width() - 250, root.winfo_height()))

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.rectangle(frame, ponto_inferior_esquerdo, ponto_superior_direito, (255, 0, 0), 2)

            cars = car_cascade.detectMultiScale(gray, 1.1, 1)

            for (x, y, w, h) in cars:
                centro_carro = (x + w // 2, y + h // 2)
                posicao_atual = x  # Considerando o eixo X como posição do carro

                if (ponto_inferior_esquerdo[0] < centro_carro[0] < ponto_superior_direito[0] and 
                    ponto_inferior_esquerdo[1] < centro_carro[1] < ponto_superior_direito[1]):
                    
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    car_roi = frame[y:y + h, x:x + w]

                    results = reader.readtext(car_roi)

                    # Se o carro for novo (não detectado antes), adiciona no dicionário
                    if (x, y, w, h) not in carros_deteccao:
                        carros_deteccao[(x, y, w, h)] = {
                            'tempo_inicio': time.time(),
                            'posicao_inicial': posicao_atual
                        }
                    else:
                        # Se o carro já foi detectado, calcula a velocidade
                        tempo_fim = time.time()
                        tempo_inicio = carros_deteccao[(x, y, w, h)]['tempo_inicio']
                        posicao_inicial = carros_deteccao[(x, y, w, h)]['posicao_inicial']
                        velocidade = calcular_velocidade(tempo_inicio, tempo_fim, posicao_inicial, posicao_atual)
                        
                        if velocidade > limite_velocidade:
                            cv2.putText(frame, f"Velocidade: {velocidade:.2f} km/h", (x, y - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                            with open("velocidades_registradas.txt", "a") as v:
                                v.write(f"Carro em ({x}, {y}) - Velocidade: {velocidade:.2f} km/h\n")

                    for (bbox, text, prob) in results:
                        (top_left, top_right, bottom_right, bottom_left) = bbox
                        top_left = tuple(map(int, top_left))
                        bottom_right = tuple(map(int, bottom_right))

                        if prob > 0.8:
                            cv2.rectangle(car_roi, top_left, bottom_right, (255, 0, 0), 2)
                            cv2.putText(car_roi, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

                            if text not in placas_registradas:
                                placas_registradas.append(text)
                                with open("placas_detectadas.txt", "a") as f:
                                    f.write(text + "\n")

                    # Atualiza a posição final e tempo final do carro
                    carros_deteccao[(x, y, w, h)]['tempo_inicio'] = time.time()
                    carros_deteccao[(x, y, w, h)]['posicao_inicial'] = posicao_atual

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            label_video.imgtk = imgtk
            label_video.configure(image=imgtk)

            limpar_carros_deteccao()  # Limpa detecções antigas
        else:
            cap.release()
            messagebox.showinfo("Fim", "A câmera foi desligada.")

        root.after(10, reproduzir_camera)

    reproduzir_camera()
    messagebox.showinfo("Carregar Câmera", "Câmera Carregada!")

def on_closing():
    if cap is not None:
        cap.release()
    root.destroy()

# Interface gráfica
root = tk.Tk()
root.title("Monitoramento de Carros e Placas")
root.geometry("1000x600")
root.configure(bg="#1c1f24")
root.protocol("WM_DELETE_WINDOW", on_closing)

font_title = tkfont.Font(family="Helvetica", size=20)

title_label = tk.Label(root, text="Revlo", bg="#1c1f24", fg="red", font=font_title)
title_label.place(x=850, y=10)

# Botões arredondados e customizados
btn_frame = tk.Frame(root, bg="#1c1f24")
btn_frame.place(x=750, y=50)

def estilizar_botao(botao):
    botao.config(bg="#F44336", fg="white", font=("Helvetica", 12), relief="flat")
    botao.pack(pady=10, ipadx=20, ipady=10)

btn_start = tk.Button(btn_frame, text="Iniciar", command=carregar_camera)
estilizar_botao(btn_start)

btn_stop = tk.Button(btn_frame, text="Parar", command=on_closing)
estilizar_botao(btn_stop)

btn_set_speed = tk.Button(btn_frame, text="Definir Limite de Velocidade", command=lambda: messagebox.showinfo("Definir Limite", "Funcionalidade em desenvolvimento"))
estilizar_botao(btn_set_speed)

label_video = tk.Label(root)
label_video.place(x=50, y=50)

root.mainloop()
