#Написать многопоточный и асинхронный серверы, которые обрабатывают внешние запросы  пор страницам сайта https://dental-first.ru/catalog.
# Для тестирования напишите сервер, который отправляет множественные запросы по различным страницам сайта.
# Сами  сервера должны сохранять названия товаров в файл.
# Сравните время выполнения, потребляемую память, и нагрузку на сервер.
# названия товаров под одной любой категорией, ссылки вставить как тестовые данные, readme файл на каких Url и как запускать

from aiohttp import web
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import re

# асинхронный сервер

async def fetch_and_parse(session, url):  # асинхронная функция для парсинга
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            items = []  # названия товаров

            # Удаляем весь блок "Лидеры продаж" из HTML
            for slider in soup.find_all(class_='slider-block'):
                slider.decompose()

            # Теперь все оставшиеся .set-card - это товары нужной категории
            total_price = 0
            for card in soup.select('.set-card'):
                product_link = card.select_one('a.di_b.c_b')
                if product_link:
                    text = product_link.text.strip()
                    if text and text not in items:
                        items.append(text)
                #поиск цены
                price_text = card.get_text()
                prices = re.findall(r'(\d+)\s*₽', price_text)
                if prices:
                    try:

                        price = int(prices[0])
                        total_price += price
                    except:
                        pass
            return {
                'url': url,
                'items': items,
                'count': len(items),
                'total_price': total_price
            }
    except Exception as e:
        return {'url': url, 'error': str(e), 'items': []}


async def handle_request(request):
    url = request.query.get('url', 'https://dental-first.ru/catalog')

    async with aiohttp.ClientSession() as session:
        result = await fetch_and_parse(session, url)

        # сохранение в файл
        with open('async_items.txt', 'a', encoding='utf-8') as f:
            f.write(f"URL: {result['url']}\n")
            for item in result.get('items', []):
                f.write(f"- {item}\n")
            f.write(f"Всего товаров: {result.get('count', 0)}\n")
            f.write(f"Суммарная стоимость: {result.get('total_price', 0)} ₽\n")
            f.write("-" * 20 + "\n")

        return web.json_response(result)


def run_async_server(): # запуск сервера
    app = web.Application()
    app.router.add_get('/parse', handle_request)

    runner = web.AppRunner(app)

    async def start():
        await runner.setup()
        site = web.TCPSite(runner, '127.0.0.1', 8081) # выбор порта
        await site.start()
        print("Асинхронный сервер запущен")
        await asyncio.Event().wait()  # Бесконечное ожидание

    asyncio.run(start())

if __name__ == '__main__':
    run_async_server()