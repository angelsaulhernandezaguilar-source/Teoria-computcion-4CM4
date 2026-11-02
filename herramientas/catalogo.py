"""Catalogo de los automatas de las Listas 2 y 3.

Cada entrada une un archivo .jff con su enunciado, su justificacion de diseno
y un "oraculo": una definicion del lenguaje escrita de forma independiente del
automata (a partir del enunciado), contra la que se comparan los archivos.
"""

import re


# ---------------------------------------------------------------------------
# Automatas dados por tabla en los enunciados (transcritos de las listas)
# ---------------------------------------------------------------------------

def tabla(inicial, finales, simbolos, renglones):
    """Oraculo a partir de una tabla: renglones 'A: B C' o, en AFN, 'A: BC -'."""
    delta = {}
    for r in renglones.split(";"):
        q, resto = r.split(":")
        for a, destino in zip(simbolos, resto.split()):
            delta[q.strip(), a] = set() if destino == "-" else set(destino)

    def oraculo(w, desde=None):
        actuales = set(desde or inicial)
        for c in w:
            actuales = {n for q in actuales for n in delta.get((q, c), ())}
        return bool(actuales & set(finales))

    oraculo.delta = delta
    oraculo.finales = set(finales)
    return oraculo


T149 = tabla("A", "C", "01", "A: B C; B: A C; C: C A")
T150 = tabla("A", "BCD", "01a", "A: B C D; B: B C C; C: A A D; D: B B B")
T151 = tabla("A", "CEF", "01", "A: C E; B: F E; C: A G; D: C E; E: I B; F: D H; G: F I; H: C J; I: J E; J: I E")
T152 = tabla("A", "DEF", "012", "A: C E B; B: D E B; C: A D F; D: F B C; E: F B A; F: D B C")
T153 = tabla("A", "DFG", "01", "A: B C; B: D E; C: F G; D: D E; E: F G; F: E D; G: F G")
T154 = tabla("A", "EGHJ", "01", "A: D K; B: H K; C: I E; D: C G; E: K I; F: B E; G: C I; H: C B; I: G K; J: F B; K: C F")
T155 = tabla("A", "F", "01", "A: B C; B: D E; C: K G; D: H E; E: F D; F: J G; G: E G; H: B K; I: C A; J: D G; K: F D; L: C J")
T192 = tabla("A", "C", "01", "A: B BC; B: AB -; C: AC -")
T193 = tabla("A", "D", "01", "A: - BC; B: AD BCD; C: C AC; D: C D")
T194 = tabla("A", "CD", "012", "A: AB AC A; B: - - -; C: AB ABCD -; D: B A -")
T195 = tabla("A", "CE", "01", "A: AB A; B: A C; C: A D; D: D E; E: E CD")
T254 = tabla("A", "B", "01", "A: A B; B: A B")
T255 = tabla("A", "A", "01", "A: B B; B: A B")
T256 = tabla("A", "B", "012", "A: B A A; B: B B A")
T257 = tabla("A", "BC", "01", "A: B C; B: C B; C: A A")
T258 = tabla("A", "C", "01", "A: C C; B: A C; C: B A")
T260 = tabla("A", "D", "01", "A: - BC; B: ABD CD; C: AC AE; D: - DE; E: AE -")


# ---------------------------------------------------------------------------
# Oraculos escritos a partir del enunciado
# ---------------------------------------------------------------------------

def contiene(*patrones):
    return lambda w: all(p in w for p in patrones)


def regex(expresion):
    return lambda w: re.fullmatch(expresion, w) is not None


def traslapadas(w, p):
    return sum(w.startswith(p, i) for i in range(len(w)))


def bloques_con_cero(w):
    return len(w) >= 3 and len(w) % 3 == 0 and all("0" in w[i:i + 3] for i in range(0, len(w), 3))


def ventanas_con_cero(w):
    return all("0" in w[i:i + 3] for i in range(len(w) - 2))


def palancas(w):
    """Simula el mecanismo del ejercicio 124; todas las palancas inician a la izquierda."""
    izq, der, cen = True, True, True
    salida = None
    for c in w:
        if c == "0":
            if izq:
                salida = "A"
            else:
                salida = "A" if cen else "R"
                cen = not cen
            izq = not izq
        else:
            if der:
                salida = "A" if cen else "R"
                cen = not cen
            else:
                salida = "R"
            der = not der
    return salida == "A"


