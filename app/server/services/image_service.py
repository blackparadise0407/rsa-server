from base64 import b64encode
from os import getcwd, path, remove
from typing import List

from bson import ObjectId

from ..common.aes import AES128
from ..common.database import image_collection
from ..common.utils import current_timestamp, get_fdecrypted_sym_key
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
    return "Upload image successfully"


def get_image_by_creator(user: UserDto) -> list:
    cursor = image_collection.find({"created_by_id": ObjectId(user["id"])})
    if cursor.count() == 0:
        return []
    decrypted_sym_key = get_fdecrypted_sym_key(user["pem"], user["sym_key"])
    # Init aes instance
    aes = AES128(bytes.fromhex(decrypted_sym_key))
    images = []
    for image in cursor:
        images.append(image)
        filename = get_filename_from_path(image["url"])
        file_path = get_public_file_absolute_path(filename)
        in_file = open(file_path, "rb")
        raw = in_file.read()
        decrypted = aes.decrypt(raw)
        image["blob"] = str(b64encode(decrypted), "utf-8")

    return image_entities(images)


def delete_images(id_list: List[str]):
    images_cursor = image_collection.find(
        {"_id": {"$in": [ObjectId(id) for id in id_list]}}
    )
    for image in images_cursor:
        file_name = get_filename_from_path(image["url"])
        file_path = path.join(getcwd(), "public", file_name)
        remove(file_path)
    image_collection.delete_many({"_id": {"$in": [ObjectId(id) for id in id_list]}})


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
