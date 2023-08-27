import httpx
from src.wallet.config_wallet import api_moralis, api_moralis_url, api_infura, router
from web3 import Web3


async def transaction_search(body: dict):
    block = body['block']
    address = body['address']
    w3 = Web3(Web3.HTTPProvider(api_infura))

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
            result = response.json()
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
            print("Request failed:", response.text)

