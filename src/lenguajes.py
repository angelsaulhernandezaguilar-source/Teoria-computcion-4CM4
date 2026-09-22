"""
Nucleo de operaciones basicas sobre cadenas y lenguajes.

Funciones puras, sin ninguna dependencia de Flet ni de interfaz alguna,
para que se puedan probar de forma automatica (ver tests/test_lenguajes.py)
y para que la interfaz (app.py) sea solo una capa delgada encima de este
modulo.

Convencion adoptada en este programa: la cadena vacia (lambda, escrita aqui
como "") SI figura entre los prefijos, los sufijos y las subcadenas de
cualquier cadena w, incluida la propia cadena vacia. Esta es la convencion
estandar en teoria de la computacion: todo prefijo/sufijo/subcadena de
longitud 0 es la cadena vacia, y toda cadena tiene exactamente una subcadena
de longitud 0. Se documenta aqui porque el enunciado pide precisarlo y
justificarlo en el reporte (ver docs/05-aplicacion.md).
"""

from itertools import product


def prefijos(cadena: str) -> list[str]:
    """Todos los prefijos de `cadena`, de menor a mayor longitud.

    Una cadena w de longitud n tiene exactamente n + 1 prefijos (incluidas
    la cadena vacia y w misma): uno por cada longitud posible de 0 a n.
    """
    return [cadena[:i] for i in range(len(cadena) + 1)]


def sufijos(cadena: str) -> list[str]:
    """Todos los sufijos de `cadena`, de mayor a menor longitud.

    Simetrico a prefijos: una cadena de longitud n tiene n + 1 sufijos.
    """
    n = len(cadena)
    return [cadena[i:] for i in range(n + 1)]


def subcadenas(cadena: str) -> list[str]:
    """Todas las subcadenas DISTINTAS de `cadena` (incluida la vacia).

    Una cadena de longitud n tiene, como maximo, n*(n+1)/2 + 1 subcadenas
    distintas (la subcadena vacia, mas una por cada par (inicio, longitud)
    con 1 <= longitud <= n - inicio). El maximo solo se alcanza cuando
    ningun bloque se repite; si hay simbolos repetidos, varias subcadenas de
    distintas posiciones coinciden y el numero real de subcadenas distintas
    es menor.
    """
    n = len(cadena)
    vistas: dict[str, None] = {}
    vistas[""] = None
    for i in range(n):
        for j in range(i + 1, n + 1):
            vistas[cadena[i:j]] = None
    # Se preserva un orden util para mostrar: por longitud y luego por
    # aparicion, aprovechando que dict conserva el orden de insercion.
    return sorted(vistas.keys(), key=lambda s: (len(s), s))


def maximo_numero_subcadenas(n: int) -> int:
    """Cota superior de subcadenas distintas para una cadena de longitud n."""
    return n * (n + 1) // 2 + 1


# --------------------------------------------------------------------------
# Cerradura de Kleene (Sigma*) y cerradura positiva (Sigma+)
# --------------------------------------------------------------------------

LIMITE_CADENAS = 200_000


def _cuenta_cerradura(tam_alfabeto: int, longitud_max: int, positiva: bool) -> int:
    """Cuenta cuantas cadenas tendria Sigma* o Sigma+ hasta esa longitud,
    sin generarlas, para poder rechazar antes de construir nada."""
    inicio = 1 if positiva else 0
    return sum(tam_alfabeto ** i for i in range(inicio, longitud_max + 1))


def cerradura_kleene(alfabeto: list[str], longitud_max: int) -> list[str]:
    """Sigma* truncado: todas las cadenas sobre `alfabeto` de longitud 0
    hasta `longitud_max`, incluida la cadena vacia (Sigma^0 = {lambda}).

    Como |Sigma*| es infinito, esta funcion siempre trabaja con un tope de
    longitud que da el usuario; por eso se le llama "truncado". El numero
    de cadenas generadas crece como |Sigma|^n, asi que antes de construir
    nada se verifica el total contra LIMITE_CADENAS.
    """
    if not alfabeto:
        raise ValueError("El alfabeto no puede estar vacio.")
    total = _cuenta_cerradura(len(alfabeto), longitud_max, positiva=False)
    if total > LIMITE_CADENAS:
        raise ValueError(
            f"La combinacion pedida generaria {total:,} cadenas, mas de "
            f"{LIMITE_CADENAS:,}. Reduzca el alfabeto o la longitud maxima."
        )
    resultado = [""]
    for longitud in range(1, longitud_max + 1):
        for tupla in product(alfabeto, repeat=longitud):
            resultado.append("".join(tupla))
    return resultado


def cerradura_positiva(alfabeto: list[str], longitud_max: int) -> list[str]:
    """Sigma+ truncado: Sigma* truncado sin la cadena vacia.

    Sigma+ = Sigma* \\ {lambda}: es exactamente la misma construccion que
    cerradura_kleene, quitando el unico elemento de longitud 0.
    """
    if not alfabeto:
        raise ValueError("El alfabeto no puede estar vacio.")
    total = _cuenta_cerradura(len(alfabeto), longitud_max, positiva=True)
    if total > LIMITE_CADENAS:
        raise ValueError(
            f"La combinacion pedida generaria {total:,} cadenas, mas de "
            f"{LIMITE_CADENAS:,}. Reduzca el alfabeto o la longitud maxima."
        )
    resultado = []
    for longitud in range(1, longitud_max + 1):
        for tupla in product(alfabeto, repeat=longitud):
            resultado.append("".join(tupla))
    return resultado


def parsear_alfabeto(texto: str) -> list[str]:
    """Convierte "a,b,c" en ['a', 'b', 'c'], quitando espacios y vacios,
    y sin repetir simbolos (conserva el primer orden en que aparecen)."""
    simbolos = [s.strip() for s in texto.split(",")]
    simbolos = [s for s in simbolos if s != ""]
    vistos: dict[str, None] = {}
    for s in simbolos:
        vistos[s] = None
    return list(vistos.keys())
