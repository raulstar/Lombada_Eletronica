import cv2
import time
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
#from PIL import Image, ImageTk
import os  # Para manipulação de diretórios

# Variáveis globais
cap = None
limite_velocidade = 60.0  # Valor padrão do limite de velocidade
distancia_real_metros = 5  # Distância real em metros que o objeto percorre em um segundo
fps = 30  # FPS (quadros por segundo) estimado da câmera

# Função para iniciar a captura de vídeo
def iniciar_sistema():
    global cap
    cap = cv2.VideoCapture(0)  # Verifique se está capturando a câmera correta (troque 1 para 0 ou 2 se necessário)

    if not cap.isOpened():
        messagebox.showerror("Erro", "Falha ao acessar a câmera.")
        return

    # Variáveis de controle
    objetos_anterior = {}
    tempo_anterior = time.time()

    # Loop para capturar vídeo
    def capturar_video():
        nonlocal objetos_anterior, tempo_anterior
        ret, frame = cap.read()
        if ret:
            # Ajustar a imagem para preencher toda a tela
            frame = cv2.resize(frame, (root.winfo_width() - 250, root.winfo_height()))  # Redimensiona para preencher
            
            # Converter para escala de cinza
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Aplicar o detector de bordas
            edges = cv2.Canny(gray, 50, 150)

            # Encontrar contornos
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            objetos_atual = {}

            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:  # Ignora contornos pequenos
                    (x, y, w, h) = cv2.boundingRect(contour)
                    centro_objeto = (x + w // 2, y + h // 2)

                    # Adiciona o objeto à lista de objetos atuais
                    objetos_atual[centro_objeto] = (x, y, w, h)

                    # Calcula a velocidade se o objeto foi visto na iteração anterior
                    if centro_objeto in objetos_anterior:
                        # Calcula a distância percorrida em pixels
                        distancia_pixels = np.linalg.norm(np.array(centro_objeto) - np.array(list(objetos_anterior.keys())[0]))
                        tempo_atual = time.time()
                        tempo_gasto = tempo_atual - tempo_anterior
                        
                        # Calcula a velocidade em metros por segundo
                        if tempo_gasto > 0 and distancia_pixels > 5:  # Apenas calcular se houver movimento significativo
                            # Aqui, a escala pode ser ajustada de acordo com a câmera
                            # A conversão de pixels para metros deve ser ajustada de acordo com a sua câmera
                            fator_escala = distancia_real_metros / 100  # 100 pixels correspondem a 5 metros
                            velocidade_mps = (distancia_pixels / tempo_gasto) * fator_escala
                            velocidade_kmph = velocidade_mps * 3.6  # km/h

                            # Mostra a velocidade no console e na interface
                            if velocidade_kmph > 0:  # Evita mostrar velocidade zero
                                label_velocidade.config(text=f'Velocidade: {velocidade_kmph:.2f} km/h')
                                print(f'Velocidade calculada: {velocidade_kmph:.2f} km/h')

                                # Verifica se a velocidade ultrapassa o limite
                                if velocidade_kmph > limite_velocidade:
                                    print("Objeto acima do limite! Capturando imagem...")
                                    # Garante que a pasta de imagens existe
                                    os.makedirs("imagens_acima_limite", exist_ok=True)
                                    # Salva a imagem na pasta "imagens_acima_limite"
                                    cv2.imwrite(f'imagens_acima_limite/objeto_acima_limite_{time.time()}.png', frame)

            # Atualiza a lista de objetos anteriores
            objetos_anterior = objetos_atual
            tempo_anterior = time.time()

            # Exibir o frame na interface
            ##img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            ##imgtk = ImageTk.PhotoImage(image=img)
            ##label_video.imgtk = imgtk
            ##label_video.configure(image=imgtk)

        root.after(10, capturar_video)

    capturar_video()
    messagebox.showinfo("Iniciar", "Sistema Iniciado!")

# Função para parar a captura de vídeo
def parar_sistema():
    global cap
    if cap:
        cap.release()
        cap = None
    label_video.config(image='')  # Limpa a imagem exibida
    messagebox.showinfo("Parar", "Sistema Parado!")

# Função para atualizar o limite de velocidade
def atualizar_limite():
    global limite_velocidade
    try:
        novo_limite = float(entry_limite.get())
        limite_velocidade = novo_limite
        messagebox.showinfo("Limite Atualizado", f"Novo limite: {novo_limite} km/h")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido")

# Cria a janela principal
root = tk.Tk()
root.title("Monitoramento de Velocidade")
root.geometry("1000x600")
root.configure(bg="#1c1f24")

# Define uma fonte moderna
font_title = tkfont.Font(family="Helvetica", size=24, weight="bold")
font_label = tkfont.Font(family="Helvetica", size=14)
font_entry = tkfont.Font(family="Helvetica", size=14)

# Adiciona logo e nome da empresa
label_nome_empresa = tk.Label(root, text="Revlo", font=font_title, bg="#1c1f24", fg="#ffffff")
label_nome_empresa.pack(pady=10)

# Frame para ações no lado esquerdo
frame_acao = tk.Frame(root, bg="#292b2f", width=250)
frame_acao.pack(side=tk.LEFT, fill=tk.Y)

# Adiciona título para as ações
label_titulo = tk.Label(frame_acao, text="Ações", font=font_title, bg="#292b2f", fg="#ffffff")
label_titulo.pack(pady=10)

# Campo para definir limite de velocidade
label_limite = tk.Label(frame_acao, text="Limite de Velocidade (km/h):", font=font_label, bg="#292b2f", fg="#ffffff")
label_limite.pack(pady=10)
entry_limite = tk.Entry(frame_acao, font=font_entry)
entry_limite.pack(pady=5)

btn_atualizar_limite = tk.Button(frame_acao, text="Atualizar Limite", command=atualizar_limite, font=font_label, bg="#4CAF50", fg="#ffffff")
btn_atualizar_limite.pack(pady=10)

# Botões de controle
btn_iniciar = tk.Button(frame_acao, text="Iniciar", command=iniciar_sistema, font=font_label, bg="#2196F3", fg="#ffffff")
btn_iniciar.pack(pady=10)

btn_parar = tk.Button(frame_acao, text="Parar", command=parar_sistema, font=font_label, bg="#F44336", fg="#ffffff")
btn_parar.pack(pady=10)

# Label para exibir a velocidade
label_velocidade = tk.Label(frame_acao, text="Velocidade: 0.00 km/h", font=font_label, bg="#292b2f", fg="#ffffff")
label_velocidade.pack(pady=10)

# Label para exibir o vídeo
label_video = tk.Label(root, bg="#1c1f24")
label_video.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

root.mainloop()
