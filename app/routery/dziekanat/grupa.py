from fastapi import APIRouter, Path, Body, HTTPException, status
from typing import Annotated, Dict, Any
from app.serwisy.grupa import SerwisGrup
from app.modele.grupa import GrupaTworzenie

router = APIRouter(
    prefix="/grupy",
    tags=["dziekanat - grupy"],
    responses={404: {"message": "Nie znaleziono"}, 403: {"message": "Brak dostępu"}}
)

@router.get("/", summary="Pobierz listę wszystkich grup")
async def pobierz_wszystkie_grupy():
    try:
        return await SerwisGrup.pobierz_wszystkie_grupy()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas pobierania listy grup: {str(e)}"
        )

@router.get("/{grupa_id}", summary="Pobierz dane konkretnej grupy")
async def pobierz_grupe(grupa_id: Annotated[str, Path(title="ID grupy")]):
    try:
        grupa = await SerwisGrup.pobierz_grupe_po_id(grupa_id)
        if not grupa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grupa o ID {grupa_id} nie została znaleziona"
            )
        return grupa
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas pobierania grupy: {str(e)}"
        )

@router.post("/", status_code=201, summary="Utwórz nową grupę")
async def utworz_grupe(dane_grupy: Annotated[Dict[str, Any], Body()]):
    try:
        grupa = GrupaTworzenie(**dane_grupy)
        return await SerwisGrup.utworz_grupe(grupa)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Błąd podczas tworzenia grupy: {str(e)}"
        )

@router.put("/{grupa_id}", summary="Zaktualizuj dane grupy")
async def aktualizuj_grupe(grupa_id: Annotated[str, Path(title="ID grupy")], dane_aktualizacji: Annotated[Dict[str, Any], Body()]):
    try:
        grupa = GrupaTworzenie(**dane_aktualizacji)
        success = await SerwisGrup.aktualizuj_grupe(grupa_id, grupa)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grupa o ID {grupa_id} nie została znaleziona"
            )
        return {"message": f"Grupa {grupa_id} zaktualizowana pomyślnie"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Błąd podczas aktualizacji grupy: {str(e)}"
        )

@router.delete("/{grupa_id}", summary="Usuń grupę")
async def usun_grupe(grupa_id: Annotated[str, Path(title="ID grupy")]):
    try:
        success = await SerwisGrup.usun_grupe(grupa_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grupa o ID {grupa_id} nie została znaleziona"
            )
        return {"message": f"Grupa {grupa_id} usunięta pomyślnie"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Błąd podczas usuwania grupy: {str(e)}"
        )

@router.post("/{grupa_id}/studenci/{student_id}", summary="Przypisz studenta do grupy")
async def przypisz_studenta_do_grupy(
    grupa_id: Annotated[str, Path(title="ID grupy")],
    student_id: Annotated[str, Path(title="ID studenta")]
):
    try:
        success = await SerwisGrup.przypisz_studenta_do_grupy(grupa_id, student_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grupa o ID {grupa_id} nie została znaleziona"
            )
        return {"message": f"Student {student_id} przypisany do grupy {grupa_id} pomyślnie"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Błąd podczas przypisywania studenta do grupy: {str(e)}"
        )

@router.delete("/{grupa_id}/studenci/{student_id}", summary="Usuń studenta z grupy")
async def usun_studenta_z_grupy(grupa_id: Annotated[str, Path(title="ID grupy")], student_id: Annotated[str, Path(title="UID studenta")]):
    try:
        success = await SerwisGrup.usun_studenta_z_grupy(grupa_id, student_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grupa o ID {grupa_id} nie została znaleziona lub student nie jest przypisany do grupy"
            )
        return {"message": f"Student {student_id} usunięty z grupy {grupa_id} pomyślnie"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Błąd podczas usuwania studenta z grupy: {str(e)}"
        )

@router.put("/{grupa_id}/nauczyciel/{nauczyciel_id}", summary="Przypisz/zmień nauczyciela prowadzącego grupę")
async def przypisz_nauczyciela_do_grupy(
    grupa_id: Annotated[str, Path(title="ID grupy")],
    nauczyciel_id: Annotated[str, Path(title="ID nauczyciela")]
):
    try:
        success = await SerwisGrup.zmien_wykladowce_grupy(grupa_id, nauczyciel_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grupa o ID {grupa_id} nie została znaleziona"
            )
        return {"message": f"Nauczyciel {nauczyciel_id} przypisany do grupy {grupa_id} pomyślnie"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Błąd podczas przypisywania nauczyciela do grupy: {str(e)}"
        )