from dependency_injector import containers, providers

from src import config_db
from src.database import Database
from src.users.requests import UserRequest
from src.wallet.requests import WalletRequest
from src.wallet.services import WalletService


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
