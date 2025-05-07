from fastapi import APIRouter, Path, Body, HTTPException, status
from typing import Annotated, Dict, Any
from app.serwisy.uzytkownik import SerwisUzytkownikow
from app.modele.uzytkownik import UzytkownikTworzenie

router = APIRouter(
    prefix="/uzytkowniki",
    tags=["dziekanat - uzytkowniki"],
    responses={404: {"message": "Nie znaleziono"}, 403: {"message": "Brak dostępu"}}
)

@router.get("/", summary="Pobierz listę wszystkich użytkowników")
async def pobierz_wszystkich_uzytkownikow():
    try:
        return await SerwisUzytkownikow.pobierz_wszystkich_uzytkownikow()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas pobierania listy użytkowników: {str(e)}"
        )

@router.get("/{uzytkownik_id}", summary="Pobierz dane konkretnego użytkownika")
async def pobierz_uzytkownika(uzytkownik_id: Annotated[str, Path(title="UID użytkownika")]):
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
        )

@router.post("/", status_code=201, summary="Utwórz nowego użytkownika")
async def utworz_uzytkownika(dane_uzytkownika: Annotated[Dict[str, Any], Body()]):
    try:
        uzytkownik = UzytkownikTworzenie(**dane_uzytkownika)
        return await SerwisUzytkownikow.utworz_uzytkownika(uzytkownik)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Błąd podczas tworzenia użytkownika: {str(e)}"
        )

@router.put("/{uzytkownik_id}", summary="Zaktualizuj dane użytkownika")
async def aktualizuj_uzytkownika(uzytkownik_id: Annotated[str, Path(title="UID użytkownika")], dane_aktualizacji: Annotated[Dict[str, Any], Body()]):
    try:
        uzytkownik = UzytkownikTworzenie(**dane_aktualizacji)
        success = await SerwisUzytkownikow.aktualizuj_uzytkownika(uzytkownik_id, uzytkownik)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Użytkownik o ID {uzytkownik_id} nie został znaleziony"
            )
        return {"message": f"Użytkownik {uzytkownik_id} zaktualizowany pomyślnie"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Błąd podczas aktualizacji użytkownika: {str(e)}"
        )

@router.delete("/{uzytkownik_id}", summary="Usuń użytkownika")
async def usun_uzytkownika(uzytkownik_id: Annotated[str, Path(title="UID użytkownika")]):
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
        )