from dependency_injector import containers, providers

from src import config_db
from src.database import Database
from src.users.repository import UserRequest
from src.wallet.repository import WalletRequest
from src.wallet.services import WalletService
from src.wallet.utils import get_balance


class WalletContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["src.wallet"])

    db = providers.Singleton(Database, db_url=config_db.db_url)

    wallet_request = providers.Factory(
        WalletRequest,
        session_factory=db.provided.session,
        get_balance=get_balance
    )

    wallet_service = providers.Factory(
        WalletService,
        wallet_request=wallet_request
    )

