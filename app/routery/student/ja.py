from fastapi import APIRouter

router = APIRouter(
    prefix="/student/ja",
    tags=["student - ja"],
    responses={403: {"message": "Brak dostępu"}}
)

@router.get("/", summary="Pobierz dane profilowe")
async def pobierz_dane_profilowe():
    return {"message": "Pobieranie profilu bieżącego studenta (symulacja)."}