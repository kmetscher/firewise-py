from fastapi import FastAPI
from pydantic import BaseModel

class SubmittedFire(BaseModel):
    latitude: float
    longitude: float
    size: float
    discovery_timestamp: int
    containment_timestamp: int

server = FastAPI()

@server.get("/")
async def root():
    return {"message": "Howdy!"}
