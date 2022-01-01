from pydantic import BaseModel
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {"user": {"username": "John Doe", "password": "abc123",}}

