"""Repozytorium do zarządzania danymi ocen w Firestore."""

from typing import Dict, List, Optional, Any
from datetime import datetime

from firebase_admin import firestore

from app.modele.ocena import Ocena, OcenaTworzenie
from app.konfiguracja.firebase_config import db


class RepozytoriumOcen:
    """Klasa repozytorium do interakcji z kolekcją 'grades' w Firestore."""
    COLLECTION_NAME = 'grades'

    @classmethod
    async def utworz_ocene(cls, dane_oceny: OcenaTworzenie) -> Ocena:
        """Tworzy nową ocenę w Firestore."""
        try:
            student_doc = db.collection('users').document(dane_oceny.studentId).get()
            if not student_doc.exists:
                raise ValueError(f"Student o ID {dane_oceny.studentId} nie istnieje")

            group_doc = db.collection('groups').document(dane_oceny.grupaId).get()
            if not group_doc.exists:
                raise ValueError(f"Grupa o ID {dane_oceny.grupaId} nie istnieje")

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
        """Pobiera dane oceny na podstawie jej ID."""
        ocena_doc = db.collection(cls.COLLECTION_NAME).document(ocena_id).get()
        if ocena_doc.exists:
            return ocena_doc.to_dict()
        return None

    @classmethod
    async def pobierz_oceny_studenta(cls, student_id: str) -> List[Dict[str, Any]]:
        """Pobiera dane wszystkich ocen dla danego studenta."""
        oceny = []
        oceny_docs = (
            db.collection(cls.COLLECTION_NAME)
            .where('studentId', '==', student_id)
            .stream()
        )
        for doc in oceny_docs:
            oceny.append(doc.to_dict())
        return oceny

    @classmethod
    async def pobierz_oceny_z_grupy(cls, grupa_id: str) -> List[Dict[str, Any]]:
        """Pobiera dane wszystkich ocen dla danej grupy."""
        oceny = []
        oceny_docs = db.collection(cls.COLLECTION_NAME).where('groupId', '==', grupa_id).stream()
        for doc in oceny_docs:
            oceny.append(doc.to_dict())
        return oceny

    @classmethod
    async def pobierz_wszystkie_oceny(cls) -> List[Dict[str, Any]]:
        """Pobiera dane wszystkich ocen z Firestore."""
        oceny = []
        oceny_docs = db.collection(cls.COLLECTION_NAME).stream()
        for doc in oceny_docs:
            oceny.append(doc.to_dict())
        return oceny

    @classmethod
    async def aktualizuj_ocene(cls, ocena_id: str, dane_oceny: Dict[str, Any]) -> bool:
        """Aktualizuje dane istniejącej oceny."""
        try:
            ocena_ref = db.collection(cls.COLLECTION_NAME).document(ocena_id)
            ocena_doc = ocena_ref.get()
            if not ocena_doc.exists:
                raise ValueError(f"Ocena o ID {ocena_id} nie istnieje")

            update_data = {}

            if 'studentId' in dane_oceny:
                student_id = dane_oceny['studentId']
                student_doc = db.collection('users').document(student_id).get()
                if not student_doc.exists:
                    raise ValueError(f"Student o ID {student_id} nie istnieje")
                update_data['studentId'] = student_id

            if 'grupaId' in dane_oceny:
                group_id = dane_oceny['grupaId']
                group_doc = db.collection('groups').document(group_id).get()
                if not group_doc.exists:
                    raise ValueError(f"Grupa o ID {group_id} nie istnieje")
                update_data['groupId'] = group_id

            current_student_id = update_data.get('studentId', ocena_doc.to_dict().get('studentId'))
            current_group_id = update_data.get('groupId', ocena_doc.to_dict().get('groupId'))

            if current_student_id and current_group_id:
                group_doc_for_check = db.collection('groups').document(current_group_id).get()
                if group_doc_for_check.exists:
                    grupa_data = group_doc_for_check.to_dict()
                    if current_student_id not in grupa_data.get('studentsIds', []):
                        raise ValueError(f"Student o ID {current_student_id} nie należy do grupy o ID {current_group_id}")
                else:
                    raise ValueError(f"Grupa o ID {current_group_id} nie istnieje do sprawdzenia przynależności studenta")

            if 'wartoscOceny' in dane_oceny:
                update_data['value'] = dane_oceny['wartoscOceny']

            if 'wystawionePrzez' in dane_oceny:
                update_data['givenBy'] = dane_oceny['wystawionePrzez']

            if not update_data:
                return True

            ocena_ref.update(update_data)
            return True
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Wystąpił błąd podczas aktualizacji oceny: {e}")

    @classmethod
    async def usun_ocene(cls, ocena_id: str) -> bool:
        """Usuwa ocenę z Firestore."""
        try:
            db.collection(cls.COLLECTION_NAME).document(ocena_id).delete()
            return True
        except Exception as e:
            raise e
