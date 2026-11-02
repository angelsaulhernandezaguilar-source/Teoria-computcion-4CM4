# Ejercicio 2. Investigación: qué es la Teoría de la Computación

## 1. Qué es la Teoría de la Computación y qué preguntas se plantea

La Teoría de la Computación es la rama de las ciencias de la computación que estudia, de forma matemática y abstracta, qué puede calcularse en absoluto, con qué eficiencia puede calcularse y qué modelos mínimos de máquina bastan para reconocer o generar un lenguaje dado. No se ocupa de un lenguaje de programación ni de una computadora concreta, sino de modelos formales —autómatas, gramáticas, máquinas de Turing— que capturan la noción de "cómputo" con independencia de la tecnología con la que se implemente.

Dos definiciones de autores distintos, comparadas:

- Sipser (2013) la describe como el estudio de las capacidades y limitaciones fundamentales de las computadoras, y organiza el campo en tres grandes áreas: complejidad computacional (qué tan difícil es un problema), computabilidad (qué es posible calcular en absoluto) y teoría de autómatas (qué modelo formal de máquina hace falta para resolver un problema o reconocer un lenguaje).
- Hopcroft et al. (2007) la presentan de forma más operativa, como el estudio de modelos matemáticos de computación —los autómatas y las gramáticas— y de las clases de lenguajes que esos modelos pueden reconocer o generar, con especial atención a la relación entre el poder expresivo de un modelo y los recursos (estados, memoria, tiempo) que necesita.

Ambas definiciones coinciden en el fondo —modelos formales de cómputo y sus límites— pero difieren en el énfasis: Sipser organiza el campo alrededor de tres preguntas generales ("¿se puede calcular?", "¿qué tan eficientemente?", "¿con qué máquina mínima?"), mientras que Hopcroft et al. lo presentan desde la maquinaria formal misma (autómatas y gramáticas) hacia las preguntas que esa maquinaria permite responder. En este curso, que empieza precisamente por autómatas y lenguajes formales, conviene tener presentes las dos miradas: la de las preguntas que se quieren responder y la de las herramientas formales con las que se responden.

## 2. Sus orígenes: el programa de Hilbert, el Entscheidungsproblem y las paradojas de la lógica matemática

A principios del siglo XX, David Hilbert propuso un programa para fundamentar toda la matemática sobre una base estrictamente formal (Davis, 2000): un conjunto finito de axiomas y reglas de inferencia del que se pudiera derivar mecánicamente cualquier verdad matemática, con la garantía de que ese sistema fuera a la vez consistente (libre de contradicciones) y completo (capaz de decidir toda proposición). Parte de ese programa era el *Entscheidungsproblem* ("problema de decisión"), planteado formalmente por Hilbert y Ackermann (1928): ¿existe un procedimiento puramente mecánico que, dada cualquier proposición de la lógica de primer orden, determine en un número finito de pasos si es válida o no?

El programa de Hilbert se topó antes con las paradojas de la lógica matemática que ya venían inquietando a la disciplina: la paradoja de Russell sobre el conjunto de todos los conjuntos que no se contienen a sí mismos, y las técnicas de diagonalización de Cantor, que muestran que ciertos conjuntos infinitos no pueden enumerarse. Gödel (1931) llevó esa misma técnica de diagonalización a la aritmética y demostró, con sus teoremas de incompletitud, que ningún sistema formal suficientemente potente para expresar la aritmética puede ser a la vez consistente y completo: siempre habrá enunciados verdaderos que el sistema no pueda demostrar. Esto ya debilitaba el programa de Hilbert, pero dejaba abierta la pregunta más modesta del *Entscheidungsproblem*: aunque no se pueda demostrar todo, ¿se puede al menos decidir mecánicamente qué es válido?

