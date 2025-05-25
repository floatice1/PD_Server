import firebase_admin
from firebase_admin import credentials, firestore, auth

try:
    cred = credentials.Certificate("app\konfiguracja\serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Błąd podczas inicjalizacji Firebase Admin SDK: {e}")
    raise e

db = firestore.client()

__all__ = ['auth', 'db']