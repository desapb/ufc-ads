import ast
import csv
import json
from datetime import datetime
import redis as redis

#import sys
#sys.path.insert(0, '/home/ads/Documents/avaliacao-desempenho')
#export PYTHONPATH='/home/ads/Documents/avaliacao-desempenho'

from etl.processar import transform_message, extract_messages

redis = redis.Redis('localhost')


def carga_dados(total: int, lote: int):
    retorno = extract_messages(total, lote)
    for r in retorno:
        redis.rpush('queue:fd', json.dumps(r))


def processar_dados():
    packed = redis.blpop(['queue:fd'], 30)
    if not packed:
        return
    dict_str = packed[1].decode("UTF-8")
    #retorno_dict = ast.literal_eval(dict_str)
    retorno = transform_message(dict_str)
    if retorno:
        with open('../logs/redis_processo.log', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            row = [retorno['id'], retorno['lote'], retorno['date_send'], datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')]
            writer.writerow(row)
