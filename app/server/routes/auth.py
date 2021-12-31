from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

# from app.server.models.user import UserSchema
from ..models.common import ResponseModel, ErrorResponseModel
from ..services.auth import create_access_token

router = APIRouter()


@router.get("/", response_description="Retrieve current user")
def get_current_user_data():
    print(create_access_token({"sub": "Kyle"}))
    return ResponseModel({}, "Get all users successfuly")
