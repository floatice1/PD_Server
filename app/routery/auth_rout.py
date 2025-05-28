from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Dict, Any, Optional
from pydantic import BaseModel

from app.serwisy.uzytkownik_serw import SerwisUzytkownikow
from app.modele.uzytkownik import UzytkownikLogin

router = APIRouter(
    prefix="/auth",
    tags=["autentykacja"],
    responses={401: {"description": "Nieautoryzowany dostęp"}}
)

class TokenResponse(BaseModel):
    token: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/login", response_model=TokenResponse)
async def login(dane_logowania: Annotated[UzytkownikLogin, Body()]):
    user_data = await SerwisUzytkownikow.zaloguj_uzytkownika(dane_logowania)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowy email lub hasło",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "token": user_data.pop("token")
    }
