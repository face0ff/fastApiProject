"""Containers module."""
import logging
from loguru import logger
from dependency_injector import containers, providers

from src import config_db
from src.database import Database
from src.users.requests import UserRequest
from src.users.services import UserService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["src.users"])

    db = providers.Singleton(Database, db_url=config_db.db_url)

    user_request = providers.Factory(
        UserRequest,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_request=user_request,
    )
