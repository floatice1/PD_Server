from fastapi import APIRouter

router = APIRouter(
    prefix="/student/oceny",
    tags=["student - oceny"],
    responses={403: {"message": "Brak dostępu"}}
)

@router.get("/", summary="Pobierz swoje oceny")
async def pobierz_oceny():
    return {"message": "Lista ocen bieżącego studenta (symulacja)."}