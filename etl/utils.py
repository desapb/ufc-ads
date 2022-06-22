import hashlib

import unidecode
from nltk import tokenize
from nltk.corpus import stopwords
import re, string


def message_anonimization(text_content):

    if not text_content:
        return None

    if text_content == '<Arquivo de mídia oculto>':
        return None

    # Anonimizando Email
    regex_email = '([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})'
    text_content = re.sub(regex_email, '[EMAIL]', text_content)

    # Anonimizando Nomes de Usuarios
    # @nome ou @434343434
    regex_users = '\@\w+'
    text_content = re.sub(regex_users, '[USER]', text_content)

    #Anonimiza telefone
    text_content = re.sub('\d+ \d+-\d+', '[PHONE]', text_content)  # XX XXXX-XXXX
    text_content = re.sub('\(\d+\) \d+-\d+', '[PHONE]', text_content)  # (XX) XXXX-XXXX
    text_content = re.sub('/ \d+-\d+', '[PHONE]', text_content)  # (XX) XXXX-XXXX / XXXX-XXXX
    text_content = re.sub('cel \d+-\d+', '[PHONE]', text_content) # cel XXXXX-XXXX

    return text_content


def message_clean(text_content):

    if not text_content:
        return None

    if text_content == '<Arquivo de mídia oculto>':
        return None

    # stopwords
    stopwords_pt = set(stopwords.words('portuguese'))

    # inclui lista de stopwords sem acentos
    stopwords_pt.update([unidecode.unidecode(w) for w in stopwords_pt])

    # Inclui pontuacao nos stopwords
    punct = list(string.punctuation)
    stopwords_pt.update(punct)

    new_stopwords = ['aí', 'ai', 'pra', 'vão', 'vao', 'vou', 'onde', 'lá', 'la', 'aqui',
                     'tá', 'ta', 'pode', 'pois', 'so', 'deu', 'agora', 'todo', 'vai', 'ser', 'boa'
                     'nao', 'ja', 'manda', 'vc', 'ola'
                     'bom', 'dia', 'bem', 'oii', 'oi', 'oie', 'ter',
                     'kkk', 'kkkk', 'ta', 'voce', 'alguem', 'ne', 'pq', 'opa', 'tchau', 'entao',
                     'cara', 'to', 'mim', 'vcs', 'tbm', 'tudo', 'ainda', '[?][?]', '[?]', '...']
    stopwords_pt.update(new_stopwords)

    # Frase em minusculo
    text_content = text_content.lower()

    # Remove urls da frase
    text_content = __remove_url(text_content)

    # Remove os acentos da frase
    text_content = unidecode.unidecode(text_content)
    nova_frase = list()

    # tokeniza a frase
    frase_token = tokenize.WordPunctTokenizer().tokenize(text_content)
    for palavra in frase_token:
        palavra = palavra.lower()
        # verifica se o token esta na lista de stopwords
        # verifica se o token tem mais de 2 caracteres
        # verifica se o token nao eh um numero
        # verifica se nao eh uma risada
        if palavra not in stopwords_pt:
            if len(palavra) > 2:
                if not palavra.isdigit():
                    if not bool(re.match('(?:a*(?:ha)+h?|(?:kk+)|(?:##+)|(?:oi+))', palavra)):
                        nova_frase.append(palavra)

    frase_processada = ' '.join(nova_frase)

    return frase_processada


def is_travazap(text):
    """
    Sera considerado trava-zap se, apos remover os caracteres especiais,
    a mensagem ficar com menos de 1% de caracteres validos.
    text: text_content
    return: True / False
    """

    if not text:
        return False

    # Remove espacos em branco do texto original
    text = text.replace(' ', '').replace('\n', '')
    tam_text = len(text)

    #remove caracteres especiais
    tam_result = re.sub('[^a-zA-Z0-9]', '', text)
    tam_result = len(tam_result)

    x = tam_result * 100 / tam_text
    #print('tam_original: {} - tam_final: {} => {}'.format(tam_text, tam_result, x))
    return True if x > 0 and x <= 1 else False


def __remove_url(text):

    if not text:
        return None

    url_regex = "((http|ftp|https)://)?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
    URLless_string = re.sub(url_regex, "", text)
    return URLless_string


def hash_md5(text):
    hashmd5 = hashlib.md5(text.encode('utf-8')).hexdigest()
    return hashmd5


# def find_country_by_phone(id_member):
#     '''
#     Funcao para buscar dados do pais de acordo com o numero telefonico do whatsapp.
#     Inicia verificando se o ddi eh brasileiro, caso nao seja, itera a partir do
#     primeiro caractere buscando um ddi correspondente.
#     '''
#     cod_ddi = id_member[:2]
#     cod_ddd = id_member[2:4]
#
#     retorno = {'ddd': None,
#                'ddi': None,
#                'country': None,
#                'country_iso3': None,
#                'state': None,
#                'latitude': None,
#                'longitude': None}
#
#     if cod_ddi == '55':
#         # SE FOR BRASIL
#         country = session.query(Country).filter(Country.ddi == cod_ddi).first()
#         code_locale = cod_ddi+'-'+cod_ddd
#         brazil_state = session.query(Locale).filter(Locale.ddd == code_locale).first()
#
#         if country:
#             retorno['country'] = country.name
#             retorno['ddi'] = country.ddi
#             retorno['country'] = country.name
#             retorno['country_iso3'] = country.name_iso3
#             retorno['state'] = brazil_state.initials if brazil_state else None  #INICIAIS OU NOME DO ESTADO?
#             retorno['latitude'] = brazil_state.latitude if brazil_state else None
#             retorno['longitude'] = brazil_state.longitude if brazil_state else None
#             retorno['ddd'] = cod_ddd
#     else:
#         # SE NAO FOR BRASIL
#         for i in range(1, 5, 1):
#             ddi = id_member[:i]
#
#             # CASO O DDI SEJA 1 (ESTADOS UNIDOS, CANADA, PORTO RICO, ...)
#             if ddi == '1':
#                 cod_ddi = '1-' + id_member[1:4]
#                 retorno['ddi'] = cod_ddi
#                 country = session.query(Country).filter(Country.ddi == cod_ddi).first()
#                 if country:
#                     retorno['ddi'] = country.ddi
#                     retorno['country'] = country.name
#                     retorno['country_iso3'] = country.name_iso3
#                     retorno['latitude'] = country.latitude
#                     retorno['longitude'] = country.longitude
#                     break
#                 else:
#                     # SE NAO ENCONTRAR UM PAIS, BUSCA POR LOCALIDADE
#                     localidade = session.query(Locale).filter(Locale.ddd == cod_ddi).first()
#                     if localidade:
#                         retorno['ddi'] = localidade.country.ddi
#                         retorno['ddd'] = localidade.ddd
#                         retorno['country'] = localidade.country.name
#                         retorno['country_iso3'] = localidade.country.name_iso3
#                         retorno['state'] = localidade.state
#                         retorno['latitude'] = localidade.latitude if localidade.latitude else localidade.country.latitude
#                         retorno['longitude'] = localidade.longitude if localidade.longitude else localidade.country.longitude
#                     break
#             else:
#                 retorno['ddi'] = ddi
#                 country = session.query(Country).filter(Country.ddi == ddi).first()
#                 if country:
#                     retorno['ddi'] = country.ddi
#                     retorno['country'] = country.name
#                     retorno['country_iso3'] = country.name_iso3
#                     retorno['latitude'] = country.latitude
#                     retorno['longitude'] = country.longitude
#                     break
#
#     return retorno

