from typing import List, Optional, Dict, Any
from app.modele.grupa import Grupa, GrupaTworzenie
from app.repozytoria.grupa import RepozytoriumGrup

class SerwisGrup:
    @staticmethod
    async def utworz_grupe(dane_grupy: GrupaTworzenie) -> Grupa:
        return await RepozytoriumGrup.utworz_grupe(dane_grupy)

    @staticmethod
    async def pobierz_grupe_po_id(grupa_id: str) -> Optional[Dict[str, Any]]:
        return await RepozytoriumGrup.pobierz_grupe_po_id(grupa_id)

    @staticmethod
    async def pobierz_wszystkie_grupy() -> List[Dict[str, Any]]:
        return await RepozytoriumGrup.pobierz_wszystkie_grupy()

    @staticmethod
    async def aktualizuj_grupe(grupa_id: str, dane_grupy: GrupaTworzenie) -> bool:
        return await RepozytoriumGrup.aktualizuj_grupe(grupa_id, dane_grupy)

    @staticmethod
    async def usun_grupe(grupa_id: str) -> bool:
        return await RepozytoriumGrup.usun_grupe(grupa_id)

    @staticmethod
    async def przypisz_studenta_do_grupy(grupa_id: str, student_id: str) -> bool:
        return await RepozytoriumGrup.przypisz_studenta_do_grupy(grupa_id, student_id)

    @staticmethod
    async def usun_studenta_z_grupy(grupa_id: str, student_id: str) -> bool:
        return await RepozytoriumGrup.usun_studenta_z_grupy(grupa_id, student_id)

    @staticmethod
    async def zmien_wykladowce_grupy(grupa_id: str, wykladowca_id: str) -> bool:
        return await RepozytoriumGrup.zmien_wykladowce_grupy(grupa_id, wykladowca_id)