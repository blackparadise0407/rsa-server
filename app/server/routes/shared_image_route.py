from fastapi import APIRouter
from fastapi.param_functions import Depends

from ..schemas.shared_image_schema import CreateSharedImageDto
from ..schemas.user_schema import UserDto
from ..services.auth_service import jwt_authentication
from ..services.shared_image_service import create_shared_image

router = APIRouter()


@router.post(
    "", response_description="Share image to specific user", response_model=str
)
def share_image_to(
    body: CreateSharedImageDto, user: UserDto = Depends(jwt_authentication),
):
    create_shared_image(user["id"], body)
    return "Share photo successfully"

