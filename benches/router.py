from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy import select, insert, func
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

@router.get("/nearest_bench/")
async def get_nearest_bench(latitude: float, longitude: float, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Bench).order_by(
    func.pow(Bench.latitude - latitude, 2) + func.pow(Bench.longitude - longitude, 2)
    ))
    nearest_point = result.scalars().first()

    return {'latitude': nearest_point.latitude, 'longitude': nearest_point.longitude}

@router.post("/bench/create")
async def create_bench(operation: BenchCreate, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    try:
        stmt = insert(Bench).values(**operation.model_dump(exclude={"creator_id"}), creator_id=user.id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    except:
        return {"status": "error"}