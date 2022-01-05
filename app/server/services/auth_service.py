import random
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from ..common.database import user_collection
from ..common.exceptions import BadRequestException, UnauthorizedException
from ..common.rsa import RSA
from ..common.utils import hex_to_bin
from ..schemas.auth_schema import LoginDto, RegisterDto
from ..schemas.user_schema import user_entity
from .user_service import get_user_by_id, get_user_by_username

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = ACCESS_TOKEN_EXPIRE_MINUTES
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_user_with_credentials(data: LoginDto):
    user = get_user_by_username(data.username)
    if not user:
        raise BadRequestException(detail="User not found")
    if user["username"] != data.username:
        raise BadRequestException(detail="Invalid credentials")
    if not verify_password(data.password, user["password"]):
        raise BadRequestException(detail="Invalid credentials")
    return create_access_token({"sub": str(user["_id"])})


def create_user_with_encryption(data: RegisterDto) -> str:
    user = get_user_by_username(data.username)
    if user:
        raise BadRequestException(detail="User already exists")
    hashed_password = get_password_hash(data.password)
    exponent, pem, pub = RSA.gen_key_pair()
    encrypted_sym_key = hex(
        int(RSA.encrypt(hex_to_bin(generate_random_sym_key()[2:]), pub, exponent), 2)
    )
    saved_user = {
        "username": data.username,
        "password": hashed_password,
        "sym_key": encrypted_sym_key,
        "pub": f"{exponent}.{pub}",
        "pem": f"{exponent}.{pem}",
    }
    user_collection.insert_one(saved_user).inserted_id
    return "Register successfully"


def jwt_authentication(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException()
    except ExpiredSignatureError:
        raise UnauthorizedException(detail="Token expired")
    except JWTError:
        raise UnauthorizedException()
    user = get_user_by_id(user_id)
    if user is None:
        raise UnauthorizedException()
    return user_entity(user)


def generate_random_sym_key() -> str:
    return hex(random.getrandbits(128))
