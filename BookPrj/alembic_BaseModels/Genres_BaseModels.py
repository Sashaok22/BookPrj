from typing import Optional
from pydantic import BaseModel, Field


class GenresSchema(BaseModel):
    id: Optional[int]
    genre_name: str = Field(..., min_length=2)
    short_description: str = Field(..., min_length=2)

    class Config:
        orm_mode = True