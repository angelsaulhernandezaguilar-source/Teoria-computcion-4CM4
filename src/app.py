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


def mostrar(cadenas):
    """Une las cadenas para la pantalla, escribiendo la vacia como lambda."""
    return ", ".join(c if c else "λ" for c in cadenas) or "∅"


def main(page: ft.Page):
    page.title = "Práctica 1 - Operaciones básicas sobre lenguajes"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    selector = ft.FilePicker()
    page.services.append(selector)

    async def guardar(texto, nombre):
        # En modo web el navegador descarga el archivo a partir de src_bytes.
        await selector.save_file(file_name=nombre, src_bytes=texto.encode("utf-8"))

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
            f"Prefijos ({len(pre)}): {mostrar(pre)}\n\n"
            f"Sufijos ({len(suf)}): {mostrar(suf)}\n\n"
            f"Subcadenas distintas ({len(sub)}): "
            f"{mostrar(sub)}"
        )
        salida_op1.value = texto
        resumen_op1.value = (
            f"Para |w| = {n}: exactamente {n + 1} prefijos y {n + 1} sufijos; "
            f"como máximo {maximo_numero_subcadenas(n)} subcadenas distintas "
            f"(menos si hay símbolos repetidos). La cadena vacía se cuenta "
            f"como prefijo, sufijo y subcadena de cualquier cadena."
        )
        _ultimo_resultado_op1["texto"] = texto
        page.update()

    async def guardar_op1(e):
        await guardar(_ultimo_resultado_op1["texto"], "operacion1_resultado.txt")

    boton_guardar_op1 = ft.Button("Guardar en archivo", on_click=guardar_op1)

    seccion_op1 = ft.Column(
        [
            ft.Text("Operación 1. Subcadenas, prefijos y sufijos", size=18, weight="bold"),
            ft.Row([entrada_cadena, ft.Button("Calcular", on_click=calcular_op1)]),
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
        label="Longitud máxima", hint_text="ej: 3", width=200
    )
    salida_op2 = ft.Text(selectable=True)
    mensaje_op2 = ft.Text(selectable=True, color=ft.Colors.RED)
    _ultimo_resultado_op2 = {"texto": ""}

    def calcular_op2(e):
        mensaje_op2.value = ""
        try:
            alfabeto = parsear_alfabeto(entrada_alfabeto.value or "")
            try:
                n = int(entrada_longitud.value)
            except (TypeError, ValueError):
                raise ValueError("La longitud máxima debe ser un número entero.")

            kleene = cerradura_kleene(alfabeto, n)
            positiva = cerradura_positiva(alfabeto, n)

            texto = (
                f"Sigma* (truncado a longitud {n}), {len(kleene)} cadenas:\n"
                f"{mostrar(kleene)}\n\n"
                f"Sigma+ (truncado a longitud {n}), {len(positiva)} cadenas:\n"
                f"{mostrar(positiva)}"
            )
            salida_op2.value = texto
            _ultimo_resultado_op2["texto"] = texto
        except ValueError as err:
            salida_op2.value = ""
            _ultimo_resultado_op2["texto"] = ""
            mensaje_op2.value = str(err)
        page.update()

    async def guardar_op2(e):
        await guardar(_ultimo_resultado_op2["texto"], "operacion2_resultado.txt")

    boton_guardar_op2 = ft.Button("Exportar a archivo", on_click=guardar_op2)

    seccion_op2 = ft.Column(
        [
            ft.Text("Operación 2. Cerradura de Kleene y cerradura positiva", size=18, weight="bold"),
            ft.Row([entrada_alfabeto, entrada_longitud, ft.Button("Calcular", on_click=calcular_op2)]),
            mensaje_op2,
            salida_op2,
            boton_guardar_op2,
        ],
        spacing=8,
    )

    page.add(
        ft.Text("Operaciones básicas sobre cadenas y lenguajes", size=24, weight="bold"),
        ft.Divider(),
        seccion_op1,
        ft.Divider(),
        seccion_op2,
    )


if __name__ == "__main__":
    ft.run(main)  # en versiones anteriores de Flet: ft.app(target=main)
