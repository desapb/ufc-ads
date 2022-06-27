import csv
import json
import subprocess as sp

from datetime import timedelta, datetime
from timeit import default_timer as timer
import pika

from etl.processar import extract_messages, transform_message

QUEUE = 'ads'


def _channel_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=10))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)
    return channel


def carga_dados(total: int, lote: int):
    retorno = extract_messages(total, lote)
    channel = _channel_rabbitmq()
    for r in retorno:
        channel.basic_publish(exchange='',
                              routing_key=QUEUE,
                              body=json.dumps(r))


def cenario_a(iteracao, lista):
    print('Iniciando carga de dados')
    start = timer()

    with open('../logs/rabbitmq/cenario_a.csv', 'a', encoding='UTF8', newline='') as f:
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


def _callback(iteracao, body, total):
    dict_str = body.decode("UTF-8")
    retorno = transform_message(dict_str)

    tempo_processar_ini = retorno['date_send']
    print('Iteracao: {} / Dados: {}'.format(iteracao, total), end='\r')

    # Gera arquivo
    tempo_processar_fim = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('../logs/rabbitmq/cenario_b.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=';')

        # Intervalo de entrada e saida da fila
        time_1 = datetime.strptime(tempo_processar_ini, '%Y-%m-%d %H:%M:%S')
        time_2 = datetime.strptime(tempo_processar_fim, '%Y-%m-%d %H:%M:%S')
        intervalo_entrada_saida_fila = time_2 - time_1

        # ITERACAO, DATA ENTRADA FILA, DATA SAIDA DA FILA, INTERVALO DE ENTRADA E SAIDA DA FILA
        row = [iteracao, tempo_processar_ini, tempo_processar_fim, intervalo_entrada_saida_fila.total_seconds()]
        writer.writerow(row)


def cenario_b(iteracao, qnt_dados):
    # Inicia processamento dos dados
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=10))
    channel = connection.channel()

    total = 0
    for method_frame, properties, body in channel.consume(QUEUE):

        total = total + 1
        _callback(iteracao, body, total)

        channel.basic_ack(method_frame.delivery_tag)

        if method_frame.delivery_tag == qnt_dados:
             break

    # Cancel the consumer and return any pending messages
    requeued_messages = channel.cancel()
    print('Requeued %i messages' % requeued_messages)

    # Close the channel and the connection
    channel.close()
    connection.close()