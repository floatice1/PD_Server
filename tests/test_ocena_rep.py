import pytest
from unittest.mock import MagicMock, MagicMock, call

from app.modele.ocena import Ocena, OcenaTworzenie
from app.repozytoria.ocena import RepozytoriumOcen

from .conftest import mock_iterator, mock_iterator

pytestmark = pytest.mark.asyncio

@pytest.fixture(autouse=True)
def mock_db(mocker):
    """Fixture do mockowania obiektu db Firestore i modułu firestore."""
    mock_firestore_db = MagicMock()
    mocker.patch('app.repozytoria.ocena.db', mock_firestore_db)
    
    mock_firestore_module = MagicMock()
    mock_firestore_module.SERVER_TIMESTAMP = 'SERVER_TIMESTAMP_MOCK'
    mocker.patch('app.repozytoria.ocena.firestore', mock_firestore_module)
    return mock_firestore_db

@pytest.mark.asyncio
async def test_utworz_ocene_sukces(mock_db):
    """Testuje pomyślne tworzenie nowej oceny."""
    dane_oceny = OcenaTworzenie(studentId="student1", grupaId="grupa1", wartoscOceny="4.5", wystawionePrzez="wykladowca1")

    mock_student_doc = MagicMock(exists=True)
    mock_group_doc = MagicMock(exists=True)
    mock_group_doc.to_dict.return_value = {'studentsIds': ['student1', 'student2']}
    
    mock_ocena_doc_ref = MagicMock(id="nowaOcena123")
    mock_ocena_doc_ref.set = MagicMock()

    def collection_side_effect(name):
        if name == 'users':
            return MagicMock(document=MagicMock(return_value=MagicMock(get=MagicMock(return_value=mock_student_doc))))
        elif name == 'groups':
            return MagicMock(document=MagicMock(return_value=MagicMock(get=MagicMock(return_value=mock_group_doc))))
        elif name == RepozytoriumOcen.COLLECTION_NAME:
            return MagicMock(document=MagicMock(return_value=mock_ocena_doc_ref))
        return MagicMock()

    mock_db.collection.side_effect = collection_side_effect

    wynik = await RepozytoriumOcen.utworz_ocene(dane_oceny)

    assert wynik.ocenaId == "nowaOcena123"
    assert wynik.studentId == "student1"
    assert wynik.wartoscOceny == "4.5"

    mock_ocena_doc_ref.set.assert_called_once_with({
        'id': "nowaOcena123",
        'studentId': dane_oceny.studentId,
        'groupId': dane_oceny.grupaId,
        'value': dane_oceny.wartoscOceny,
        'created_at': 'SERVER_TIMESTAMP_MOCK',
        'givenBy': dane_oceny.wystawionePrzez
    })

@pytest.mark.asyncio
async def test_utworz_ocene_student_nie_istnieje(mock_db):
    """Testuje błąd, gdy student nie istnieje."""
    dane_oceny = OcenaTworzenie(studentId="nieistniejacy", grupaId="grupa1", wartoscOceny="4.0", wystawionePrzez="wykladowca1")
    mock_student_doc = MagicMock(exists=False)
    mock_db.collection.return_value.document.return_value.get = MagicMock(return_value=mock_student_doc)

    with pytest.raises(ValueError, match="Student o ID nieistniejacy nie istnieje"):
        await RepozytoriumOcen.utworz_ocene(dane_oceny)

@pytest.mark.asyncio
async def test_utworz_ocene_grupa_nie_istnieje(mock_db):
    """Testuje błąd, gdy grupa nie istnieje."""
    dane_oceny = OcenaTworzenie(studentId="student1", grupaId="nieistniejaca", wartoscOceny="4.0", wystawionePrzez="wykladowca1")
    mock_student_doc = MagicMock(exists=True)
    mock_group_doc = MagicMock(exists=False)
    
    def get_side_effect(*args, **kwargs):
        if 'nieistniejaca' in str(args) or 'nieistniejaca' in str(kwargs):
             return mock_group_doc
        return mock_student_doc

    mock_get = MagicMock(side_effect=[mock_student_doc, mock_group_doc])
    mock_db.collection.return_value.document.return_value.get = mock_get


    with pytest.raises(ValueError, match="Grupa o ID nieistniejaca nie istnieje"):
        await RepozytoriumOcen.utworz_ocene(dane_oceny)

@pytest.mark.asyncio
async def test_utworz_ocene_student_nie_w_grupie(mock_db):
    """Testuje błąd, gdy student nie należy do grupy."""
    dane_oceny = OcenaTworzenie(studentId="student3", grupaId="grupa1", wartoscOceny="4.0", wystawionePrzez="wykladowca1")
    mock_student_doc = MagicMock(exists=True)
    mock_group_doc = MagicMock(exists=True)
    mock_group_doc.to_dict.return_value = {'studentsIds': ['student1', 'student2']}

    mock_get = MagicMock(side_effect=[mock_student_doc, mock_group_doc])
    mock_db.collection.return_value.document.return_value.get = mock_get

    with pytest.raises(ValueError, match="Student o ID student3 nie należy do grupy"):
        await RepozytoriumOcen.utworz_ocene(dane_oceny)