def alumno(w):
    """Ejercicio 148: se aprueba tras un P seguido de A, con a lo sumo dos P por ano."""
    usadas, esperando = 0, False
    for c in w:
        if esperando:
            if c == "A":
                return True
            if c != "S":
                return False
            esperando = False
            usadas = (usadas + 1) % 2
        elif c == "P":
            esperando = True
        elif c != "N":
            return False
    return False


def binario_lsb(w, m):
    return sum(int(b) << i for i, b in enumerate(w)) % m == 0


def binario_msb(w, m):
    return int(w or "0", 2) % m == 0


# Diagrama del ejercicio 128. F no es absorbente: con 0 y con 1 regresa a D.
M128 = tabla("A", "F", "01", "A: B C; B: C D; C: D E; D: F E; E: E F; F: D D")


L2 = [
    ("97", "ejercicio_097", "Palabras de Σ₁ = {0,1,2} cuya longitud es múltiplo de 3.",
     "Solo importa la longitud: el estado guarda el residuo |prefijo| mod 3. q0 es inicial y de aceptación porque |λ| = 0.",
     lambda w: len(w) % 3 == 0),
    ("99", "ejercicio_099", "Palabras de Σ₁ que terminan con 001001.",
     "Autómata de búsqueda de sufijo (función de fallo tipo KMP): el estado qj indica que los últimos j símbolos leídos son el prefijo más largo de 001001 que es sufijo del prefijo leído. Un 2 regresa siempre a q0. Solo q6 acepta y puede abandonarse si llegan más símbolos.",
     lambda w: w.endswith("001001")),
    ("102", "ejercicio_102", "Palabras de Σ₃ = {a,b} que contienen abbbab.",
     "Mismo principio de búsqueda: qj = j símbolos de abbbab ya coinciden. q6 es de aceptación y absorbente: una vez hallada la subcadena, lo que siga no importa.",
     contiene("abbbab")),
    ("103", "ejercicio_103", "Palabras de Σ₃ que contienen aabbba.",
     "Búsqueda de aabbba: qj = longitud del mayor prefijo del patrón que es sufijo de lo leído; q6 absorbente de aceptación.",
     contiene("aabbba")),
    ("106", "ejercicio_106", "Palabras de Σ₁ que incluyen la subcadena 1101001.",
     "Búsqueda de 1101001: qj = j símbolos del patrón coinciden; el 2 no aparece en el patrón y reinicia la búsqueda; q7 absorbente de aceptación.",
     contiene("1101001")),
    ("107", "ejercicio_107", "Palabras de Σ₁ que incluyen al menos una vez 0101 y al menos una vez 021.",
     "Intersección por autómata producto: cada estado es un par (avance en 0101, avance en 021), y acepta solo cuando ambos patrones ya aparecieron. Se minimizó por particiones a 13 estados.",
     contiene("0101", "021")),
    ("109", "ejercicio_109", "Palabras de Σ₂ = {a,b,c,0,1} que incluyen abbcb y cbaabb, pudiendo traslaparse.",
     "Producto de dos búsquedas con función de fallo; esta detecta de forma natural los traslapes (abbcbaabb cuenta). Cada estado guarda el avance en cada patrón. Minimizado de 56 a 22 estados.",
     contiene("abbcb", "cbaabb")),
    ("111", "ejercicio_111", "Palabras de Σ₁ que contienen exactamente tres veces 01002.",
     "El estado es el par (avance en la búsqueda de 01002, ocurrencias vistas, saturadas en 4). 01002 no se traslapa consigo mismo. Acepta si el contador vale 3 al terminar.",
     lambda w: traslapadas(w, "01002") == 3),
    ("112", "ejercicio_112", "Palabras de Σ₁ que contienen dos veces 010 sin traslape (01010 no pertenece; 010010 sí).",
     "El estado es (avance en 010, ocurrencias contadas). Al completar una ocurrencia la búsqueda vuelve a cero, de modo que sus símbolos no se reutilizan. Acepta con contador exactamente 2.",
     lambda w: w.count("010") == 2),
    ("113", "ejercicio_113", "Palabras de Σ₁ que contienen dos veces 010, pudiendo traslaparse.",
     "Igual que el 112, pero tras cada ocurrencia se sigue la función de fallo (el último 0 sirve de inicio de la siguiente), por lo que 01010 sí pertenece.",
     lambda w: traslapadas(w, "010") == 2),
    ("118", "ejercicio_118", "L = {w ∈ Σ₃* : w = a x ab y a, con x, y ∈ Σ₃*}.",
     "Los estados recuerdan: si el primer símbolo fue a; si ya apareció ab después de esa a; y, una vez visto, si el último símbolo fue a. La palabra más corta es aaba.",
     regex(r"a[ab]*ab[ab]*a")),
    ("120", "ejercicio_120", "Palabras de Σ₁ cuyo primer y último carácter son distintos.",
     "El estado es (primer símbolo, último símbolo). El primero queda fijo y el segundo se actualiza. λ se rechaza porque no tiene esos caracteres. Tras minimizar quedan 7 estados.",
     lambda w: len(w) > 0 and w[0] != w[-1]),
    ("121", "ejercicio_121", "Palabras de Σ₁ de longitud 3n, tales que cada bloque de 3 tiene al menos un 0 (se toma n ≥ 1).",
     "El estado guarda la posición dentro del bloque y si el bloque ya tiene 0; un bloque sin 0 lleva a un estado de rechazo absorbente. Se toma ℕ = {1, 2, …}, como en la Tarea 2, por lo que λ se rechaza.",
     bloques_con_cero),
    ("122", "ejercicio_122", "Palabras de Σ₁ en las que toda terna de símbolos consecutivos tiene un 0.",
     "El estado es el tamaño de la racha actual sin ceros (0, 1 o 2). Con racha 3 se pasa al rechazo absorbente.",
     ventanas_con_cero),
    ("123", "ejercicio_123", "Palabras de Σ₃ de la forma w x w, con w ∈ Σ₃² y x ∈ Σ₃*.",
     "El estado memoriza los dos primeros símbolos, los dos últimos y si ya se leyeron al menos 4. Acepta si coinciden y |w x w| ≥ 4.",
     lambda w: len(w) >= 4 and w[:2] == w[-2:]),
    ("124", "ejercicio_124", "Mecanismo de tres palancas: se acepta si la última canica sale por A.",
     "Las palancas tienen 2³ = 8 configuraciones. El AFD amplía el estado a (configuración, última salida), con 13 estados alcanzables; acepta los de salida A. Se toma la posición inicial con las tres palancas a la izquierda.",
     palancas),
    ("128", "ejercicio_128_M", "Autómata M del diagrama del ejercicio 128 (lenguaje L).",
     "Transcripción del diagrama: cada estado es uno de A a F del enunciado (q0 = A, …, q5 = F); F es de aceptación y regresa a D con 0 y con 1.",
     M128),
    ("128", "ejercicio_128_L2", "L₂: palabras de L a las que se les quita el último símbolo.",
     "u ∈ L₂ ⇔ existe c con uc ∈ L. Se conservan estados y transiciones, y F' = {q : ∃c, δ(q,c) ∈ F} = {D, E}, pues D llega a F con 0 y E con 1, mientras que F va a D con ambos símbolos.",
     lambda w: M128(w + "0") or M128(w + "1")),
    ("131", "ejercicio_131", "Dibujar M = ({q1,q2},{0,1},δ,q1,{q2}) y hallar L(M).",
     "El estado solo recuerda el último símbolo: 1 lleva a q2 y 0 lleva a q1. L(M) = Σ*1, las cadenas que terminan en 1.",
     lambda w: w.endswith("1")),
    ("133", "ejercicio_133", "Tabla y diagrama del autómata dado con Q = {q0,q1,q2,q3}, F = {q0}.",
     "Los estados codifican la paridad de a y de b: q0 (par, par), q1 (par, impar), q2 (impar, par), q3 (impar, impar). Acepta si ambas son pares.",
     lambda w: w.count("a") % 2 == 0 and w.count("b") % 2 == 0),
    ("135", "ejercicio_135", "L = {bᵐ a bⁿ : m, n > 0}.",
     "Etapas: inicio; ya hay b; ya se leyó la única a; ya hay b tras la a (acepta). Cualquier violación va al rechazo absorbente.",
     regex(r"b+ab+")),
    ("137", "ejercicio_137", "Cadenas sobre {a,b} con prefijo ab.",
     "Estados: nada leído; leí a; prefijo ab confirmado (aceptación absorbente); rechazo absorbente.",
     lambda w: w.startswith("ab")),
    ("139", "ejercicio_139", "Cadenas en {0,1}* con número par de ceros.",
     "El estado guarda la paridad de los ceros leídos; 0 la invierte y 1 no la cambia.",
     lambda w: w.count("0") % 2 == 0),
    ("141", "ejercicio_141", "Cadenas en {0,1}* donde cada 0 tiene un 1 inmediatamente a su derecha.",
     "Estados: correcto (sin 0 pendiente), pendiente (último símbolo 0 aún sin su 1) y rechazo absorbente (00).",
     lambda w: "00" not in w and not w.endswith("0")),
    ("143a", "ejercicio_143a", "Lenguaje del autómata de la figura (a).",
     "Un solo estado, inicial y de aceptación, con lazos a y b: L = Σ*.",
     lambda w: True),
    ("143b", "ejercicio_143b", "Lenguaje del autómata de la figura (b).",
     "Transcripción de la figura: q0 -a→ q1, lazos a y b en q1, y q1 -b→ q0. Es no determinista en (q1, b) y q0 no tiene transición con b. Si la palabra empieza con a, el camino que se queda en q1 la acepta; si empieza con b, el cómputo muere; λ termina en q0. L = a(a+b)*.",
     lambda w: w.startswith("a")),
    ("145", "ejercicio_145", "Número binario leído de derecha a izquierda que es múltiplo de 5.",
     "Un bit nuevo pesa 2ⁱ mod 5, y 2 tiene orden 4 módulo 5, de modo que basta guardar (residuo, posición mod 4). Tras minimizar quedan 5 estados. λ representa el 0 y se acepta.",
     lambda w: binario_lsb(w, 5)),
    ("147", "ejercicio_147", "Número binario leído de izquierda a derecha que es múltiplo de 6.",
     "El estado guarda el residuo del valor leído: r' = (2r + b) mod 6. De los 6 residuos quedan 4 estados distinguibles.",
     lambda w: binario_msb(w, 6)),
    ("148", "ejercicio_148", "Progreso de un alumno con Σ = {P,N,A,S}: máximo dos convocatorias por año; termina al aprobar.",
     "q0: inicio de año, 0 presentaciones. q1: se presentó y espera resultado. q4: ya aplazó una vez. q5: segunda presentación. q3: aprobó (aceptación absorbente). q2: secuencia sin sentido (rechazo). N no consume oportunidad; dos S reinician el año.",
     alumno),
    ("149", "ejercicio_149", "Autómata dado por tabla; hallar Q, Σ, A₀, F y valores de δ̂.",
     "Transcripción de la tabla: q0 = A, q1 = B, q2 = C.", T149),
    ("150", "ejercicio_150", "Autómata dado por tabla con Σ = {0,1,a}; hallar Q, Σ, A₀, F y valores de δ̂.",
     "Transcripción de la tabla: q0 = A, q1 = B, q2 = C, q3 = D.", T150),
]

