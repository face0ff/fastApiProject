import asyncio
from propan.fastapi import RabbitRouter
from src.wallet.utils import transactions_search

router = RabbitRouter('amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost')


@router.broker.handle(queue="list_transactions")
async def list_transactions_handler(body):
    # async with Redis.from_url("redis://localhost") as redis:
    #     json_data = json.dumps(body)
    #     transactions = await redis.set('transactions', json_data)
    await transactions_search(body)


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