@pytest.mark.asyncio
async def test_pobierz_ocene_po_id_sukces(mock_db):
    """Testuje pomyślne pobranie oceny po ID."""
    mock_data = {"id": "ocena1", "value": "5.0"}
    mock_doc = MagicMock(exists=True)
    mock_doc.to_dict.return_value = mock_data
    mock_db.collection.return_value.document.return_value.get = MagicMock(return_value=mock_doc)

    wynik = await RepozytoriumOcen.pobierz_ocene_po_id("ocena1")
    assert wynik == mock_data

@pytest.mark.asyncio
async def test_pobierz_ocene_po_id_nie_istnieje(mock_db):
    """Testuje pobranie nieistniejącej oceny."""
    mock_doc = MagicMock(exists=False)
    mock_db.collection.return_value.document.return_value.get = MagicMock(return_value=mock_doc)

    wynik = await RepozytoriumOcen.pobierz_ocene_po_id("nieistniejaca")
    assert wynik is None

@pytest.mark.asyncio
async def test_pobierz_oceny_studenta_sukces(mock_db):
    """Testuje pobranie ocen dla studenta."""
    mock_doc1 = MagicMock(to_dict=MagicMock(return_value={"id": "o1", "value": "5"}))
    mock_doc2 = MagicMock(to_dict=MagicMock(return_value={"id": "o2", "value": "4"}))
    
    mock_db.collection.return_value.where.return_value.stream = MagicMock(
        return_value=mock_iterator([mock_doc1, mock_doc2])
    )

    wynik = await RepozytoriumOcen.pobierz_oceny_studenta("student1")

    assert len(wynik) == 2
    assert wynik[0] == {"id": "o1", "value": "5"}
    mock_db.collection.return_value.where.assert_called_once_with('studentId', '==', 'student1')

@pytest.mark.asyncio
async def test_pobierz_oceny_z_grupy_sukces(mock_db):
    """Testuje pobranie ocen dla grupy."""
    mock_doc1 = MagicMock(to_dict=MagicMock(return_value={"id": "o1", "value": "5"}))
    
    mock_db.collection.return_value.where.return_value.stream = MagicMock(
        return_value=mock_iterator([mock_doc1])
    )

    wynik = await RepozytoriumOcen.pobierz_oceny_z_grupy("grupa1")

    assert len(wynik) == 1
    assert wynik[0] == {"id": "o1", "value": "5"}
    mock_db.collection.return_value.where.assert_called_once_with('groupId', '==', 'grupa1')

@pytest.mark.asyncio
async def test_pobierz_wszystkie_oceny_sukces(mock_db):
    """Testuje pobranie wszystkich ocen."""
    mock_doc1 = MagicMock(to_dict=MagicMock(return_value={"id": "o1"}))
    mock_doc2 = MagicMock(to_dict=MagicMock(return_value={"id": "o2"}))
    
    mock_db.collection.return_value.stream = MagicMock(
        return_value=mock_iterator([mock_doc1, mock_doc2])
    )

    wynik = await RepozytoriumOcen.pobierz_wszystkie_oceny()

    assert len(wynik) == 2

@pytest.mark.asyncio
async def test_aktualizuj_ocene_sukces(mock_db):
    """Testuje pomyślną aktualizację oceny."""
    mock_ocena_doc = MagicMock(exists=True)
    mock_ocena_doc.to_dict.return_value = {'studentId': 's1', 'groupId': 'g1'}
    
    mock_grupa_doc = MagicMock(exists=True)
    mock_grupa_doc.to_dict.return_value = {'studentsIds': ['s1']}
    
    mock_ocena_ref = MagicMock()
    mock_ocena_ref.get = MagicMock(return_value=mock_ocena_doc)
    mock_ocena_ref.update = MagicMock()

    mock_db.collection.return_value.document.return_value = mock_ocena_ref
    mock_db.collection.return_value.document.return_value.get = MagicMock(
        side_effect = [mock_ocena_doc, mock_grupa_doc]
    )

    wynik = await RepozytoriumOcen.aktualizuj_ocene("ocena1", {"wartoscOceny": "3.5"})

    assert wynik is True
    mock_ocena_ref.update.assert_called_once_with({'value': "3.5"})

@pytest.mark.asyncio
async def test_aktualizuj_ocene_nie_istnieje(mock_db):
    """Testuje błąd aktualizacji, gdy ocena nie istnieje."""
    mock_ocena_doc = MagicMock(exists=False)
    mock_db.collection.return_value.document.return_value.get = MagicMock(return_value=mock_ocena_doc)

    with pytest.raises(ValueError, match="Ocena o ID ocenaNieIstniejaca nie istnieje"):
        await RepozytoriumOcen.aktualizuj_ocene("ocenaNieIstniejaca", {"wartoscOceny": 3.5})

@pytest.mark.asyncio
async def test_usun_ocene_sukces(mock_db):
    """Testuje pomyślne usunięcie oceny."""
    mock_db.collection.return_value.document.return_value.delete = MagicMock()

    wynik = await RepozytoriumOcen.usun_ocene("ocenaDoUsuniecia")

    assert wynik is True
    mock_db.collection.return_value.document.return_value.delete.assert_called_once()