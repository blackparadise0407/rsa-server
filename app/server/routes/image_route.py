from os import getcwd, path

from aiofiles import open
from fastapi import APIRouter, Body, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends

from ..common.database import user_collection
from ..schemas.user_schema import UserDto
from ..services.auth_service import jwt_authentication
from ..services.image_service import create_image, generate_filename

router = APIRouter()


@router.get("/me", response_description="Retrieve all current's images")
async def get_all_image_of_user():
    return "Ok"


@router.post("", response_description="Upload an image")
async def upload_image(
    user: UserDto = Depends(jwt_authentication), file: UploadFile = File(...)
):
    file_path = path.join(getcwd(), "public", generate_filename(file.filename))
    async with open(file_path, "wb") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
    create_image(file_path, user)
    return "ok"
