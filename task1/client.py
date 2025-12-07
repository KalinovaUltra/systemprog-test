#Написать многопоточный и асинхронный серверы, которые обрабатывают внешние запросы  пор страницам сайта https://dental-first.ru/catalog.
# Для тестирования напишите сервер, который отправляет множественные запросы по различным страницам сайта.
# Сами  сервера должны сохранять названия товаров в файл.
# Сравните время выполнения, потребляемую память, и нагрузку на сервер.
# названия товаров под одной любой категорией, ссылки вставить как тестовые данные, readme файл на каких Url и как запускать

# from threading import Thread
# import requests
# import time
#
# text = ''
#
# def main(server_type='sync'):
#     threads = []
#     global text
#     text += f'\n\nСейчас тестируется {server_type}\n\n'
#     n = 0
#
#     def req(): #два порта
#         nonlocal n
#         if server_type == 'threading':
#             port = 8082
#         elif server_type == 'async':
#             port = 8081
#
#         response = requests.get(f"http://127.0.0.1:{port}")
#         global text
#         text += response.text
#         n += 1
#         return n
#
#     for i in range(10):
#         t = Thread(target=req, args=())
#         threads.append(t)
#
#     for t in threads:
#         t.start()
#
#     for t in threads:
#         t.join()
#
#     print(f"Сервер типа {server_type} обработал {n} запросов")
#
#
# if __name__ == '__main__':
#     begin = time.time()
#     main(server_type="threading")
#     flask_end = time.time() - begin
#     print("threading завершил работу")
#
# if __name__ == '__main__':
#     begin = time.time()
#     main(server_type="async")
#     flask_end = time.time() - begin
#     print("async завершил работу")

import requests
import time
import threading
import psutil
import os


def test_server(server_type, port, urls, results): #отправляем запросы
    start_time = time.time()
    successful_requests = 0

    def make_request(url):
        nonlocal successful_requests
        try:
            response = requests.get(
                f"http://127.0.0.1:{port}/parse",
                params={'url': url},
                timeout=5
            )
            if response.status_code == 200:
                successful_requests += 1
        except:
            pass

    # создание потоков
    threads = []
    for url in urls:
        t = threading.Thread(target=make_request, args=(url,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    execution_time = time.time() - start_time
    process = psutil.Process(os.getpid()) # использованная память
    memory_usage = process.memory_info().rss / 1024 / 1024

    results[server_type] = {
        'execution_time': execution_time,
        'successful_requests': successful_requests,
        'total_requests': len(urls),
        'memory_usage_mb': memory_usage,
        'requests_per_second': successful_requests / execution_time if execution_time > 0 else 0
    }


def main():
    # тестовые ссылки
    test_urls = [
        'https://dental-first.ru/catalog/stomatologicheskie-materialy/shtifty3/shtifty-guttaperchivye-gapadent/',
        'https://dental-first.ru/catalog/stomatologicheskie-materialy/shtifty3/shtifty-bezzolnye/shtifty-bezzolnye-angelus/',
        'https://dental-first.ru/catalog/stomatologicheskie-materialy/shtifty3/shtifty-titanovye/'
    ]

    results = {'async': [], 'threading': []}

    for i in range(3):
        print(f"\nТест #{i + 1}")
        # асинхронный
        print("Запуск асинхронного сервера")
        test_result = {}
        test_server('async', 8081, test_urls, test_result)
        results['async'].append(test_result['async'])

        # многопоточный
        print("Запускаем многопоточный сервер")
        test_result = {}
        test_server('threading', 8082, test_urls, test_result)
        results['threading'].append(test_result['threading'])

    for server_type in ['async', 'threading']:
        print(f"\n{server_type.upper()} СЕРВЕР:")
        avg_time = sum(r['execution_time'] for r in results[server_type]) / 3
        avg_memory = sum(r['memory_usage_mb'] for r in results[server_type]) / 3
        avg_rps = sum(r['requests_per_second'] for r in results[server_type]) / 3

        print(f"Среднее время выполнения: {avg_time:.2f} сек")
        print(f"Среднее использование памяти: {avg_memory:.2f} МБ")
        print(f"Средняя скорость: {avg_rps:.2f} запросов/сек")
        print(
            f"Успешных запросов: {results[server_type][0]['successful_requests']}/{results[server_type][0]['total_requests']}")

if __name__ == '__main__':
    main()
