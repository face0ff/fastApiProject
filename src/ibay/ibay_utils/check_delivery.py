import loguru
from src.ibay.containers import ProductContainer

import asyncio
import random
import httpx


async def make_request(url, semaphore):
    async with semaphore:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                await asyncio.sleep(random.uniform(0, 1))
                return True
            except httpx.HTTPError:
                return False




async def check_delivery(body):
    url = "https://www.google.com"
    success_count = 0
    loguru.logger.critical('Пробуем доставить')

    semaphore = asyncio.Semaphore(100)

    tasks = [make_request(url, semaphore) for _ in range(1000)]
    results = await asyncio.gather(*tasks)
    success_count = sum(results)

    if success_count < 900:
        print("Все 1000 запросов успешно выполнены")
        request = ProductContainer.order_request()
        body = {
            'result': "Delivery",
            'transaction_id': body['transaction_id']
        }

        await request.change_status(body)

    else:
        print(f"Выполнено {success_count} из 1000 запросов")
        request = ProductContainer.order_request()
        body = {
            'result': "Failed",
            'transaction_id': body['transaction_id']
        }
        await request.change_status(body)


async def test_delivery():
    request = ProductContainer.order_request()
    last_delivery_order = await request.get_old_delivery()

    if last_delivery_order:
        if random.uniform(0, 10) > 5:
            body = {
                'result': "Success",
                'transaction_id': last_delivery_order.transaction_id
            }
            await request.change_status(body)
        else:
            body = {
                'result': "Failed",
                'transaction_id': last_delivery_order.transaction_id
            }
            await request.change_status(body)
    else:
        loguru.logger.info("Ордеров со статусом ДОСТАВКА больше нет")
