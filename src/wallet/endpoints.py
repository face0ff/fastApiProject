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


@router.get("/import_key")
@inject
async def import_key(key, request: Request,
                     wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.import_wallet(request, key)


@router.get("/create_transaction")
@inject
async def create_transaction(value, wallet_sender, wallet_receiver,
                             wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.create_transaction(value, wallet_sender, wallet_receiver)



