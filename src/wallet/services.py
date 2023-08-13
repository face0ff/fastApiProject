import secrets

from loguru import logger
from eth_account import Account
import os
import jwt

from src.users.requests import UserRequest
from src.wallet.requests import WalletRequest

from fastapi import HTTPException, status, Response


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