# Los problemas 162-188 piden un AFN para los problemas de la Lista 2.
DISENO_AFN = {
    "97": "Contador módulo 3; el no determinismo no reduce nada.",
    "99": "q0 se queda con cualquier símbolo y adivina dónde empieza 001001; el resto es una cadena lineal sin salidas al final.",
    "102": "q0 con lazo adivina el inicio de abbbab; el último estado es absorbente.",
    "103": "q0 con lazo adivina el inicio de aabbba; el último estado es absorbente.",
    "106": "q0 con lazo adivina el inicio de 1101001; el último estado es absorbente.",
    "107": "Adivina el orden de los patrones: una rama busca 0101 y luego 021; otra, al revés; más las ramas con traslape.",
    "109": "Ramas para cada orden de los patrones y para los traslapes posibles.",
    "111": "Se conserva el AFD: el AFN acepta si algún camino acepta, por lo que adivinar posiciones no garantiza que no haya más ocurrencias.",
    "112": "Se conserva el AFD por la misma razón que el 111: contar exactamente requiere descartar todas las demás ocurrencias.",
    "113": "Se conserva el AFD por la misma razón que el 111.",
    "118": "Lee a, adivina dónde está ab y adivina la a final.",
    "120": "Recuerda el primer símbolo y adivina que el símbolo actual, distinto de él, es el último.",
    "121": "Adivina en cada bloque en qué posición está su 0.",
    "122": "Solo los estados útiles de la racha; la transición indefinida reemplaza al estado de rechazo.",
    "123": "Recuerda w, adivina dónde comienza su segunda copia al final.",
}
_L2 = {e[0]: e for e in L2 if e[1] != "ejercicio_128_M"}

