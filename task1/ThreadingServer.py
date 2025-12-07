from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue
import time

# многопоточный сервер

app = Flask(__name__)


def parse_page(url):  # функция для парсинга
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = []  # названия товаров

        # удаляем лишнее в html
        for slider in soup.find_all(class_='slider-block'):
            slider.decompose()

        # товары нужной категории
        for card in soup.select('.set-card'):
            product_link = card.select_one('a.di_b.c_b')
            if product_link:
                text = product_link.text.strip()
                if text and text not in items:
                    items.append(text)

        return {
            'url': url,
            'items': items,
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
    run_threading_server()  #  вызов функции