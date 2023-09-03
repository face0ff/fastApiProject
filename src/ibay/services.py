from src.ibay.models import Product
from src.ibay.repository import ProductRequest, OrderRequest
from src.ibay.schemas import Order


class ProductService:

    def __init__(self, product_request: ProductRequest) -> None:
        self.requests: ProductRequest = product_request

    async def get_products(self):
        return await self.requests.get_all()

    async def get_product_by_id(self, product_id: int) -> Product:
        return await self.requests.get_by_id(product_id)

    async def create_product(self, product_data: dict) -> Product:
        return await self.requests.add(product_data)


class OrderService:

    def __init__(self, order_request: OrderRequest) -> None:
        self.requests: OrderRequest = order_request

    async def get_orders(self, email):
        return await self.requests.get_all(email)

    async def create_order(self, order_data: dict, email:str) -> Order:
        return await self.requests.add(order_data, email)