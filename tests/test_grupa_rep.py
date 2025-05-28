import pytest
from unittest.mock import AsyncMock, MagicMock
from app.repozytoria.grupa_rep import RepozytoriumGrup
from app.modele.grupa import GrupaTworzenie, Grupa
from firebase_admin import firestore

firestore.SERVER_TIMESTAMP = "mocked_timestamp"

@pytest.fixture(autouse=True)
def mock_db(mocker):
    """Fixture to mock the Firestore db object."""
    mock_firestore_db = MagicMock()
    mocker.patch('app.repozytoria.grupa_rep.db', mock_firestore_db)
    return mock_firestore_db

@pytest.mark.asyncio
async def test_utworz_grupe_sukces(mock_db):
    """Testuje pomyślne utworzenie grupy."""
    mock_doc_ref = MagicMock()
    mock_doc_ref.id = "nowe_id_grupy"

    mock_collection_ref = MagicMock()
    mock_collection_ref.document.return_value = mock_doc_ref

    mock_subject_doc = MagicMock()
    mock_subject_doc.exists = True
    mock_subject_doc_ref = MagicMock()
    mock_subject_doc_ref.get = MagicMock(return_value=mock_subject_doc)

    def collection_side_effect(name):
        if name == RepozytoriumGrup.COLLECTION_NAME:
            return mock_collection_ref
        elif name == 'subjects':
            mock_subjects_collection = MagicMock()
            mock_subjects_collection.document.return_value = mock_subject_doc_ref
            return mock_subjects_collection
        return MagicMock()

    mock_db.collection.side_effect = collection_side_effect

    dane_grupy = GrupaTworzenie(
        nazwa="Testowa Grupa",
        przedmiotId="przedmiot_abc",
        wykladowcaId="wykladowca_xyz"
    )

    grupa = await RepozytoriumGrup.utworz_grupe(dane_grupy)

    assert isinstance(grupa, Grupa)
    assert grupa.grupaId == "nowe_id_grupy"
    assert grupa.nazwa == "Testowa Grupa"
    assert grupa.przedmiotId == "przedmiot_abc"
    assert grupa.wykladowcaId == "wykladowca_xyz"
    assert grupa.studenciIds == []

    mock_db.collection.assert_any_call(RepozytoriumGrup.COLLECTION_NAME)
    mock_db.collection.assert_any_call('subjects')
    mock_collection_ref.document.assert_called_once_with()
    mock_doc_ref.set.assert_called_once_with({
        'id': "nowe_id_grupy",
        'name': "Testowa Grupa",
        'subjectId': "przedmiot_abc",
        'lecturerId': "wykladowca_xyz",
        'studentsIds': [],
        'createdAt': "mocked_timestamp"
    })

@pytest.mark.asyncio
async def test_utworz_grupe_przedmiot_nie_istnieje(mock_db):
    """Testuje błąd przy tworzeniu grupy z nieistniejącym ID przedmiotu."""
    mock_subject_doc_result = MagicMock()
    mock_subject_doc_result.exists = False

    mock_subject_doc_ref = MagicMock()
    mock_subject_doc_ref.get = MagicMock(return_value=mock_subject_doc_result)

    mock_subjects_collection = MagicMock()
    mock_subjects_collection.document.return_value = mock_subject_doc_ref

    mock_groups_collection = MagicMock()

    def collection_side_effect(name):
        if name == 'subjects':
            return mock_subjects_collection
        elif name == RepozytoriumGrup.COLLECTION_NAME:
            return mock_groups_collection
        return MagicMock()

    mock_db.collection.side_effect = collection_side_effect

    dane_grupy = GrupaTworzenie(
        nazwa="Grupa z Błędnym Przedmiotem",
        przedmiotId="nie_istniejacy_przedmiot",
        wykladowcaId="wykladowca_xyz"
    )

    with pytest.raises(ValueError, match="Przedmiot o ID nie_istniejacy_przedmiot nie istnieje"):
        await RepozytoriumGrup.utworz_grupe(dane_grupy)

@pytest.mark.asyncio
async def test_pobierz_grupe_po_id_sukces(mock_db):
    """Testuje pomyślne pobranie grupy po ID."""
    mock_grupa_data = {
        'id': "istniejace_id_grupy",
        'name': "Istniejąca Grupa",
        'subjectId': "przedmiot_def",
        'lecturerId': "wykladowca_uvw",
        'studentsIds': ["student1", "student2"]
    }

    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = mock_grupa_data

    mock_doc_ref = MagicMock()
    mock_doc_ref.get = MagicMock(return_value=mock_doc)

    mock_collection_ref = MagicMock()
    mock_collection_ref.document.return_value = mock_doc_ref

    mock_db.collection.return_value = mock_collection_ref

    grupa_id = "istniejace_id_grupy"
    grupa_data = await RepozytoriumGrup.pobierz_grupe_po_id(grupa_id)

    assert grupa_data == mock_grupa_data

    mock_db.collection.assert_called_once_with(RepozytoriumGrup.COLLECTION_NAME)
    mock_collection_ref.document.assert_called_once_with(grupa_id)
    mock_doc_ref.get.assert_called_once_with()

