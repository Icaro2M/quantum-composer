from pydantic import BaseModel


class ErrorResponseSchema(BaseModel):
    error: str
    message: str
    details: list[str] = []