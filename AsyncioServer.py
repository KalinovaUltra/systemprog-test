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

# асинхронный сервер

async def fetch_and_parse(session, url):  # фунция для парсинга
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            # названия товаров
            items = []
            for item in soup.select('.product-card__title, .catalog-item__name, .product-item-link'):
                if item.text.strip():
                    items.append(item.text.strip())

            return {
                'url': url,
                'items': items[:10],  # первые 10 товаров
                'count': len(items)
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
            f.write("-" * 50 + "\n")

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