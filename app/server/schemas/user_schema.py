from pydantic import BaseModel


def user_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "username": str(item["username"]),
        "sym_key": str(item["sym_key"]),
        "pub": str(item["pub"]),
        "pem": str(item["pem"]),
    }


def user_entities(entities) -> list:
    return [user_entity(item) for item in entities]


class UserDto(BaseModel):
    id: str
    username: str
    sym_key: str
    pub: str
    pem: str
