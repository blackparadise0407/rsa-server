from pydantic import BaseModel, validator


def shared_image_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "shared_by_id": str(item["shared_by_id"]),
        "shared_to_id": str(item["shared_to_id"]),
        "image_id": str(item["image_id"]),
    }


def shared_image_entities(entities) -> list:
    return [shared_image_entity(item) for item in entities]


class CreateSharedImageDto(BaseModel):
    shared_to_id: str
    image_id: str

    @validator("image_id")
    def image_id_not_empty(cls, v: str):
        if not v:
            raise ValueError("Image id is required")
        return v

    @validator("shared_to_id")
    def shared_to_id_not_empty(cls, v: str):
        if not v:
            raise ValueError("Shared to user id is required")
        return v


class SharedImageDto(BaseModel):
    id: str
    shared_by_id: str
    shared_to_id: str
    image_id: str
