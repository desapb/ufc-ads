import csv
import json
import redis as redis
import subprocess as sp

from datetime import timedelta, datetime
from timeit import default_timer as timer

from etl.processar import transform_message, extract_messages

redis = redis.Redis('localhost')


def carga_dados(total: int, lote: int):
    retorno = extract_messages(total, lote)
    for r in retorno:
        redis.rpush('queue:fd', json.dumps(r))


def cenario_a(iteracao, lista):
    print('Iniciando carga de dados')
    start = timer()

    with open('../logs/redis/cenario_a.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        # output = sp.getoutput('docker stats --format "{{.Name}}; {{.MemUsage}}" --no-stream')
        # writer.writerow([iteracao, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), output])

        for item in lista:
            qnt_dados = item[0]
            lote = item[1]

            carga_dados(qnt_dados, lote)
            output = sp.getoutput('docker stats --format "{{.Name}}; {{.MemUsage}}" --no-stream')
            output_split = output.split(";")
            writer.writerow([iteracao, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), str(output_split[0]), str(output_split[1])])
            print('Iteracao: {} / Lote de Dados: {}'.format(iteracao, lote), end='\r')

    end = timer()
    print('Carga concluída!: {tempo}'.format(tempo=timedelta(seconds=end - start)))


def cenario_b(iteracao):
    total = 0
    processar = True
    tempo_processar_ini = None

    # Inicia processamento dos dados
    while processar != None:
        processar = _processar_dados()
        if not tempo_processar_ini:
            tempo_processar_ini = processar['date_send']
        total = total + 1
        print('Iteracao: {} / Dados: {}'.format(iteracao, total), end='\r')

    # Gera arquivo
    tempo_processar_fim = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('../logs/redis/cenario_b.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=';')

        # Intervalo de entrada e saida da fila
        time_1 = datetime.strptime(tempo_processar_ini, '%Y-%m-%d %H:%M:%S')
        time_2 = datetime.strptime(tempo_processar_fim, '%Y-%m-%d %H:%M:%S')
        intervalo_entrada_saida_fila = time_2 - time_1

        # ITERACAO, DATA ENTRADA FILA, DATA SAIDA DA FILA, INTERVALO DE ENTRADA E SAIDA DA FILA
        row = [iteracao, tempo_processar_ini, tempo_processar_fim, intervalo_entrada_saida_fila.total_seconds()]
        writer.writerow(row)


def _processar_dados():
    packed = redis.blpop(['queue:fd'], 30)
    if not packed:
        return None

    dict_str = packed[1].decode("UTF-8")
    retorno = transform_message(dict_str)
    return retorno