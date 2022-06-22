import json
import csv
from datetime import datetime

from etl.processar import extract_messages, transform_message

from kafka import KafkaProducer, KafkaConsumer

QUEUE = 'ads'


def carga_dados(total: int, lote: int):
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    retorno = extract_messages(total, lote)
    for r in retorno:
        producer.send(QUEUE, value=json.dumps(r))


def processar_dados():
    consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                             value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                             auto_offset_reset='earliest')
    consumer.subscribe(topics=QUEUE)

    total = 0
    with open('../logs/kafka/kafka_processo.log', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        for message in consumer:
            total = total + 1
            print(total)
            retorno = transform_message(message.value)
            row = [retorno['id'], retorno['date_send'], datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')]
            writer.writerow(row)
