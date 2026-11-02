# Teoría de la Computación — Práctica 1: Operaciones básicas sobre lenguajes

**Nombre completo:** Ángel Saúl Hernández Aguilar
**Boleta:** 2025630123
**Grupo:** 4CM4
**Carrera:** Ingeniería en Sistemas Computacionales
**Unidad de aprendizaje:** Teoría de la Computación
**Profesor:** M. en C. Gabriel Hurtado Avilés
**Fecha de entrega:** *(completar el día que se confirme la última confirmación en `main`; fecha límite: martes 22 de septiembre de 2026)*

## Qué hay aquí

| Carpeta / archivo | Contenido |
|---|---|
| `docs/01-entorno.md` | Ejercicio 1: investigación (Parte A), repositorio (Parte B) y los tres contenedores de Python (Parte C) |
| `docs/02-investigacion.md` | Ejercicio 2: qué es la Teoría de la Computación |
| `docs/03-estado-del-arte.md` | Ejercicio 3: fichas y tabla comparativa de los cinco artículos |
| `docs/04-jflap.md` | Ejercicio 4: autómatas en JFLAP (Lista 2 completa; Lista 3 pendiente, ver el propio documento) |
| `docs/05-aplicacion.md` | Ejercicio 5: la aplicación con interfaz gráfica |
| `docs/conclusiones.md` | Conclusiones de la práctica |
| `docs/bibliografia.md` | Todas las referencias en formato APA 7 |
| `entorno/` | `Dockerfile` y `compose.yml` de los tres contenedores (py311, py312, py313) |
| `automatas/` | Los `.jff` de las Listas 2 y 3 (ver `automatas/README.md`) |
| `src/lenguajes.py` | Núcleo puro: subcadenas, prefijos, sufijos, cerradura de Kleene y positiva |
| `src/app.py` | Interfaz gráfica en Flet |
| `tests/test_lenguajes.py` | Pruebas con pytest |
| `evidencias/` | Capturas de pantalla que respaldan cada ejercicio |

## Cómo se ejecuta

Requiere Docker Desktop (o Podman) instalado y encendido. Desde la raíz del repositorio:

```bash
cd entorno
docker compose build
docker compose up py312          # levanta la interfaz; abrir http://localhost:8550
docker compose run --rm py311 pytest -q
docker compose run --rm py313 pytest -q
docker compose down
```

Si se usa Podman en lugar de Docker Desktop, los mismos comandos funcionan sustituyendo `docker` por `podman`.

Alternativa sin Docker, con un entorno virtual de Python 3.12 (versión de referencia del curso):

```bash
py -3.12 -m venv venv
venv\Scripts\activate            # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python src/app.py
```

Las pruebas, sin Docker:

```bash
pip install pytest
pytest -q
```

## Uso de inteligencia artificial en este trabajo

En cumplimiento del principio de transparencia académica, se documenta aquí el uso de un asistente de inteligencia artificial (Claude, de Anthropic) en la elaboración de esta práctica:

- Se usó como apoyo para **redactar y organizar** la investigación de las Partes A y del Ejercicio 2, a partir de fuentes verificadas y citadas explícitamente en `docs/bibliografia.md`.
- Se usó para **redactar el código** de `src/lenguajes.py`, `src/app.py` y `tests/test_lenguajes.py`, siguiendo la separación entre núcleo e interfaz que pide el enunciado; el código se ejecutó y se probó (`pytest -q`, 14 pruebas aprobadas) antes de incluirse en este repositorio.
- Se usó para **consultar y verificar fuentes actuales** citadas en el reporte (el calendario de fin de soporte de Python en `devguide.python.org`, el requisito de versión de Flet en PyPI, y los datos de los dos artículos localizados para el Ejercicio 3), en vez de citarlas de memoria.
- Las decisiones de diseño (qué exigir en cada operación, qué convención adoptar para la cadena vacía, cómo justificar la elección de versiones de Python) se revisaron y se adoptaron por el autor de este repositorio, no se copiaron sin verificar.

## Licencia y autoría

Trabajo académico individual para la Unidad de Aprendizaje de Teoría de la Computación, ESCOM–IPN, periodo 2027-1.
