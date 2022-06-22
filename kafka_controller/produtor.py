from datetime import timedelta, datetime
from timeit import default_timer as timer

from kafka_controller.controller import carga_dados

if __name__ == '__main__':
    start = timer()
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # carga_dados(59970, 0)
    # carga_dados(26470, 1)
    # carga_dados(11860, 2)
    # carga_dados(8940, 3)
    # carga_dados(13370, 4)
    # carga_dados(36070, 5)
    # carga_dados(69760, 6)
    # carga_dados(94120, 7)
    # carga_dados(106790, 8)
    # carga_dados(127260, 9)
    # carga_dados(133540, 10)
    # carga_dados(156410, 11)
    # carga_dados(158880, 12)
    # carga_dados(140640, 13)
    # carga_dados(129040, 14)
    # carga_dados(136170, 15)
    # carga_dados(150140, 16)
    # carga_dados(161370, 17)
    # carga_dados(195860, 18)
    # carga_dados(215090, 19)
    carga_dados(215360, 20)
    # carga_dados(188960, 21)
    # carga_dados(172990, 22)
    # carga_dados(116950, 23)

    end = timer()
    print('Carga concluída!: {tempo}'.format(tempo=timedelta(seconds=end - start)))
