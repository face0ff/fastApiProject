# from dependency_injector import containers, providers
#
# from src import config_db
# from src.celery.celery import app
# from src.database import Database
# from src.users.requests import UserRequest
# from src.wallet.requests import WalletRequest
# from src.wallet.services import WalletService
#
#
# class CeleryContainer(containers.DeclarativeContainer):
#     wiring_config = containers.WiringConfiguration(packages=["src.celery"])
#     celery = app
