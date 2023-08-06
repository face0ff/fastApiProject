import loguru
from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from src.users import schemas
from src.users.containers import Container
from src.users.services import UserService


router = APIRouter(prefix="/users", tags=['Users'])


@router.get("/")
@inject
def get_list(
        user_service: UserService = Depends(Provide[Container.user_service]),
):

    return user_service.get_users()


@router.get("/{user_id}")
@inject
def get_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        return user_service.get_user_by_id(user_id)
    except NameError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
def add(
        user_data: schemas.User,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.create_user(user_data)
