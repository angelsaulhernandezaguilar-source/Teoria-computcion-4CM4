"""Genera docs/04-jflap.md. Uso: casos -> (JflapLote) -> documento.

    python herramientas/generar_reporte.py casos
    java -cp ...;JFLAP.jar JflapLote casos.tsv evidencias/jflap/resultados-jflap.tsv
    python herramientas/generar_reporte.py documento
"""

import pathlib
import re
import sys

from catalogo import DELTA_GORRO, ER, L2, L3, L3_AFN, VF, er_a_python, traza, vf_python
from jff import Automata
from verificar import cargar, elegir_casos, mas_corta_aceptada, oraculo_de, verificar

RAIZ = pathlib.Path(__file__).resolve().parent.parent
RESULTADOS = RAIZ / "evidencias" / "jflap" / "resultados-jflap.tsv"
FINITOS = {"ej158": "L = {01}", "ej262_AFN": "L = {ab, ba}", "ej262_AFD": "L = {ab, ba}"}
PASOS = [
    ("lista2-afd", "ejercicio_139", "0110", "Par de ceros"),
    ("lista2-afd", "ejercicio_097", "012", "Longitud múltiplo de 3"),
    ("lista2-afd", "ejercicio_118", "aaba", "a x ab y a, palabra más corta"),
    ("lista2-afd", "ejercicio_135", "bab", "bᵐ a bⁿ, palabra más corta"),
    ("lista3-afn", "ej263_AFN", "1001", "AFN: varias configuraciones simultáneas"),
    ("lista3-afn", "ej192_AFN", "0111", "AFN del problema 192 a)"),
    ("lista3-afn", "ej262_AFD", "ba", "AFD para {ab, ba}"),
]


def v(w):
    return f"`{w}`" if w else "λ"


def todos():
    for grupo, entradas in (("lista2-afd", L2), ("lista3-afn", L3_AFN), ("lista3-afn", L3)):
        for e in entradas:
            yield grupo, e


def casos():
    with open("casos.tsv", "w", encoding="utf-8") as f:
        for carpeta, e in todos():
            val, inv = elegir_casos(cargar(carpeta, e[1]), oraculo_de(carpeta, e), e[1])
            for w in val + inv:
                f.write(f"automatas/{carpeta}/{e[1]}.jff\t{w}\n")


def tabla_md(aut):
    minimos = aut.prefijo_minimo()
    lineas = ["| Estado | " + " | ".join(aut.alfabeto) + " | Prefijo más corto que llega |",
              "|---|" + "---|" * (len(aut.alfabeto) + 1)]
    for nombre, marca, destinos in aut.tabla():
        celdas = [", ".join(d) or "∅" for d in destinos.values()]
        llega = minimos.get(nombre)
        lineas.append(f"| {marca}{nombre} | " + " | ".join(celdas) + f" | {v(llega) if llega is not None else 'inalcanzable'} |")
    return "\n".join(lineas)


def seccion(carpeta, e, jflap):
    problema, archivo, enunciado, diseno, _ = e
    aut = cargar(carpeta, archivo)
    val, inv = elegir_casos(aut, oraculo_de(carpeta, e), archivo)
    corta = mas_corta_aceptada(aut)
    s = [f"### Problema {problema} — `{archivo}.jff`", "", f"**Enunciado.** {enunciado}", "",
         f"**Diseño.** {diseno}", ""]
    t = tabla_md(aut)
    if len(aut.nombres) > 10:
        t = f"<details><summary>Tabla de transiciones ({len(aut.nombres)} estados)</summary>\n\n{t}\n\n</details>"
    s += [t, "", "| Cadena | Se espera | JFLAP | Caso |", "|---|---|---|---|"]
    for w, tipo in [(x, "Acepta") for x in val] + [(x, "Rechaza") for x in inv]:
        notas = []
        if w == "":
            notas.append("frontera: vacía")
        if w == corta and w:
            notas.append("frontera: aceptada más corta")
        if corta and w and len(w) == len(corta) - 1:
            notas.append("frontera: un símbolo menos")
        if any(c not in aut.alfabeto for c in w):
            notas.append("símbolo fuera de Σ")
        assert (tipo == "Acepta") == jflap[archivo, w], (archivo, w)
        s.append(f"| {v(w)} | {tipo} | {'Acepta' if jflap[archivo, w] else 'Rechaza'} | {'; '.join(notas)} |")
    if archivo in FINITOS:
        s += ["", f"{FINITOS[archivo]} es finito, por lo que no existen tres cadenas válidas distintas."]
    return "\n".join(s) + "\n"


