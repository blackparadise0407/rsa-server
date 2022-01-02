from os import path
from time import time

from ..schemas.image_schema import CreateImageDto
from ..schemas.user_schema import UserDto
from ..common.database import image_collection


def generate_filename(file_path):
    base = path.basename(file_path)
    return (
        f"{path.splitext(base)[0]}-{str(round(time() * 1000))}{path.splitext(base)[1]}"
    )


def create_image(file_path: str, user: UserDto):
    saved_image = {"url": file_path, "created_by": user["id"]}
    image_id = image_collection.insert_one(saved_image).inserted_id
    return image_collection.find_one({"_id": image_id})

