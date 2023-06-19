from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str

class LogRequest(BaseModel):
    input: str

class Post(BaseModel):
    id: Optional[UUID]
    title: str
    description: str

    class Config:
        orm_mode = True


class DeletePostResponse(BaseModel):
    detail: str


class UpdatePost(BaseModel):
    id: UUID
    title: str
    description: str

    class Config:
        orm_mode = True


class PrecomputeSearchInput(BaseModel):
    latitude: float
    longitude: float
    magnitude: float
    class Config:
        orm_mode = True

class PrecomputeSearchResponse(BaseModel):
    latitude: float
    longitude: float
    magnitude: float
    image: str  = None
    location: str = None
    name: str = None
    description: str = None
    status: bool

class Log(BaseModel):
    id: Optional[UUID]
    title: str
    description: str

    class Config:
        orm_mode = True


class LogResponse(BaseModel):
    status: str  = "Ok"

class logInput(BaseModel):
    timestamp: str  = None
    component: str  = None
    loglevel: str  = None
    transaction_id: str  = None
    message: str  = None
    class Config:
        orm_mode = True