### Problema 116 — L = {aⁿ bᵐ cⁿ⁺¹ : m, n ∈ ℕ}: no es regular

No hay archivo `.jff`, porque no existe un AFD para este lenguaje. Supóngase que L es regular y sea p la constante del lema del bombeo. Se toma w = aᵖ b⁰ cᵖ⁺¹ ∈ L. Toda descomposición w = xyz con |xy| ≤ p y |y| ≥ 1 cumple y = aᵏ, con k ≥ 1. Entonces xy⁰z = aᵖ⁻ᵏ cᵖ⁺¹ tiene k + 1 símbolos c más que a, en lugar de uno, así que xy⁰z ∉ L. Esto contradice el lema. Por tanto, L no es regular.

### Problema 125 — lenguaje de (Q, Σ, δ, A₀, Q \ F)

Como el AFD es total, cada w termina en un único estado q = δ̂(A₀, w), y w se acepta si y solo si q ∉ F. El lenguaje es el complemento, Σ* \ L(A).

### Problema 126 — lenguaje si F = ∅

Ningún cómputo puede terminar en un estado de F, así que L(A) = ∅.

### Problema 127 — lenguaje si F = Q

Todo cómputo termina en algún estado de Q = F, así que L(A) = Σ*.

### Problema 143 — lenguajes de las figuras

L(a) = Σ* = (a+b)* y L(b) = a(a+b)*.

### Problema 149 — datos

Q = {A, B, C}, Σ = {0, 1}, A₀ = A, F = {C}.

### Problema 150 — datos

Q = {A, B, C, D}, Σ = {0, 1, a}, A₀ = A, F = {B, C, D}.

