from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session
from models.models import User

router = APIRouter(
        tags=["users"]
)

@router.get("/users")
async def get_users(limit: int, offset: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(User)
        result = await session.execute(query)
        return {"status": "success",
                "data": result.mappings().all()[offset:][:limit],
                "details": None}
    except Exception:
        return {"status": "error"}

@router.get("/user/{user_username}")
async def get_user(user_username: str, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(user_username == User.username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found )=")
    return user