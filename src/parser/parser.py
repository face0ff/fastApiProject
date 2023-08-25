import asyncio
from web3 import Web3
from propan.fastapi import RabbitRouter
import os
import dotenv

dotenv.load_dotenv()

api_infura = os.getenv('API_INFURA')
api_infura = f"https://sepolia.infura.io/v3/{api_infura}"

router = RabbitRouter('amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost')
blocks_list = []


async def get_last_block_number() -> object:
    w3 = Web3(Web3.HTTPProvider(api_infura))
    latest_block_number = w3.eth.block_number
    # full_blocks_list = await create_block_list(latest_block_number)
    # transactions_from_block = await get_transaction_from_block(full_blocks_list)
    # async with router.broker as broker:
    #     await broker.publish(f"Hello, Propan! last block == {latest_block_number}", queue="test")
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
        async with router.broker as broker:
            await broker.publish(set(transactions_from_block),
                                 queue="list_transactions")

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
