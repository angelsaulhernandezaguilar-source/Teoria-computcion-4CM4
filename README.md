# Teoría de la Computación — Práctica 1: Operaciones básicas sobre lenguajes

**Nombre completo:** Ángel Saúl Hernández Aguilar  
**Boleta:** 2025630123  
**Grupo:** 4CM4  
**Carrera:** Ingeniería en Sistemas Computacionales  
**Unidad de aprendizaje:** Teoría de la Computación  
**Profesor:** M. en C. Gabriel Hurtado Avilés  
**Fecha límite de entrega:** martes 22 de septiembre de 2026 (la fecha efectiva es la de la última confirmación en `main`)

## Qué hay aquí

| Documento | Contenido |
|---|---|
| [Ejercicio 1](docs/01-entorno.md) | Investigación, repositorio y los tres contenedores |
| [Ejercicio 2](docs/02-investigacion.md) | Qué es la Teoría de la Computación |
| [Ejercicio 3](docs/03-estado-del-arte.md) | Fichas y comparación de los cinco textos |
| [Ejercicio 4](docs/04-jflap.md) | Autómatas de las Listas 2 y 3, con pruebas |
| [Ejercicio 5](docs/05-aplicacion.md) | Aplicación con interfaz gráfica |
| [Conclusiones](docs/conclusiones.md) | Conclusiones de la práctica |
| [Bibliografía](docs/bibliografia.md) | Referencias en formato APA 7 |

| Carpeta | Contenido |
|---|---|
| `entorno/` | `Dockerfile` y `compose.yml` |
| `automatas/` | Archivos `.jff` de la Lista 2 y de la Lista 3 |
| `src/` | `lenguajes.py` (núcleo) y `app.py` (interfaz) |
| `tests/` | Pruebas con pytest |
| `herramientas/` | Verificación de los `.jff` y generación del documento del Ejercicio 4 |
| `evidencias/` | Capturas y salidas de cada ejercicio |

**Versión de Flet:** 0.86.5.

## Cómo se ejecuta

Requiere Docker Desktop (o Podman) instalado y encendido. Desde la raíz del repositorio:

```bash
cd entorno
docker compose build
docker compose run --rm py311 python --version
docker compose run --rm py312 python --version
docker compose run --rm py313 python --version
docker compose run --rm py311 pytest -q
docker compose run --rm py312 pytest -q
docker compose run --rm py313 pytest -q
docker compose up py312          # levanta la interfaz; abrir http://localhost:8550
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
pytest -q
```

## Uso de inteligencia artificial en este trabajo

En cumplimiento del principio de transparencia académica, se documenta aquí el uso de un asistente de inteligencia artificial en la elaboración de esta práctica:

- Se usó como apoyo para **redactar y organizar** la investigación de las Partes A y del Ejercicio 2, a partir de fuentes verificadas y citadas explícitamente en `docs/bibliografia.md`.
- Se usó para **redactar el código** de `src/lenguajes.py`, `src/app.py` y `tests/test_lenguajes.py`, siguiendo la separación entre núcleo e interfaz que pide el enunciado; el código se ejecutó y se probó en los tres contenedores (19 pruebas aprobadas en cada uno).
- Se usó para **consultar y verificar fuentes actuales** citadas en el reporte (el calendario de fin de soporte de Python en `devguide.python.org`, el requisito de versión de Flet en PyPI, y los datos de los dos artículos localizados para el Ejercicio 3), en vez de citarlas de memoria.
- **No** se usó para inventar resultados de lectura que no correspondan a lo escrito en las fuentes primarias: la respuesta sobre la dificultad de leer el texto original del Ejercicio 3 la redacta el autor, y es su responsabilidad haber leído los cinco textos y poder defenderlos.
- Las decisiones de diseño (qué exigir en cada operación, qué convención adoptar para la cadena vacía, cómo justificar la elección de versiones de Python) se revisaron y se adoptaron por el autor de este repositorio, no se copiaron sin verificar.

## Licencia y autoría

Trabajo académico individual para la Unidad de Aprendizaje de Teoría de la Computación, ESCOM–IPN, periodo 2027-1.
