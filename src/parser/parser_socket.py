import asyncio
import json
import os
import dotenv
import loguru
# from web3 import Web3
from websockets import connect
from propan.fastapi import RabbitRouter
from redis.asyncio.client import Redis

dotenv.load_dotenv()
api_infura = os.getenv('API_INFURA')

router = RabbitRouter('amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost')
api_infura_ws_url = f"wss://sepolia.infura.io/ws/v3/{api_infura}"
api_infura_url = f"https://sepolia.infura.io/v3/{api_infura}"


# web3 = Web3(Web3.HTTPProvider(api_infura_url))

async def get_event():
    async with Redis.from_url("redis://localhost") as redis:
        await redis.set('count', '0')
    loguru.logger.info('First launch')
    async with connect(api_infura_ws_url) as ws:
        await ws.send('{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newHeads"]}')
        subscription_response = await ws.recv()
        print(subscription_response)

        while True:
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=15)
                response = json.loads(message)
                latest_block_number = int(response['params']['result']['number'], 16)
                async with router.broker as broker:
                    await broker.publish(latest_block_number,
                                         queue="latest_block_number")
                loguru.logger.critical(latest_block_number)
            except:
                pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(get_event())
