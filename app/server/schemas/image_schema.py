from pydantic import BaseModel, validator


class CreateImageDto(BaseModel):
    url: str
    created_by: str

    @validator("url")
    def url_not_empty(cls, v: str):
        if not v:
            raise ValueError("Url is required")
        return v
