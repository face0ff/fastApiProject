from loguru import logger
from fastapi import APIRouter, Depends, Response, status, Request, Header
from fastapi import HTTPException

from dependency_injector.wiring import inject, Provide

from src.users import schemas
from src.users.containers import UserContainer
from src.users.services import UserService
from src.utils.get_token_from_cookie import get_token_from_cookie

router = APIRouter(prefix="/users", tags=['Users'])


@router.get("/")
@inject
async def get_list(
        email: str = Depends(get_token_from_cookie),
        user_service: UserService = Depends(Provide[UserContainer.user_service]),
):
    return await user_service.get_users()


@router.get("/{user_id}")
@inject
async def get_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[UserContainer.user_service]),
):
    try:
        return await user_service.get_user_by_id(user_id)
    except NameError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/add", status_code=status.HTTP_201_CREATED)
@inject
async def add(
        user_data: schemas.User,
        user_service: UserService = Depends(Provide[UserContainer.user_service]),
):
    if user_data.password1 != user_data.password2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пароли не совпадают")
    return await user_service.create_user(user_data)


@router.post("/auth", status_code=status.HTTP_200_OK)
@inject
async def auth(
        request: Request,
        response: Response,
        auth_data: schemas.Login,
        user_service: UserService = Depends(Provide[UserContainer.user_service]),

):
    return await user_service.auth_user(auth_data, request, response)


@router.put("/edit_profile", status_code=status.HTTP_200_OK)
@inject
async def edit_profile(
        user_data: schemas.Profile,
        email: str = Depends(get_token_from_cookie),
        user_service: UserService = Depends(Provide[UserContainer.user_service]),
):
    if user_data.password1 != user_data.password2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пароли не совпадают")
    return await user_service.update_user(user_data, email)


@router.post("/profile", status_code=status.HTTP_200_OK)
@inject
async def profile(
        email: str = Depends(get_token_from_cookie),
        user_service: UserService = Depends(Provide[UserContainer.user_service])
):
    return await user_service.get_profile(email)


@router.get("/logout", status_code=status.HTTP_200_OK)
@inject
async def logout(
        response: Response,
        email: str = Depends(get_token_from_cookie)):
    response.delete_cookie(key="token")  # Удалить куки с токеном
    return {"message": "Пользователь успешно вышел"}

