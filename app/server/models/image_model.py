from pydantic import BaseModel
from pydantic import BaseModel, Field


class ImageSchema(BaseModel):
    url: str = Field(...)
    uploaded_by: str = Field(...)
