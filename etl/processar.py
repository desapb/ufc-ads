import csv
from datetime import datetime
import json

from etl.utils import hash_md5, is_travazap, message_anonimization, message_clean


def transform_message(msg: str):
    try:
        # Converte mensagem json em dict
        obj = json.loads(msg)

        # Converte a mensagem em objeto python
        msg = {}
        msg['date_send'] = obj['date_send']
        msg['lote'] = obj['lote']
        msg['id'] = obj['id']
        msg['date_message'] = obj['date_message']

        msg['text_content'] = obj['text_content']
        msg['id_member'] = obj['id_member']
        msg['id_group'] = obj['id_group']

        # Midia
        msg['media_url'] = obj['media_url']
        msg['has_media_url'] = True if msg['media_url'] else False

        msg['media_type'] = obj['media_type']
        msg['has_media'] = True if msg['media_type'] else False

        # Anonimiza membro
        msg['id_member_anonymous'] = hash_md5(msg['id_member'])

        # Anonimiza Grupo
        msg['id_group_anonymous'] = hash_md5(msg['id_group'])

        # Descobre Localizacao
        # locale = find_country_by_phone(msg.id_member)
        # msg.country = locale['country']
        # msg.country_iso3 = locale['country_iso3']
        # msg.state = locale['state']
        # msg.ddd = locale['ddd']
        # msg.ddi = locale['ddi']
        # msg.latitude = locale['latitude']
        # msg.longitude = locale['longitude']

        # Trava zap
        msg['trava_zap'] = is_travazap(msg['text_content'])

        if not msg['trava_zap']:
            # Anonimiza mensagem
            msg['text_content_anonymous'] = message_anonimization(msg['text_content'])

            # Limpa mensagem
            msg['text_content_clean'] = message_clean(msg['text_content_anonymous'])

        return msg

    except Exception as e:
        print('-- ERRO --')
        print(e)


def extract_messages(total: int, lote: int):
    retorno = []
    with open('../dataset/msgfull.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        next(reader, None)
        line_count = 0

        for row in reader:
            if line_count == total:
                return retorno

            dados = {
                'id': row[0],
                'date_message': row[1],
                'text_content': row[2],
                'id_member': row[3],
                'id_group': row[4],
                'media_url': row[5],
                'media_type': row[6],
                'date_send': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                'lote': lote
            }

            retorno.append(dados)
            line_count = line_count + 1