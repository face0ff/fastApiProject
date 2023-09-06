from fastapi import APIRouter, Depends

from dependency_injector.wiring import inject, Provide
from src.utils.get_token_from_cookie import get_token_from_cookie
from src.wallet.containers import WalletContainer

from src.wallet.services import WalletService

router = APIRouter(prefix="/wallets", tags=['Wallets'])


@router.post("/create/")
@inject
async def create(
        email: str = Depends(get_token_from_cookie),
        wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.create_wallet(email)


@router.post("/import_key/")
@inject
async def import_key(
        key,
        email: str = Depends(get_token_from_cookie),
        wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.import_wallet(email, key)


@router.post("/create_transaction/")
@inject
async def create_transaction(
        value: float,
        wallet_sender,
        wallet_receiver,
        wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.create_transaction(value, wallet_sender, wallet_receiver)


@router.get("/balance/")
@inject
async def balance(
        address,
        wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.show_balance(address)


@router.get("/my/")
@inject
async def wallets(
        email: str = Depends(get_token_from_cookie),
        wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.show_wallets(email)

@router.get("/my/transactions/")
@inject
async def transactions(
        email: str = Depends(get_token_from_cookie),
        wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.show_all_user_transactions(email)
