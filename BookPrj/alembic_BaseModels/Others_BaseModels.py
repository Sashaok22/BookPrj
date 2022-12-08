from pydantic import BaseModel, Field


# Class for displaying server responses.
class WebError(BaseModel):
    error_code: int = Field(..., description="Code of handled server response error")
    msg: str = Field(..., description="Message error")
