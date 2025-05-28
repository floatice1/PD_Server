"""Moduł zawierający routery dla zarządzania grupami."""

from typing import Annotated, Dict, Any

from fastapi import APIRouter, Path, Body, HTTPException, status

from app.serwisy.grupa_serw import SerwisGrup
from app.modele.grupa import GrupaAktualizacja, GrupaTworzenie

router = APIRouter(
    prefix="/grupy",
    tags=["grupy"],
    responses={
        404: {"message": "Nie znaleziono"},
        403: {"message": "Brak dostępu"},
        400: {"message": "Błąd danych"}
    }
)


@router.get("/", summary="Pobierz listę wszystkich grup")
async def pobierz_wszystkie_grupy():
    """Pobiera listę wszystkich grup."""
    try:
        return await SerwisGrup.pobierz_wszystkie_grupy()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas pobierania listy grup: {str(e)}"
        ) from e


@router.get("/{grupa_id}", summary="Pobierz dane konkretnej grupy")
async def pobierz_grupe(
    grupa_id: Annotated[str, Path(title="ID grupy")]
):
    """Pobiera dane konkretnej grupy na podstawie jej ID."""
    try:
        grupa = await SerwisGrup.pobierz_grupe_po_id(grupa_id)
        if not grupa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grupa o ID {grupa_id} nie została znaleziona"
            )
        return grupa
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas pobierania grupy: {str(e)}"
        ) from e


@router.post("/", status_code=201, summary="Utwórz nową grupę")
async def utworz_grupe(
    dane_grupy: GrupaTworzenie
):
    """Tworzy nową grupę."""
    try:
        return await SerwisGrup.utworz_grupe(dane_grupy)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas tworzenia grupy: {str(e)}"
        ) from e


@router.put("/{grupa_id}", summary="Zaktualizuj dane grupy")
async def aktualizuj_grupe(
    grupa_id: Annotated[str, Path(title="ID grupy")] ,
    dane_aktualizacji: Annotated[GrupaAktualizacja, Body()]
):
    """Aktualizuje dane grupy na podstawie jej ID."""
    try:
        update_data_dict = dane_aktualizacji.model_dump(exclude_unset=True)
        if not update_data_dict:
            raise ValueError("Nie podano danych do aktualizacji")

        zaktualizowana_grupa = await SerwisGrup.aktualizuj_grupe(
            grupa_id, update_data_dict
        )
        if not zaktualizowana_grupa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grupa o ID {grupa_id} nie istnieje"
            )
        return {"message": f"Grupa {grupa_id} zaktualizowana pomyślnie",
                "updated_data": zaktualizowana_grupa}
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        ) from ve
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas aktualizacji grupy: {str(e)}"
        ) from e


@router.delete("/{grupa_id}", summary="Usuń grupę")
async def usun_grupe(
    grupa_id: Annotated[str, Path(title="ID grupy do usunięcia")]
):
    """Usuwa grupę o podanym ID."""
    try:
        success = await SerwisGrup.usun_grupe(grupa_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grupa o ID {grupa_id} nie została znaleziona"
            )
        return {"message": f"Grupa {grupa_id} usunięta pomyślnie"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas usuwania grupy: {str(e)}"
        ) from e


@router.post("/{grupa_id}/studenci/{student_id}", summary="Przypisz studenta do grupy")
async def przypisz_studenta_do_grupy(
    grupa_id: Annotated[str, Path(title="ID grupy")],
    student_id: Annotated[str, Path(title="ID studenta")]
):
    """Przypisuje studenta do grupy."""
    try:
        success = await SerwisGrup.przypisz_studenta_do_grupy(grupa_id, student_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grupa o ID {grupa_id} nie została znaleziona"
            )
        return {"message": f"Student {student_id} przypisany do grupy {grupa_id} pomyślnie"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas przypisywania studenta do grupy: {str(e)}"
        ) from e


@router.delete("/{grupa_id}/studenci/{student_id}", summary="Usuń studenta z grupy")
async def usun_studenta_z_grupy(
    grupa_id: Annotated[str, Path(title="ID grupy")],
    student_id: Annotated[str, Path(title="UID studenta")]
):
    """Usuwa studenta z grupy."""
    try:
        success = await SerwisGrup.usun_studenta_z_grupy(grupa_id, student_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grupa o ID {grupa_id} nie została znaleziona lub student nie jest przypisany do grupy"
            )
        return {"message": f"Student {student_id} usunięty z grupy {grupa_id} pomyślnie"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas usuwania studenta z grupy: {str(e)}"
        ) from e
