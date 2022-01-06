from os import getcwd, path
from typing import List

from aiofiles import open
from fastapi import APIRouter, File, UploadFile
from fastapi.param_functions import Depends
from pydantic import parse_obj_as

from ..schemas.image_schema import ImageDto
from ..schemas.user_schema import UserDto
from ..services.auth_service import jwt_authentication
from ..services.image_service import (
    create_image,
    delete_images,
    encrypt_image,
    generate_filename,
    generate_url,
    get_fdecrypted_sym_key,
    get_image_by_creator,
)

router = APIRouter()


@router.get(
    "/mine",
    response_description="Retrieve all current's images",
    response_model=List[ImageDto],
)
async def get_current_user_images(user: UserDto = Depends(jwt_authentication)):
    return parse_obj_as(List[ImageDto], get_image_by_creator(user))


@router.post("", response_description="Upload an image", response_model=ImageDto)
async def upload_image(
    user: UserDto = Depends(jwt_authentication), file: UploadFile = File(...)
):
    file_name = generate_filename(file.filename)
    url = generate_url(file_name)
    file_path = path.join(getcwd(), "public", generate_filename(file.filename))
    async with open(file_path, "wb") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
    decrypted_sym_key = get_fdecrypted_sym_key(user["pem"], user["sym_key"])
    encrypt_image(file_path, decrypted_sym_key)
    image = create_image(url, user)
    return ImageDto.parse_obj(image)


@router.delete("", response_model=str)
def delete_many_by_id(ids: List[str]):
    delete_images(ids)
    return "Delete image(s) successfully"