@pytest.mark.asyncio
async def test_pobierz_grupe_po_id_nie_istnieje(mock_db):
    """Testuje pobranie grupy, która nie istnieje."""
    mock_doc = MagicMock()
    mock_doc.exists = False

    mock_doc_ref = MagicMock()
    mock_doc_ref.get = MagicMock(return_value=mock_doc)

    mock_collection_ref = MagicMock()
    mock_collection_ref.document.return_value = mock_doc_ref

    mock_db.collection.return_value = mock_collection_ref

    grupa_id = "nie_istniejace_id_grupy"
    grupa_data = await RepozytoriumGrup.pobierz_grupe_po_id(grupa_id)

    assert grupa_data is None

    mock_db.collection.assert_called_once_with(RepozytoriumGrup.COLLECTION_NAME)
    mock_collection_ref.document.assert_called_once_with(grupa_id)
    mock_doc_ref.get.assert_called_once_with()

@pytest.mark.asyncio
async def test_pobierz_wszystkie_grupy_sukces(mock_db):
    """Testuje pomyślne pobranie wszystkich grup bez zmiany funkcji."""
    mock_grupy_data = [
        {
            'id': "grupa1",
            'name': "Grupa A",
            'subjectId': "przedmiot_x",
            'lecturerId': "wykladowca_1",
            'studentsIds': ["student_a", "student_b"]
        },
        {
            'id': "grupa2",
            'name': "Grupa B",
            'subjectId': "przedmiot_y",
            'lecturerId': "wykladowca_2",
            'studentsIds': []
        }
    ]

    mock_doc1 = MagicMock()
    mock_doc1.to_dict.return_value = mock_grupy_data[0]
    mock_doc2 = MagicMock()
    mock_doc2.to_dict.return_value = mock_grupy_data[1]

    def mock_stream():
        yield mock_doc1
        yield mock_doc2

    mock_collection_ref = MagicMock()
    mock_collection_ref.stream = MagicMock(return_value=mock_stream())

    mock_db.collection.return_value = mock_collection_ref

    wszystkie_grupy = await RepozytoriumGrup.pobierz_wszystkie_grupy()

    assert wszystkie_grupy == mock_grupy_data

    mock_db.collection.assert_called_once_with(RepozytoriumGrup.COLLECTION_NAME)
    mock_collection_ref.stream.assert_called_once_with()

@pytest.mark.asyncio
async def test_aktualizuj_grupe_wykladowca_nie_istnieje(mock_db):
    """Testuje aktualizację grupy z nieistniejącym ID wykładowcy."""
    mock_grupa_doc = MagicMock()
    mock_grupa_doc.exists = True
    
    mock_wykladowca_doc = MagicMock()
    mock_wykladowca_doc.exists = False

    mock_grupa_ref = MagicMock()
    mock_grupa_ref.get = MagicMock(return_value=mock_grupa_doc)

    mock_wykladowca_ref = MagicMock()
    mock_wykladowca_ref.get = MagicMock(return_value=mock_wykladowca_doc)

    def collection_side_effect(name):
        if name == RepozytoriumGrup.COLLECTION_NAME:
            return MagicMock(document=MagicMock(return_value=mock_grupa_ref))
        elif name == 'users':
            return MagicMock(document=MagicMock(return_value=mock_wykladowca_ref))
        return MagicMock()

    mock_db.collection.side_effect = collection_side_effect

    with pytest.raises(ValueError, match="Użytkownik o ID zlyWykladowca nie istnieje"):
        await RepozytoriumGrup.aktualizuj_grupe("grupa1", {"wykladowcaId": "zlyWykladowca"})

