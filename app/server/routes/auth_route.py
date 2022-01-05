from fastapi import APIRouter, Body
from fastapi.param_functions import Depends

from ..schemas.auth_schema import LoginDto, RegisterDto, TokenData
from ..schemas.user_schema import UserDto
from ..services.auth_service import (
    create_user_with_encryption,
    jwt_authentication,
    validate_user_with_credentials,
)

router = APIRouter()


@router.get("", response_description="Retrieve current user", response_model=UserDto)
async def get_current_user_data(user: UserDto = Depends(jwt_authentication)):
    return UserDto.parse_obj(user)


@router.post(
    "/login", response_description="Login with credentials", response_model=TokenData
)
async def login(body: LoginDto):
    token = validate_user_with_credentials(body)
    return TokenData(access_token=token, token_type="bearer")


@router.post(
    "/register", response_description="Register with credentials", response_model=str,
)
async def register(body: RegisterDto):
    res = create_user_with_encryption(body)
    return res

