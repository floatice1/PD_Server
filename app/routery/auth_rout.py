"""Router FastAPI do obsługi uwierzytelniania użytkowników."""

from typing import Annotated, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.serwisy.uzytkownik_serw import SerwisUzytkownikow
from app.modele.uzytkownik import UzytkownikLogin

router = APIRouter(
    prefix="/auth",
    tags=["autentykacja"],
    responses={401: {"description": "Nieautoryzowany dostęp"}}
)

class TokenResponse(BaseModel):
    """Model odpowiedzi zawierający token JWT."""
    token: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> Dict[str, Any]:
    """
    Pobiera aktualnie zalogowanego użytkownika na podstawie tokenu JWT.

    Args:
        token: Token JWT z nagłówka autoryzacji.

    Returns:
        Słownik zawierający dane użytkownika.

    Raises:
        HTTPException: Jeśli token jest nieprawidłowy lub użytkownik nie istnieje.
    """
    user = await SerwisUzytkownikow.weryfikuj_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowe dane uwierzytelniające",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/login", response_model=TokenResponse)
async def login(dane_logowania: Annotated[UzytkownikLogin, Body()]):
    """
    Endpoint do logowania użytkownika.

    Args:
        dane_logowania: Obiekt zawierający email i hasło użytkownika.

    Returns:
        Token JWT po udanym uwierzytelnieniu.

    Raises:
        HTTPException: Jeśli email lub hasło są nieprawidłowe.
    """
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

@router.get("/me", response_model=Dict[str, Any])
async def read_users_me(current_user: Annotated[Dict[str, Any], Depends(get_current_user)]):
    """
    Pobiera dane aktualnie zalogowanego użytkownika.

    Args:
        current_user: Dane aktualnie zalogowanego użytkownika (uzyskane z zależności).

    Returns:
        Słownik zawierający dane użytkownika.
    """
    return current_user
    