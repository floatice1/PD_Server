from firebase_admin import firestore
from typing import Dict, List, Optional, Any
from datetime import datetime

from app.modele.ocena import Ocena, OcenaTworzenie
from app.konfiguracja.firebase_config import db

class RepozytoriumOcen:
    COLLECTION_NAME = 'grades'
    
    @classmethod
    async def utworz_ocene(cls, dane_oceny: OcenaTworzenie) -> Ocena:
        try:
            student_doc = db.collection('users').document(dane_oceny.studentId).get()
            if not student_doc.exists:
                raise ValueError(f"Student o ID {dane_oceny.studentId} nie istnieje")

            group_doc = db.collection('groups').document(dane_oceny.grupaId).get()
            if not group_doc.exists:
                raise ValueError(f"Groupa o ID {dane_oceny.grupaId} nie istnieje")

            grupa_data = group_doc.to_dict()
            if dane_oceny.studentId not in grupa_data.get('studentsIds', []):
                raise ValueError(f"Student o ID {dane_oceny.studentId} nie należy do grupy")

            ocena_doc_ref = db.collection(cls.COLLECTION_NAME).document()
            ocena_info = {
                'id': ocena_doc_ref.id,
                'studentId': dane_oceny.studentId,
                'groupId': dane_oceny.grupaId,
                'value': dane_oceny.wartoscOceny,
                'created_at': firestore.SERVER_TIMESTAMP,
                'givenBy': dane_oceny.wystawionePrzez
            }
            ocena_doc_ref.set(ocena_info)
            
            return Ocena(
                ocenaId=ocena_doc_ref.id,
                studentId=dane_oceny.studentId,
                grupaId=dane_oceny.grupaId,
                wartoscOceny=dane_oceny.wartoscOceny,
                wystawionePrzez=dane_oceny.wystawionePrzez
            )
        except Exception as e:
            raise e
    
    @classmethod
    async def pobierz_ocene_po_id(cls, ocena_id: str) -> Optional[Dict[str, Any]]:
        ocena_doc = db.collection(cls.COLLECTION_NAME).document(ocena_id).get()
        if ocena_doc.exists:
            return ocena_doc.to_dict()
        return None
    
    @classmethod
    async def pobierz_oceny_studenta(cls, student_id: str) -> List[Dict[str, Any]]:
        oceny = []
        oceny_docs = db.collection(cls.COLLECTION_NAME).where('studentId', '==', student_id).stream()
        for doc in oceny_docs:
            oceny.append(doc.to_dict())
        return oceny
    
    @classmethod
    async def pobierz_oceny_z_grupy(cls, grupa_id: str) -> List[Dict[str, Any]]:
        oceny = []
        oceny_docs = db.collection(cls.COLLECTION_NAME).where('groupId', '==', grupa_id).stream()
        for doc in oceny_docs:
            oceny.append(doc.to_dict())
        return oceny
    
    @classmethod
    async def aktualizuj_ocene(cls, ocena_id: str, dane_oceny: Dict[str, Any]) -> bool:
        try:
            db.collection(cls.COLLECTION_NAME).document(ocena_id).update(dane_oceny)
            return True
        except Exception as e:
            raise e
    
    @classmethod
    async def usun_ocene(cls, ocena_id: str) -> bool:
        try:
            db.collection(cls.COLLECTION_NAME).document(ocena_id).delete()
            return True
        except Exception as e:
            raise e