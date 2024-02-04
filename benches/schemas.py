from pydantic import BaseModel


class BenchCreate(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    creator_id: int
