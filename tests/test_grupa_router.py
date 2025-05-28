import pytest
from fastapi import status
from unittest.mock import patch, AsyncMock
from app.modele.grupa import Grupa, GrupaTworzenie, GrupaAktualizacja
from app.serwisy.grupa_serw import SerwisGrup

@patch.object(SerwisGrup, 'pobierz_wszystkie_grupy', new_callable=AsyncMock)
def test_pobierz_wszystkie_grupy_sukces(mock_pobierz_wszystkie, async_client):
    oczekiwane_grupy = [
        {"grupaId": "g1", "nazwa": "Grupa A", "przedmiotId": "p1", "wykladowcaId": "w1", "studenciIds": []},
        {"grupaId": "g2", "nazwa": "Grupa B", "przedmiotId": "p2", "wykladowcaId": "w2", "studenciIds": ["s1"]}
    ]
    mock_pobierz_wszystkie.return_value = oczekiwane_grupy

    response = async_client.get("/grupy/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == oczekiwane_grupy
    mock_pobierz_wszystkie.assert_called_once()

@patch.object(SerwisGrup, 'pobierz_wszystkie_grupy', new_callable=AsyncMock)
def test_pobierz_wszystkie_grupy_brak_danych(mock_pobierz_wszystkie, async_client):
    mock_pobierz_wszystkie.return_value = []

    response = async_client.get("/grupy/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    mock_pobierz_wszystkie.assert_called_once()

@patch.object(SerwisGrup, 'pobierz_wszystkie_grupy', new_callable=AsyncMock)
def test_pobierz_wszystkie_grupy_blad_serwera(mock_pobierz_wszystkie, async_client):
    mock_pobierz_wszystkie.side_effect = Exception("Błąd serwera")

    response = async_client.get("/grupy/")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Błąd podczas pobierania listy grup" in response.json()["detail"]
    mock_pobierz_wszystkie.assert_called_once()

@patch.object(SerwisGrup, 'pobierz_grupe_po_id', new_callable=AsyncMock)
def test_pobierz_grupe_sukces(mock_pobierz_grupe_po_id, async_client):
    grupa_id = "g1"
    oczekiwana_grupa = {"grupaId": grupa_id, "nazwa": "Grupa A", "przedmiotId": "p1", "wykladowcaId": "w1", "studenciIds": []}
    mock_pobierz_grupe_po_id.return_value = oczekiwana_grupa

    response = async_client.get(f"/grupy/{grupa_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == oczekiwana_grupa
    mock_pobierz_grupe_po_id.assert_called_once_with(grupa_id)

@patch.object(SerwisGrup, 'pobierz_grupe_po_id', new_callable=AsyncMock)
def test_pobierz_grupe_nie_znaleziono(mock_pobierz_grupe_po_id, async_client):
    grupa_id = "nieistniejaca_grupa"
    mock_pobierz_grupe_po_id.return_value = None

    response = async_client.get(f"/grupy/{grupa_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert f"Grupa o ID {grupa_id} nie została znaleziona" in response.json()["detail"]
    mock_pobierz_grupe_po_id.assert_called_once_with(grupa_id)

@patch.object(SerwisGrup, 'utworz_grupe', new_callable=AsyncMock)
def test_utworz_grupe_sukces(mock_utworz_grupe, async_client):
    dane_do_utworzenia = {"nazwa": "Nowa Grupa", "przedmiotId": "p3"}
    nowa_grupa_id = "g3"
    mock_grupa_obiekt = Grupa(grupaId=nowa_grupa_id, studenciIds=[], **dane_do_utworzenia)
    mock_utworz_grupe.return_value = mock_grupa_obiekt

    response = async_client.post("/grupy/", json=dane_do_utworzenia)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == mock_grupa_obiekt.model_dump(mode='json')
    mock_utworz_grupe.assert_called_once()
    args, _ = mock_utworz_grupe.call_args
    assert isinstance(args[0], GrupaTworzenie)
    assert args[0].nazwa == dane_do_utworzenia["nazwa"]

@patch.object(SerwisGrup, 'utworz_grupe', new_callable=AsyncMock)
def test_utworz_grupe_nieprawidlowe_dane(mock_utworz_grupe, async_client):
    dane_do_utworzenia = {"nazwa": "Brakuje przedmiotu"}

    response = async_client.post("/grupy/", json=dane_do_utworzenia)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    mock_utworz_grupe.assert_not_called()

@patch.object(SerwisGrup, 'utworz_grupe', new_callable=AsyncMock)
def test_utworz_grupe_blad_serwera(mock_utworz_grupe, async_client):
    dane_do_utworzenia = {"nazwa": "Grupa Błąd", "przedmiotId": "p_err"}
    mock_utworz_grupe.side_effect = Exception("Błąd bazy danych")

    response = async_client.post("/grupy/", json=dane_do_utworzenia)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Błąd podczas tworzenia grupy" in response.json()["detail"]
    mock_utworz_grupe.assert_called_once()

@patch.object(SerwisGrup, 'aktualizuj_grupe', new_callable=AsyncMock)
def test_aktualizuj_grupe_sukces(mock_aktualizuj_grupe, async_client):
    grupa_id = "g1"
    dane_aktualizacji = {"nazwa": "Zaktualizowana Grupa A"}
    zaktualizowana_grupa_dane = {"grupaId": grupa_id, "nazwa": "Zaktualizowana Grupa A", "przedmiotId": "p1", "wykladowcaId": "w1", "studenciIds": []}
    mock_aktualizuj_grupe.return_value = zaktualizowana_grupa_dane

    response = async_client.put(f"/grupy/{grupa_id}", json=dane_aktualizacji)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Grupa {grupa_id} zaktualizowana pomyślnie"
    assert response.json()["updated_data"] == zaktualizowana_grupa_dane
    mock_aktualizuj_grupe.assert_called_once_with(grupa_id, dane_aktualizacji)

@patch.object(SerwisGrup, 'aktualizuj_grupe', new_callable=AsyncMock)
def test_aktualizuj_grupe_nie_istnieje(mock_aktualizuj_grupe, async_client):
    grupa_id = "nieistniejaca_grupa"
    dane_aktualizacji = {"nazwa": "Test"}
    mock_aktualizuj_grupe.return_value = None

    response = async_client.put(f"/grupy/{grupa_id}", json=dane_aktualizacji)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert f"Grupa o ID {grupa_id} nie istnieje" in response.json()["detail"]
    mock_aktualizuj_grupe.assert_called_once_with(grupa_id, dane_aktualizacji)

@patch.object(SerwisGrup, 'aktualizuj_grupe', new_callable=AsyncMock)
def test_aktualizuj_grupe_puste_dane(mock_aktualizuj_grupe, async_client):
    grupa_id = "g1"
    dane_aktualizacji = {}

    response = async_client.put(f"/grupy/{grupa_id}", json=dane_aktualizacji)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Nie podano danych do aktualizacji" in response.json()["detail"]

@patch.object(SerwisGrup, 'usun_grupe', new_callable=AsyncMock)
def test_usun_grupe_sukces(mock_usun_grupe, async_client):
    grupa_id = "g1"
    mock_usun_grupe.return_value = True

    response = async_client.delete(f"/grupy/{grupa_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Grupa {grupa_id} usunięta pomyślnie"
    mock_usun_grupe.assert_called_once_with(grupa_id)

@patch.object(SerwisGrup, 'usun_grupe', new_callable=AsyncMock)
def test_usun_grupe_nie_znaleziono(mock_usun_grupe, async_client):
    grupa_id = "nieistniejaca_grupa"
    mock_usun_grupe.return_value = False

    response = async_client.delete(f"/grupy/{grupa_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert f"Grupa o ID {grupa_id} nie została znaleziona" in response.json()["detail"]
    mock_usun_grupe.assert_called_once_with(grupa_id)

@patch.object(SerwisGrup, 'przypisz_studenta_do_grupy', new_callable=AsyncMock)
def test_przypisz_studenta_do_grupy_sukces(mock_przypisz_studenta, async_client):
    grupa_id = "g1"
    student_id = "s1"
    mock_przypisz_studenta.return_value = True

    response = async_client.post(f"/grupy/{grupa_id}/studenci/{student_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Student {student_id} przypisany do grupy {grupa_id} pomyślnie"
    mock_przypisz_studenta.assert_called_once_with(grupa_id, student_id)

@patch.object(SerwisGrup, 'przypisz_studenta_do_grupy', new_callable=AsyncMock)
def test_przypisz_studenta_do_grupy_nie_znaleziono_grupy(mock_przypisz_studenta, async_client):
    grupa_id = "nieistniejaca_grupa"
    student_id = "s1"
    mock_przypisz_studenta.return_value = False

    response = async_client.post(f"/grupy/{grupa_id}/studenci/{student_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert f"Grupa o ID {grupa_id} nie została znaleziona" in response.json()["detail"]
    mock_przypisz_studenta.assert_called_once_with(grupa_id, student_id)

@patch.object(SerwisGrup, 'usun_studenta_z_grupy', new_callable=AsyncMock)
def test_usun_studenta_z_grupy_sukces(mock_usun_studenta, async_client):
    grupa_id = "g1"
    student_id = "s1"
    mock_usun_studenta.return_value = True

    response = async_client.delete(f"/grupy/{grupa_id}/studenci/{student_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Student {student_id} usunięty z grupy {grupa_id} pomyślnie"
    mock_usun_studenta.assert_called_once_with(grupa_id, student_id)

@patch.object(SerwisGrup, 'usun_studenta_z_grupy', new_callable=AsyncMock)
def test_usun_studenta_z_grupy_nie_znaleziono(mock_usun_studenta, async_client):
    grupa_id = "g1"
    student_id = "nieistniejacy_student"
    mock_usun_studenta.return_value = False

    response = async_client.delete(f"/grupy/{grupa_id}/studenci/{student_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "lub student nie jest przypisany do grupy" in response.json()["detail"]
    mock_usun_studenta.assert_called_once_with(grupa_id, student_id)