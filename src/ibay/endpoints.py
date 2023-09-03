
from fastapi import APIRouter, Depends, Response, status, Request, Header

from dependency_injector.wiring import inject, Provide

from src.ibay import schemas
from src.ibay.containers import ProductContainer
from src.ibay.services import ProductService, OrderService
from src.utils.get_token_from_cookie import get_token_from_cookie

router = APIRouter(prefix="/products", tags=['Products'])





@router.get("/")
@inject
async def get_list(
        email: str = Depends(get_token_from_cookie),
        product_service: ProductService = Depends(Provide[ProductContainer.product_service]),
):
    return await product_service.get_products()


@router.get("/id/{product_id}/")
@inject
async def get_by_id(
        product_id: int,
        email: str = Depends(get_token_from_cookie),
        product_service: ProductService = Depends(Provide[ProductContainer.product_service]),
):
    try:
        return await product_service.get_product_by_id(product_id)
    except NameError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/add/", status_code=status.HTTP_201_CREATED)
@inject
async def add(
        product_data: schemas.Product,
        email: str = Depends(get_token_from_cookie),
        product_service: ProductService = Depends(Provide[ProductContainer.product_service]),
):

    return await product_service.create_product(product_data)


@router.get("/order")
@inject
async def get_list(
        email: str = Depends(get_token_from_cookie),
        order_service: OrderService = Depends(Provide[ProductContainer.order_service]),
):
    return await order_service.get_orders(email)

@router.post("/order/add/", status_code=status.HTTP_201_CREATED)
@inject
async def add(
        order_data: schemas.Order,
        email: str = Depends(get_token_from_cookie),
        order_service: OrderService = Depends(Provide[ProductContainer.order_service]),
):

    return await order_service.create_order(order_data, email)