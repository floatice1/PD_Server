import pytest
from fastapi import status
from unittest.mock import patch, AsyncMock
from app.modele.ocena import Ocena, OcenaTworzenie
from app.serwisy.ocena import SerwisOcen
import datetime

sample_ocena_data = {
    "studentId": "s1",
    "grupaId": "g1",
    "wystawionePrzez": "w1",
    "wartoscOceny": "5.0"
}

sample_ocena_response = {
    "ocenaId": "o1",
    "timestamp": "2023-01-01T10:00:00.000Z",
    **sample_ocena_data
}

def ocena_to_json_serializable(ocena):
    if isinstance(ocena, dict):
        ocena_dict = ocena
    elif isinstance(ocena, Ocena):
        ocena_dict = ocena.model_dump(mode='json')
    else:
        return ocena

    if 'timestamp' in ocena_dict and isinstance(ocena_dict['timestamp'], datetime.datetime):
        ocena_dict['timestamp'] = ocena_dict['timestamp'].isoformat().replace('+00:00', 'Z')
    return ocena_dict


@patch.object(SerwisOcen, 'pobierz_wszystkie_oceny', new_callable=AsyncMock)
def test_pobierz_wszystkie_oceny_sukces(mock_pobierz_wszystkie, async_client):
    oczekiwane_oceny = [sample_ocena_response]
    mock_pobierz_wszystkie.return_value = oczekiwane_oceny

    response = async_client.get("/oceny/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == oczekiwane_oceny
    mock_pobierz_wszystkie.assert_called_once()

@patch.object(SerwisOcen, 'pobierz_wszystkie_oceny', new_callable=AsyncMock)
def test_pobierz_wszystkie_oceny_brak_danych(mock_pobierz_wszystkie, async_client):
    mock_pobierz_wszystkie.return_value = []

    response = async_client.get("/oceny/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    mock_pobierz_wszystkie.assert_called_once()

@patch.object(SerwisOcen, 'pobierz_wszystkie_oceny', new_callable=AsyncMock)
def test_pobierz_wszystkie_oceny_blad_serwera(mock_pobierz_wszystkie, async_client):
    mock_pobierz_wszystkie.side_effect = Exception("Błąd serwera")

    response = async_client.get("/oceny/")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Błąd podczas pobierania listy ocen" in response.json()["detail"]
    mock_pobierz_wszystkie.assert_called_once()

@patch.object(SerwisOcen, 'pobierz_ocene_po_id', new_callable=AsyncMock)
def test_pobierz_ocene_sukces(mock_pobierz_ocene_po_id, async_client):
    ocena_id = "o1"
    oczekiwana_ocena = sample_ocena_response
    mock_pobierz_ocene_po_id.return_value = oczekiwana_ocena

    response = async_client.get(f"/oceny/{ocena_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == oczekiwana_ocena
    mock_pobierz_ocene_po_id.assert_called_once_with(ocena_id)

@patch.object(SerwisOcen, 'pobierz_ocene_po_id', new_callable=AsyncMock)
def test_pobierz_ocene_nie_znaleziono(mock_pobierz_ocene_po_id, async_client):
    ocena_id = "nieistniejaca_ocena"
    mock_pobierz_ocene_po_id.return_value = None

    response = async_client.get(f"/oceny/{ocena_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert f"Ocena o ID {ocena_id} nie została znaleziona" in response.json()["detail"]
    mock_pobierz_ocene_po_id.assert_called_once_with(ocena_id)

@patch.object(SerwisOcen, 'pobierz_ocene_po_id', new_callable=AsyncMock)
def test_pobierz_ocene_blad_serwera(mock_pobierz_ocene_po_id, async_client):
    ocena_id = "o_err"
    mock_pobierz_ocene_po_id.side_effect = Exception("Błąd bazy danych")

    response = async_client.get(f"/oceny/{ocena_id}")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Błąd podczas pobierania oceny" in response.json()["detail"]
    mock_pobierz_ocene_po_id.assert_called_once_with(ocena_id)

@patch.object(SerwisOcen, 'utworz_ocene', new_callable=AsyncMock)
def test_utworz_ocene_sukces(mock_utworz_ocene, async_client):
    dane_do_utworzenia = sample_ocena_data
    nowa_ocena_id = "o2"
    mock_ocena_obiekt = Ocena(ocenaId=nowa_ocena_id, timestamp=datetime.datetime.utcnow(), **dane_do_utworzenia)
    mock_utworz_ocene.return_value = mock_ocena_obiekt

    response = async_client.post("/oceny/", json=dane_do_utworzenia)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == ocena_to_json_serializable(mock_ocena_obiekt)
    mock_utworz_ocene.assert_called_once()
    args, _ = mock_utworz_ocene.call_args
    assert isinstance(args[0], OcenaTworzenie)
    assert args[0].model_dump(exclude_unset=True) == dane_do_utworzenia

@patch.object(SerwisOcen, 'utworz_ocene', new_callable=AsyncMock)
def test_utworz_ocene_nieprawidlowe_dane(mock_utworz_ocene, async_client):
    dane_do_utworzenia = {
        "grupaId": "g1",
        "wystawionePrzez": "w1",
        "wartoscOceny": "5.0"
    }

    response = async_client.post("/oceny/", json=dane_do_utworzenia)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Błąd podczas tworzenia oceny" in response.json()["detail"]
    mock_utworz_ocene.assert_not_called()

@patch.object(SerwisOcen, 'utworz_ocene', new_callable=AsyncMock)
def test_utworz_ocene_blad_serwera(mock_utworz_ocene, async_client):
    dane_do_utworzenia = sample_ocena_data
    mock_utworz_ocene.side_effect = Exception("Błąd bazy danych")

    response = async_client.post("/oceny/", json=dane_do_utworzenia)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Błąd podczas tworzenia oceny" in response.json()["detail"]
    mock_utworz_ocene.assert_called_once()

@patch.object(SerwisOcen, 'aktualizuj_ocene', new_callable=AsyncMock)
@patch.object(SerwisOcen, 'pobierz_ocene_po_id', new_callable=AsyncMock)
def test_aktualizuj_ocene_sukces(mock_pobierz_ocene_po_id, mock_aktualizuj_ocene, async_client):
    ocena_id = "o1"
    dane_aktualizacji = {"wartoscOceny": "4.5"}
    zaktualizowana_ocena_dane = {**sample_ocena_response, **dane_aktualizacji}
    mock_aktualizuj_ocene.return_value = True
    mock_pobierz_ocene_po_id.return_value = zaktualizowana_ocena_dane

    response = async_client.put(f"/oceny/{ocena_id}", json=dane_aktualizacji)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Ocena {ocena_id} zaktualizowana pomyślnie"
    assert response.json()["updated_data"] == zaktualizowana_ocena_dane
    mock_aktualizuj_ocene.assert_called_once_with(ocena_id, dane_aktualizacji)
    mock_pobierz_ocene_po_id.assert_called_once_with(ocena_id)

@patch.object(SerwisOcen, 'aktualizuj_ocene', new_callable=AsyncMock)
@patch.object(SerwisOcen, 'pobierz_ocene_po_id', new_callable=AsyncMock)
def test_aktualizuj_ocene_nie_istnieje(mock_pobierz_ocene_po_id, mock_aktualizuj_ocene, async_client):
    ocena_id = "nieistniejaca_ocena"
    dane_aktualizacji = {"wartoscOceny": "4.0"}
    mock_aktualizuj_ocene.return_value = False
    mock_pobierz_ocene_po_id.return_value = None

    response = async_client.put(f"/oceny/{ocena_id}", json=dane_aktualizacji)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert f"Ocena o ID {ocena_id} nie istnieje" in response.json()["detail"]
    mock_aktualizuj_ocene.assert_called_once_with(ocena_id, dane_aktualizacji)
    mock_pobierz_ocene_po_id.assert_not_called()

@patch.object(SerwisOcen, 'aktualizuj_ocene', new_callable=AsyncMock)
@patch.object(SerwisOcen, 'pobierz_ocene_po_id', new_callable=AsyncMock)
def test_aktualizuj_ocene_puste_dane(mock_pobierz_ocene_po_id, mock_aktualizuj_ocene, async_client):
    ocena_id = "o1"
    dane_aktualizacji = {}
    mock_aktualizuj_ocene.side_effect = ValueError("Nie podano danych do aktualizacji")

    response = async_client.put(f"/oceny/{ocena_id}", json=dane_aktualizacji)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Błąd podczas aktualizacji oceny" in response.json()["detail"]
    mock_aktualizuj_ocene.assert_called_once_with(ocena_id, dane_aktualizacji) 
    mock_pobierz_ocene_po_id.assert_not_called()

@patch.object(SerwisOcen, 'aktualizuj_ocene', new_callable=AsyncMock)
@patch.object(SerwisOcen, 'pobierz_ocene_po_id', new_callable=AsyncMock)
def test_aktualizuj_ocene_blad_serwera(mock_pobierz_ocene_po_id, mock_aktualizuj_ocene, async_client):
    ocena_id = "o_err"
    dane_aktualizacji = {"wartoscOceny": "3.0"}
    mock_aktualizuj_ocene.side_effect = Exception("Błąd bazy danych")

    response = async_client.put(f"/oceny/{ocena_id}", json=dane_aktualizacji)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Błąd podczas aktualizacji oceny" in response.json()["detail"]
    mock_aktualizuj_ocene.assert_called_once_with(ocena_id, dane_aktualizacji)
    mock_pobierz_ocene_po_id.assert_not_called()

@patch.object(SerwisOcen, 'usun_ocene', new_callable=AsyncMock)
def test_usun_ocene_sukces(mock_usun_ocene, async_client):
    ocena_id = "o1"
    mock_usun_ocene.return_value = True

    response = async_client.delete(f"/oceny/{ocena_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Ocena {ocena_id} usunięta pomyślnie"
    mock_usun_ocene.assert_called_once_with(ocena_id)

@patch.object(SerwisOcen, 'usun_ocene', new_callable=AsyncMock)
def test_usun_ocene_nie_znaleziono(mock_usun_ocene, async_client):
    ocena_id = "nieistniejaca_ocena"
    mock_usun_ocene.return_value = False

    response = async_client.delete(f"/oceny/{ocena_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert f"Ocena o ID {ocena_id} nie została znaleziona" in response.json()["detail"]
    mock_usun_ocene.assert_called_once_with(ocena_id)

@patch.object(SerwisOcen, 'usun_ocene', new_callable=AsyncMock)
def test_usun_ocene_blad_serwera(mock_usun_ocene, async_client):
    ocena_id = "o_err"
    mock_usun_ocene.side_effect = Exception("Błąd bazy danych")

    response = async_client.delete(f"/oceny/{ocena_id}")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Błąd podczas usuwania oceny" in response.json()["detail"]
    mock_usun_ocene.assert_called_once_with(ocena_id)
