from pydantic import BaseModel
from enum import Enum

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenDane(BaseModel):
    email: str | None = None
    uid: str | None = None
    rola: Rola | None = None