import traceback

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import Depends
from starlette.requests import Request
from starlette.responses import Response

from .routes.auth_route import router as AuthRouter
from .routes.image_route import router as ImageRouter
from .routes.user_route import router as UserRouter
from .routes.shared_image_route import router as SharedImageRouter
from .services.auth_service import jwt_authentication

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    UserRouter,
    tags=["User"],
    prefix="/user",
    dependencies=[Depends(jwt_authentication)],
)
app.include_router(AuthRouter, tags=["Auth"], prefix="/auth")
app.include_router(
    ImageRouter,
    tags=["Image"],
    prefix="/image",
    dependencies=[Depends(jwt_authentication)],
)
app.include_router(
    SharedImageRouter,
    tags=["Share image"],
    prefix="/shared-image",
    dependencies=[Depends(jwt_authentication)],
)

app.mount("/public", StaticFiles(directory="public"), name="public")


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
