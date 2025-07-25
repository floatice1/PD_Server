"""Moduł zawierający routery dla zarządzania użytkownikami."""

from typing import Annotated, Dict, Any

from fastapi import APIRouter, Path, Body, HTTPException, status

from app.serwisy.uzytkownik_serw import SerwisUzytkownikow
from app.modele.uzytkownik import UzytkownikTworzenie, UzytkownikAktualizacja

router = APIRouter(
    prefix="/uzytkownicy",
    tags=["uzytkownicy"],
    responses={
        404: {"message": "Nie znaleziono"},
        403: {"message": "Brak dostępu"},
        400: {"message": "Błąd danych"}
    }
)


@router.get("/", summary="Pobierz listę wszystkich użytkowników")
async def pobierz_wszystkich_uzytkownikow():
    """Pobiera listę wszystkich użytkowników."""
    try:
        return await SerwisUzytkownikow.pobierz_wszystkich_uzytkownikow()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas pobierania listy użytkowników: {str(e)}"
        ) from e


@router.get("/{uzytkownik_id}", summary="Pobierz dane konkretnego użytkownika")
async def pobierz_uzytkownika(
    uzytkownik_id: Annotated[str, Path(title="ID użytkownika")]
):
    """Pobiera dane konkretnego użytkownika na podstawie jego ID."""
    try:
        uzytkownik = await SerwisUzytkownikow.pobierz_uzytkownika_po_id(uzytkownik_id)
        if not uzytkownik:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Użytkownik o ID {uzytkownik_id} nie został znaleziony"
            )
        return uzytkownik
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas pobierania użytkownika: {str(e)}"
        ) from e


@router.post("/", status_code=201, summary="Utwórz nowego użytkownika")
async def utworz_uzytkownika(
    dane_uzytkownika: Annotated[Dict[str, Any], Body()]
):
    """Tworzy nowego użytkownika."""
    try:
        uzytkownik = UzytkownikTworzenie(**dane_uzytkownika)
        return await SerwisUzytkownikow.utworz_uzytkownika(uzytkownik)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas tworzenia użytkownika: {str(e)}"
        ) from e


@router.put("/{uzytkownik_id}", summary="Zaktualizuj dane użytkownika")
async def aktualizuj_uzytkownika(
    uzytkownik_id: Annotated[str, Path(title="ID użytkownika")],
    dane_aktualizacji: Annotated[UzytkownikAktualizacja, Body()]
):
    """Aktualizuje dane użytkownika na podstawie jego ID."""
    try:
        zaktualizowany_uzytkownik = await SerwisUzytkownikow.aktualizuj_uzytkownika(
            uzytkownik_id, dane_aktualizacji.model_dump(exclude_unset=True)
        )
        if not zaktualizowany_uzytkownik:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Użytkownik o ID {uzytkownik_id} nie istnieje"
            )
        return {"message": f"Użytkownik {uzytkownik_id} zaktualizowany pomyślnie",
                "updated_data": zaktualizowany_uzytkownik}
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        ) from ve
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas aktualizacji użytkownika: {str(e)}"
        ) from e


@router.delete("/{uzytkownik_id}", summary="Usuń użytkownika")
async def usun_uzytkownika(
    uzytkownik_id: Annotated[str, Path(title="ID użytkownika")]
):
    """Usuwa użytkownika na podstawie jego ID."""
    try:
        success = await SerwisUzytkownikow.usun_uzytkownika(uzytkownik_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Użytkownik o ID {uzytkownik_id} nie został znaleziony"
            )
        return {"message": f"Użytkownik {uzytkownik_id} usunięty pomyślnie"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Błąd podczas usuwania użytkownika: {str(e)}"
        ) from e
