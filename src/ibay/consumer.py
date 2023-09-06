import asyncio
from propan.fastapi import RabbitRouter
import loguru
from src.ibay.containers import ProductContainer
from src.wallet.config_wallet import router
from src.ibay.tasks import check_delivery_task


@router.broker.handle(queue="transaction_success")
async def result_handler(body):
    loguru.logger.critical(body)
    if body['result'] == 'Success':
        check_delivery_task.apply_async(args=[body], queue='check_delivery')

    elif body['result'] == 'Refund':
        request = ProductContainer.order_request()
        body = {
            'result': "Refund",
            'transaction_id': body['transaction_id']
        }
        await request.change_status(body)


    else:
        request = ProductContainer.order_request()
        body = {
            'result': "Failed",
            'transaction_id': body['transaction_id']
        }
        await request.change_status(body)


async def main():
    await router.broker.start()
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(router.broker.stop())
        loop.close()
