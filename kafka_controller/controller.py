import json
import csv
from datetime import timedelta, datetime
from timeit import default_timer as timer
from etl.processar import extract_messages, transform_message
import subprocess as sp

from kafka import KafkaProducer, KafkaConsumer

QUEUE = 'ads'


def carga_dados(total: int, lote: int):
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    retorno = extract_messages(total, lote)
    for r in retorno:
        producer.send(QUEUE, value=json.dumps(r))


def cenario_b(iteracao):
    consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                             value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                             auto_offset_reset='earliest',
                             consumer_timeout_ms=5000)
    consumer.subscribe(topics=QUEUE)

    total = 0
    tempo_processar_ini = None
    with open('../logs/kafka/cenario_b.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=';')

        for message in consumer:
            retorno = transform_message(message.value)

            if not tempo_processar_ini:
                tempo_processar_ini = retorno['date_send']

            tempo_processar_fim = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Intervalo de entrada e saida da fila
            time_1 = datetime.strptime(tempo_processar_ini, '%Y-%m-%d %H:%M:%S')
            time_2 = datetime.strptime(tempo_processar_fim, '%Y-%m-%d %H:%M:%S')
            intervalo_entrada_saida_fila = time_2 - time_1

            # ITERACAO, DATA ENTRADA FILA, DATA SAIDA DA FILA, INTERVALO DE ENTRADA E SAIDA DA FILA
            row = [iteracao, tempo_processar_ini, tempo_processar_fim, intervalo_entrada_saida_fila.total_seconds()]
            writer.writerow(row)

            total = total + 1
            print('Iteracao: {} / Lote de Dados: {}'.format(iteracao, total), end='\r')

    consumer.close()


def cenario_a(iteracao, lista):
    print('Iniciando carga de dados')
    start = timer()

    with open('../logs/kafka/cenario_a.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=';')

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

