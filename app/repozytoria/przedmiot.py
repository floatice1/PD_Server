"""Repozytorium do zarządzania danymi przedmiotów w Firestore."""

from typing import Dict, List, Optional, Any

from firebase_admin import firestore

from app.modele.przedmiot import Przedmiot, PrzedmiotTworzenie
from app.konfiguracja.firebase_config import db


class RepozytoriumPrzedmiotow:
    """Klasa repozytorium do interakcji z kolekcją 'subjects' w Firestore."""
    COLLECTION_NAME = 'subjects'

    @classmethod
    async def utworz_przedmiot(cls, dane_przedmiotu: PrzedmiotTworzenie) -> Przedmiot:
        """Tworzy nowy przedmiot w Firestore."""
        try:
            przedmiot_doc_ref = db.collection(cls.COLLECTION_NAME).document()
            przedmiot_info = {
                'id': przedmiot_doc_ref.id,
                'name': dane_przedmiotu.nazwa,
                'description': dane_przedmiotu.opis,
                'created_at': firestore.SERVER_TIMESTAMP
            }

            przedmiot_doc_ref.set(przedmiot_info)

            return Przedmiot(
                przedmiotId=przedmiot_doc_ref.id,
                nazwa=dane_przedmiotu.nazwa,
                opis=dane_przedmiotu.opis
            )
        except Exception as e:
            raise e

    @classmethod
    async def pobierz_przedmiot_po_id(cls, przedmiot_id: str) -> Optional[Dict[str, Any]]:
        """Pobiera dane przedmiotu na podstawie jego ID."""
        przedmiot_doc = db.collection(cls.COLLECTION_NAME).document(przedmiot_id).get()
        if przedmiot_doc.exists:
            return przedmiot_doc.to_dict()
        return None

    @classmethod
    async def pobierz_wszystkie_przedmioty(cls) -> List[Dict[str, Any]]:
        """Pobiera dane wszystkich przedmiotów z Firestore."""
        przedmioty = []
        przedmiot_docs = db.collection(cls.COLLECTION_NAME).stream()
        for doc in przedmiot_docs:
            przedmioty.append(doc.to_dict())
        return przedmioty

    @classmethod
    async def aktualizuj_przedmiot(
        cls,
        przedmiot_id: str,
        dane_przedmiotu: PrzedmiotTworzenie
    ) -> Optional[Przedmiot]:
        """Aktualizuje dane istniejącego przedmiotu."""
        try:
            przedmiot_doc = db.collection(cls.COLLECTION_NAME).document(przedmiot_id)
            przedmiot_info = {
                'name': dane_przedmiotu.nazwa,
                'description': dane_przedmiotu.opis,
                'updated_at': firestore.SERVER_TIMESTAMP
            }

            przedmiot_doc.update(przedmiot_info)

            return Przedmiot(
                przedmiotId=przedmiot_id,
                nazwa=dane_przedmiotu.nazwa,
                opis=dane_przedmiotu.opis
            )
        except Exception as e:
            raise e

    @classmethod
    async def usun_przedmiot(cls, przedmiot_id: str) -> bool:
        """Usuwa przedmiot z Firestore."""
        try:
            db.collection(cls.COLLECTION_NAME).document(przedmiot_id).delete()
            return True
        except Exception as e:
            raise e