La respuesta llegó en 1936, de forma independiente, con Church (1936), mediante el cálculo lambda y las funciones recursivas, y Turing (1936), mediante su máquina abstracta: ambos demostraron que el *Entscheidungsproblem* no tiene solución algorítmica, es decir, que no existe tal procedimiento mecánico general. Para poder demostrar esa imposibilidad, Turing tuvo que hacer algo adicional y de enorme trascendencia: dar, por primera vez, una definición formal y precisa de qué significa "procedimiento mecánico" o "algoritmo", a través de su máquina. Esa definición es, en sentido estricto, el punto de partida de la Teoría de la Computación como disciplina propia.

## 3. Sus tres ramas y la pregunta que responde cada una

- **Teoría de autómatas y lenguajes formales.** Estudia distintos modelos de máquina abstracta (autómatas finitos, autómatas de pila, máquinas de Turing) y los lenguajes que cada uno puede reconocer o generar. Responde a la pregunta: *¿qué modelo mínimo de máquina —y qué tipo de gramática— basta para reconocer un lenguaje dado?* (Hopcroft et al., 2007).
- **Computabilidad.** Estudia qué problemas admiten en absoluto una solución algorítmica, sin importar cuánto tiempo o memoria tome resolverlos. Responde a la pregunta: *¿es posible calcular esto, existe algún algoritmo que lo resuelva?* (el problema de la detención —*halting problem*— es su ejemplo canónico de problema indecidible) (Sipser, 2013).
- **Complejidad computacional.** Da por hecho que un problema es computable y pregunta, en cambio, con qué eficiencia —cuánto tiempo, cuánta memoria— puede resolverse, y cómo se comparan entre sí distintos problemas según esa dificultad (la pregunta P frente a NP es la más conocida de esta rama). Responde a la pregunta: *dado que sí se puede calcular, ¿qué tan caro es hacerlo?* (Arora y Barak, 2009).

Las tres ramas están ordenadas, de hecho, en una jerarquía natural de exigencia: la teoría de autómatas trabaja con los modelos más restringidos y las preguntas más concretas; la computabilidad usa el modelo más general (la máquina de Turing) para preguntar si algo se puede resolver en absoluto; y la complejidad, una vez aceptado que algo es computable, mide cuánto cuesta.

## 4. La tesis de Church-Turing

La tesis de Church-Turing afirma que toda función que sea "efectivamente calculable" —es decir, calculable siguiendo un procedimiento mecánico, paso a paso, por un ser humano con lápiz y papel y tiempo y memoria ilimitados— puede calcularse mediante una máquina de Turing. Dicho de otro modo: la noción intuitiva e informal de "algoritmo" coincide exactamente con la noción formal y precisa de "función computable por una máquina de Turing" (Copeland, 2020).

Varios modelos de cómputo completamente distintos entre sí se demostraron equivalentes a la máquina de Turing en cuanto al conjunto de funciones que pueden calcular: el cálculo lambda de Church, las funciones recursivas generales de Gödel y Herbrand, las máquinas de Post y los algoritmos de Markov, entre otros. El hecho de que modelos ideados de manera independiente, con formalismos completamente distintos, converjan siempre a la misma clase de funciones computables es la evidencia más fuerte a favor de la tesis.

Se le llama *tesis* y no *teorema* porque no es un enunciado que se demuestre a partir de axiomas dentro de un sistema formal: relaciona una noción informal (qué significa que un humano pueda calcular algo "efectivamente", seguir un algoritmo) con una noción formal (la máquina de Turing). Como uno de los dos lados de esa relación —la noción intuitiva— nunca se definió formalmente, no hay manera de demostrar la equivalencia con el rigor de un teorema matemático; solo puede acumularse evidencia a favor (como la convergencia de todos los modelos conocidos), y por eso permanece, casi noventa años después, en la categoría de tesis ampliamente aceptada, no de teorema demostrado.

## 5. Alfabeto, cadena y lenguaje; operaciones sobre cadenas y lenguajes

Las definiciones de esta sección siguen a Hopcroft et al. (2007) y Kozen (1997).

