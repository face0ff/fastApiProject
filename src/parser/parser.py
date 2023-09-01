import asyncio
from web3 import Web3
from propan.fastapi import RabbitRouter
import os
import dotenv
import json
from redis.asyncio.client import Redis
from src.wallet.containers import WalletContainer

dotenv.load_dotenv()

api_infura = os.getenv('API_INFURA')
api_infura = f"https://sepolia.infura.io/v3/{api_infura}"

router = RabbitRouter('amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost')

# async def get_last_block_number() -> object:
#     w3 = Web3(Web3.HTTPProvider(api_infura))
#     latest_block_number = w3.eth.block_number
#     return latest_block_number
#
# async def all_lost_block_in_base() -> object:
#     lost_block = []
#     request = WalletContainer.wallet_request()
#     last_block_in_base = await request.get_last_block_from_base()
#     last_block_in_blockchain = await get_last_block_number()
#     if last_block_in_blockchain > last_block_in_base:
#         offset = int(last_block_in_blockchain) - last_block_in_base
#         for i in range(1, offset):
#             lost_block.append(last_block_in_base + i)
#         return lost_block
#
# async def get_transaction_from_block(last_block=None, lost_block=None):
#     w3 = Web3(Web3.HTTPProvider(api_infura))
#     transactions_list = []
#     if last_block:
#
#         block = w3.eth.get_block(int(last_block))
#         transactions = block.transactions
#         for tx_hash in transactions:
#             # tx = w3.eth.get_transaction(tx_hash)
#             transactions_list.append(tx_hash.hex())
#         body = {
#             'transactions_from_block': transactions_list,
#             'latest_block_number': last_block
#         }
#         async with router.broker as broker:
#             await broker.publish(body,
#                                  queue="list_transactions")
#
#     else:
#
#         for block_number in lost_block:
#             print(block_number)
#             await asyncio.sleep(14)
#             block = w3.eth.get_block(int(block_number))
#             transactions = block.transactions
#
#             for tx_hash in transactions:
#                 # tx = w3.eth.get_transaction(tx_hash)
#                 transactions_list.append(tx_hash.hex())
#
#             body = {
#                 'transactions_from_block': transactions_list,
#                 'latest_block_number': block_number
#             }
#             async with router.broker as broker:
#                 await broker.publish(body,
#                                      queue="list_transactions")
#
# async def main():
#     latest_block = await get_last_block_number()
#     while True:
#         lost_block = await all_lost_block_in_base()
#
#         async with Redis.from_url("redis://localhost") as redis:
#             last_block_save = await redis.get('last_block')
#         if lost_block:
#             await get_transaction_from_block(lost_block=lost_block)
#
#         elif latest_block > int(last_block_save.decode()):
#             await get_transaction_from_block(last_block=latest_block)
#
#
#         await asyncio.sleep(14)
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     try:
#         loop.run_until_complete(main())
#     except KeyboardInterrupt:
#         pass
#     finally:
#         loop.run_until_complete(router.broker.stop())
#         loop.close()



blocks_list = []


async def get_last_block_number() -> object:
    w3 = Web3(Web3.HTTPProvider(api_infura))
    latest_block_number = w3.eth.block_number
    return latest_block_number


async def create_block_list(latest_block_number):
    if not blocks_list:
        blocks_list.append(latest_block_number)
    else:
        last_block_in_list = int(blocks_list[-1])
        if last_block_in_list + 1 == latest_block_number:
            blocks_list.append(latest_block_number)
        else:
            offset = int(latest_block_number) - last_block_in_list
            for i in range(1, offset):
                blocks_list.append(last_block_in_list + i)
            if latest_block_number not in blocks_list:
                blocks_list.append(latest_block_number)
    return blocks_list


async def get_transaction_from_block(full_blocks_list: list):
    w3 = Web3(Web3.HTTPProvider(api_infura))
    print(full_blocks_list)
    transactions_list = []
    for block_number in full_blocks_list[1:]:
        print(block_number)
        block = w3.eth.get_block(int(block_number))
        transactions = block.transactions

        for tx_hash in transactions:
            # tx = w3.eth.get_transaction(tx_hash)
            transactions_list.append(tx_hash.hex())

    if len(blocks_list) > 1:
        last_element = blocks_list[-1]
        blocks_list.clear()
        blocks_list.append(last_element)

    return transactions_list


async def main():
    while True:
        latest_block_number = await get_last_block_number()
        full_blocks_list = await create_block_list(latest_block_number)
        transactions_from_block = await get_transaction_from_block(full_blocks_list)
        body = {
            'transactions_from_block': transactions_from_block,
            'latest_block_number': latest_block_number
        }
        async with router.broker as broker:
            await broker.publish(body,
                                 queue="list_transactions")


        await asyncio.sleep(4)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(router.broker.stop())
        loop.close()