L3_AFN = [
    (n, f"AFN_T2_{n}", "AFN para el problema " + n + " de la Lista 2: " + _L2[n][2], DISENO_AFN[n], _L2[n][4])
    for n in DISENO_AFN
]

_SIMP = "Partición: se inicia con {no finales, finales} y se separan los estados que van a bloques distintos con algún símbolo, hasta estabilizar; cada estado del resultado representa un bloque de estados equivalentes."
_ORIG = "Transcripción de la tabla. Los estados inaccesibles se hallan con un recorrido en anchura desde el inicial."
_AFD = "Construcción de subconjuntos: cada estado es el conjunto de estados del AFN alcanzables con el prefijo leído; acepta si contiene un estado final."

L3 = [
    ("151", "ej151_original", "Diagrama del autómata de la tabla 151.", _ORIG + " No hay inaccesibles.", T151),
    ("151", "ej151_simplificado", "Autómata 151 simplificado.", _SIMP, T151),
    ("152", "ej152_original", "Diagrama del autómata de la tabla 152.", _ORIG + " No hay inaccesibles.", T152),
    ("152", "ej152_simplificado", "Autómata 152 simplificado.", _SIMP, T152),
    ("153", "ej153_original", "Diagrama del autómata de la tabla 153.", _ORIG + " No hay inaccesibles.", T153),
    ("153", "ej153_simplificado", "Autómata 153 simplificado.", _SIMP, T153),
    ("154", "ej154_original", "Diagrama del autómata de la tabla 154.", _ORIG, T154),
    ("154", "ej154_sin_inaccesibles", "Autómata 154 sin el estado inaccesible J.", "El recorrido desde A nunca alcanza J; se elimina con sus transiciones.", T154),
    ("154", "ej154_simplificado", "Autómata 154 simplificado.", _SIMP, T154),
    ("155", "ej155_original", "Diagrama del autómata de la tabla 155.", _ORIG, T155),
    ("155", "ej155_sin_inaccesibles", "Autómata 155 sin los estados inaccesibles I y L.", "El recorrido desde A no alcanza I ni L; se eliminan.", T155),
    ("155", "ej155_simplificado", "Autómata 155 simplificado.", _SIMP, T155),
    ("156", "ej156_original", "Tabla del autómata del diagrama 156.", "Transcripción del diagrama de la lista.", None),
    ("156", "ej156_simplificado", "Autómata 156 simplificado.", _SIMP, "ej156_original"),
    ("157", "ej157_original", "Tabla del autómata del diagrama 157.", "Transcripción del diagrama de la lista.", None),
    ("157", "ej157_simplificado", "Autómata 157 simplificado.", _SIMP, "ej157_original"),
    ("158", "ej158", "Describir el AFN de la figura 158.", "Cadena lineal q1→q2→q3: acepta únicamente 01.", lambda w: w == "01"),
    ("159", "ej159", "Describir el AFN de la figura 159.", "q1 consume unos; luego exige 01: L = 1*01.", regex(r"1*01")),
    ("160", "ej160", "Describir el AFN de la figura 160.", "Exige el prefijo 01 y q3 absorbe el resto: L = 01(0+1)*.", lambda w: w.startswith("01")),
    ("161", "ej161", "Describir el AFN de la figura 161.", "Ciclo q1→q2→q3→q1 que lee 010; q1 acepta: L = (010)*.", regex(r"(010)*")),
    ("189", "ej189_AFN", "AFN para palabras que contienen 00101 o 00110.", "q0 con lazo adivina dónde empieza el patrón; dos ramas comparten 001 y terminan en un estado absorbente.", lambda w: "00101" in w or "00110" in w),
    ("190", "ej190_AFN", "AFN para palabras que contienen 11010 y 10100.", "Una rama por cada orden de los patrones y por cada traslape posible; cada estado indica qué patrón y cuántos símbolos se llevan.", contiene("11010", "10100")),
    ("192", "ej192_AFN", "AFN de la tabla 192.", "Transcripción de la tabla.", T192),
    ("192", "ej192_AFD", "AFD equivalente al 192.", _AFD, T192),
    ("193", "ej193_AFN", "AFN de la tabla 193.", "Transcripción de la tabla.", T193),
    ("193", "ej193_AFD", "AFD equivalente al 193.", _AFD, T193),
    ("194", "ej194_AFN", "AFN de la tabla 194.", "Transcripción de la tabla.", T194),
    ("194", "ej194_AFD", "AFD equivalente al 194.", _AFD, T194),
    ("195", "ej195_AFN", "AFN de la tabla 195.", "Transcripción de la tabla.", T195),
    ("195", "ej195_AFD", "AFD equivalente al 195.", _AFD, T195),
    ("254", "ej254", "Autómata de la tabla 254.", "Transcripción. El estado recuerda si el último símbolo fue 1.", T254),
    ("255", "ej255", "Autómata de la tabla 255.", "Transcripción de la tabla.", T255),
    ("256", "ej256", "Autómata de la tabla 256.", "Transcripción de la tabla.", T256),
    ("257", "ej257", "Autómata de la tabla 257.", "Transcripción de la tabla.", T257),
    ("258", "ej258", "Autómata de la tabla 258.", "Transcripción de la tabla.", T258),
    ("260", "ej260_AFN", "AFN de la tabla 260.", "Transcripción de la tabla.", T260),
    ("260", "ej260_AFD", "AFD equivalente al 260.", _AFD, T260),
    ("260", "ej260_AFD_min", "AFD del 260, minimizado.", _SIMP, T260),
    ("261", "ej261_AFN", "AFN de la figura 261.", "q0 con lazo adivina el inicio de 00; la rama q3, q4 no acepta nunca.", lambda w: w.endswith("00")),
    ("261", "ej261_AFD", "AFD equivalente al 261.", _AFD, lambda w: w.endswith("00")),
    ("261", "ej261_AFD_min", "AFD del 261, minimizado.", "El estado guarda cuántos ceros finales se llevan (0, 1, 2 o más).", lambda w: w.endswith("00")),
    ("262", "ej262_AFN", "AFN que acepta {ab, ba}.", "Dos ramas que convergen en el estado final: q1 = leí a; q2 = leí b.", lambda w: w in ("ab", "ba")),
    ("262", "ej262_AFD", "AFD que acepta {ab, ba}.", _AFD + " ∅ es el estado de rechazo.", lambda w: w in ("ab", "ba")),
    ("263", "ej263_AFN", "AFN de la figura 263.", "q0 con lazo adivina el inicio de 01.", lambda w: w.endswith("01")),
    ("263", "ej263_AFD", "AFD equivalente al 263.", _AFD, lambda w: w.endswith("01")),
]

