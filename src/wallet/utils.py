import httpx
from web3 import Web3

from src.wallet.config_wallet import api_etherscan_url, api_etherscan, api_infura


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
    # value_wei = w3.to_wei(value, 'ether'),  # Сумма в Wei (0.1 ETH)
    # gas_price = w3.to_wei(await get_gas(), 'wei')  # Цена газа в Wei
    gas_price = await get_gas()
    print(gas_price)
    nonce = w3.eth.get_transaction_count(account)

    transaction = {
        'to': receiver,
        'value': w3.to_wei(value, 'ether'),
        'gas': 21000,  # Лимит газа для базовой транзакции
        'gasPrice': gas_price,
        'nonce': nonce,
    }

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print("Transaction)))))))))>:", tx_hash)
    result = {
        'tx_hash': tx_hash.hex(),
        'fee': 21000*gas_price
    }
    return result
