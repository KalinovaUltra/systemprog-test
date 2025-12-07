#Напишите асинхронный и многопоточный сокеты, и клиент для них,
# которые считывают количество строк в файлах некой директории.
# Сравните показатели потребления, и время выполнения.
# Определите, какая минимальная память гарантировано обеспечит обработку 1000 одновременных запросов

import asyncio #асинхронный
import os
from aiohttp import web


async def count_lines_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return {"filename": os.path.basename(filepath), "lines": len(lines)}
    except Exception as e:
        return {"filename": os.path.basename(filepath), "error": str(e)}


async def handle_request(request):
    directory = request.query.get('directory', '.')  # текущая директория

    if not os.path.exists(directory):
        return web.json_response({"error": f"Directory {directory} not found"})

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    tasks = []

    for filename in files:
        filepath = os.path.join(directory, filename)
        tasks.append(count_lines_in_file(filepath))

    results = await asyncio.gather(*tasks)
    return web.json_response({"directory": directory, "files": results})


def run_async_server():
    app = web.Application()
    app.router.add_get('/count', handle_request)

    print("Асинхронный сервер запущен на порту 8081")
    web.run_app(app, host='127.0.0.1', port=8081)


if __name__ == '__main__':
    run_async_server()