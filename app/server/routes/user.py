from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..services.user import get_all_users

# from app.server.models.user import UserSchema
from ..models.common import ResponseModel, ErrorResponseModel

router = APIRouter()


@router.get("/", response_description="Retrieve all users")
async def get_all_users_data():
    users = await get_all_users()
    return ResponseModel(users, "Get all users successfuly")