# Expresiones regulares: (problema, archivo, enunciado, razonamiento, oraculo)
ER = [
    ("236", "ej236_ER", "L = {x001y : x, y ∈ Σ*}.", "Cualquier prefijo, 001 y cualquier sufijo.", contiene("001")),
    ("237", "ej237_ER", "L = {x010 : x ∈ Σ*}.", "Cualquier prefijo seguido de 010.", lambda w: w.endswith("010")),
    ("238", "ej238_ER", "L = Σ³ ∪ Σ⁵.", "Tres símbolos y, opcionalmente, dos más (en JFLAP, ! es λ).", lambda w: len(w) in (3, 5)),
    ("239", "ej239_ER", "Cadenas que comienzan con 01 o terminan con 10.", "Unión de las dos condiciones.", lambda w: w.startswith("01") or w.endswith("10")),
    ("240", "ej240_ER", "Cadenas de longitud par que contienen 01.", "Con E = ((0+1)(0+1))*: o 01 empieza en posición par (E 01 E), o en impar (E(0+1)01(0+1)E).", lambda w: len(w) % 2 == 0 and "01" in w),
    ("254", "ej254_ER", "Expresión regular del autómata 254.", "Lema de Arden sobre las ecuaciones del autómata.", T254),
    ("255", "ej255_ER", "Expresión regular del autómata 255.", "Lema de Arden.", T255),
    ("256", "ej256_ER", "Expresión regular del autómata 256.", "Lema de Arden.", T256),
    ("257", "ej257_ER", "Expresión regular del autómata 257.", "Lema de Arden.", T257),
    ("258", "ej258_ER", "Expresión regular del autómata 258.", "Lema de Arden.", T258),
]

