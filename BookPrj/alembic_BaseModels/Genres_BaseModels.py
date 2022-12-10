from typing import Optional
from pydantic import BaseModel, Field


# Genres BaseModel, required for validate the data of the added genre
class GenreSchema(BaseModel):
    _id: Optional[int] = Field(description="Genre id field")
    genre_name: str = Field(..., min_length=2, max_length=50, description="Genre name field")
    short_description: str = Field(..., min_length=2, max_length=50, description="Genre short description field")

    class Config:
        orm_mode = True


# Genres BaseModel, required for validation and submission of the list of genres
class GenresSchema(BaseModel):
    genres: Optional[list[GenreSchema]] = Field(description="List of models of genres")

    class Config:
        orm_mode = True

