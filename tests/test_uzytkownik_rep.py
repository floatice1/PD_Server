import pytest
from unittest.mock import MagicMock
from app.repozytoria.uzytkownik_rep import RepozytoriumUzytkownikow
from app.modele.uzytkownik import UzytkownikTworzenie, Rola
from firebase_admin import firestore
from firebase_admin import auth as firebase_auth

@pytest.mark.asyncio
async def test_utworz_uzytkownika_sukces(mock_db, mock_auth):
    """Testuje pomyślne utworzenie użytkownika."""
    dane_uzytkownika = UzytkownikTworzenie(
        email="test@example.com",
        haslo="SuperSecretPassword123",
        imie="Jan Kowalski",
        rola=Rola.STUDENT
    )

    mock_firebase_user = MagicMock(spec=firebase_auth.UserRecord)
    mock_firebase_user.uid = "mock_user_uid_001"
    mock_firebase_user.email = dane_uzytkownika.email
    mock_firebase_user.display_name = dane_uzytkownika.imie
    mock_auth.create_user.return_value = mock_firebase_user

    mock_doc_ref = mock_db.collection.return_value.document.return_value
    mock_doc_ref.id = mock_firebase_user.uid

    wynik_uid = await RepozytoriumUzytkownikow.utworz_uzytkownika(dane_uzytkownika)

    assert wynik_uid == mock_firebase_user.uid

    mock_auth.create_user.assert_called_once_with(
        email=dane_uzytkownika.email,
        password=dane_uzytkownika.haslo,
        display_name=dane_uzytkownika.imie
    )
    mock_auth.set_custom_user_claims.assert_called_once_with(
        mock_firebase_user.uid,
        {"role": dane_uzytkownika.rola.value}
    )
    mock_db.collection.assert_called_once_with('users')
    mock_db.collection.return_value.document.assert_called_once_with(mock_firebase_user.uid)
    mock_doc_ref.set.assert_called_once()
    
    args, kwargs = mock_doc_ref.set.call_args
    assert 'uid' in args[0] and args[0]['uid'] == mock_firebase_user.uid
    assert 'email' in args[0] and args[0]['email'] == dane_uzytkownika.email
    assert 'name' in args[0] and args[0]['name'] == dane_uzytkownika.imie
    assert 'role' in args[0] and args[0]['role'] == dane_uzytkownika.rola.value
    assert 'created_at' in args[0] and isinstance(args[0]['created_at'], type(firestore.SERVER_TIMESTAMP))


@pytest.mark.asyncio
async def test_pobierz_uzytkownika_po_id_sukces(mock_db):
    """Testuje pomyślne pobranie użytkownika po ID."""
    user_id = "test_user_id_1"
    oczekiwane_dane = {
        "uid": user_id,
        "email": "existing@example.com",
        "name": "Existing User",
        "role": "student"
    }

    mock_doc_snapshot = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc_snapshot.exists = True
    mock_doc_snapshot.to_dict.return_value = oczekiwane_dane

    wynik = await RepozytoriumUzytkownikow.pobierz_uzytkownika_po_id(user_id)

    assert wynik == oczekiwane_dane
    mock_db.collection.assert_called_once_with('users')
    mock_db.collection.return_value.document.assert_called_once_with(user_id)
    mock_doc_snapshot.to_dict.assert_called_once()


@pytest.mark.asyncio
async def test_pobierz_uzytkownika_po_id_nie_istnieje(mock_db):
    """Testuje pobranie użytkownika, który nie istnieje."""
    user_id = "non_existent_user_id"

    mock_doc_snapshot = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc_snapshot.exists = False
    mock_doc_snapshot.to_dict.return_value = None

    wynik = await RepozytoriumUzytkownikow.pobierz_uzytkownika_po_id(user_id)

    assert wynik is None
    mock_db.collection.assert_called_once_with('users')
    mock_db.collection.return_value.document.assert_called_once_with(user_id)
    mock_doc_snapshot.to_dict.assert_not_called()


@pytest.mark.asyncio
async def test_pobierz_wszystkich_uzytkownikow_sukces(mock_db):
    """Testuje pomyślne pobranie wszystkich użytkowników."""
    from tests.conftest import mock_iterator

    mock_doc1 = MagicMock(to_dict=MagicMock(return_value={"uid": "u1", "name": "User A"}))
    mock_doc2 = MagicMock(to_dict=MagicMock(return_value={"uid": "u2", "name": "User B"}))

    mock_db.collection.return_value.stream.return_value = mock_iterator([mock_doc1, mock_doc2])

    wynik = await RepozytoriumUzytkownikow.pobierz_wszystkich_uzytkownikow()

    assert len(wynik) == 2
    assert wynik[0] == {"uid": "u1", "name": "User A"}
    assert wynik[1] == {"uid": "u2", "name": "User B"}
    mock_db.collection.assert_called_once_with('users')
    mock_db.collection.return_value.stream.assert_called_once()


