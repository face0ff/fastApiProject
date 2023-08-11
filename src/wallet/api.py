from loguru import logger
from eth_account import Account



def create_wallet():
    private_key = Account.create().private_key.hex()
    account = Account.from_key(private_key)

    logger("Адрес кошелька: {}", account.address)
    logger("Приватный ключ: {}", private_key


def import_wallet(private_key):
    account = Account.from_key(private_key)
    logger("Адрес кошелька: {}", account.address)


