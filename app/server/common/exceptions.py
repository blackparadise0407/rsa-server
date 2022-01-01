from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    def __init__(self, detail="Could not validate credentials"):
        self.detail = detail
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.headers = {"WWW-Authenticate": "Bearer"}


class BadRequestException(HTTPException):
    def __init__(self, detail="Bad request"):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail


class ForbiddenException(HTTPException):
    def __init__(self, detail="You have insufficient permissions"):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = detail


class NotFoundException(HTTPException):
    def __init__(self, detail="The requested resource is not available"):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = detail

