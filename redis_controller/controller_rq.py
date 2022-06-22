"""
Utiliza biblioteca RQ
"""

import json

import redis
from rq import Queue, Worker
from rq.serializers import JSONSerializer

redis = redis.Redis('localhost')


def _carga_dados(msg):
    print(msg)


def carga_dados_fila():
    q = Queue(connection=redis, name='faroldigital')
    job = q.enqueue(_carga_dados)
    print('Tamanho da fila: ' + str(len(q.jobs)))


def consumidor():
    w = Worker(connection=redis, queues=['faroldigital'], serializer=JSONSerializer)
    w.work()