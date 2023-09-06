
import asyncio
import loguru
from src.celery.celery import app
from src.ibay.ibay_utils import check_delivery


@app.task()
def check_delivery_task(body):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_delivery.check_delivery(body))


@app.task()
def get_last_delivery_order_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_delivery.test_delivery())
