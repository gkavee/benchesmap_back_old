from pydantic import BaseModel


class BenchCreate(BaseModel):
    name: str
    latitude: float
    longitude: float

