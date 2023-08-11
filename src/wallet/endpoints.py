from fastapi import APIRouter, Depends, Response, status, Request, Header
from fastapi import HTTPException

from dependency_injector.wiring import inject, Provide

from src.users import schemas
from src.wallet.containers import WalletContainer

from src.wallet.services import WalletService

router = APIRouter(prefix="/wallets", tags=['Wallets'])


@router.get("/create")
@inject
async def create(request: Request, wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.create_wallet(request)

# def import_wallet(private_key):
#     account = Account.from_key(private_key)
#     logger("Адрес кошелька: {}", account.address)
@router.get("/import")
@inject
async def import_key(key, request: Request, wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.import_wallet(request, key)