- **Alfabeto (Σ).** Un conjunto finito y no vacío de símbolos. Ejemplo: Σ = {0, 1}.
- **Cadena.** Una secuencia finita de símbolos tomados de un alfabeto Σ. La cadena que no tiene ningún símbolo se llama cadena vacía y se denota λ (o ε).
- **Lenguaje.** Cualquier subconjunto de Σ*, es decir, cualquier colección de cadenas sobre ese alfabeto (incluyendo el conjunto vacío ∅ y el propio Σ*).

**Operaciones sobre cadenas:**

- *Concatenación* (xy): unir dos cadenas una después de la otra. Si x = "ab" y y = "ba", entonces xy = "abba".
- *Potencia* (w^n): concatenar una cadena consigo misma n veces; w^0 = λ por convención (producto vacío), w^1 = w, w^2 = ww, etc.
- *Reflexión o reversa* (w^R): la misma cadena escrita en orden inverso. Si w = "abc", entonces w^R = "cba".

**Operaciones sobre lenguajes** (siendo L1 y L2 lenguajes sobre el mismo alfabeto):

- *Potencia* (L^n): L⁰ = {λ} y L^(n+1) = L^n L, es decir, concatenar n cadenas de L.
- *Reflexión* (L^R): {w^R : w ∈ L}, las cadenas de L escritas al revés.
- *Unión* (L1 ∪ L2): las cadenas que están en L1, en L2 o en ambos.
- *Intersección* (L1 ∩ L2): las cadenas que están simultáneamente en L1 y en L2.
- *Diferencia* (L1 − L2): las cadenas que están en L1 pero no en L2.
- *Concatenación de lenguajes* (L1L2): todas las cadenas que resultan de concatenar una cadena de L1 con una de L2.
- *Cerradura de Kleene* (Σ\*): la unión de Σ elevado a todas las potencias posibles, Σ\* = Σ⁰ ∪ Σ¹ ∪ Σ² ∪ ⋯, es decir, el conjunto de absolutamente todas las cadenas finitas que pueden formarse con símbolos de Σ, incluida la cadena vacía.
- *Cerradura positiva* (Σ⁺): lo mismo que Σ\*, pero sin incluir la cadena vacía: Σ⁺ = Σ¹ ∪ Σ² ∪ ⋯ = Σ\* − {λ}.

**¿Por qué Σ⁰ = {λ}?** Por la misma convención que hace que cualquier número elevado a la potencia 0 sea 1: un "producto vacío" (aquí, la concatenación de cero cadenas) se define como el elemento neutro de la operación, y el elemento neutro de la concatenación es precisamente la cadena vacía (concatenar λ con cualquier cadena w da w sin cambios). Por eso, sin importar de qué símbolos esté hecho Σ, elevarlo a la potencia 0 da siempre el mismo conjunto de un solo elemento: {λ}.

**¿Qué distingue a Σ\* de Σ⁺?** Exactamente esa cadena vacía: Σ\* la incluye (por eso Σ\* siempre es infinito y nunca vacío, incluso si Σ tiene un solo símbolo) y Σ⁺ no. En términos algebraicos, (Σ\*, concatenación) es un monoide (tiene elemento neutro, λ), mientras que (Σ⁺, concatenación) es solo un semigrupo (la operación es asociativa, pero no hay elemento neutro dentro del propio conjunto).

## 6. La jerarquía de Chomsky

Chomsky (1956) propuso esta clasificación; las máquinas asociadas se presentan en Hopcroft et al. (2007).

| Tipo | Nombre | Forma de las reglas de producción | Máquina que lo reconoce |
|---|---|---|---|
| 0 | Recursivamente enumerable (sin restricción) | α → β, sin ninguna restricción sobre α y β | Máquina de Turing |
| 1 | Sensible al contexto | αAβ → αγβ, con \|γ\| ≥ \|A\| (no decrece la longitud) | Autómata linealmente acotado |
| 2 | Libre de contexto | A → γ, con A un solo símbolo no terminal | Autómata de pila |
| 3 | Regular | A → aB o A → a (lineales por la derecha), o su equivalente por la izquierda | Autómata finito (determinista o no determinista) |

