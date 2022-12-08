from typing import Optional
from pydantic import BaseModel, Field


class GenresSchema(BaseModel):
    _id: Optional[int] = Field(description="Genre id field")
    genre_name: str = Field(..., min_length=2, description="Genre name field")
    short_description: str = Field(..., min_length=2, description="Genre short description field")

    class Config:
        orm_mode = True
