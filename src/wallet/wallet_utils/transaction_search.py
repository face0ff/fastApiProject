import asyncio
import httpx
from src.wallet.config_wallet import api_moralis, api_moralis_url, router
import json
from redis.asyncio.client import Redis
import loguru
from src.wallet.containers import WalletContainer

w3 = WalletContainer.w3


async def transaction_search(body: dict):
    block = body['block']
    address = body['address']

    headers = {
        "accept": "application/json",
        "X-API-Key": api_moralis,
    }

    params = {
        "chain": "sepolia",
        "from_block": block
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{api_moralis_url}/{address}/",
            headers=headers,
            params=params,
        )
        if response.status_code == 200:
            await asyncio.sleep(1)
            result = response.json()
            if result['result']:
                transaction = result['result'][0]
                gas_used = int(transaction['receipt_gas_used'])
                gas_price = int(transaction['gas_price'])
                value = w3.from_wei(int(transaction['value']), 'ether')
                fee = w3.from_wei(int(gas_used * gas_price), 'ether')
                async with router.broker as broker:
                    body = {
                        "txn_hash": transaction['hash'],
                        "address_from": transaction['from_address'],
                        "address_to": transaction['to_address'],
                        "value": value,
                        "fee": fee,
                    }
                    await broker.publish(body, queue="transaction_save")
            else:
                loguru.logger.critical("Попытаемся еще разочек")
                return False
        else:
            print("Request failed:", response.text)
            return False


async def all_lost_block_in_base(last_block_number) -> object:
    lost_block = []
    async with Redis.from_url("redis://localhost") as redis:
        count = await redis.get('count')
    if count.decode() == '0':
        request = WalletContainer.wallet_request()
        last_block_in_base = await request.get_last_block_from_base()
        if last_block_number > last_block_in_base:
            offset = int(last_block_number) - last_block_in_base
            for i in range(1, offset):
                lost_block.append(last_block_in_base + i)
        async with Redis.from_url("redis://localhost") as redis:
            await redis.set('count', '1')

        return lost_block
    else:
        return None


async def transaction_ws_search_service(body: int):
    block_number = body
    block = w3.eth.get_block(int(block_number), full_transactions=True)
    transactions_block_list = block.transactions

    request = WalletContainer.wallet_request()
    await request.last_block_save(block_number)

    async with Redis.from_url("redis://localhost") as redis:
        await redis.set('last_block', block_number)
        wallet_list = await redis.get('wallet_list')
        wallet_list = json.loads(wallet_list)

    addresses = set()
    for tx_hash in transactions_block_list:

        sender_address = tx_hash['from']
        recipient_address = tx_hash.get('to', None)

        addresses.add(sender_address)
        if recipient_address:
            addresses.add(recipient_address)

    unique_addresses = list(addresses)

    loguru.logger.info(f'Block number={block_number}, unique_addresses={unique_addresses}, wallet_list= {wallet_list}')

    matching_addresses = [address for address in unique_addresses if str(address) in wallet_list]

    if matching_addresses:

        for address in matching_addresses:
            loguru.logger.critical(f'BLOCK={block_number}, ADDRESS={address}')
            async with router.broker as broker:
                body = {
                    'block': block_number,
                    'address': address
                }
                await broker.publish(body, queue="block")

    loguru.logger.info(f"Ничего такого в базе нет")


async def transaction_ws_search(body: int):
    lost_block_list = await all_lost_block_in_base(body)
    if lost_block_list:
        for block in lost_block_list:
            await transaction_ws_search_service(block)
            await asyncio.sleep(1)
    else:
        await transaction_ws_search_service(body)
