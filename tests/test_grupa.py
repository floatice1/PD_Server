"""Testy dla modelu Grupa."""

import pytest
from app.modele.grupa import Grupa

def test_utworz_grupe():
    """Testuje tworzenie instancji Grupy."""
    grupa = Grupa(
        grupaId="test_id",
        nazwa="Testowa Grupa",
        przedmiotId="przedmiot_test_id",
        wykladowcaId="prowadzacy_test_id",
        studenciIds=["student1", "student2"]
    )

    assert grupa.grupaId == "test_id"
    assert grupa.nazwa == "Testowa Grupa"
    assert grupa.przedmiotId == "przedmiot_test_id"
    assert grupa.wykladowcaId == "prowadzacy_test_id"
    assert grupa.studenciIds == ["student1", "student2"]

def test_grupa_bez_studentow():
    """Testuje tworzenie instancji Grupy bez studentów."""
    grupa = Grupa(
        grupaId="test_id_2",
        nazwa="Druga Grupa",
        przedmiotId="przedmiot_test_id_2",
        wykladowcaId="prowadzacy_test_id_2",
        studenciIds=[]
    )

    assert grupa.grupaId == "test_id_2"
    assert grupa.nazwa == "Druga Grupa"
    assert grupa.przedmiotId == "przedmiot_test_id_2"
    assert grupa.wykladowcaId == "prowadzacy_test_id_2"
    assert grupa.studenciIds == []