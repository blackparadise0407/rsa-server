from bson import ObjectId

from ..common.database import image_collection, shared_image_collection, user_collection
from ..common.exceptions import BadRequestException
from ..schemas.shared_image_schema import CreateSharedImageDto


def create_shared_image(current_user_id: str, payload: CreateSharedImageDto):
    shared_by_id = current_user_id
    shared_to_id = payload.shared_to_id
    image_id = payload.image_id
    if shared_by_id == shared_to_id:
        raise BadRequestException("Cannot share to own")

    if not ObjectId.is_valid(shared_to_id):
        raise BadRequestException("Shared-to user id is not valid")

    exist_shared_to = user_collection.find_one({"_id": ObjectId(shared_to_id)})
    if exist_shared_to is None:
        raise BadRequestException("Shared-to user is not available")

    exist_image = image_collection.find_one({"_id": ObjectId(image_id)})
    if exist_image is None:
        raise BadRequestException("Shared image is not available")

    shared_image = {
        "shared_by_id": ObjectId(shared_by_id),
        "shared_to_id": ObjectId(shared_to_id),
        "image_id": ObjectId(image_id),
    }

    exist_shared_image = shared_image_collection.find_one(shared_image)
    if exist_shared_image:
        raise BadRequestException("Image is already shared to this user")
    shared_image_collection.insert_one(shared_image)

