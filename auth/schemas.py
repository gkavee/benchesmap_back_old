from fastapi_users import schemas
from fastapi_users.schemas import PYDANTIC_V2


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdate(schemas.BaseUserUpdate):
    email: str
    password: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False