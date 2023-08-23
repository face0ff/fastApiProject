from dependency_injector import containers, providers

# from src.celery.containers import CeleryContainer
from src.users.containers import UserContainer
from src.wallet.containers import WalletContainer
from src import config_db
from src.database import Database


class MainContainer(containers.DeclarativeContainer):
    db = providers.Singleton(Database, db_url=config_db.db_url)

    user_container = providers.Container(UserContainer)
    wallet_container = providers.Container(WalletContainer)
    # celery_container = providers.Container(CeleryContainer)

    #
    # user_request = user_container.user_request
    # wallet_request = wallet_container.wallet_request
    #
    # user_service = user_container.user_service
    # wallet_service = wallet_container.wallet_service
    # get_token_from_cookie = providers.Singleton(get_token_from_cookie),
