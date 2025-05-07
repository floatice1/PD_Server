from firebase_admin import firestore
from typing import Dict, List, Optional, Any

from app.modele.przedmiot import Przedmiot, PrzedmiotTworzenie
from app.konfiguracja.firebase_config import db

class RepozytoriumPrzedmiotow:
    COLLECTION_NAME = 'subjects'
    
    @classmethod
    async def utworz_przedmiot(cls, dane_przedmiotu: PrzedmiotTworzenie) -> Przedmiot:
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
        przedmiot_doc = db.collection(cls.COLLECTION_NAME).document(przedmiot_id).get()
        if przedmiot_doc.exists:
            return przedmiot_doc.to_dict()
        return None
    
    @classmethod
    async def pobierz_wszystkie_przedmioty(cls) -> List[Dict[str, Any]]:
        przedmioty = []
        przedmiot_docs = db.collection(cls.COLLECTION_NAME).stream()
        for doc in przedmiot_docs:
            przedmioty.append(doc.to_dict())
        return przedmioty
    
    @classmethod
    async def aktualizuj_przedmiot(cls, przedmiot_id: str, dane_przedmiotu: PrzedmiotTworzenie) -> Optional[Przedmiot]:
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
        try:
            db.collection(cls.COLLECTION_NAME).document(przedmiot_id).delete()
            return True
        except Exception as e:
            raise e