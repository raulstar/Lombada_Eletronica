import csv
import datetime
import os.path

agora = datetime.datetime.now()
hora_formatada = agora.strftime("%H:%M:%S")  # Formato: HH:MM:SS
variavel = "Valor da variável"

nome_arquivo = 'dados.csv'
cabecalho = ['Hora', 'Variável']

arquivo_existe = os.path.isfile(nome_arquivo)

with open(nome_arquivo, 'a', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv)
    if not arquivo_existe:
        writer.writerow(cabecalho)
    writer.writerow([hora_formatada, variavel])
