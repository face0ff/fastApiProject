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

    async def wallet_action(self, request, key=None):
        if key:
            try:
                wallet = Account.from_key(key)
            except:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid key")
        else:
            key = "0x" + secrets.token_hex(32)
            wallet = Account.from_key(key)
        token = request.cookies.get("token")
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        email: str = payload.get("sub")
        user = await self.requests.get_by_email(email)
        return {
            "wallet": wallet,
            "key": key,
            "user": user
        }

    async def create_wallet(self, request):
        request = await self.wallet_action(request)
        return await self.requests.save_wallet(request['wallet'], request['key'], request['user'])

    async def import_wallet(self, request, key):
        request = await self.wallet_action(request, key)
        return await self.requests.save_wallet(request['wallet'], request['key'], request['user'])
