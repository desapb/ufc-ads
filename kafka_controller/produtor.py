import os
import sys
from time import sleep

from controller import cenario_a


if __name__ == '__main__':
    total_iteracao = int(sys.argv[1])

    lista = [(17991, 0), (7941, 1), (3558, 2), (2682, 3), (4011, 4), (10821, 5), (10821, 6), (28236, 7), (32037, 8),
             (38178, 9), (40062, 10), (46923, 11), (47664, 12), (42192, 13), (38712, 14), (40851, 15), (45042, 16),
             (48411, 17), (58758, 18), (64527, 19), (64608, 20), (56688, 21), (51897, 22), (35085, 23)]

    for it in range(total_iteracao):
        print('Iniciando iteração: {}'.format(it))
        print('Reiniciando docker')
        os.system('docker-compose -f ../docker/kafka/docker-compose.yml down')
        os.system('docker-compose -f ../docker/kafka/docker-compose.yml up -d')
        sleep(5)
        cenario_a(it, lista)

    os.system('docker-compose -f ../docker/kafka/docker-compose.yml down')
    print('Fim da carga!')
