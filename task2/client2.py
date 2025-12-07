import requests
import asyncio
import aiohttp
import time
import psutil
import os

# тест многопоточного сервера
def test_threading():
    print("Многопоточный сервер:")
    start = time.time()
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024  # в МБ
    response = requests.get('http://127.0.0.1:8082/count',
                            params={'directory': '.'})
    data = response.json()

    print(f"Директория: {data.get('directory')}")
    for file_info in data.get('files', []):
        print(f"  {file_info.get('filename')}: {file_info.get('lines')} строк")

    mem_after = process.memory_info().rss / 1024 / 1024

    print(f"Время: {time.time() - start:.3f} сек")
    print(f"Потребление памяти: {mem_after - mem_before:.2f} МБ")

# тест асинхронного сервера
async def test_async():
    print("\nАсинхронный сервер:")
    start = time.time()
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024  # в МБ
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8081/count',
                               params={'directory': '.'}) as response:
            data = await response.json()
    mem_after = process.memory_info().rss / 1024 / 1024
    print(f"Директория: {data.get('directory')}")
    for file_info in data.get('files', []):
        print(f"  {file_info.get('filename')}: {file_info.get('lines')} строк")

    print(f"Время: {time.time() - start:.3f} сек")
    print(f"Потребление памяти: {mem_after - mem_before:.2f} МБ")


def test_many_requests():
    print("\nТест 1000 запросов к многопоточному серверу:")
    start = time.time()

    import threading
    results = []

    def make_request():
        try:
            requests.get('http://127.0.0.1:8082/count', timeout=2)
            results.append(True)
        except:
            results.append(False)

    threads = []
    for i in range(100):
        t = threading.Thread(target=lambda: [make_request() for _ in range(10)])
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start
    print(f"1000 запросов за: {elapsed:.2f} сек")
    print(f"Успешно: {sum(results)}/1000")
    print("\nОценка памяти для 1000 запросов: ~1-2 ГБ")


def main():
    test_threading()
    asyncio.run(test_async())
    test_many_requests()


if __name__ == '__main__':
    main()