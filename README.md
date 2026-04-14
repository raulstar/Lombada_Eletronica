#  Lombada Eletrônica - Sistema de Detecção de Velocidade com Visão Computacional

##  Descrição do Projeto
Este projeto tem como objetivo desenvolver um sistema capaz de rastrear, identificar e registrar a velocidade de veículos, além de capturar imagens, utilizando visão computacional com OpenCV em Python 3.

Na primeira versão o sistema opera em um computador embarcado, utilizando uma câmera de vídeo para monitoramento contínuo do tráfego.
Na segunda versão Usam um sensor de radar niko-ondas Para ler A velocidade.

---

##  Objetivo
Desenvolver um programa que:
- Detecte veículos em vídeo
- Rastreie cada veículo com ID único
- Calcule a velocidade com base no método VASCAR
- Registre dados e imagens dos veículos
- Identifique infrações de velocidade

---

##  Requisitos do Sistema

###  Hardware
- Gabinete metálico
– Estrutura metalica
- Banco de bateria
- A placa solar
- Mini PC x64
- Mínimo:
  - 4 GB RAM
  - Processador Intel Celeron N4120
- Compatível com:
  - Windows 10 / Windows 11 (23H2)
  - (Opcional) Raspberry Pi OS (Debian)
  - Câmera de CFTV

---

### 🧠 Software
- Python 3
- OpenCV
- Adu

---

## 🏗️ Arquitetura de Referência
Protótipo base:
https://github.com/raulstar/Software_Lombada

---

## 📋 Funcionalidades

### 🎥 Entrada de Vídeo
- Captura via:
  - Arquivo de vídeo
  - Câmera embarcada
- Suporte a resoluções:
  - 1280x720
  - 1920x1080
- FPS configurável ou automático

---

### 🚘 Detecção e Rastreamento
- Identificação de veículos em diferentes:
  - Ângulos
  - Elevações
  - Sentidos de tráfego
- Atribuição de ID único por veículo
- Caixa de detecção (bounding box)
- Região de interesse (ROI) configurável

---

### 📏 Cálculo de Velocidade
- Baseado no método VASCAR
- Linhas de início/fim configuráveis
- Exibição em tempo real:
  - ID
  - Velocidade

---

### 🚨 Controle de Velocidade
- Definição de limite de velocidade
- Identificação de veículos infratores

---

### 🧾 Registro de Dados (LOG)

ID   VELOCIDADE   DATA/HORA
--------------------------------------------------
1    20.66 KM/h   2025-01-21 09:16:21  <--- excedeu limite
4    29.94 KM/h   2025-01-21 09:16:26  <--- excedeu limite
7    35.99 KM/h   2025-01-21 09:16:55  <--- excedeu limite

---

### 📸 Captura de Imagens
- Registro automático de veículos infratores
- Foco na placa
- Imagens com qualidade suficiente para OCR futuro

---

### 🔌 Comunicação Serial
- Detecção automática de portas seriais
- Envio de dados via:

serial.Serial("COMX", 9600, timeout=0.5)

- Formato ASCII com velocidade excedida

---

### 📦 Dependências
Deve incluir:
- Lista completa de bibliotecas
- Versões utilizadas
- Código-fonte completo

---

## 🧪 Testes Realizados
- Resoluções testadas:
  - 1280x720
  - 1920x1080

---

## ⚠️ Limitações do Protótipo Atual
- Baixa precisão na detecção
- Identificação incorreta de partes de veículos
- Velocidades inconsistentes
- Perda de veículos reais
- Múltiplos registros para o mesmo veículo

---

## 📊 Problemas Observados
- Captura de objetos errados (ex: vidro do carro)
- Falha em detectar veículos grandes (ex: caminhões)
- Poucas imagens com foco correto na placa
- Associação incorreta entre ID e imagem

---

## ✅ Requisitos Esperados
- Um único registro por veículo
- Associação correta entre:
  - ID
  - Imagem
  - Velocidade
- Geração de miniatura por registro com uma ID

---

## 🔮 Futuras Etapas
- Migração para nuvem
- Interface web (browser)
- Controle de acesso
- Suporte a múltiplas câmeras
- Integração com OCR (leitura de placas)
- Registro e consulta de todos os dados capturados
- O uso do Radar de microondas

---

## 🧪 Protótipo
O protótipo atual já implementa grande parte das funcionalidades, porém ainda com limitações de precisão:

https://github.com/raulstar/Software_Lombada

---

## 🖼️ Imagens

![Image 1](Midias/20250206_171159.jpg)
![Image 2](Midias/20250423_175401.jpg)
![Image 3](Midias/20250421_145853.jpg)

---

## 🎥 Vídeos

[Video 1](Midias/20250423_180011.mp4)
[Video 2](Midias/Primeiro teste (2).mp4)

---

## 📌 Observação Final
Apesar das limitações, o protótipo demonstrou viabilidade ao:
- Detectar veículos corretamente em diversos cenários
- Capturar imagens com enquadramento adequado da placa
O pretóxico Radar Foi usado diversas vezes inclusive um dado para clientes Mas o projeto está alto pausado no Momento.
O próximo passo ser A captura das irmãs com a Câmera e o enviou para um servidor via MQTT.
