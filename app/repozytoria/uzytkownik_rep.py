"""Repozytorium do zarządzania danymi użytkowników w Firestore."""

from typing import Dict, List, Optional, Any
from firebase_admin import firestore

from app.konfiguracja.firebase_config import db, auth


class RepozytoriumUzytkownikow:
    """Klasa repozytorium do interakcji z kolekcją 'users' w Firestore."""
    COLLECTION_NAME = 'users'

    @classmethod
    async def utworz_uzytkownika(
        cls,
        dane_uzytkownika: Dict[str, Any]
    ) -> str:
        """Tworzy nowego użytkownika w Firestore i Authentication."""
        try:
            firebase_user = auth.create_user(
                email=dane_uzytkownika.email,
                password=dane_uzytkownika.haslo,
                display_name=dane_uzytkownika.imie
            )

            auth.set_custom_user_claims(firebase_user.uid, {"role": dane_uzytkownika.rola.value})

            user_doc_ref = db.collection(cls.COLLECTION_NAME).document(firebase_user.uid)
            user_info = {
                'uid': firebase_user.uid,
                'email': dane_uzytkownika.email,
                'name': dane_uzytkownika.imie,
                'role': dane_uzytkownika.rola.value,
                'created_at': firestore.SERVER_TIMESTAMP
            }
            user_doc_ref.set(user_info)

            return user_info['uid']
        except Exception as e:
            raise e

    @classmethod
    async def pobierz_uzytkownika_po_id(
        cls,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Pobiera dane użytkownika na podstawie ID."""
        user_doc = db.collection(cls.COLLECTION_NAME).document(user_id).get()
        if user_doc.exists:
            return user_doc.to_dict()
        return None

    @classmethod
    async def pobierz_wszystkich_uzytkownikow(cls) -> List[Dict[str, Any]]:
        """Pobiera listę wszystkich zarejestrowanych użytkowników."""
        users = []
        user_docs = db.collection(cls.COLLECTION_NAME).stream()
        for doc in user_docs:
            users.append(doc.to_dict())
        return users

    @classmethod
    async def aktualizuj_uzytkownika(
        cls,
        user_id: str,
        dane_uzytkownika: Dict[str, Any]
    ) -> bool:
        """Aktualizuje dane użytkownika w Firestore i Authentication."""
        try:
            user_doc_ref = db.collection(cls.COLLECTION_NAME).document(user_id)
            user_doc = user_doc_ref.get()

            if not user_doc.exists:
                return False

            update_data = {}
            if 'email' in dane_uzytkownika:
                update_data['email'] = dane_uzytkownika['email']
            if 'haslo' in dane_uzytkownika:
                update_data['password'] = dane_uzytkownika['haslo']
            if 'imie' in dane_uzytkownika:
                update_data['display_name'] = dane_uzytkownika['imie']

            firebase_user = None
            if update_data:
                firebase_user = auth.update_user(
                    user_id,
                    **update_data
                )
            else:
                firebase_user = auth.get_user(user_id)


            if 'rola' in dane_uzytkownika:
                auth.set_custom_user_claims(
                    firebase_user.uid,
                    {"role": dane_uzytkownika['rola'].value}
                )

            user_info = {}
            if 'email' in dane_uzytkownika:
                user_info['email'] = dane_uzytkownika['email']
            if 'imie' in dane_uzytkownika:
                user_info['name'] = dane_uzytkownika['imie']
            if 'rola' in dane_uzytkownika:
                user_info['role'] = dane_uzytkownika['rola'].value
            user_info['updated_at'] = firestore.SERVER_TIMESTAMP
            user_doc_ref.update(user_info)

            return True
        except Exception as e:
            raise e

    @classmethod
    async def usun_uzytkownika(cls, user_id: str) -> bool:
        """Usuwa użytkownika z Firestore i Authentication."""
        try:
            auth.delete_user(user_id)
            db.collection(cls.COLLECTION_NAME).document(user_id).delete()
            return True
        except Exception as e:
            raise e
