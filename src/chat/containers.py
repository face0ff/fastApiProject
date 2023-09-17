"""Containers module."""
import logging
from loguru import logger
from dependency_injector import containers, providers

from src import config_db
from src.chat.repository import ChatRequest
from src.database import Database
from src.users.permissions import Permissions
from src.users.repository import UserRequest
from src.users.services import UserService
from src.users.utils import send_registration_email


class ChatContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["src.chat"])

    db = providers.Singleton(Database, db_url=config_db.db_url)

    chat_request = providers.Factory(
        ChatRequest,
        session_factory=db.provided.session,
    )
