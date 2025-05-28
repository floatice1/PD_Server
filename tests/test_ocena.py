"""Testy dla modelu Ocena."""

import pytest
from app.modele.ocena import Ocena
import datetime

def test_utworz_ocene():
    """Testuje tworzenie instancji Ocena."""
    ocena = Ocena(
        ocenaId="test_ocena_id",
        wartoscOceny="4.5",
        studentId="test_student_id",
        grupaId="test_grupa_id",
        wystawionePrzez="test_uzytkownik_id",
        timestamp=datetime.datetime(2023, 1, 1)
    )

    assert ocena.ocenaId == "test_ocena_id"
    assert ocena.wartoscOceny == "4.5"
    assert ocena.studentId == "test_student_id"
    assert ocena.grupaId == "test_grupa_id"
    assert ocena.wystawionePrzez == "test_uzytkownik_id"
    assert ocena.timestamp == datetime.datetime(2023, 1, 1)

def test_ocena_minimalne_pola():
    """Testuje tworzenie instancji Ocena z minimalnymi wymaganymi polami."""
    ocena = Ocena(
        ocenaId="test_ocena_id_2",
        wartoscOceny="3.0",
        studentId="test_student_id_2",
        grupaId="test_grupa_id_2",
        wystawionePrzez="test_uzytkownik_id_2"
    )
    assert ocena.ocenaId == "test_ocena_id_2"
    assert ocena.wartoscOceny == "3.0"
    assert ocena.studentId == "test_student_id_2"
    assert ocena.grupaId == "test_grupa_id_2"
    assert ocena.wystawionePrzez == "test_uzytkownik_id_2"