from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.database import get_async_session
from auth.manager import get_user_manager
from benches.schemas import BenchCreate
from models.models import Bench, User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)

router = APIRouter(
        tags=["benches"]
)

@router.get("/benches")
async def get_benches(limit: int, offset: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Bench)
        result = await session.execute(query)
        return {"status": "success",
                "data": result.mappings().all()[offset:][:limit],
                "details": None}
    except:
        return {"status": "error"}

@router.get("/bench/{bench_id}")
async def get_bench(bench_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Bench).where(bench_id == Bench.id)
        result = await session.execute(query)
        bench = result.scalar_one_or_none()
        if bench is None:
            raise HTTPException(status_code=404, detail="bench not found )=")
        return {"status": "success",
                "data": bench,
                "details": None}
    except:
        return {"status": "error"}

@router.post("/bench/create")
async def create_bench(operation: BenchCreate, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    try:
        stmt = insert(Bench).values(**operation.model_dump(exclude={"creator_id"}), creator_id=user.id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    except:
        return {"status": "error"}