def er_a_python(expresion):
    """Traduce la sintaxis de JFLAP (+ union, ! lambda) a la del modulo re."""
    return expresion.replace("+", "|").replace("!", "(?:)")


# 201-235: (problema, cadena, expresion de la lista, razon)
VF = [
    (201, "a", "a+b", "Se elige a en la unión."),
    (202, "a", "ab", "L(ab) = {ab}."),
    (203, "a", "a*+b*", "a ∈ L(a*)."),
    (204, "a", "ab*", "b⁰ = λ."),
    (205, "a", "a*b", "Toda palabra termina en b."),
    (206, "ab", "a+b", "Solo hay palabras de longitud 1."),
    (207, "ab", "ab", "Es la propia palabra."),
    (208, "ab", "λa*b", "λ es neutro y a¹b = ab."),
    (209, "ab", "∅a*b", "∅ es absorbente: el lenguaje es vacío."),
    (210, "ab", "(a+b)*", "Dos repeticiones: a y b."),
    (211, "ab", "abc*", "c⁰ = λ."),
    (212, "ab", "ab*c", "Toda palabra termina en c."),
    (213, "ab", "ab*c*", "b¹ y c⁰."),
    (214, "ab", "(a+b+c)*", "Dos repeticiones: a y b."),
    (215, "ab", "(abc)*", "Las longitudes son múltiplos de 3."),
    (216, "ab", "(ab)*c", "Toda palabra termina en c."),
    (217, "ab", "a(bc)*", "Las palabras tienen longitud impar."),
    (218, "ab", "a(b+c)*", "a seguida de una b."),
    (219, "ab", "(a+b)*c", "Toda palabra termina en c."),
    (220, "ab", "(a+b)*c*", "ab y c⁰."),
    (221, "aa", "a+b", "Solo hay palabras de longitud 1."),
    (222, "aa", "a*+b*", "a² ∈ L(a*)."),
    (223, "aa", "a*b*", "a² y b⁰."),
    (224, "aa", "(a+b)*", "Dos repeticiones de a."),
    (225, "aa", "a(a+b)*", "a seguida de a."),
    (226, "", "a", "L(a) = {a}."),
    (227, "", "(a+b)*", "Cero repeticiones."),
    (228, "", "(a+b)*+a", "λ ∈ L((a+b)*)."),
    (229, "", "∅", "L(∅) no tiene palabras."),
    (230, "", "λ", "L(λ) = {λ}."),
    (231, "", "λ+a", "Se elige λ en la unión."),
    (232, "", "λa", "L(λa) = {a}."),
    (233, "", "ab*", "Toda palabra empieza con a."),
    (234, "", "(ab)*", "Cero repeticiones."),
]


