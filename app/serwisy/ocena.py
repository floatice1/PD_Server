"""Moduł serwisowy dla zarządzania ocenami."""

from typing import List, Optional, Dict, Any
from app.modele.ocena import Ocena, OcenaTworzenie
from app.repozytoria.ocena import RepozytoriumOcen


class SerwisOcen:
    """Klasa serwisowa do obsługi operacji na ocenach."""

    @staticmethod
    async def utworz_ocene(dane_oceny: OcenaTworzenie) -> Ocena:
        """Tworzy nową ocenę."""
        return await RepozytoriumOcen.utworz_ocene(dane_oceny)

    @staticmethod
    async def pobierz_ocene_po_id(ocena_id: str) -> Optional[Dict[str, Any]]:
        """Pobiera ocenę po jej identyfikatorze."""
        return await RepozytoriumOcen.pobierz_ocene_po_id(ocena_id)

    @staticmethod
    async def pobierz_wszystkie_oceny() -> List[Dict[str, Any]]:
        """Pobiera listę wszystkich ocen."""
        return await RepozytoriumOcen.pobierz_wszystkie_oceny()

    @staticmethod
    async def aktualizuj_ocene(
        ocena_id: str,
        dane_aktualizacji: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Aktualizuje dane istniejącej oceny."""
        if not dane_aktualizacji:
            raise ValueError("Nie podano danych do aktualizacji")

        zaktualizowano = await RepozytoriumOcen.aktualizuj_ocene(ocena_id, dane_aktualizacji)
        if zaktualizowano:
            return await RepozytoriumOcen.pobierz_ocene_po_id(ocena_id)
        return None

    @staticmethod
    async def usun_ocene(ocena_id: str) -> bool:
        """Usuwa ocenę po jej identyfikatorze."""
        return await RepozytoriumOcen.usun_ocene(ocena_id)

    @staticmethod
    async def pobierz_oceny_dla_studenta(student_id: str) -> List[Dict[str, Any]]:
        """Pobiera oceny dla danego studenta."""
        return await RepozytoriumOcen.pobierz_oceny_dla_studenta(student_id)

    @staticmethod
    async def pobierz_oceny_z_przedmiotu(przedmiot_id: str) -> List[Dict[str, Any]]:
        """Pobiera oceny z przedmiotu."""
        return await RepozytoriumOcen.pobierz_oceny_z_przedmiotu(przedmiot_id)
