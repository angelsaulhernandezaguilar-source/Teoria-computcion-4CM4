# Ejercicio 4. Autómatas finitos en JFLAP

## Qué ya está resuelto: la Lista 2 (ejercicios 94 a 150)

Los ejercicios marcados con asterisco de la Lista 2 (autómatas finitos) ya se diseñaron, se verificaron programáticamente contra la definición del lenguaje correspondiente y, donde fue posible, se minimizaron, como parte de la Tarea 2 de este mismo curso (documento `HernandezAguilar_AngelSaul_2025630123_TC_Tarea02.pdf`, que vive junto a este repositorio). Los 31 archivos `.jff` resultantes ya se copiaron a `automatas/lista2-afd/` de este repositorio:

```
ejercicio_097.jff  ejercicio_109.jff  ejercicio_122.jff  ejercicio_137.jff  ejercicio_147.jff
ejercicio_099.jff  ejercicio_111.jff  ejercicio_123.jff  ejercicio_139.jff  ejercicio_148.jff
ejercicio_102.jff  ejercicio_112.jff  ejercicio_124.jff  ejercicio_141.jff  ejercicio_149.jff
ejercicio_103.jff  ejercicio_113.jff  ejercicio_128_L2.jff ejercicio_143a.jff ejercicio_150.jff
ejercicio_106.jff  ejercicio_118.jff  ejercicio_128_M.jff  ejercicio_143b.jff
ejercicio_107.jff  ejercicio_120.jff  ejercicio_131.jff    ejercicio_145.jff
                                       ejercicio_133.jff
                                       ejercicio_135.jff
```

El documento de la Tarea 2 ya explica, para cada uno, el proceso de diseño y qué representa cada estado (por ejemplo: en el ejercicio 97, los tres estados representan el residuo de la longitud leída al dividirla entre 3; en el 145, el estado codifica el residuo módulo 5 del valor binario leído hasta el momento, más la posición leída módulo 4). Esa misma explicación se reutiliza aquí como la "documentación del proceso de diseño" que pide este ejercicio; no hace falta reescribirla, solo enlazarla:

- Tabla de transiciones incluida en el propio documento de la Tarea 2 para, entre otros, los ejercicios 97, 99, 102, 103, 106, 112, 113, 120, 128, 133, 137, 139, 141, 143, 145 y 147 — son más de los cinco que exige el mínimo del enunciado.
- Los ejercicios 107, 109 y 111 tienen automátas grandes (13, 22 y 21 estados) que se dejaron **solo** en el archivo `.jff` por claridad del reporte en PDF; en este repositorio, al ser el propio `.jff` el entregable, eso ya no es una limitación: se abren y se simulan directamente.

**Lo que falta para cerrar por completo este ejercicio con la Lista 2** (trabajo de laboratorio, no de diseño, porque el diseño ya está hecho):

1. Abrir cada uno de los `.jff` en JFLAP y, para al menos cinco autómatas, correr **Input → Step with Closure** (simulación paso a paso) con capturas de pantalla, guardadas en `evidencias/jflap/`.
2. Para cada autómata, probar al menos tres cadenas válidas y tres inválidas (la propia Tarea 2 ya da, para varios ejercicios, un ejemplo de cadena aceptada que sirve como punto de partida — por ejemplo `001001` para el ejercicio 99, o `0010` para el 124) y documentar el resultado.
3. Incluir al menos un caso frontera por autómata (la cadena vacía, la cadena aceptada más corta, o una que quede justo debajo del umbral que pide el enunciado).

## Lo que falta por completo: la Lista 3 (ejercicios 151 a 263)

A diferencia de la Lista 2, la Lista 3 —simplificación de autómatas, AFN, AFN-λ y expresiones regulares, ejercicios 151 a 263— **todavía no se ha trabajado**. Es, en volumen, un trabajo comparable al que ya se hizo para la Lista 2 (más de 100 ejercicios marcados, de los cuales el profesor pide solo los que llevan asterisco), y por su naturaleza —simplificación de AFD, conversión AFN → AFD, eliminación de transiciones λ, construcción de expresiones regulares— no se puede resolver de forma responsable en las horas que quedan antes de la fecha de entrega de esta práctica sin sacrificar la calidad y la verificación programática que sí se aplicó a la Lista 2.

**Recomendación honesta para la entrega de mañana:** dado que el Ejercicio 4 vale 20 de los 100 puntos y evalúa "autómatas correctos, archivos .jff versionados, pruebas y justificación del diseño" en conjunto con el resto de la práctica, conviene priorizar así, en este orden, con el tiempo que quede hoy:

1. Completar primero el Ejercicio 1 (25 puntos: repositorio, Docker) y el Ejercicio 5 (15 puntos: la aplicación), que ya están resueltos en este repositorio y solo requieren que tú ejecutes los pasos de Git y Docker.
2. Usar el tiempo restante en la evidencia de JFLAP de la Lista 2 (capturas, pruebas de cadenas), que ya está diseñada y solo falta documentar visualmente.
3. Entregar la Lista 3 como trabajo en progreso, documentado honestamente como tal en este mismo archivo (mejor una nota clara de "pendiente, se continúa en la siguiente entrega" que faltar a la regla del curso de "nada que no sea tuyo, sin decirlo"), y seguir avanzándola en una sesión aparte — puedo ayudarte a resolverla con el mismo nivel de rigor que la Lista 2 en cuanto quede lista la parte de Git y Docker, o en una sesión dedicada solo a eso.

## Estructura de entrega

Todos los autómatas se exportan en formato `.jff` y se versionan dentro de `automatas/`, separados por lista:

```
automatas/
  lista2-afd/       # ejercicios 94-150, Lista 2 (completo, ver arriba)
  lista3-afnd/       # ejercicios 151-263, Lista 3 (pendiente, ver arriba)
```
