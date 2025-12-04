#Напишите асинхронный и многопоточный сокеты, и клиент для них,
# которые считывают количество строк в файлах некой директории.
# Сравните показатели потребления, и время выполнения.
# Определите, какая минимальная память гарантировано обеспечит обработку 1000 одновременных запросов

from threading import Thread
import requests
import time

text = ''

def main(server_type='sync'):
    threads = []
    global text
    text += f'\n\nСейчас тестируется {server_type}\n\n'
    n = 0

    def req(): #два порта
        nonlocal n
        if server_type == 'threading':
            port = 8082
        elif server_type == 'async':
            port = 8081

        response = requests.get(f"http://127.0.0.1:{port}")
        global text
        text += response.text
        n += 1
        return n

    for i in range(10):
        t = Thread(target=req, args=())
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f"Сервер типа {server_type} обработал {n} запросов")


if __name__ == '__main__':
    begin = time.time()
    main(server_type="threading")
    flask_end = time.time() - begin
    print("threading завершил работу")

if __name__ == '__main__':
    begin = time.time()
    main(server_type="async")
    flask_end = time.time() - begin
    print("async завершил работу")