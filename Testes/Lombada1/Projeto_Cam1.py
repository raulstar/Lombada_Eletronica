import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk
import easyocr
import time

# Variáveis globais
cap = None
reader = easyocr.Reader(['pt'])  # Inicializa o leitor de OCR
placas_registradas = []  # Lista para armazenar as placas detectadas
limite_velocidade = 60.0  # Limite de velocidade padrão em km/h
camera_address = 2  # Endereço da câmera (0 para webcam, ou USB no Linux)

# Caminho do classificador Haar Cascade para carros
car_cascade_path = "cars.xml"  # Altere para o caminho correto

# Carregar o classificador Haar Cascade para carros
car_cascade = cv2.CascadeClassifier(car_cascade_path)

if car_cascade.empty():
    print("Erro: Não foi possível carregar o classificador Haar Cascade para carros.")
    exit()

# Definir variáveis para o cálculo de velocidade
carros_deteccao = {}
linha_referencia_y = 100

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
        if tempo_atual - carros_deteccao[carro] > 10:
            del carros_deteccao[carro]

# Função para carregar e reproduzir o vídeo da câmera
def carregar_camera():
    global cap
    cap = cv2.VideoCapture(camera_address)  # Usa o endereço fornecido

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

            cv2.line(frame, (0, linha_referencia_y), (frame.shape[1], linha_referencia_y), (255, 0, 0), 2)

            cars = car_cascade.detectMultiScale(gray, 1.1, 1)

            for (x, y, w, h) in cars:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                car_roi = frame[y:y + h, x:x + w]

                results = reader.readtext(car_roi)
                for (bbox, text, prob) in results:
                    (top_left, top_right, bottom_right, bottom_left) = bbox
                    top_left = tuple(map(int, top_left))
                    bottom_right = tuple(map(int, bottom_right))

                    if prob > 0.8:  # Apenas placas com alta confiança
                        cv2.rectangle(car_roi, top_left, bottom_right, (255, 0, 0), 2)
                        cv2.putText(car_roi, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

                        if text not in placas_registradas:
                            placas_registradas.append(text)
                            with open("placas_detectadas.txt", "a") as f:
                                f.write(text + "\n")

                centro_carro = y + h // 2
                if centro_carro >= linha_referencia_y and (x, y, w, h) not in carros_deteccao:
                    carros_deteccao[(x, y, w, h)] = time.time()

            for (x, y, w, h) in list(carros_deteccao.keys()):
                tempo_cruzamento = time.time() - carros_deteccao[(x, y, w, h)]
                if tempo_cruzamento > 1:
                    posicao_inicial = linha_referencia_y - h // 2
                    posicao_final = y + h // 2
                    velocidade = calcular_velocidade(carros_deteccao[(x, y, w, h)], time.time(), posicao_inicial, posicao_final)

                    if velocidade > limite_velocidade:
                        cv2.putText(frame, f"Acima do limite! {velocidade:.2f} km/h", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    else:
                        cv2.putText(frame, f"Velocidade: {velocidade:.2f} km/h", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    with open("velocidades_registradas.txt", "a") as v:
                        v.write(f"Carro detectado na posição ({x}, {y}) com velocidade: {velocidade:.2f} km/h\n")

                    del carros_deteccao[(x, y, w, h)]

            limpar_carros_deteccao()

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            label_video.imgtk = imgtk
            label_video.configure(image=imgtk)
        else:
            cap.release()
            messagebox.showinfo("Fim", "A câmera foi desligada.")

        root.after(10, reproduzir_camera)

    reproduzir_camera()
    messagebox.showinfo("Carregar Câmera", "Câmera Carregada!")

def parar_sistema():
    global cap
    root.destroy()##
    if cap:
        cap.release()
        cap = None
    label_video.config(image='')
    messagebox.showinfo("Parar", "Sistema Parado!")

def atualizar_limite():
    global limite_velocidade
    try:
        novo_limite = float(entry_limite.get())
        limite_velocidade = novo_limite
        messagebox.showinfo("Limite Atualizado", f"Novo limite: {novo_limite} km/h")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido")

def atualizar_endereco_camera():
    global camera_address
    camera_address = entry_camera_address.get()
    messagebox.showinfo("Endereço Atualizado", f"Endereço da câmera atualizado para: {camera_address}")

def on_closing():
    global cap
    if cap:
        cap.release()
    root.destroy()

root = tk.Tk()
root.title("Monitoramento de Carros e Placas")
root.geometry("1000x600")
root.configure(bg="#1c1f24")
root.protocol("WM_DELETE_WINDOW", on_closing)

font_title = tkfont.Font(family="Helvetica", size=24, weight="bold")
font_label = tkfont.Font(family="Helvetica", size=14)

label_nome_empresa = tk.Label(root, text="Revlo", font=font_title, bg="#1c1f24", fg="#ffffff")
label_nome_empresa.pack(pady=10)

frame_acao = tk.Frame(root, bg="#292b2f", width=250)
frame_acao.pack(side=tk.LEFT, fill=tk.Y)

label_limite = tk.Label(frame_acao, text="Limite de Velocidade (km/h):", font=font_label, bg="#292b2f", fg="#ffffff")
label_limite.pack(pady=10)
entry_limite = tk.Entry(frame_acao, font=font_label)
entry_limite.pack(pady=5)

btn_atualizar_limite = tk.Button(frame_acao, text="Atualizar Limite", command=atualizar_limite, font=font_label, bg="#4CAF50", fg="#ffffff")
btn_atualizar_limite.pack(pady=10)

label_camera_address = tk.Label(frame_acao, text="Endereço da Câmera (USB/Video):", font=font_label, bg="#292b2f", fg="#ffffff")
label_camera_address.pack(pady=10)
entry_camera_address = tk.Entry(frame_acao, font=font_label)
entry_camera_address.pack(pady=5)

btn_atualizar_camera_address = tk.Button(frame_acao, text="Atualizar Endereço", command=atualizar_endereco_camera, font=font_label, bg="#4CAF50", fg="#ffffff")
btn_atualizar_camera_address.pack(pady=10)

btn_carregar_camera = tk.Button(frame_acao, text="Iniciar Sistema", command=carregar_camera, font=font_label, bg="#4CAF50", fg="#ffffff")
btn_carregar_camera.pack(pady=10)

btn_parar_sistema = tk.Button(frame_acao, text="Parar Sistema", command=parar_sistema, font=font_label, bg="#f44336", fg="#ffffff")
btn_parar_sistema.pack(pady=10)

# Label onde o vídeo será exibido
label_video = tk.Label(root, bg="#1c1f24")
label_video.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Iniciar a interface gráfica
root.mainloop()

