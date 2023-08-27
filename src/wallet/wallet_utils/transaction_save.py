from src.wallet.containers import WalletContainer



async def transaction_save(body):
    request = WalletContainer.wallet_request()
    value = body['value']
    address_to = body['address_to']
    address_from = body['address_from']
    txn_hash = body['txn_hash']
    fee = body['fee']
    all_wallets = await request.save_transaction(value, address_to, address_from, txn_hash, fee)
