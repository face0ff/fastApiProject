import asyncio
import loguru
import httpx
from src.celery.celery import app
from src.ibay.containers import ProductContainer


async def make_request(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Проверяем успешность запроса
            return True
        except httpx.HTTPError:
            return False


@app.task()
async def check_delivery(body):
    url = "https://www.google.com"
    success_count = 0
    loguru.logger.critical('Пробуем доставить')
    tasks = [make_request(url) for _ in range(100)]
    results = await asyncio.gather(*tasks)
    success_count = sum(results)

    if success_count == 1000:
        print("Все 10000 запросов успешно выполнены")
        request = ProductContainer.order_request()
        body = {
            'result': "Delivery",
            'transaction_id': body['transaction_id']
        }

        await request.change_status(body)

    else:
        print(f"Выполнено {success_count} из 10000 запросов")
        request = ProductContainer.order_request()
        body = {
            'result': "Failed",
            'transaction_id': body['transaction_id']
        }
        await request.change_status(body)