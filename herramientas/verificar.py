"""Compara cada .jff con el oraculo de su enunciado y elige los casos de prueba."""

import pathlib
import random
import re

from catalogo import ER, entradas_fa, er_a_python
from jff import Automata, cadenas

RAIZ = pathlib.Path(__file__).resolve().parent.parent / "automatas"


def cargar(carpeta, archivo):
    return Automata(RAIZ / carpeta / f"{archivo}.jff")


def oraculo_de(carpeta, entrada):
    """Una entrada sin oraculo se compara con su autómata de referencia."""
    _, archivo, _, _, oraculo = entrada
    if oraculo is None:
        return cargar(carpeta, archivo).acepta
    if isinstance(oraculo, str):
        return cargar(carpeta, oraculo).acepta
    return oraculo


def muestra(aut, azar, longitud_exhaustiva=None, aleatorias=1500, longitud_larga=40):
    """Todas las cadenas cortas mas cadenas largas al azar sobre el alfabeto."""
    alfabeto = aut.alfabeto
    if longitud_exhaustiva is None:
        longitud_exhaustiva = 0
        while len(alfabeto) ** (longitud_exhaustiva + 1) <= 3000:
            longitud_exhaustiva += 1
    yield from cadenas(alfabeto, longitud_exhaustiva)
    for _ in range(aleatorias):
        yield "".join(azar.choice(alfabeto) for _ in range(azar.randint(0, longitud_larga)))


def mas_corta_aceptada(aut):
    """BFS sobre los subconjuntos alcanzables del autómata."""
    inicio = frozenset(aut._cerradura({aut.inicial}))
    vistos, cola = {inicio}, [(inicio, "")]
    while cola:
        actual, w = cola.pop(0)
        if actual & aut.finales:
            return w
        for a in aut.alfabeto:
            s = frozenset(aut._cerradura({n for q in actual for n in aut.delta.get((q, a), ())}))
            if s and s not in vistos:
                vistos.add(s)
                cola.append((s, w + a))
    return None


def elegir_casos(aut, oraculo, semilla):
    """Tres validas y tres invalidas como minimo, con casos frontera al frente."""
    azar = random.Random(semilla)
    alfabeto = aut.alfabeto
    corta = mas_corta_aceptada(aut)
    validas, invalidas = [corta], []
    if "" not in validas and oraculo(""):
        validas.append("")
    if not oraculo(""):
        invalidas.append("")
    if corta:
        for i in range(len(corta)):  # justo por debajo de la aceptada mas corta
            for candidata in (corta[:i] + corta[i + 1:],):
                if not oraculo(candidata) and candidata not in invalidas:
                    invalidas.append(candidata)
                    break
            if len(invalidas) >= 2:
                break
    for _ in range(40000):
        if len(validas) >= 3 and len(invalidas) >= 3:
            break
        base = corta + "".join(azar.choice(alfabeto) for _ in range(azar.randint(0, 6)))
        base = "".join(azar.choice(alfabeto) for _ in range(azar.randint(0, 4))) + base
        destino = validas if oraculo(base) else invalidas
        if len(destino) < 3 and base not in destino:
            destino.append(base)
    fuera = [s for s in ("x", "ax", "xa") if len(invalidas) < 3]
    # Lenguaje universal: solo un simbolo fuera del alfabeto produce rechazo.
    invalidas += fuera[: 3 - len(invalidas)]
    return validas, invalidas


def verificar():
    """Devuelve la lista de discrepancias y el total de cadenas comparadas."""
    fallos, total = [], 0
    for carpeta, entrada in entradas_fa():
        aut = cargar(carpeta, entrada[1])
        oraculo = oraculo_de(carpeta, entrada)
        azar = random.Random(entrada[1])
        for w in muestra(aut, azar):
            total += 1
            if aut.acepta(w) != bool(oraculo(w)):
                fallos.append((entrada[1], w))
                break
    for problema, archivo, _, _, oraculo in ER:
        expresion = Automata(RAIZ / "lista3-afn" / f"{archivo}.jff").expresion
        patron = re.compile(er_a_python(expresion))
        simbolos = "012" if problema == "256" else "01"
        for w in cadenas(simbolos, 8 if problema == "256" else 11):
            total += 1
            if (patron.fullmatch(w) is not None) != bool(oraculo(w)):
                fallos.append((archivo, w))
                break
    return fallos, total


if __name__ == "__main__":
    discrepancias, comparadas = verificar()
    print(f"{comparadas} cadenas comparadas; {len(discrepancias)} discrepancias")
    for d in discrepancias:
        print(d)
