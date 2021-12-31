from ..config.database import user_collection
from ..schemas.user import user_entity


def get_all_users():
    users = []
    for user in user_collection.find():
        users.append(user_entity(user))
    return users


def get_user_by_username(username: str):
    return user_collection.find_one({username})
