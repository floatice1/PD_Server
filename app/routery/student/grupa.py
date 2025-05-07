from fastapi import APIRouter, Path

router = APIRouter(
    prefix="/student/grupy",
    tags=["student - grupy"],
    responses={404: {"message": "Nie znaleziono"}, 403: {"message": "Brak dostępu"}}
)

@router.get("/", summary="Pobierz listę grup, do których jest przypisany")
async def pobierz_grupy():
    return {"message": "Lista grup przypisanych do studenta (symulacja)."}

@router.get("/{grupa_id}", summary="Pobierz szczegóły grupy, do której jest przypisany")
async def pobierz_szczegoly_grupy(grupa_id: str = Path(title="ID grupy")):
    return {"message": f"Pobieranie szczegółów grupy {grupa_id} (symulacja dla Studenta)."}