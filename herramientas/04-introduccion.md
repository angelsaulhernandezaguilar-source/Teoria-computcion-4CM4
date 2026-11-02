# Ejercicio 4. Autómatas finitos en JFLAP

Este documento resuelve los problemas con asterisco de la Lista 2 y de la Lista 3. Hay {n_jff} archivos `.jff` en `automatas/`. Las tablas y los resultados se generan con `herramientas/generar_reporte.py` a partir de esos archivos, de modo que no pueden diferir de ellos.

## Cómo se validó

1. **Contra el enunciado.** `herramientas/catalogo.py` define cada lenguaje a partir de su enunciado, sin usar el autómata. `tests/test_automatas.py` compara ambos con {comparadas} cadenas, entre ellas todas las cortas sobre cada alfabeto y otras largas al azar. No hubo discrepancias.
2. **En JFLAP.** `herramientas/JflapLote.java` ejecuta {n_casos} casos en el motor de JFLAP 7.1. Los resultados están en `evidencias/jflap/resultados-jflap.tsv`. Cada autómata tiene al menos tres cadenas válidas, tres inválidas y un caso frontera, salvo los lenguajes finitos, donde se indica.
3. **Paso a paso.** Se simularon siete autómatas en la ventana de JFLAP. `herramientas/JflapPasos.java` conduce la ventana y guarda la imagen de cada paso.

Los problemas 128, 143, 156 a 161, 261 y 263 se dan por figura, y sus archivos se cotejaron con la figura a alta resolución. En 156 y 157, la definición de referencia es esa misma transcripción.

**Cómo leer las tablas.** → marca el estado inicial y ∗ los de aceptación. La última columna da la cadena más corta que alcanza cada estado, como ejemplo de la información del prefijo que el estado resume.

## Correcciones respecto a la Tarea 2

Al cotejar las figuras se hallaron dos errores en lo entregado en la Tarea 2. Aquí ya están corregidos:

| Problema | En la Tarea 2 | Correcto según la figura |
|---|---|---|
| 128 | F era absorbente y F' = {{D, E, F}} | F regresa a D con 0 y con 1, por lo que F' = {{D, E}} |
| 143(b) | q0 pasaba a q1 con a y con b; L = Σ⁺ | q0 solo sale con a y q1 regresa a q0 con b; L = a(a+b)* |

Ejemplo del 128: `0010011` termina en D y no pertenece a L; con la tabla de la Tarea 2 sí pertenecía, porque F no se abandonaba.

