from firebase_admin import firestore
from typing import Dict, List, Optional, Any

from app.modele.uzytkownik import Uzytkownik, UzytkownikTworzenie
from app.konfiguracja.firebase_config import db, auth

class RepozytoriumUzytkownikow:
    COLLECTION_NAME = 'users'
    
    @classmethod
    async def utworz_uzytkownika(cls, dane_uzytkownika: UzytkownikTworzenie) -> Uzytkownik:
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
            
            return Uzytkownik(
                uid=firebase_user.uid,
                email=dane_uzytkownika.email,
                imie=dane_uzytkownika.imie,
                rola=dane_uzytkownika.rola
            )
        except Exception as e:
            raise e
    
    @classmethod
    async def pobierz_uzytkownika_po_id(cls, user_id: str) -> Optional[Dict[str, Any]]:
        user_doc = db.collection(cls.COLLECTION_NAME).document(user_id).get()
        if user_doc.exists:
            return user_doc.to_dict()
        return None
    
    @classmethod
    async def pobierz_wszystkich_uzytkownikow(cls) -> List[Dict[str, Any]]:
        users = []
        user_docs = db.collection(cls.COLLECTION_NAME).stream()
        for doc in user_docs:
            users.append(doc.to_dict())
        return users
    
    @classmethod
    async def aktualizuj_uzytkownika(cls, user_id: str, dane_uzytkownika: UzytkownikTworzenie) -> Uzytkownik:
        try:
            firebase_user = auth.update_user(
                user_id,
                email=dane_uzytkownika.email,
                password=dane_uzytkownika.haslo,
                display_name=dane_uzytkownika.imie
            )

            auth.set_custom_user_claims(firebase_user.uid, {"role": dane_uzytkownika.rola.value})

            user_doc_ref = db.collection(cls.COLLECTION_NAME).document(user_id)
            user_info = {
                'email': dane_uzytkownika.email,
                'name': dane_uzytkownika.imie,
                'role': dane_uzytkownika.rola.value,
                'updated_at': firestore.SERVER_TIMESTAMP
            }
            user_doc_ref.update(user_info)
            
            return Uzytkownik(
                uid=user_id,
                email=dane_uzytkownika.email,
                imie=dane_uzytkownika.imie,
                rola=dane_uzytkownika.rola
            )
        except Exception as e:
            raise e
    
    @classmethod
    async def usun_uzytkownika(cls, user_id: str) -> bool:
        try:
            auth.delete_user(user_id)
            db.collection(cls.COLLECTION_NAME).document(user_id).delete()
            return True
        except Exception as e:
            raise e