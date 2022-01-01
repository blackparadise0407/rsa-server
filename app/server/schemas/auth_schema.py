from pydantic import BaseModel, validator


class TokenData(BaseModel):
    access_token: str
    token_type: str


class LoginDto(BaseModel):
    username: str
    password: str

    @validator("username")
    def username_not_empty(cls, v: str):
        if not v:
            raise ValueError("Username is required")
        return v

    @validator("password")
    def password_not_empty(cls, v: str):
        if not v:
            raise ValueError("Password is required")
        return v


class RegisterDto(BaseModel):
    username: str
    password: str

    @validator("username")
    def username_not_empty(cls, v: str):
        if not v:
            raise ValueError("Username is required")
        if len(v) > 255:
            raise ValueError("Username must be less than 255 characters")
        return v

    @validator("password")
    def password_not_empty(cls, v: str):
        if not v:
            raise ValueError("Password is required")
        return v
