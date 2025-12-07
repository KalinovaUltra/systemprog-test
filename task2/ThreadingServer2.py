#Напишите асинхронный и многопоточный сокеты, и клиент для них,
# которые считывают количество строк в файлах некой директории.
# Сравните показатели потребления, и время выполнения.
# Определите, какая минимальная память гарантировано обеспечит обработку 1000 одновременных запросов

from flask import Flask, request, jsonify #многопоточный
import os
from concurrent.futures import ThreadPoolExecutor
import threading

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=10)  # пул потоков


def count_lines_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return {"filename": os.path.basename(filepath), "lines": len(lines)}
    except Exception as e:
        return {"filename": os.path.basename(filepath), "error": str(e)}


@app.route('/count')
def handle_request():
    directory = request.args.get('directory', '.')  # текущая директория

    if not os.path.exists(directory):
        return jsonify({"error": f"Directory {directory} not found"})

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    futures = []

    for filename in files:
        filepath = os.path.join(directory, filename)
        future = executor.submit(count_lines_in_file, filepath)
        futures.append(future)

    results = [future.result() for future in futures]

    return jsonify({"directory": directory, "files": results})


def run_threading_server():
    print("Многопоточный сервер запущен на порту 8082")
    app.run(host='127.0.0.1', port=8082, threaded=True)


if __name__ == '__main__':
    run_threading_server()
