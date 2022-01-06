from pydantic import BaseModel, validator


def image_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "url": item["url"],
        "created_by_id": str(item["created_by_id"]),
        "created_at": str(item["created_at"]),
        "blob": str(item.get("blob", "")),
        "created_by": item.get("created_by"),
    }


def image_entities(entities) -> list:
    return [image_entity(item) for item in entities]


class CreateImageDto(BaseModel):
    url: str
    created_by_id: str

    @validator("url")
    def url_not_empty(cls, v: str):
        if not v:
            raise ValueError("Url is required")
        return v


class ImageDto(BaseModel):
    id: str
    url: str
    created_by_id: str
    created_at: int
    blob: str
    created_by: dict
