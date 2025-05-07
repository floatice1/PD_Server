from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(
    prefix="/wykladowca/ja",
    tags=["wykladowca - ja"],
    responses={403: {"message": "Brak dostępu"}}
)

@router.get("/", summary="Pobierz dane profilowe")
async def pobierz_dane_profilowe():
    return {"message": "Pobieranie profilu bieżącego wykładowcy (symulacja)."}