"""
Suite minima de pruebas para el nucleo de lenguajes.py.

Debe aprobar igual en los tres contenedores (py311, py312, py313) del
Ejercicio 1: es la evidencia de que el programa no depende de un
comportamiento particular de una sola version de Python.
"""

import pytest

from lenguajes import (
    cerradura_kleene,
    cerradura_positiva,
    maximo_numero_subcadenas,
    parsear_alfabeto,
    prefijos,
    subcadenas,
    sufijos,
)


# --------------------------------------------------------------------
# Caso frontera: la cadena vacia
# --------------------------------------------------------------------

def test_prefijos_de_cadena_vacia():
    assert prefijos("") == [""]


def test_sufijos_de_cadena_vacia():
    assert sufijos("") == [""]


def test_subcadenas_de_cadena_vacia():
    assert subcadenas("") == [""]


# --------------------------------------------------------------------
# Alfabeto de un solo simbolo
# --------------------------------------------------------------------

def test_prefijos_alfabeto_un_simbolo():
    assert prefijos("aaa") == ["", "a", "aa", "aaa"]


def test_sufijos_alfabeto_un_simbolo():
    assert sufijos("aaa") == ["aaa", "aa", "a", ""]


def test_subcadenas_alfabeto_un_simbolo():
    # Con simbolos repetidos, las subcadenas distintas son muchas menos
    # que el maximo teorico: aqui solo hay 4 ("", "a", "aa", "aaa").
    assert subcadenas("aaa") == ["", "a", "aa", "aaa"]
    assert maximo_numero_subcadenas(3) == 7


# --------------------------------------------------------------------
# Prefijos y sufijos de una cadena de longitud 1
# --------------------------------------------------------------------

def test_prefijos_longitud_1():
    assert prefijos("b") == ["", "b"]


def test_sufijos_longitud_1():
    assert sufijos("b") == ["b", ""]


# --------------------------------------------------------------------
# Diferencia entre Sigma* y Sigma+ para longitud 0
# --------------------------------------------------------------------

def test_sigma_estrella_longitud_0_es_solo_lambda():
    assert cerradura_kleene(["a", "b"], 0) == [""]


def test_sigma_positiva_longitud_0_es_vacio():
    # Sigma+ nunca incluye la cadena vacia, ni siquiera truncado a longitud 0.
    assert cerradura_positiva(["a", "b"], 0) == []


def test_diferencia_kleene_y_positiva_longitud_0():
    kleene = set(cerradura_kleene(["a", "b"], 0))
    positiva = set(cerradura_positiva(["a", "b"], 0))
    assert kleene - positiva == {""}


# --------------------------------------------------------------------
# Casos generales de cerradura, para longitudes pequenas
# --------------------------------------------------------------------

def test_cerradura_kleene_longitud_2_dos_simbolos():
    resultado = cerradura_kleene(["a", "b"], 2)
    esperado = ["", "a", "b", "aa", "ab", "ba", "bb"]
    assert sorted(resultado, key=len) == sorted(esperado, key=len)
    assert set(resultado) == set(esperado)


def test_cerradura_positiva_rechaza_combinacion_enorme():
    with pytest.raises(ValueError):
        # 26^20 es muchisimo mayor que el limite de 200 000 cadenas.
        cerradura_positiva(list("abcdefghijklmnopqrstuvwxyz"), 20)


def test_parsear_alfabeto_quita_espacios_y_duplicados():
    assert parsear_alfabeto(" a, b ,a,c") == ["a", "b", "c"]
