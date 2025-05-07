from fastapi import APIRouter, Path, Body
from typing import Dict, Any

router = APIRouter(
    prefix="/wykladowca/oceny",
    tags=["wykladowca - oceny"],
    responses={404: {"message": "Nie znaleziono"}, 403: {"message": "Brak dostępu"}}
)

@router.post("/", status_code=201, summary="Utwórz nową ocenę")
async def utworz_ocene(dane_oceny: Dict[str, Any] = Body()):
    return {"message": "Ocena utworzona pomyślnie (symulacja dla Wykładowcy).", "received_data": dane_oceny}

@router.put("/{ocena_id}", summary="Zaktualizuj swoją ocenę")
async def aktualizuj_ocene(ocena_id: str = Path(title="ID oceny"), dane_aktualizacji: Dict[str, Any] = Body()):
    return {"message": f"Ocena {ocena_id} zaktualizowana pomyślnie (symulacja dla Wykładowcy).", "received_data": dane_aktualizacji}