def conjunto(c):
    return "{" + ", ".join(sorted(c)) + "}" if c else "∅"


def trazas_afn(archivo, w):
    aut = cargar("lista3-afn", archivo)
    actuales = {aut.inicial}
    pasos = [conjunto(aut.nombres[q] for q in actuales)]
    for c in w:
        actuales = {n for q in actuales for n in aut.delta.get((q, c), ())}
        pasos.append(conjunto(aut.nombres[q] for q in actuales))
    return " → ".join(pasos)


def documento():
    jflap = {}
    for linea in RESULTADOS.read_text(encoding="utf-8").splitlines():
        ruta, w, r = linea.split("\t")
        jflap[pathlib.Path(ruta).stem, w] = r == "true"
    faltan, comparadas = verificar()
    assert not faltan, faltan
    n_jff = len(list((RAIZ / "automatas").rglob("*.jff")))
    d = [(RAIZ / "herramientas" / "04-introduccion.md").read_text(encoding="utf-8").format(
        n_jff=n_jff, comparadas=f"{comparadas:,}".replace(",", " "), n_casos=len(jflap))]

    d.append("## Simulación paso a paso en JFLAP\n")
    d.append("Cada figura es la ventana real de JFLAP, en la vista *Input → Step with Closure*, tras leer toda la cadena. El estado sombreado es la configuración actual; el fondo verde indica aceptación. Los pasos intermedios se guardan junto a cada figura en `evidencias/jflap/`.\n")
    for _, archivo, w, titulo in PASOS:
        d.append(f"**`{archivo}.jff` con {v(w)}** ({titulo})\n\n![{archivo}](../evidencias/jflap/{archivo}-paso{len(w)}.png)\n")

    d.append("## Lista 2: autómatas finitos (94 a 150)\n")
    d.append("Los problemas con asterisco sin autómata propio se resuelven al final de esta lista.\n")
    d += [seccion("lista2-afd", e, jflap) for e in L2]
    d.append((RAIZ / "herramientas" / "04-teoria.md").read_text(encoding="utf-8"))

    for c, _, tabla, pedidos in [x for x in DELTA_GORRO if x[0] in (149, 150)]:
        d.append(f"### Valores de δ̂ del problema {c}\n\n| Inicio | Cadena | Recorrido | Resultado |\n|---|---|---|---|")
        for p in pedidos:
            z, w = p.split("|")
            ps = traza(tabla, z, w)
            d.append(f"| {z} | {v(w)} | {' → '.join(conjunto(x) for x in ps)} | {conjunto(ps[-1])} |")
        d.append("")

    d.append("## Lista 3: simplificación, AFN y expresiones regulares (151 a 263)\n")
    d.append("### Problemas 151 a 161\n")
    d += [seccion("lista3-afn", e, jflap) for e in L3 if int(e[0]) <= 161]
    d.append("### Problemas 162 a 188: AFN para los problemas con asterisco de la Lista 2\n")
    d.append("El problema 116 no tiene AFN porque su lenguaje no es regular.\n")
    d += [seccion("lista3-afn", e, jflap) for e in L3_AFN]
    d.append("### Problemas 189 a 195\n")
    d += [seccion("lista3-afn", e, jflap) for e in L3 if 189 <= int(e[0]) <= 190]
    d.append(f"**Diagrama de la palabra 1001011 (189):** {trazas_afn('ej189_AFN', '1001011')}. Termina con un estado de aceptación: se acepta.\n")
    d.append(f"**Diagrama de la palabra 01101010100 (190):** {trazas_afn('ej190_AFN', '01101010100')}. Termina con un estado de aceptación: se acepta.\n")
    d.append("**Problema 191 (método).** Con la construcción de subconjuntos, δ_D(Z, a) = ⋃_{q∈Z} δ(q, a), y un subconjunto es de aceptación si contiene un estado de F. Por eso δ̂_D(Z, ω) coincide con δ̂(Z, ω), como muestran los cálculos siguientes.\n")
    d += [seccion("lista3-afn", e, jflap) for e in L3 if 192 <= int(e[0]) <= 195]
    for c, _, tabla, pedidos in [x for x in DELTA_GORRO if x[0] >= 192]:
        d.append(f"**δ̂(Z, ω) y δ̂_D(Z, ω), problema {c}**\n\n| Z | ω | Recorrido | Resultado | ¿Contiene un final? |\n|---|---|---|---|---|")
        for p in pedidos:
            z, w = p.split("|")
            ps = traza(tabla, z, w)
            d.append(f"| {conjunto(z)} | {v(w)} | {' → '.join(conjunto(x) for x in ps)} | {conjunto(ps[-1])} | {'Sí' if ps[-1] & tabla.finales else 'No'} |")
        d.append("")

    d.append("### Problemas 201 a 235: verdadero o falso\n")
    d.append("w ∈ L(r) si w se obtiene de r eligiendo una alternativa en cada +, un número de repeticiones en cada ∗ y concatenando. Además, L(∅) = ∅, ∅r = ∅, L(λ) = {λ} y λr = r. Cada respuesta se calculó con el módulo `re` de Python.\n")
    d.append("| Problema | Afirmación | Respuesta | Razón |\n|---|---|---|---|")
    for n, w, e, razon in VF:
        r = re.fullmatch(vf_python(e), w) is not None
        d.append(f"| {n} | {w or 'λ'} ∈ L({e}) | {'V' if r else 'F'} | {razon} |")
    d.append("| 235 | ∅ ∈ L(∅) | F | L(∅) es el conjunto vacío de palabras, y ∅ ni siquiera es una palabra. |\n")

    d.append("### Problemas 236 a 240 y 254 a 258: expresiones regulares\n")
    d.append("En la sintaxis de JFLAP, `+` es unión y `!` es λ. JFLAP no simula directamente una expresión, de modo que estas se probaron con `re` de Python, contra todas las cadenas de hasta 11 símbolos (hasta 8 en el problema 256, con tres símbolos). Se abren en JFLAP en *Regular Expression*.\n")
    d.append("| Problema | Archivo | Enunciado | Expresión | Razonamiento | Cadenas de prueba |\n|---|---|---|---|---|---|")
    for problema, archivo, enunciado, razon, oraculo in ER:
        expresion = Automata(RAIZ / "automatas" / "lista3-afn" / f"{archivo}.jff").expresion
        muestras = ["", "0", "1", "01", "10", "001", "010", "0101", "00100", "0110"]
        patron = re.compile(er_a_python(expresion))
        pruebas = []
        for x in muestras[:8]:
            assert (patron.fullmatch(x) is not None) == bool(oraculo(x))
            pruebas.append(f"{v(x)} {'✓' if oraculo(x) else '✗'}")
        d.append(f"| {problema} | `{archivo}.jff` | {enunciado} | `{expresion}` | {razon} | {', '.join(pruebas)} |")
    d.append("")

    d.append("### Problemas 254 a 258: autómatas\n")
    d += [seccion("lista3-afn", e, jflap) for e in L3 if 254 <= int(e[0]) <= 258]
    d.append("### Problemas 260 a 263: equivalencia entre AFN y AFD\n")
    d += [seccion("lista3-afn", e, jflap) for e in L3 if int(e[0]) >= 260]
    (RAIZ / "docs" / "04-jflap.md").write_text("\n".join(d), encoding="utf-8")


if __name__ == "__main__":
    {"casos": casos, "documento": documento}[sys.argv[1]]()
