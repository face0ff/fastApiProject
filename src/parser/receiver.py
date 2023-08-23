import asyncio
from propan.fastapi import RabbitRouter

router = RabbitRouter('amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost')


@router.broker.handle(queue="test")
async def base_handler(body):
    print(body)


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
