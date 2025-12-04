#Написать многопоточный и асинхронный серверы, которые обрабатывают внешние запросы  пор страницам сайта https://dental-first.ru/catalog.
# Для тестирования напишите сервер, который отправляет множественные запросы по различным страницам сайта.
# Сами  сервера должны сохранять названия товаров в файл.
# Сравните время выполнения, потребляемую память, и нагрузку на сервер.
# названия товаров под одной любой категорией, ссылки вставить как тестовые данные, readme файл на каких Url и как запускать

from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue
import time

# многопоточный сервер

app = Flask(__name__)

def parse_page(url): # фунция для парсинга
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = [] # названия товаров
        for item in soup.select('.product-card__title, .catalog-item__name, .product-item-link'):
            if item.text.strip():
                items.append(item.text.strip())

        return {
            'url': url,
            'items': items[:10], # первые 10 товаров
            'count': len(items)
        }
    except Exception as e:
        return {'url': url, 'error': str(e), 'items': []}


@app.route('/parse')
def handle_request():
    url = request.args.get('url', 'https://dental-first.ru/catalog')
    result = parse_page(url)

    # сохранение в файл
    with open('threading_items.txt', 'a', encoding='utf-8') as f:
        f.write(f"URL: {result['url']}\n")
        for item in result.get('items', []):
            f.write(f"- {item}\n")
        f.write(f"Всего товаров: {result.get('count', 0)}\n")
        f.write("-" * 50 + "\n")

    return jsonify(result)


def run_threading_server(): # запуск сервера
    print("Многопоточный сервер запущен") # выбор порта
    app.run(host='127.0.0.1', port=8082, threaded=True)


if __name__ == '__main__':
    run_threading_server()