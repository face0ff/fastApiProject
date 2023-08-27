import secrets
from eth_account import Account
from src.wallet.repository import WalletRequest

from fastapi import HTTPException, status


class WalletService:

    def __init__(self, wallet_request: WalletRequest) -> None:
        self.requests: WalletRequest = wallet_request

    async def wallet_action(self, email, key=None):
        if key:
            try:
                wallet = Account.from_key(key)
            except:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid key")
        else:
            key = "0x" + secrets.token_hex(32)
            wallet = Account.from_key(key)
        user = await self.requests.get_by_email(email)
        return {
            "wallet": wallet,
            "key": key,
            "user": user
        }

    async def create_wallet(self, email):
        request = await self.wallet_action(email)
        return await self.requests.save_wallet(request['wallet'], request['key'], request['user'])

    async def import_wallet(self, email, key):
        request = await self.wallet_action(email, key)
        return await self.requests.save_wallet(request['wallet'], request['key'], request['user'])

    async def create_transaction(self, value, wallet_sender, wallet_receiver):
        print(await self.requests.save_balance(wallet_sender), value)
        if await self.requests.save_balance(wallet_sender) >= value:
            return await self.requests.save_transaction(value, wallet_sender, wallet_receiver)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Бабки бабки .... бабки!")

    async def show_balance(self, address):
        return await self.requests.save_balance(address)

    async def show_wallets(self, email):
        return await self.requests.get_all_user_wallets(email)

    async def show_all_wallets(self):
        return await self.requests.get_all_wallets()