@pytest.mark.asyncio
async def test_aktualizuj_grupe_uzytkownik_nie_jest_wykladowca(mock_db):
    """Testuje aktualizację grupy z ID użytkownika, który nie jest wykładowcą."""
    mock_grupa_doc = MagicMock()
    mock_grupa_doc.exists = True
    
    mock_wykladowca_doc = MagicMock()
    mock_wykladowca_doc.exists = True
    mock_wykladowca_doc.to_dict.return_value = {'role': 'student'}

    mock_grupa_ref = MagicMock()
    mock_grupa_ref.get = MagicMock(return_value=mock_grupa_doc)

    mock_wykladowca_ref = MagicMock()
    mock_wykladowca_ref.get = MagicMock(return_value=mock_wykladowca_doc)

    def collection_side_effect(name):
        if name == RepozytoriumGrup.COLLECTION_NAME:
            return MagicMock(document=MagicMock(return_value=mock_grupa_ref))
        elif name == 'users':
            return MagicMock(document=MagicMock(return_value=mock_wykladowca_ref))
        return MagicMock()

    mock_db.collection.side_effect = collection_side_effect

    with pytest.raises(ValueError, match="Użytkownik o ID nieWykladowca nie jest wykładowcą"):
        await RepozytoriumGrup.aktualizuj_grupe("grupa1", {"wykladowcaId": "nieWykladowca"})

@pytest.mark.asyncio
async def test_przypisz_studenta_do_grupy_uzytkownik_nie_istnieje(mock_db):
    """Testuje przypisanie nieistniejącego użytkownika jako studenta."""
    mock_user_doc = MagicMock()
    mock_user_doc.exists = False
    mock_db.collection.return_value.document.return_value.get = MagicMock(return_value=mock_user_doc)

    with pytest.raises(ValueError, match="Użytkownik o ID zlyStudent nie istnieje"):
        await RepozytoriumGrup.przypisz_studenta_do_grupy("grupa1", "zlyStudent")

@pytest.mark.asyncio
async def test_usun_studenta_z_grupy_nie_student(mock_db):
    """Testuje usunięcie użytkownika, który nie jest studentem."""
    mock_user_doc = MagicMock()
    mock_user_doc.exists = True
    mock_user_doc.to_dict.return_value = {'role': 'wykladowca'}
    mock_db.collection.return_value.document.return_value.get = MagicMock(return_value=mock_user_doc)

    with pytest.raises(ValueError, match="Użytkownik o ID nieStudent nie jest studentem"):
        await RepozytoriumGrup.usun_studenta_z_grupy("grupa1", "nieStudent")

@pytest.mark.asyncio
async def test_zmien_wykladowce_grupy_uzytkownik_nie_istnieje(mock_db):
    """Testuje zmianę na nieistniejącego użytkownika jako wykładowcę."""
    mock_user_doc = MagicMock()
    mock_user_doc.exists = False
    mock_db.collection.return_value.document.return_value.get = MagicMock(return_value=mock_user_doc)

    with pytest.raises(ValueError, match="Użytkownik o ID zlyWykladowca nie istnieje"):
        await RepozytoriumGrup.zmien_wykladowce_grupy("grupa1", "zlyWykladowca")

@pytest.mark.asyncio
async def test_aktualizuj_grupe_wiele_pol(mock_db):
    """Testuje aktualizację wielu pól grupy jednocześnie."""
    dane_aktualizacji = {
        "nazwa": "Nowa Nazwa",
        "przedmiotId": "nowyPrzedmiot1",
        "wykladowcaId": "nowyWykladowca1"
    }
    
    mock_grupa_doc = MagicMock()
    mock_grupa_doc.exists = True
    
    mock_subject_doc = MagicMock()
    mock_subject_doc.exists = True

    mock_lecturer_doc = MagicMock()
    mock_lecturer_doc.exists = True
    mock_lecturer_doc.to_dict.return_value = {'role': 'wykladowca'}

    mock_grupa_ref = MagicMock()
    mock_grupa_ref.get = MagicMock(return_value=mock_grupa_doc)

    mock_subject_ref = MagicMock(get=MagicMock(return_value=mock_subject_doc))
    mock_lecturer_ref = MagicMock(get=MagicMock(return_value=mock_lecturer_doc))

    def collection_side_effect(name):
        if name == RepozytoriumGrup.COLLECTION_NAME:
            return MagicMock(document=MagicMock(return_value=mock_grupa_ref))
        elif name == 'subjects':
            return MagicMock(document=MagicMock(return_value=mock_subject_ref))
        elif name == 'users':
            return MagicMock(document=MagicMock(return_value=mock_lecturer_ref))
        return MagicMock()

    mock_db.collection.side_effect = collection_side_effect

    wynik = await RepozytoriumGrup.aktualizuj_grupe("grupa1", dane_aktualizacji)

    assert wynik is True
    mock_grupa_ref.update.assert_called_once_with({
        'name': 'Nowa Nazwa',
        'subjectId': 'nowyPrzedmiot1',
        'lecturerId': 'nowyWykladowca1',
        'updatedAt': 'mocked_timestamp'
    })

    mock_subject_ref.get.assert_called_once()
    mock_lecturer_ref.get.assert_called_once()