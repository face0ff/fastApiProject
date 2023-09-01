from dependency_injector import containers, providers
from src import config_db
from src.database import Database
from src.ibay.repository import ProductRequest
from src.ibay.services import ProductService


class ProductContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["src.ibay"])

    db = providers.Singleton(Database, db_url=config_db.db_url)

    product_request = providers.Factory(
        ProductRequest,
        session_factory=db.provided.session,
    )

    product_service = providers.Factory(
        ProductService,
        product_request=product_request,
    )
