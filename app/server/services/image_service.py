from base64 import b64encode
from os import getcwd, path, remove
from typing import List

from bson import ObjectId
from pydantic.utils import Obj

from ..common.aes import AES128
from ..common.database import image_collection, shared_image_collection, user_collection
from ..common.utils import current_timestamp, get_fdecrypted_sym_key
from ..schemas.image_schema import image_entities, image_entity
from ..schemas.user_schema import UserDto, user_entity
from ..common.exceptions import BadRequestException


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


def create_multiple_image(files: List[dict], user: UserDto):
    saved_images = []
    for file in files:
        saved_images.append(
            {
                "url": file["file_path"],
                "created_by_id": ObjectId(user["id"]),
                "created_at": current_timestamp(),
            }
        )
    image_collection.insert_many(saved_images)


def get_image_by_creator(user: UserDto) -> list:
    cursor = image_collection.find({"created_by_id": ObjectId(user["id"])})
    if cursor.count() == 0:
        return []
    decrypted_sym_key = get_fdecrypted_sym_key(user["pem"], user["sym_key"])
    # Init aes instance
    aes = AES128(bytes.fromhex(decrypted_sym_key))
    images = []
    found_user_dict = {}

    for image in cursor:
        created_by_id = str(image["created_by_id"])
        found_user = found_user_dict.get(created_by_id)
        if found_user is None:
            found_user = user_collection.find_one({"_id": ObjectId(created_by_id)})
            formatted_user = {
                "id": str(found_user["_id"]),
                "username": found_user["username"],
            }
            found_user_dict[created_by_id] = formatted_user
            found_user = formatted_user

        filename = get_filename_from_path(image["url"])
        file_path = get_public_file_absolute_path(filename)
        in_file = open(file_path, "rb")
        raw = in_file.read()
        decrypted = aes.decrypt(raw)
        image["blob"] = str(b64encode(decrypted), "utf-8")
        image["created_by"] = found_user
        images.append(image)

    return image_entities(images)


def get_shared_image_of_user(user: UserDto) -> list:
    cursor = shared_image_collection.find({"shared_to_id": ObjectId(user["id"])})
    if cursor.count() == 0:
        return []
    images = []
    found_user_dict = {}

    for shared_image in cursor:
        shared_by = user_collection.find_one({"_id": shared_image["shared_by_id"]})
        decrypted_sym_key = get_fdecrypted_sym_key(
            shared_by["pem"], shared_by["sym_key"]
        )
        aes = AES128(bytes.fromhex(decrypted_sym_key))
        image = image_collection.find_one({"_id": shared_image["image_id"]})
        if image:
            created_by_id = str(image["created_by_id"])
            found_user = found_user_dict.get(created_by_id)
            if found_user is None:
                found_user = user_collection.find_one({"_id": ObjectId(created_by_id)})
                formatted_user = {
                    "id": str(found_user["_id"]),
                    "username": found_user["username"],
                }
                found_user_dict[created_by_id] = formatted_user
                found_user = formatted_user
            filename = get_filename_from_path(image["url"])
            file_path = get_public_file_absolute_path(filename)
            in_file = open(file_path, "rb")
            raw = in_file.read()
            decrypted = aes.decrypt(raw)
            image["blob"] = str(b64encode(decrypted), "utf-8")
            image["created_by"] = found_user
            images.append(image)

    return image_entities(images)


def delete_images(id_list: List[str], user: UserDto):
    images_cursor = image_collection.find(
        {"_id": {"$in": [ObjectId(id) for id in id_list]}}
    )
    delete_ids = []
    for image in images_cursor:
        if str(image["created_by_id"]) == user["id"]:
            shared_image_collection.delete_one({"image_id": image["_id"]})
            delete_ids.append(str(image["_id"]))
            file_name = get_filename_from_path(image["url"])
            file_path = path.join(getcwd(), "public", file_name)
            remove(file_path)
    image_collection.delete_many({"_id": {"$in": [ObjectId(id) for id in delete_ids]}})


def encrypt_image(file_path: str, key: str):
    # Init aes instance
    aes = AES128(bytes.fromhex(key))
    # read binary file from path
    in_file = open(file_path, "rb")
    raw = in_file.read()
    encrypted = aes.encrypt(raw)
    out_file = open(file_path, "wb+")
    out_file.write(encrypted)
    out_file.close()


def get_public_file_absolute_path(filename: str) -> str:
    return path.join(getcwd(), "public", filename)


def get_filename_from_path(file_path: str) -> str:
    return path.basename(file_path)
