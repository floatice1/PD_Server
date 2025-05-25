"""Moduł serwisowy dla zarządzania użytkownikami."""

from typing import List, Optional, Dict, Any

from firebase_admin import auth

from app.modele.uzytkownik import Uzytkownik, UzytkownikTworzenie
from app.repozytoria.uzytkownik_rep import RepozytoriumUzytkownikow


class SerwisUzytkownikow:
    """Klasa serwisowa do obsługi operacji na użytkownikach."""

    @staticmethod
    async def utworz_uzytkownika(dane_uzytkownika: UzytkownikTworzenie) -> Uzytkownik:
        """Tworzy nowego użytkownika."""
        return await RepozytoriumUzytkownikow.utworz_uzytkownika(dane_uzytkownika)

    @staticmethod
    async def pobierz_uzytkownika_po_id(uzytkownik_id: str) -> Optional[Dict[str, Any]]:
        """Pobiera użytkownika po jego identyfikatorze."""
        return await RepozytoriumUzytkownikow.pobierz_uzytkownika_po_id(uzytkownik_id)

    @staticmethod
    async def pobierz_wszystkich_uzytkownikow() -> List[Dict[str, Any]]:
        """Pobiera listę wszystkich użytkowników."""
        return await RepozytoriumUzytkownikow.pobierz_wszystkich_uzytkownikow()

    @staticmethod
    async def aktualizuj_uzytkownika(
        uzytkownik_id: str,
        dane_aktualizacji: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Aktualizuje dane istniejącego użytkownika."""
        if not dane_aktualizacji:
            raise ValueError("Nie podano danych do aktualizacji")

        zaktualizowano = await RepozytoriumUzytkownikow.aktualizuj_uzytkownika(
            uzytkownik_id,
            dane_aktualizacji
        )
        if zaktualizowano:
            return await RepozytoriumUzytkownikow.pobierz_uzytkownika_po_id(uzytkownik_id)
        return None

    @staticmethod
    async def usun_uzytkownika(uzytkownik_id: str) -> bool:
        """Usuwa użytkownika po jego identyfikatorze."""
        return await RepozytoriumUzytkownikow.usun_uzytkownika(uzytkownik_id)

    @staticmethod
    async def generuj_token_resetu_hasla(email: str) -> str:
        """Generuje token do resetowania hasła dla podanego adresu email."""
        try:
            link = auth.generate_password_reset_link(email)
            return link
        except Exception as e:
            print(f"Błąd podczas generowania linku resetu hasła: {e}")
            raise ValueError("Nie udało się wygenerować linku resetu hasła.") from e

    @staticmethod
    async def generuj_token_weryfikacji_emaila(email: str) -> str:
        """Generuje token do weryfikacji adresu email dla podanego adresu email."""
        try:
            link = auth.generate_email_verification_link(email)
            return link
        except Exception as e:
            print(f"Błąd podczas generowania linku weryfikacji emaila: {e}")
            raise ValueError("Nie udało się wygenerować linku weryfikacji emaila.") from e

    @staticmethod
    async def pobierz_uzytkownika_po_emailu(email: str) -> Optional[Dict[str, Any]]:
        """Pobiera użytkownika po jego adresie email."""
        return await RepozytoriumUzytkownikow.pobierz_uzytkownika_po_emailu(email)
