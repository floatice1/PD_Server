from typing import List, Optional, Dict, Any
from app.modele.uzytkownik import Uzytkownik, UzytkownikTworzenie, UzytkownikLogin
from app.repozytoria.uzytkownik_rep import RepozytoriumUzytkownikow
from app.konfiguracja.firebase_config import auth, db
from firebase_admin import auth as firebase_auth
from datetime import datetime, timedelta
import json

class SerwisUzytkownikow:
    @staticmethod
    async def utworz_uzytkownika(dane_uzytkownika: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        nowy_uzytkownik_id = await RepozytoriumUzytkownikow.utworz_uzytkownika(dane_uzytkownika)
        if nowy_uzytkownik_id:
            return await RepozytoriumUzytkownikow.pobierz_uzytkownika_po_id(nowy_uzytkownik_id)

    @staticmethod
    async def pobierz_uzytkownika_po_id(user_id: str) -> Optional[Dict[str, Any]]:
        return await RepozytoriumUzytkownikow.pobierz_uzytkownika_po_id(user_id)

    @staticmethod
    async def pobierz_wszystkich_uzytkownikow() -> List[Dict[str, Any]]:
        return await RepozytoriumUzytkownikow.pobierz_wszystkich_uzytkownikow()

    @staticmethod
    async def aktualizuj_uzytkownika(user_id: str, dane_uzytkownika: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not dane_uzytkownika:
            raise ValueError("Nie podano danych do aktualizacji")

        zaktualizowano = await RepozytoriumUzytkownikow.aktualizuj_uzytkownika(user_id, dane_uzytkownika)
        if zaktualizowano:
            return await RepozytoriumUzytkownikow.pobierz_uzytkownika_po_id(user_id)

    @staticmethod
    async def usun_uzytkownika(user_id: str) -> bool:
        return await RepozytoriumUzytkownikow.usun_uzytkownika(user_id)

    @staticmethod
    async def zaloguj_uzytkownika(dane_logowania: UzytkownikLogin) -> Optional[Dict[str, Any]]:
        try:
            try:
                user = auth.get_user_by_email(dane_logowania.email)
            except firebase_auth.UserNotFoundError:
                return None
            
            custom_token = auth.create_custom_token(user.uid)
            
            user_data = await RepozytoriumUzytkownikow.pobierz_uzytkownika_po_id(user.uid)
            
            return {
                "uid": user.uid,
                "email": user.email,
                "token": custom_token.decode('utf-8'),
                "role": user_data.get('role') if user_data else None,
                "name": user_data.get('name') if user_data else None
            }
            
        except Exception as e:
            print(f"Błąd logowania: {str(e)}")
            return None
    
    @staticmethod
    async def weryfikuj_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            
            user_data = await RepozytoriumUzytkownikow.pobierz_uzytkownika_po_id(uid)
            return user_data
        except Exception as e:
            print(f"Błąd weryfikacji tokenu: {str(e)}")
            return None