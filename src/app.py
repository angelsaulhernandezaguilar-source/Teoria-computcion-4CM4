"""
Interfaz grafica (Flet) para las operaciones basicas sobre cadenas y
lenguajes de la Practica 1.

Este archivo SOLO conecta botones con las funciones puras de lenguajes.py.
No hay ninguna logica de calculo aqui: eso permite probar lenguajes.py con
pytest sin necesitar Flet ni un navegador (ver tests/test_lenguajes.py).
"""

import flet as ft

from lenguajes import (
    cerradura_kleene,
    cerradura_positiva,
    maximo_numero_subcadenas,
    parsear_alfabeto,
    prefijos,
    subcadenas,
    sufijos,
)


def main(page: ft.Page):
    page.title = "Practica 1 - Operaciones basicas sobre lenguajes"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    # ---------------------------------------------------------------
    # Operacion 1: subcadenas, prefijos y sufijos
    # ---------------------------------------------------------------
    entrada_cadena = ft.TextField(label="Cadena", hint_text="ej: abba", width=300)
    salida_op1 = ft.Text(selectable=True)
    resumen_op1 = ft.Text(selectable=True, italic=True)
    _ultimo_resultado_op1 = {"texto": ""}

    def calcular_op1(e):
        w = entrada_cadena.value or ""
        pre = prefijos(w)
        suf = sufijos(w)
        sub = subcadenas(w)
        n = len(w)

        texto = (
            f"Prefijos ({len(pre)}): {', '.join(repr(p) for p in pre)}\n\n"
            f"Sufijos ({len(suf)}): {', '.join(repr(s) for s in suf)}\n\n"
            f"Subcadenas distintas ({len(sub)}): "
            f"{', '.join(repr(s) for s in sub)}"
        )
        salida_op1.value = texto
        resumen_op1.value = (
            f"Para |w| = {n}: exactamente {n + 1} prefijos y {n + 1} sufijos; "
            f"como maximo {maximo_numero_subcadenas(n)} subcadenas distintas "
            f"(menos si hay simbolos repetidos). La cadena vacia se cuenta "
            f"como prefijo, sufijo y subcadena de cualquier cadena."
        )
        _ultimo_resultado_op1["texto"] = texto
        page.update()

    file_picker_op1 = ft.FilePicker(
        on_result=lambda e: (
            None
            if not e.path
            else open(e.path, "w", encoding="utf-8").write(_ultimo_resultado_op1["texto"])
        )
    )
    page.overlay.append(file_picker_op1)

    boton_guardar_op1 = ft.ElevatedButton(
        "Guardar en archivo",
        on_click=lambda e: file_picker_op1.save_file(
            file_name="operacion1_resultado.txt"
        ),
    )

    seccion_op1 = ft.Column(
        [
            ft.Text("Operacion 1. Subcadenas, prefijos y sufijos", size=18, weight="bold"),
            ft.Row([entrada_cadena, ft.ElevatedButton("Calcular", on_click=calcular_op1)]),
            salida_op1,
            resumen_op1,
            boton_guardar_op1,
        ],
        spacing=8,
    )

    # ---------------------------------------------------------------
    # Operacion 2: cerradura de Kleene y cerradura positiva
    # ---------------------------------------------------------------
    entrada_alfabeto = ft.TextField(
        label="Alfabeto (separado por comas)", hint_text="ej: a,b,c", width=300
    )
    entrada_longitud = ft.TextField(
        label="Longitud maxima de las cadenas", hint_text="ej: 3", width=200
    )
    salida_op2 = ft.Text(selectable=True)
    mensaje_op2 = ft.Text(selectable=True, color=ft.Colors.RED)
    _ultimo_resultado_op2 = {"texto": ""}

    def calcular_op2(e):
        mensaje_op2.value = ""
        try:
            alfabeto = parsear_alfabeto(entrada_alfabeto.value or "")
            n = int(entrada_longitud.value)
            if n < 0:
                raise ValueError("La longitud maxima debe ser >= 0.")

            kleene = cerradura_kleene(alfabeto, n)
            positiva = cerradura_positiva(alfabeto, n)

            texto = (
                f"Sigma* (truncado a longitud {n}), {len(kleene)} cadenas:\n"
                f"{', '.join(repr(s) for s in kleene)}\n\n"
                f"Sigma+ (truncado a longitud {n}), {len(positiva)} cadenas:\n"
                f"{', '.join(repr(s) for s in positiva)}"
            )
            salida_op2.value = texto
            _ultimo_resultado_op2["texto"] = texto
        except ValueError as err:
            salida_op2.value = ""
            mensaje_op2.value = str(err)
        page.update()

    file_picker_op2 = ft.FilePicker(
        on_result=lambda e: (
            None
            if not e.path
            else open(e.path, "w", encoding="utf-8").write(_ultimo_resultado_op2["texto"])
        )
    )
    page.overlay.append(file_picker_op2)

    boton_guardar_op2 = ft.ElevatedButton(
        "Guardar en archivo",
        on_click=lambda e: file_picker_op2.save_file(
            file_name="operacion2_resultado.txt"
        ),
    )

    seccion_op2 = ft.Column(
        [
            ft.Text("Operacion 2. Cerradura de Kleene y cerradura positiva", size=18, weight="bold"),
            ft.Row([entrada_alfabeto, entrada_longitud, ft.ElevatedButton("Calcular", on_click=calcular_op2)]),
            mensaje_op2,
            salida_op2,
            boton_guardar_op2,
        ],
        spacing=8,
    )

    page.add(
        ft.Text("Operaciones basicas sobre cadenas y lenguajes", size=24, weight="bold"),
        ft.Divider(),
        seccion_op1,
        ft.Divider(),
        seccion_op2,
    )


if __name__ == "__main__":
    ft.run(main)  # en versiones anteriores de Flet: ft.app(target=main)
