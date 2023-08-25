"""Containers module."""
import logging
from loguru import logger
from dependency_injector import containers, providers

from src import config_db
from src.database import Database
from src.users.repository import UserRequest
from src.users.services import UserService
from src.users.utils import send_registration_email


class UserContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["src.users"])

    db = providers.Singleton(Database, db_url=config_db.db_url)

    user_request = providers.Factory(
        UserRequest,
        session_factory=db.provided.session,
        send_registration_email=send_registration_email,
    )

    user_service = providers.Factory(
        UserService,
        user_request=user_request,
    )