Cada tipo es un caso particular más restringido del anterior (todo lenguaje regular es libre de contexto, todo libre de contexto es sensible al contexto, y todo sensible al contexto es recursivamente enumerable), de modo que el poder expresivo de la gramática y el poder computacional de la máquina que la reconoce crecen exactamente al mismo ritmo: a reglas de producción más permisivas les corresponde, siempre, un modelo de máquina con más memoria y más libertad de movimiento.

## 7. Autómatas finitos y expresiones regulares

**Definición formal de un AFD.** Según Sipser (2013), un autómata finito determinista es una tupla M = (Q, Σ, δ, q₀, F), donde Q es un conjunto finito de estados, Σ es el alfabeto de entrada, δ: Q × Σ → Q es la función de transición (total: para cada estado y cada símbolo hay exactamente una transición definida), q₀ ∈ Q es el estado inicial y F ⊆ Q es el conjunto de estados de aceptación. Una cadena w se acepta si, al leerla símbolo por símbolo desde q₀ siguiendo δ, la trayectoria termina en un estado de F.

**Definición formal de un AFN.** Un autómata finito no determinista es igual, salvo que la función de transición es δ: Q × Σ → 2^Q (puede llevar a cero, uno o varios estados a la vez para el mismo símbolo desde el mismo estado); una cadena se acepta si existe *al menos una* trayectoria posible que termine en un estado de F. Una variante, el AFN-λ, permite además transiciones que no consumen ningún símbolo de la entrada.

**Su equivalencia.** Aunque un AFN parece, a primera vista, un modelo más poderoso que un AFD (por permitir varias trayectorias a la vez), Rabin y Scott (1959) demostraron que ambos modelos reconocen exactamente la misma clase de lenguajes: todo AFN puede convertirse en un AFD equivalente mediante la construcción de subconjuntos (cada estado del AFD resultante representa el conjunto de todos los estados en los que el AFN podría estar simultáneamente). La no determinación resulta ser, entonces, solo una comodidad de diseño, no una fuente de poder adicional. A esa misma clase de lenguajes —los lenguajes regulares— se llega también por un tercer camino, el de las expresiones regulares: Kleene (1956) demostró que los lenguajes descritos por expresiones regulares son exactamente los mismos que reconocen los autómatas finitos, cerrando así la equivalencia entre los tres formalismos (AFD, AFN y expresiones regulares).

**Tres problemas reales donde se aplican las expresiones regulares:**

1. **Análisis léxico de compiladores e intérpretes.** La primera fase de un compilador (el *lexer*) reconoce identificadores, números, palabras reservadas y operadores de un programa fuente usando, en esencia, un autómata finito construido a partir de expresiones regulares que describen cada tipo de token.
2. **Búsqueda y autocompletado de texto.** Herramientas como `grep`, los motores de búsqueda de texto de los editores, o el autocompletado de bibliotecas como Apache Lucene, usan expresiones regulares (o máquinas de estados equivalentes) para encontrar patrones dentro de grandes volúmenes de texto de manera eficiente (Gribkoff, 2013).
3. **Detección de intrusiones en redes y bioinformática.** Los sistemas de detección de intrusiones inspeccionan el tráfico de red comparándolo contra firmas de ataques descritas como expresiones regulares, implementadas como autómatas para poder revisar paquetes a la velocidad de la red (Češka et al., 2020); de forma análoga, la búsqueda de patrones en secuencias de ADN o de proteínas en bioinformática se resuelve con las mismas técnicas de reconocimiento de patrones basadas en autómatas.

---

*Las referencias en formato APA 7 están en [`bibliografia.md`](bibliografia.md).*
