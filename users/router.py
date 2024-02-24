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