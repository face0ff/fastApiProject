import httpx
from web3 import Web3
from src.wallet.config_wallet import api_etherscan_url, api_etherscan, api_infura
from fastapi import HTTPException, status
from redis.asyncio.client import Redis

async def get_gas():
    headers = {
        "accept": "application/json",
    }
    params = {

        "action": "eth_gasPrice",
        "apikey": api_etherscan,

    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{api_etherscan_url}?module=proxy",
            headers=headers,
            params=params,
        )
        if response.status_code == 200:
            result = response.json()
            result_decimal = int(result['result'], 16)
            print(result_decimal)
            return result_decimal
        else:
            print("Request failed:", response.text)


async def create_transaction(wallet_transaction, receiver_transaction, private_key, value):
    w3 = Web3(Web3.HTTPProvider(api_infura))

    account = wallet_transaction
    private_key = private_key
    receiver = receiver_transaction
    gas_price = await get_gas()
    nonce = w3.eth.get_transaction_count(account)
    value = w3.to_wei(value, 'ether')

    transaction = {
        'to': receiver,
        'value': value,
        'gas': 21000,  # Лимит газа для базовой транзакции
        'gasPrice': gas_price,
        'nonce': nonce,
    }

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    result = {
        'tx_hash': tx_hash.hex(),
        'fee': w3.from_wei(int(21000 * gas_price), 'ether'),
        'value': w3.from_wei(value, 'ether')
    }
    return result


async def get_balance(address=None):
    w3 = Web3(Web3.HTTPProvider(api_infura))

    # address_list = await wallets()
    # print(address_list)

    headers = {
        "accept": "application/json",
    }
    params = {

        "action": "balancemulti",
        "address": address,
        "tag": "latest",
        "apikey": api_etherscan
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{api_etherscan_url}?module=account",
            headers=headers,
            params=params,
        )
        if response.status_code == 200:
            result = response.json()
            print(result['result'])
            balance = result['result'][0]['balance']
            return w3.from_wei(int(balance), 'ether')

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Проверьте все что вы ввели")


async def transactions_search(transactions_list):
    async with Redis.from_url("redis://localhost") as redis:
        user_id = await redis.get('id')
        print(user_id, transactions_list)
