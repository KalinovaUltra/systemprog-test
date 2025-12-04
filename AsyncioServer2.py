#Напишите асинхронный и многопоточный сокеты, и клиент для них,
# которые считывают количество строк в файлах некой директории.
# Сравните показатели потребления, и время выполнения.
# Определите, какая минимальная память гарантировано обеспечит обработку 1000 одновременных запросов

from aiohttp import web # асинхронный сервер
import aiohttp
import ThreadingServer

async def func_1():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dental-first.ru/catalog') as response:
                with open('itemname.txt', 'w') as file:
                    file.write(await response.text())
                return await response.json()
    except Exception as e:
        return {"error": f"func_1: {str(e)}"}

async def handler(request):
    data = []
    _data = await func_1()
    data.append(_data)
    return web.json_response(data)

app = web.Application()
app.router.add_get('/', handler)

def server():
    web.run_app(app, host='127.0.0.1', port=8082) #порт

if __name__ == '__main__':
    server()