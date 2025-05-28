"""Moduł zawierający routery dla zarządzania ocenami."""

from typing import Annotated, Dict, Any

from fastapi import APIRouter, Path, Body, HTTPException, status

from app.serwisy.ocena import SerwisOcen
from app.modele.ocena import OcenaTworzenie

router = APIRouter(
    prefix="/oceny",
    tags=["oceny"],
    responses={
        404: {"message": "Nie znaleziono"},
        403: {"message": "Brak dostępu"},
        400: {"message": "Błąd danych"}
    }
)


@router.get("/", summary="Pobierz listę wszystkich ocen")
async def pobierz_wszystkie_oceny():
    """Pobiera listę wszystkich ocen."""
    try:
        return await SerwisOcen.pobierz_wszystkie_oceny()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas pobierania listy ocen: {str(e)}"
        ) from e


@router.get("/{ocena_id}", summary="Pobierz dane konkretnej oceny")
async def pobierz_ocene(
    ocena_id: Annotated[str, Path(title="ID oceny")]
):
    """Pobiera dane konkretnej oceny na podstawie jej ID."""
    try:
        ocena = await SerwisOcen.pobierz_ocene_po_id(ocena_id)
        if not ocena:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ocena o ID {ocena_id} nie została znaleziona"
            )
        return ocena
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas pobierania oceny: {str(e)}"
        ) from e


@router.post("/", status_code=201, summary="Utwórz nową ocenę")
async def utworz_ocene(
    dane_oceny: Annotated[Dict[str, Any], Body()]
):
    """Tworzy nową ocenę."""
    try:
        ocena = OcenaTworzenie(**dane_oceny)
        return await SerwisOcen.utworz_ocene(ocena)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Błąd podczas tworzenia oceny: {str(e)}"
        ) from e


@router.put("/{ocena_id}", summary="Zaktualizuj dane oceny")
async def aktualizuj_ocene(
    ocena_id: Annotated[str, Path(title="ID oceny")],
    dane_aktualizacji: Annotated[Dict[str, Any], Body()]
):
    """Aktualizuje dane oceny na podstawie jej ID."""
    try:
        zaktualizowana_ocena = await SerwisOcen.aktualizuj_ocene(
            ocena_id, dane_aktualizacji
        )
        if not zaktualizowana_ocena:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ocena o ID {ocena_id} nie istnieje"
            )
        updated_data = await SerwisOcen.pobierz_ocene_po_id(ocena_id)
        if not updated_data:
             raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Błąd podczas pobierania zaktualizowanej oceny o ID {ocena_id}"
            )
        return {"message": f"Ocena {ocena_id} zaktualizowana pomyślnie",
                "updated_data": updated_data}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas aktualizacji oceny: {str(e)}"
        ) from e


@router.delete("/{ocena_id}", summary="Usuń ocenę")
async def usun_ocene(
    ocena_id: Annotated[str, Path(title="ID oceny")]
):
    """Usuwa ocenę na podstawie jej ID."""
    try:
        success = await SerwisOcen.usun_ocene(ocena_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ocena o ID {ocena_id} nie została znaleziona"
            )
        return {"message": f"Ocena {ocena_id} usunięta pomyślnie"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas usuwania oceny: {str(e)}"
        ) from e
