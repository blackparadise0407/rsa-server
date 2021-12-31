from ..config.database import user_collection


async def get_all_users():
    users = []
    for user in user_collection.find():
        print(user)
        users.append({"username": user["username"], "password": user["password"]})
    return users
