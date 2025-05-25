from firebase_admin import firestore
from typing import Dict, List, Optional, Any

from app.modele.grupa import Grupa, GrupaTworzenie
from app.konfiguracja.firebase_config import db

class RepozytoriumGrup:
    COLLECTION_NAME = 'groups'
    
    @classmethod
    async def utworz_grupe(cls, dane_grupy: GrupaTworzenie) -> Grupa:
        try:
            subject_doc = db.collection('subjects').document(dane_grupy.przedmiotId).get()
            if not subject_doc.exists:
                raise ValueError(f"Przedmiot o ID {dane_grupy.przedmiotId} nie istnieje")

            grupa_doc_ref = db.collection(cls.COLLECTION_NAME).document()
            grupa_info = {
                'id': grupa_doc_ref.id,
                'name': dane_grupy.nazwa,
                'subjectId': dane_grupy.przedmiotId,
                'lecturerId': dane_grupy.wykladowcaId,
                'studentsIds': [],
                'createdAt': firestore.SERVER_TIMESTAMP
            }
            grupa_doc_ref.set(grupa_info)
            
            return Grupa(
                grupaId=grupa_doc_ref.id,
                nazwa=dane_grupy.nazwa,
                przedmiotId=dane_grupy.przedmiotId,
                wykladowcaId=dane_grupy.wykladowcaId,
                studenciIds=[]
            )
        except Exception as e:
            raise e
    
    @classmethod
    async def pobierz_grupe_po_id(cls, grupa_id: str) -> Optional[Dict[str, Any]]:
        grupa_doc = db.collection(cls.COLLECTION_NAME).document(grupa_id).get()
        if grupa_doc.exists:
            return grupa_doc.to_dict()
        return None
    
    @classmethod
    async def pobierz_wszystkie_grupy(cls) -> List[Dict[str, Any]]:
        grupy = []
        grupa_docs = db.collection(cls.COLLECTION_NAME).stream()
        for doc in grupa_docs:
            grupy.append(doc.to_dict())
        return grupy
    
    @classmethod
    async def aktualizuj_grupe(cls, grupa_id: str, dane_aktualizacji: Dict[str, Any]) -> bool:
        try:
            grupa_ref = db.collection(cls.COLLECTION_NAME).document(grupa_id)
            grupa_doc = grupa_ref.get()

            if not grupa_doc.exists:
                return False

            pola_do_zapisu = {}
            if 'nazwa' in dane_aktualizacji:
                pola_do_zapisu['name'] = dane_aktualizacji['nazwa']

            if 'przedmiotId' in dane_aktualizacji:
                subject_id = dane_aktualizacji['przedmiotId']
                subject_doc = db.collection('subjects').document(subject_id).get()
                if not subject_doc.exists:
                    raise ValueError(f"Przedmiot o ID {subject_id} nie istnieje")
                pola_do_zapisu['subjectId'] = subject_id

            if 'wykladowcaId' in dane_aktualizacji:
                lecturer_id = dane_aktualizacji['wykladowcaId']
                lecturer_doc = db.collection('users').document(lecturer_id).get()
                if not lecturer_doc.exists:
                    raise ValueError(f"Użytkownik o ID {lecturer_id} nie istnieje")
                lecturer_data = lecturer_doc.to_dict()
                if lecturer_data.get('role') != 'wykladowca':
                    raise ValueError(f"Użytkownik o ID {lecturer_id} nie jest wykładowcą")
                pola_do_zapisu['lecturerId'] = dane_aktualizacji['wykladowcaId']
            
            pola_do_zapisu['updatedAt'] = firestore.SERVER_TIMESTAMP
            
            grupa_ref.update(pola_do_zapisu)
            return True
        except Exception as e:
            raise e
    
    @classmethod
    async def usun_grupe(cls, grupa_id: str) -> bool:
        try:
            db.collection(cls.COLLECTION_NAME).document(grupa_id).delete()
            return True
        except Exception as e:
            raise e
    
    @classmethod
    async def przypisz_studenta_do_grupy(cls, grupa_id: str, student_id: str) -> bool:
        try:
            user_doc = db.collection('users').document(student_id).get()
            if not user_doc.exists:
                raise ValueError(f"Użytkownik o ID {student_id} nie istnieje")
            
            user_data = user_doc.to_dict()
            if user_data.get('role') != 'student':
                raise ValueError(f"Użytkownik o ID {student_id} nie jest studentem")

            grupa_doc = db.collection(cls.COLLECTION_NAME).document(grupa_id).get()
            grupa_data = grupa_doc.to_dict()
            if student_id in grupa_data.get('studentsIds', []):
                raise ValueError(f"Student o ID {student_id} jest już przypisany do grupy")

            grupa_ref = db.collection(cls.COLLECTION_NAME).document(grupa_id)
            grupa_ref.update({
                'studentsIds': firestore.ArrayUnion([student_id]),
                'updatedAt': firestore.SERVER_TIMESTAMP
            })
            return True
        except Exception as e:
            raise e
    
    @classmethod
    async def usun_studenta_z_grupy(cls, grupa_id: str, student_id: str) -> bool:
        try:
            user_doc = db.collection('users').document(student_id).get()
            if not user_doc.exists:
                raise ValueError(f"Użytkownik o ID {student_id} nie istnieje")
            
            user_data = user_doc.to_dict()
            if user_data.get('role') != 'student':
                raise ValueError(f"Użytkownik o ID {student_id} nie jest studentem")
                
            grupa_doc = db.collection(cls.COLLECTION_NAME).document(grupa_id)
            grupa_doc.update({
                'studentsIds': firestore.ArrayRemove([student_id]),
                'updatedAt': firestore.SERVER_TIMESTAMP
            })
            return True
        except Exception as e:
            raise e
    
    @classmethod
    async def zmien_wykladowce_grupy(cls, grupa_id: str, wykladowca_id: str) -> bool:
        try:
            user_doc = db.collection('users').document(wykladowca_id).get()
            if not user_doc.exists:
                raise ValueError(f"Użytkownik o ID {wykladowca_id} nie istnieje")
            
            user_data = user_doc.to_dict()
            if user_data.get('role') != 'wykladowca':
                raise ValueError(f"Użytkownik o ID {wykladowca_id} nie jest wykładowcą")

            db.collection(cls.COLLECTION_NAME).document(grupa_id).update({
                'lecturerId': wykladowca_id,
                'updatedAt': firestore.SERVER_TIMESTAMP
            })
            return True
        except Exception as e:
            raise e