def vf_python(expresion):
    return expresion.replace("+", "|").replace("λ", "(?:)").replace("∅", "(?!)")


# Calculos de delta extendida pedidos en los enunciados.
DELTA_GORRO = [
    (149, "A", T149, ["B|0", "C|1", "A|1101", "A|01001"]),
    (150, "A", T150, ["B|10a11", "B|aa1100", "A|a01a01", "C|a11a00"]),
    (192, "A", T192, ["A|0111", "BC|010111"]),
    (193, "A", T193, ["A|01101", "AB|1101", "C|1101"]),
    (194, "A", T194, ["AC|0121", "B|20111", "C|02112", "AB|0121"]),
    (195, "A", T195, ["A|10010", "AD|0110", "BE|0100", "BCD|10100"]),
]


def traza(oraculo, desde, w):
    """Conjuntos de estados recorridos: δ̂(Z, prefijos de w)."""
    actuales, pasos = set(desde), []
    pasos.append(actuales)
    for c in w:
        actuales = {n for q in actuales for n in oraculo.delta.get((q, c), ())}
        pasos.append(actuales)
    return pasos


def entradas_fa():
    """Todas las entradas con archivo de tipo automata: (carpeta, entrada)."""
    return [("lista2-afd", e) for e in L2] + [("lista3-afn", e) for e in L3_AFN + L3]
