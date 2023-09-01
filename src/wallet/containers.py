from dependency_injector import containers, providers

from src import config_db
from src.database import Database
from src.wallet.repository import WalletRequest
from src.wallet.services import WalletService
from web3.middleware import geth_poa_middleware
from web3 import Web3
from src.wallet.config_wallet import api_infura


class WalletContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["src.wallet"])

    db = providers.Singleton(Database, db_url=config_db.db_url)

    wallet_request = providers.Factory(
        WalletRequest,
        session_factory=db.provided.session,
    )

    wallet_service = providers.Factory(
        WalletService,
        wallet_request=wallet_request
    )

    w3 = Web3(Web3.HTTPProvider(api_infura))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
