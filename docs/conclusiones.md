# Conclusiones

Esta primera práctica no pidió resolver un problema de teoría de la computación en sentido estricto, sino construir el entorno de trabajo que va a sostener las prácticas siguientes: un repositorio con historial real, un entorno reproducible en tres versiones de Python, y la primera versión —mínima pero funcional— del software interactivo que se irá ampliando práctica tras práctica.

El ejercicio que más se conecta con el contenido teórico de la Unidad Temática I es, sin duda, el Ejercicio 5: implementar prefijos, sufijos, subcadenas y las dos cerraduras obliga a precisar, en código y no solo en papel, convenciones que en la teoría a veces se dan por sentadas (que la cadena vacía es prefijo, sufijo y subcadena de cualquier cadena; que Σ\* y Σ⁺ difieren en un solo elemento pero eso basta para que uno sea monoide y el otro no) y a enfrentar de forma concreta por qué Σ\* es un conjunto infinito: un programa real no puede generarlo completo, solo truncarlo, y ese truncamiento es él mismo una lección sobre el crecimiento exponencial |Σ|^n.

El Ejercicio 4 mostró el valor de comparar cada autómata con una definición independiente: al cotejar los diagramas originales aparecieron dos errores de la Tarea 2 (problemas 128 y 143), que una verificación contra el mismo archivo no habría detectado.

También fue útil ejecutar de verdad el entorno. Las pruebas aprobaban mientras la interfaz no arrancaba por una dependencia indirecta sin versión, y una prueba del límite reveló que contar cadenas no basta para acotar la memoria.

Por último, la Parte C del Ejercicio 1 —tres contenedores con tres versiones de Python— resultó más ilustrativa de lo esperado sobre la diferencia entre un entorno virtual y un contenedor: un entorno virtual reutiliza el intérprete que ya existía en la máquina, así que jamás puede darte tres versiones distintas de Python a la vez; eso solo lo resuelve algo que traiga su propio intérprete empaquetado, que es exactamente lo que hace un contenedor.
