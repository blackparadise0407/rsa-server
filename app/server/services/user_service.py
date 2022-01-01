from bson.objectid import ObjectId
from ..common.database import user_collection
from ..schemas.user_schema import user_entity


def get_all_users():
    users = []
    for user in user_collection.find():
        users.append(user_entity(user))
    return users


def get_user_by_username(username: str):
    return user_collection.find_one({"username": username})


def get_user_by_id(id: str):
    parsed_id = id
    if type(id) is not ObjectId:
        parsed_id = ObjectId(id)
    return user_collection.find_one({"_id": parsed_id})
