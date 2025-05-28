import pytest
import pytest_asyncio
from unittest.mock import MagicMock, AsyncMock
from app.serwisy import przedmiot as serwis_przedmiot_module
from httpx import AsyncClient
from main import app as main_app
from fastapi.testclient import TestClient

async def mock_async_iterator(items):
    for item in items:
        yield item

def mock_iterator(items):
    for item in items:
        yield item

@pytest.fixture
def mock_serwis_przedmiotow():
    """
    Fixture do mockowania obiektu SerwisPrzedmiotow.
    """
    mock_serwis_instance = MagicMock()
    
    mock_serwis_instance.pobierz_wszystkie_przedmioty = AsyncMock()
    mock_serwis_instance.pobierz_przedmiot_po_id = AsyncMock()
    mock_serwis_instance.utworz_przedmiot = AsyncMock()
    mock_serwis_instance.aktualizuj_przedmiot = AsyncMock()
    mock_serwis_instance.usun_przedmiot = AsyncMock()

    with pytest.MonkeyPatch().context() as mp:
        mp.setattr(serwis_przedmiot_module, 'SerwisPrzedmiotow', mock_serwis_instance)
        yield mock_serwis_instance


@pytest_asyncio.fixture(scope="module")
def async_client():
    return TestClient(main_app)

@pytest.fixture
def mock_db():
    """
    Fixture do mockowania obiektu 'db' z firebase_admin.firestore.
    """
    mock_db_instance = MagicMock()

    mock_doc_ref = MagicMock()
    mock_doc_ref.id = "mock_doc_id_123"
    mock_doc_ref.set.return_value = None
    mock_db_instance.collection.return_value.document.return_value = mock_doc_ref
    
    mock_doc_snapshot = MagicMock()
    mock_doc_snapshot.exists = False
    mock_doc_snapshot.to_dict.return_value = None
    mock_db_instance.collection.return_value.document.return_value.get.return_value = mock_doc_snapshot

    mock_db_instance.collection.return_value.stream.return_value = mock_async_iterator([])

    mock_db_instance.collection.return_value.document.return_value.update.return_value = None

    mock_db_instance.collection.return_value.document.return_value.delete.return_value = None

    with pytest.MonkeyPatch().context() as mp:
        mp.setattr("app.repozytoria.przedmiot.db", mock_db_instance)
        mp.setattr("app.repozytoria.uzytkownik_rep.db", mock_db_instance)
        yield mock_db_instance


@pytest.fixture
def mock_auth():
    """
    Fixture do mockowania obiektu 'auth' z firebase_admin.auth.
    """
    mock_auth_instance = MagicMock()

    mock_auth_instance.create_user.return_value = MagicMock(uid="mock_user_uid_123", email="test@example.com", display_name="Test User")
    
    mock_auth_instance.set_custom_user_claims.return_value = None

    mock_auth_instance.update_user.return_value = MagicMock(uid="mock_user_uid_123", email="updated@example.com", display_name="Updated User")

    mock_auth_instance.delete_user.return_value = None

    with pytest.MonkeyPatch().context() as mp:
        mp.setattr("app.repozytoria.uzytkownik_rep.auth", mock_auth_instance)
        yield mock_auth_instance