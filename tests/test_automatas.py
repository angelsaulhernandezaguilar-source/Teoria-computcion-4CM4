"""Cada archivo .jff debe reconocer el lenguaje de su enunciado."""

from verificar import verificar


def test_todos_los_automatas_coinciden_con_su_enunciado():
    discrepancias, comparadas = verificar()
    assert discrepancias == []
    assert comparadas > 100_000
