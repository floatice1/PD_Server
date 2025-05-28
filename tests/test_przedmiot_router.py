import pytest
from fastapi import status
from unittest.mock import MagicMock, AsyncMock, patch
from app.modele.przedmiot import Przedmiot, PrzedmiotTworzenie
from app.serwisy.przedmiot import SerwisPrzedmiotow
from app.routery.przedmiot import router as przedmiot_router
from main import app

@patch.object(SerwisPrzedmiotow, 'pobierz_wszystkie_przedmioty')
def test_pobierz_wszystkie_przedmioty_sukces(mock_pobierz_wszystkie, async_client):
    """Testuje pomyślne pobranie wszystkich przedmiotów."""
    oczekiwane_przedmioty = [
        {"przedmiotId": "p1", "nazwa": "Matematyka", "opis": "Algebra"},
        {"przedmiotId": "p2", "nazwa": "Fizyka", "opis": "Mechanika"}
    ]
    mock_pobierz_wszystkie.return_value = oczekiwane_przedmioty

    response = async_client.get("/przedmioty/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == oczekiwane_przedmioty
    mock_pobierz_wszystkie.assert_called_once()


@patch.object(SerwisPrzedmiotow, 'pobierz_wszystkie_przedmioty')
def test_pobierz_wszystkie_przedmioty_brak_danych(mock_pobierz_wszystkie, async_client):
    """Testuje pobranie wszystkich przedmiotów, gdy brak danych."""
    mock_pobierz_wszystkie.return_value = []

    response = async_client.get("/przedmioty/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    mock_pobierz_wszystkie.assert_called_once()


@patch.object(SerwisPrzedmiotow, 'pobierz_wszystkie_przedmioty')
def test_pobierz_wszystkie_przedmioty_blad_serwera(mock_pobierz_wszystkie, async_client):
    """Testuje błąd serwera podczas pobierania wszystkich przedmiotów."""
    mock_pobierz_wszystkie.side_effect = Exception("Coś poszło nie tak")

    response = async_client.get("/przedmioty/")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Błąd podczas pobierania listy przedmiotów" in response.json()["detail"]
    mock_pobierz_wszystkie.assert_called_once()


@patch.object(SerwisPrzedmiotow, 'pobierz_przedmiot_po_id')
def test_pobierz_przedmiot_sukces(mock_pobierz_przedmiot_po_id, async_client):
    """Testuje pomyślne pobranie konkretnego przedmiotu."""
    przedmiot_id = "abc123xyz"
    oczekiwany_przedmiot = {"przedmiotId": przedmiot_id, "nazwa": "Historia", "opis": "Średniowiecze"}
    mock_pobierz_przedmiot_po_id.return_value = oczekiwany_przedmiot

    response = async_client.get(f"/przedmioty/{przedmiot_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == oczekiwany_przedmiot
    mock_pobierz_przedmiot_po_id.assert_called_once_with(przedmiot_id)


@patch.object(SerwisPrzedmiotow, 'pobierz_przedmiot_po_id')
def test_pobierz_przedmiot_nie_znaleziono(mock_pobierz_przedmiot_po_id, async_client):
    """Testuje pobranie przedmiotu, który nie został znaleziony."""
    przedmiot_id = "non_existent_id"
    mock_pobierz_przedmiot_po_id.return_value = None

    response = async_client.get(f"/przedmioty/{przedmiot_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert f"Przedmiot o ID {przedmiot_id} nie został znaleziony" in response.json()["detail"]
    mock_pobierz_przedmiot_po_id.assert_called_once_with(przedmiot_id)


@patch.object(SerwisPrzedmiotow, 'pobierz_przedmiot_po_id')
def test_pobierz_przedmiot_blad_serwera(mock_pobierz_przedmiot_po_id, async_client):
    """Testuje błąd serwera podczas pobierania konkretnego przedmiotu."""
    przedmiot_id = "error_id"
    mock_pobierz_przedmiot_po_id.side_effect = Exception("Błąd DB")

    response = async_client.get(f"/przedmioty/{przedmiot_id}")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Błąd podczas pobierania przedmiotu" in response.json()["detail"]
    mock_pobierz_przedmiot_po_id.assert_called_once_with(przedmiot_id)


@patch.object(SerwisPrzedmiotow, 'utworz_przedmiot')
def test_utworz_przedmiot_sukces(mock_utworz_przedmiot, async_client):
    """Testuje pomyślne utworzenie przedmiotu."""
    dane_do_utworzenia = {"nazwa": "Angielski", "opis": "Konwersacje"}
    nowy_przedmiot_id = "new_przedmiot_id_456"
    mock_przedmiot_obiekt = Przedmiot(przedmiotId=nowy_przedmiot_id, **dane_do_utworzenia)
    mock_utworz_przedmiot.return_value = mock_przedmiot_obiekt

    response = async_client.post("/przedmioty/", json=dane_do_utworzenia)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == mock_przedmiot_obiekt.model_dump(mode='json')
    
    mock_utworz_przedmiot.assert_called_once()
    args, kwargs = mock_utworz_przedmiot.call_args
    przedmiot_stworzony = args[0]
    assert isinstance(przedmiot_stworzony, PrzedmiotTworzenie)
    assert przedmiot_stworzony.nazwa == dane_do_utworzenia["nazwa"]
    assert przedmiot_stworzony.opis == dane_do_utworzenia["opis"]


@patch.object(SerwisPrzedmiotow, 'utworz_przedmiot')
def test_utworz_przedmiot_nieprawidlowe_dane(mock_utworz_przedmiot, async_client):
    """Testuje tworzenie przedmiotu z nieprawidłowymi danymi."""
    dane_do_utworzenia = {"opis": "Opis bez nazwy"}

    response = async_client.post("/przedmioty/", json=dane_do_utworzenia)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    mock_utworz_przedmiot.assert_not_called()


@patch.object(SerwisPrzedmiotow, 'utworz_przedmiot')
def test_utworz_przedmiot_blad_serwera(mock_utworz_przedmiot, async_client):
    """Testuje błąd serwera podczas tworzenia przedmiotu."""
    dane_do_utworzenia = {"nazwa": "Błąd testowy", "opis": "Opis"}
    mock_utworz_przedmiot.side_effect = Exception("Błąd bazy danych")

    response = async_client.post("/przedmioty/", json=dane_do_utworzenia)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Błąd podczas tworzenia przedmiotu" in response.json()["detail"]
    mock_utworz_przedmiot.assert_called_once()


@patch.object(SerwisPrzedmiotow, 'aktualizuj_przedmiot')
def test_aktualizuj_przedmiot_sukces(mock_aktualizuj_przedmiot, async_client):
    """Testuje pomyślną aktualizację przedmiotu."""
    przedmiot_id = "przedmiot_do_aktualizacji"
    dane_aktualizacji = {"nazwa": "Nowa nazwa przedmiotu", "opis": "Zaktualizowany opis"}

    mock_aktualizuj_przedmiot.return_value = {
        "przedmiotId": przedmiot_id,
        "nazwa": "Nowa nazwa przedmiotu",
        "opis": "Zaktualizowany opis"
    }

    response = async_client.put(f"/przedmioty/{przedmiot_id}", json=dane_aktualizacji)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Przedmiot {przedmiot_id} zaktualizowany pomyślnie"
    assert response.json()["updated_data"]["nazwa"] == "Nowa nazwa przedmiotu"
    assert response.json()["updated_data"]["opis"] == "Zaktualizowany opis"
    mock_aktualizuj_przedmiot.assert_called_once_with(
        przedmiot_id,
        {"nazwa": "Nowa nazwa przedmiotu", "opis": "Zaktualizowany opis"}
    )


@patch.object(SerwisPrzedmiotow, 'aktualizuj_przedmiot')
def test_aktualizuj_przedmiot_nie_istnieje(mock_aktualizuj_przedmiot, async_client):
    """Testuje aktualizację przedmiotu, który nie istnieje."""
    przedmiot_id = "non_existent_item"
    dane_aktualizacji = {"nazwa": "Cokolwiek"}
    mock_aktualizuj_przedmiot.return_value = None

    response = async_client.put(f"/przedmioty/{przedmiot_id}", json=dane_aktualizacji)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert f"Przedmiot o ID {przedmiot_id} nie istnieje" in response.json()["detail"]
    mock_aktualizuj_przedmiot.assert_called_once_with(
        przedmiot_id,
        {"nazwa": "Cokolwiek"}
    )


@patch.object(SerwisPrzedmiotow, 'usun_przedmiot')
def test_usun_przedmiot_sukces(mock_usun_przedmiot, async_client):
    """Testuje pomyślne usunięcie przedmiotu."""
    przedmiot_id = "przedmiot_do_usuniecia"
    mock_usun_przedmiot.return_value = True

    response = async_client.delete(f"/przedmioty/{przedmiot_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Przedmiot {przedmiot_id} usunięty pomyślnie"
    mock_usun_przedmiot.assert_called_once_with(przedmiot_id)


@patch.object(SerwisPrzedmiotow, 'usun_przedmiot')
def test_usun_przedmiot_nie_znaleziono(mock_usun_przedmiot, async_client):
    """Testuje usunięcie przedmiotu, który nie został znaleziony."""
    przedmiot_id = "non_existent_delete_id"
    mock_usun_przedmiot.return_value = False

    response = async_client.delete(f"/przedmioty/{przedmiot_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert f"Przedmiot o ID {przedmiot_id} nie został znaleziony" in response.json()["detail"]
    mock_usun_przedmiot.assert_called_once_with(przedmiot_id)


@patch.object(SerwisPrzedmiotow, 'usun_przedmiot')
def test_usun_przedmiot_blad_serwera(mock_usun_przedmiot, async_client):
    """Testuje błąd serwera podczas usuwania przedmiotu."""
    przedmiot_id = "error_delete_id"
    mock_usun_przedmiot.side_effect = Exception("Błąd podczas operacji usuwania")

    response = async_client.delete(f"/przedmioty/{przedmiot_id}")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Błąd podczas usuwania przedmiotu" in response.json()["detail"]
    mock_usun_przedmiot.assert_called_once_with(przedmiot_id)