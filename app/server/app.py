import traceback

from fastapi import FastAPI, Form
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.responses import Response

from .routes.auth_route import router as AuthRouter
from .routes.user_route import router as UserRouter
from .services.auth_service import jwt_authentication

app = FastAPI()

app.include_router(
    UserRouter,
    tags=["User"],
    prefix="/user",
    dependencies=[Depends(jwt_authentication)],
)
app.include_router(AuthRouter, tags=["Auth"], prefix="/auth")


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        traceback.print_exc()
        return Response("Internal server error", status_code=500)


app.middleware("http")(catch_exceptions_middleware)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
