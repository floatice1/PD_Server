"""Modele danych dla tokenów autoryzacyjnych."""

from typing import Optional
from pydantic import BaseModel
from .uzytkownik import Rola

class Token(BaseModel):
    """Model danych reprezentujący token autoryzacyjny."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Model danych reprezentujący dane zawarte w tokenie."""
    email: Optional[str] = None
    rola: Optional[Rola] = None
