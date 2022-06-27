import os
import sys
from time import sleep

from rabbitmq_controller.controller import carga_dados, cenario_b


if __name__ == '__main__':
    total_iteracao = int(sys.argv[1])

    for it in range(total_iteracao):
        print('Iniciando iteração: {}'.format(it))
        print('Reiniciando docker')
        os.system('docker-compose -f ../docker/rabbitmq/docker-compose.yml down')
        os.system('docker-compose -f ../docker/rabbitmq/docker-compose.yml up -d')
        sleep(10)

        # Gerar carga de dados
        print('gerando carga de dados: {}'.format(it))
        qnt_dados = 64608
        carga_dados(qnt_dados, 20)

        # Consumir os dados
        print('Consumindo os dados: {}'.format(it))
        cenario_b(it, qnt_dados)

    os.system('docker-compose -f ../docker/rabbitmq/docker-compose.yml down')
    print('Fim !')