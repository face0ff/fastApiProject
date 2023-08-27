import json
from redis.asyncio.client import Redis
import loguru
from web3 import Web3
from src.wallet.config_wallet import api_infura, router
from src.wallet.containers import WalletContainer








async def get_wallet_list():
    request = WalletContainer.wallet_request()
    all_wallets = await request.get_all_wallets()
    all_wallets = json.dumps(all_wallets)
    async with Redis.from_url("redis://localhost") as redis:
        await redis.set('wallet_list', all_wallets)
    loguru.logger.info(f"Этот наши все адреса {all_wallets}")


async def wallets_search(body):
    transactions_block_list = body['transactions_from_block']
    block_number = body['latest_block_number']
    async with Redis.from_url("redis://localhost") as redis:
        wallet_list = await redis.get('wallet_list')
        wallet_list = json.loads(wallet_list)

    w3 = Web3(Web3.HTTPProvider(api_infura))
    addresses = set()  # Множество для хранения уникальных адресов
    for tx_hash in transactions_block_list:
        tx = w3.eth.get_transaction(tx_hash)
        if tx:
            sender_address = tx['from']
            recipient_address = tx.get('to', None)

            # Добавляем адреса в множество
            addresses.add(sender_address)
            if recipient_address:
                addresses.add(recipient_address)

    # Преобразуем множество обратно в список
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
    return

