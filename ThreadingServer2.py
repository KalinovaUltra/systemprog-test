#Напишите асинхронный и многопоточный сокеты, и клиент для них,
# которые считывают количество строк в файлах некой директории.
# Сравните показатели потребления, и время выполнения.
# Определите, какая минимальная память гарантировано обеспечит обработку 1000 одновременных запросов


from threading import Thread # многопоточный сервер
import requests
import time

def func_1():
   response = requests.get('https://dental-first.ru/catalog')
   with open('itemname.txt', 'w') as file:
      file.write(await response.text())
   return response.json()


def general():
   func_1()


def main():
   threads = []
   for thr in range(3):
       threads.append(Thread(target=general, args=()))
   for thr in threads:
       thr.start()
   for thr in threads:
       thr.join()

if __name__ == '__main__':
   start = time.time()
   main()
   print(f'Время ваыполнения: {time.time() - start}')
