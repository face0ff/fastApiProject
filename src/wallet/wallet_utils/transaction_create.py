from src.wallet.containers import WalletContainer

w3 = WalletContainer.w3


async def create_transaction(wallet_transaction, receiver_transaction, private_key, value):
    account = wallet_transaction
    private_key = private_key
    receiver = receiver_transaction
    nonce = w3.eth.get_transaction_count(account)
    value = w3.to_wei(value, 'ether')
    gas_price = w3.eth.gas_price * 2

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
