from os import path, remove, getcwd
from time import time
from typing import List

from bson import ObjectId

from ..common.database import image_collection
from ..common.utils import current_timestamp
from ..schemas.image_schema import image_entities, image_entity
from ..schemas.user_schema import UserDto


def generate_url(file_name):
    return f"http://localhost:8000/public/{file_name}"


def generate_filename(file_path):
    base = path.basename(file_path)
    return (
        f"{path.splitext(base)[0]}-{str(current_timestamp())}{path.splitext(base)[1]}"
    )


def create_image(file_path: str, user: UserDto) -> dict:
    saved_image = {
        "url": file_path,
        "created_by_id": ObjectId(user["id"]),
        "created_at": current_timestamp(),
    }
    image_id = image_collection.insert_one(saved_image).inserted_id
    cursor = image_collection.find_one({"_id": image_id})
    return image_entity(cursor)


def get_image_by_creator(creator_id: str) -> list:
    images = []
    for image in image_collection.find({"created_by_id": ObjectId(creator_id)}):
        images.append(image)
    return image_entities(images)


def delete_images(id_list: List[str]):
    images_cursor = image_collection.find(
        {"_id": {"$in": [ObjectId(id) for id in id_list]}}
    )
    for image in images_cursor:
        file_name = path.basename(image["url"])
        file_path = path.join(getcwd(), "public", file_name)
        remove(file_path)
    image_collection.delete_many({"_id": {"$in": [ObjectId(id) for id in id_list]}})
