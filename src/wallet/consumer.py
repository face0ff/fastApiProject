import asyncio
import logging

from propan.fastapi import RabbitRouter

from src.wallet.config_wallet import router
from src.wallet.tasks import get_wallet_search_task, get_transaction_search_task, save_transaction_task


@router.broker.handle(queue="list_transactions")
async def list_transactions_handler(body):
    get_wallet_search_task.apply_async(args=[body], queue='wallet')


@router.broker.handle(queue="block")
async def list_block_handler(body):
    print(body)
    get_transaction_search_task.apply_async(args=[body], queue='transaction')


@router.broker.handle(queue="transaction_save")
async def result_handler(body):
    print(body)
    save_transaction_task.apply_async(args=[body], queue='save_result')


# @router.broker.handle(queue="token")
# async def token_handler(body):
#     async with Redis.from_url("redis://localhost") as redis:
#         user_id = await redis.get('id')


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
