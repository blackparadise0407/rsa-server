from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..common.database import user_collection

# from app.server.models.user import UserSchema
from ..models.common_model import ErrorResponseModel, ResponseModel
from ..services.user_service import get_all_users

router = APIRouter()


@router.get("", response_description="Retrieve all users")
async def get_all_users_data():
    users = get_all_users()
    return ResponseModel(users, "Get all users successfuly")