@pytest.mark.asyncio
async def test_pobierz_wszystkich_uzytkownikow_brak_danych(mock_db):
    """Testuje pobranie wszystkich użytkowników, gdy nie ma żadnych."""
    from tests.conftest import mock_iterator

    mock_db.collection.return_value.stream.return_value = mock_iterator([])

    wynik = await RepozytoriumUzytkownikow.pobierz_wszystkich_uzytkownikow()

    assert wynik == []
    mock_db.collection.assert_called_once_with('users')
    mock_db.collection.return_value.stream.assert_called_once()


@pytest.mark.asyncio
async def test_aktualizuj_uzytkownika_sukces(mock_db, mock_auth):
    """Testuje pomyślną aktualizację użytkownika."""
    user_id = "user_id_to_update"
    mock_doc_snapshot = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc_snapshot.exists = True
    mock_doc_snapshot.to_dict.return_value = {
        "uid": user_id, "email": "old@example.com", "name": "Old Name", "role": "student"
    }

    dane_do_aktualizacji = {
        "email": "new@example.com",
        "imie": "New Name",
        "rola": Rola.WYKLADOWCA
    }

    mock_firebase_user_record_get = MagicMock(spec=firebase_auth.UserRecord)
    mock_firebase_user_record_get.uid = user_id
    mock_auth.get_user.return_value = mock_firebase_user_record_get

    mock_firebase_user_record_update = MagicMock(spec=firebase_auth.UserRecord)
    mock_firebase_user_record_update.uid = user_id
    mock_auth.update_user.return_value = mock_firebase_user_record_update

    mock_doc_ref = mock_db.collection.return_value.document.return_value

    wynik = await RepozytoriumUzytkownikow.aktualizuj_uzytkownika(user_id, dane_do_aktualizacji)

    assert wynik is True

    mock_auth.update_user.assert_called_once_with(
        user_id,
        email="new@example.com",
        display_name="New Name"
    )
    mock_auth.set_custom_user_claims.assert_called_once_with(
        user_id,
        {"role": Rola.WYKLADOWCA.value}
    )
    mock_auth.get_user.assert_not_called()


    mock_db.collection.assert_called_once_with('users')
    mock_db.collection.return_value.document.assert_called_once_with(user_id)
    mock_doc_ref.get.assert_called_once()
    mock_doc_ref.update.assert_called_once()

    args, kwargs = mock_doc_ref.update.call_args
    assert 'email' in args[0] and args[0]['email'] == 'new@example.com'
    assert 'name' in args[0] and args[0]['name'] == 'New Name'
    assert 'role' in args[0] and args[0]['role'] == 'wykladowca'
    assert 'updated_at' in args[0] and isinstance(args[0]['updated_at'], type(firestore.SERVER_TIMESTAMP))


@pytest.mark.asyncio
async def test_aktualizuj_uzytkownika_nie_istnieje(mock_db, mock_auth):
    """Testuje aktualizację użytkownika, który nie istnieje."""
    user_id = "non_existent_id"
    dane_do_aktualizacji = {"imie": "New Name"}

    mock_doc_snapshot = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc_snapshot.exists = False

    wynik = await RepozytoriumUzytkownikow.aktualizuj_uzytkownika(user_id, dane_do_aktualizacji)

    assert wynik is False
    mock_db.collection.return_value.document.return_value.get.assert_called_once()
    mock_auth.update_user.assert_not_called()
    mock_auth.set_custom_user_claims.assert_not_called()
    mock_db.collection.return_value.document.return_value.update.assert_not_called()


@pytest.mark.asyncio
async def test_usun_uzytkownika_sukces(mock_db, mock_auth):
    """Testuje pomyślne usunięcie użytkownika."""
    user_id = "user_id_to_delete"

    wynik = await RepozytoriumUzytkownikow.usun_uzytkownika(user_id)

    assert wynik is True
    mock_auth.delete_user.assert_called_once_with(user_id)
    mock_db.collection.assert_called_once_with('users')
    mock_db.collection.return_value.document.assert_called_once_with(user_id)
    mock_db.collection.return_value.document.return_value.delete.assert_called_once()