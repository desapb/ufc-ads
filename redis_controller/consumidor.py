from redis_controller.controller import processar_dados

if __name__ == '__main__':
    total = 0
    while True:
        processar_dados()
        total = total + 1
        print(total)
