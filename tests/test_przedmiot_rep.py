import pytest
from unittest.mock import MagicMock, AsyncMock
from app.repozytoria.przedmiot import RepozytoriumPrzedmiotow
from app.modele.przedmiot import Przedmiot, PrzedmiotTworzenie
from firebase_admin import firestore

from .conftest import mock_async_iterator, mock_iterator

@pytest.mark.asyncio
async def test_utworz_przedmiot_sukces(mock_db):
    """Testuje pomyślne utworzenie przedmiotu."""
    dane_przedmiotu = PrzedmiotTworzenie(nazwa="Matematyka", opis="Wstęp do analizy")

    mock_doc_ref = mock_db.collection.return_value.document.return_value
    mock_doc_ref.id = "nowy_przedmiot_id"

    wynik = await RepozytoriumPrzedmiotow.utworz_przedmiot(dane_przedmiotu)

    assert isinstance(wynik, Przedmiot)
    assert wynik.przedmiotId == "nowy_przedmiot_id"
    assert wynik.nazwa == "Matematyka"
    assert wynik.opis == "Wstęp do analizy"
    
    mock_db.collection.assert_called_once_with('subjects')
    mock_db.collection.return_value.document.assert_called_once()
    mock_doc_ref.set.assert_called_once()
    
    args, kwargs = mock_doc_ref.set.call_args
    assert 'id' in args[0] and args[0]['id'] == 'nowy_przedmiot_id'
    assert 'name' in args[0] and args[0]['name'] == 'Matematyka'
    assert 'description' in args[0] and args[0]['description'] == 'Wstęp do analizy'
    assert 'created_at' in args[0] and isinstance(args[0]['created_at'], type(firestore.SERVER_TIMESTAMP))


@pytest.mark.asyncio
async def test_pobierz_przedmiot_po_id_sukces(mock_db):
    """Testuje pomyślne pobranie przedmiotu po ID."""
    przedmiot_id = "test_przedmiot_id_1"
    oczekiwane_dane = {"id": przedmiot_id, "name": "Fizyka", "description": "Mechanika kwantowa"}

    mock_doc_snapshot = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc_snapshot.exists = True
    mock_doc_snapshot.to_dict.return_value = oczekiwane_dane

    wynik = await RepozytoriumPrzedmiotow.pobierz_przedmiot_po_id(przedmiot_id)

    assert wynik == oczekiwane_dane
    mock_db.collection.assert_called_once_with('subjects')
    mock_db.collection.return_value.document.assert_called_once_with(przedmiot_id)
    mock_doc_snapshot.to_dict.assert_called_once()


@pytest.mark.asyncio
async def test_pobierz_przedmiot_po_id_nie_istnieje(mock_db):
    """Testuje pobranie przedmiotu, który nie istnieje."""
    przedmiot_id = "non_existent_id"

    mock_doc_snapshot = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc_snapshot.exists = False
    mock_doc_snapshot.to_dict.return_value = None

    wynik = await RepozytoriumPrzedmiotow.pobierz_przedmiot_po_id(przedmiot_id)

    assert wynik is None
    mock_db.collection.assert_called_once_with('subjects')
    mock_db.collection.return_value.document.assert_called_once_with(przedmiot_id)
    mock_doc_snapshot.to_dict.assert_not_called()


@pytest.mark.asyncio
async def test_pobierz_wszystkie_przedmioty_sukces(mock_db):
    """Testuje pomyślne pobranie wszystkich przedmiotów."""
    mock_doc1 = MagicMock(to_dict=MagicMock(return_value={"id": "p1", "name": "Chemia"}))
    mock_doc2 = MagicMock(to_dict=MagicMock(return_value={"id": "p2", "name": "Biologia"}))

    mock_db.collection.return_value.stream.return_value = mock_iterator([mock_doc1, mock_doc2])

    wynik = await RepozytoriumPrzedmiotow.pobierz_wszystkie_przedmioty()

    assert len(wynik) == 2
    assert wynik[0] == {"id": "p1", "name": "Chemia"}
    assert wynik[1] == {"id": "p2", "name": "Biologia"}
    mock_db.collection.assert_called_once_with('subjects')
    mock_db.collection.return_value.stream.assert_called_once()


@pytest.mark.asyncio
async def test_pobierz_wszystkie_przedmioty_brak_danych(mock_db):
    """Testuje pobranie wszystkich przedmiotów, gdy nie ma żadnych."""
    mock_db.collection.return_value.stream.return_value = mock_iterator([])

    wynik = await RepozytoriumPrzedmiotow.pobierz_wszystkie_przedmioty()

    assert wynik == []
    mock_db.collection.assert_called_once_with('subjects')
    mock_db.collection.return_value.stream.assert_called_once()


@pytest.mark.asyncio
async def test_aktualizuj_przedmiot_sukces(mock_db):
    """Testuje pomyślną aktualizację przedmiotu."""
    przedmiot_id = "id_do_aktualizacji"
    dane_przedmiotu = PrzedmiotTworzenie(nazwa="Historia nowa", opis="Historia Polski od 1945")

    mock_doc_ref = mock_db.collection.return_value.document.return_value
    
    wynik = await RepozytoriumPrzedmiotow.aktualizuj_przedmiot(przedmiot_id, dane_przedmiotu)

    assert isinstance(wynik, Przedmiot)
    assert wynik.przedmiotId == przedmiot_id
    assert wynik.nazwa == "Historia nowa"
    assert wynik.opis == "Historia Polski od 1945"

    mock_db.collection.assert_called_once_with('subjects')
    mock_db.collection.return_value.document.assert_called_once_with(przedmiot_id)
    mock_doc_ref.update.assert_called_once()

    args, kwargs = mock_doc_ref.update.call_args
    assert 'name' in args[0] and args[0]['name'] == 'Historia nowa'
    assert 'description' in args[0] and args[0]['description'] == 'Historia Polski od 1945'
    assert 'updated_at' in args[0] and isinstance(args[0]['updated_at'], type(firestore.SERVER_TIMESTAMP))


@pytest.mark.asyncio
async def test_usun_przedmiot_sukces(mock_db):
    """Testuje pomyślne usunięcie przedmiotu."""
    przedmiot_id = "id_do_usuniecia"

    mock_doc_ref = mock_db.collection.return_value.document.return_value
    
    wynik = await RepozytoriumPrzedmiotow.usun_przedmiot(przedmiot_id)

    assert wynik is True
    mock_db.collection.assert_called_once_with('subjects')
    mock_db.collection.return_value.document.assert_called_once_with(przedmiot_id)
    mock_doc_ref.delete.assert_called_once()
