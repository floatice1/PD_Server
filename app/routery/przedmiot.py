"""Moduł zawierający routery dla zarządzania przedmiotami."""

from typing import Annotated, Dict, Any

from fastapi import APIRouter, Path, Body, HTTPException, status

from app.serwisy.przedmiot import SerwisPrzedmiotow
from app.modele.przedmiot import PrzedmiotTworzenie

router = APIRouter(
    prefix="/przedmioty",
    tags=["przedmioty"],
    responses={
        404: {"message": "Nie znaleziono"},
        403: {"message": "Brak dostępu"},
        400: {"message": "Błąd danych"}
    }
)


@router.get("/", summary="Pobierz listę wszystkich przedmiotów")
async def pobierz_wszystkie_przedmioty():
    """Pobiera listę wszystkich przedmiotów."""
    try:
        return await SerwisPrzedmiotow.pobierz_wszystkie_przedmioty()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas pobierania listy przedmiotów: {str(e)}"
        ) from e


@router.get("/{przedmiot_id}", summary="Pobierz dane konkretnego przedmiotu")
async def pobierz_przedmiot(
    przedmiot_id: Annotated[str, Path(title="ID przedmiotu")]
):
    """Pobiera dane konkretnego przedmiotu na podstawie jego ID."""
    try:
        przedmiot = await SerwisPrzedmiotow.pobierz_przedmiot_po_id(przedmiot_id)
        if not przedmiot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Przedmiot o ID {przedmiot_id} nie został znaleziony"
            )
        return przedmiot
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas pobierania przedmiotu: {str(e)}"
        ) from e


@router.post("/", status_code=201, summary="Utwórz nowy przedmiot")
async def utworz_przedmiot(
    dane_przedmiotu: PrzedmiotTworzenie
):
    """Tworzy nowy przedmiot."""
    try:
        return await SerwisPrzedmiotow.utworz_przedmiot(dane_przedmiotu)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas tworzenia przedmiotu: {str(e)}"
        ) from e


@router.put("/{przedmiot_id}", summary="Zaktualizuj dane przedmiotu")
async def aktualizuj_przedmiot(
    przedmiot_id: Annotated[str, Path(title="ID przedmiotu")],
    dane_aktualizacji: Annotated[Dict[str, Any], Body()]
):
    """Aktualizuje dane przedmiotu na podstawie jego ID."""
    try:
        zaktualizowany_przedmiot = await SerwisPrzedmiotow.aktualizuj_przedmiot(
            przedmiot_id, dane_aktualizacji
        )
        if not zaktualizowany_przedmiot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Przedmiot o ID {przedmiot_id} nie istnieje"
            )
        return {"message": f"Przedmiot {przedmiot_id} zaktualizowany pomyślnie",
                "updated_data": zaktualizowany_przedmiot}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas aktualizacji przedmiotu: {str(e)}"
        ) from e


@router.delete("/{przedmiot_id}", summary="Usuń przedmiot")
async def usun_przedmiot(
    przedmiot_id: Annotated[str, Path(title="ID przedmiotu")]
):
    """Usuwa przedmiot na podstawie jego ID."""
    try:
        success = await SerwisPrzedmiotow.usun_przedmiot(przedmiot_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Przedmiot o ID {przedmiot_id} nie został znaleziony"
            )
        return {"message": f"Przedmiot {przedmiot_id} usunięty pomyślnie"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas usuwania przedmiotu: {str(e)}"
        ) from e
