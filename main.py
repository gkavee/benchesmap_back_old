from fastapi import FastAPI, Depends
from fastapi_users import fastapi_users, FastAPIUsers
from fastapi.responses import HTMLResponse

from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from fastapi.middleware.cors import CORSMiddleware

from benches.router import router as benches_router
from users.router import router as users_router

app = FastAPI(
    title='asdasddsadss'
)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(benches_router)
app.include_router(users_router)