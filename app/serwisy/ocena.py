from typing import List, Optional, Dict, Any
from app.modele.ocena import Ocena, OcenaTworzenie
from app.repozytoria.ocena import RepozytoriumOcen

class SerwisOcen:
    @staticmethod
    async def utworz_ocene(dane_oceny: OcenaTworzenie) -> Ocena:
        return await RepozytoriumOcen.utworz_ocene(dane_oceny)

    @staticmethod
    async def pobierz_wszystkie_oceny() -> List[Dict[str, Any]]:
        return await RepozytoriumOcen.pobierz_wszystkie_oceny()

    @staticmethod
    async def pobierz_ocene_po_id(ocena_id: str) -> Optional[Dict[str, Any]]:
        return await RepozytoriumOcen.pobierz_ocene_po_id(ocena_id)

    @staticmethod
    async def pobierz_oceny_studenta(student_id: str) -> List[Dict[str, Any]]:
        return await RepozytoriumOcen.pobierz_oceny_studenta(student_id)

    @staticmethod
    async def pobierz_oceny_z_przedmiotu(przedmiot_id: str) -> List[Dict[str, Any]]:
        return await RepozytoriumOcen.pobierz_oceny_z_przedmiotu(przedmiot_id)

    @staticmethod
    async def aktualizuj_ocene(ocena_id: str, dane_oceny: Dict[str, Any]) -> bool:
        wymagane_pola = {'studentId', 'grupaId', 'wystawionePrzez', 'wartoscOceny'}
        dozwolone_pola = set(dane_oceny.keys())
        if not dozwolone_pola.issubset(wymagane_pola):
            raise ValueError("Znaleziono niedozwolone pola w dane_oceny")
            
        return await RepozytoriumOcen.aktualizuj_ocene(ocena_id, dane_oceny)
    
    @staticmethod
    async def usun_ocene(ocena_id: str) -> bool:
        return await RepozytoriumOcen.usun_ocene(ocena_id)