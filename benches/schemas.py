from pydantic import BaseModel

class Bench(BaseModel):
    name: str
    description: str | None
    count: int
    latitude: float
    longitude: float

class BenchCreate(Bench):
    pass

