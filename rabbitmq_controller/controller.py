import ast
import csv
import json
from datetime import datetime

import pika

from etl.processar import extract_messages, transform_message

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
QUEUE = 'ads'
channel.queue_declare(queue=QUEUE)


def carga_dados(total: int, lote: int):
    retorno = extract_messages(total, lote)
    for r in retorno:
        channel.basic_publish(exchange='',
                              routing_key=QUEUE,
                              body=json.dumps(r))


#####################################

def callback(ch, method, properties, body):

    if not body:
        return
    dict_str = body.decode("UTF-8")
    retorno = transform_message(dict_str)
    #retorno = ast.literal_eval(retorno_str)

    with open('../logs/rabbitmq/rabbitmq_processo.log', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        row = [retorno['id'], retorno['date_send'], datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')]
        writer.writerow(row)


def processar_dados():
    channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
