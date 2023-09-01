from src.ibay.models import Product
from src.ibay.repository import ProductRequest


class ProductService:

    def __init__(self, product_request: ProductRequest) -> None:
        self.requests: ProductRequest = product_request

    async def get_products(self):
        return await self.requests.get_all()

    async def get_product_by_id(self, product_id: int) -> Product:
        return await self.requests.get_by_id(product_id)

    async def create_product(self, product_data: dict) -> Product:
        return await self.requests.add(product_data)
