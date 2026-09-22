# Ejercicio 1. Entorno de trabajo: control de versiones y contenedores

## Parte A. Investigación

### ¿Qué es un sistema de control de versiones y qué problema resuelve en un trabajo en equipo?

Un sistema de control de versiones (SCV) es un programa que lleva un historial completo de los cambios hechos a un conjunto de archivos: quién cambió qué, cuándo y por qué (a través del mensaje que acompaña cada cambio). No guarda solo "la última versión buena", como haría una carpeta con copias de seguridad, sino la secuencia completa de estados por los que pasó el proyecto, de modo que se puede reconstruir cualquier punto anterior o comparar dos momentos línea por línea.

El problema que resuelve en equipo es la coordinación: sin un SCV, cuando dos personas (o la misma persona en dos momentos distintos) modifican el mismo proyecto, no hay manera confiable de saber cuál es la versión vigente, qué cambió exactamente cada quien, ni cómo combinar el trabajo de ambos sin que uno sobrescriba al otro. Git en particular resuelve esto permitiendo que cada persona trabaje en su propia copia completa del historial (es un sistema *distribuido*) y ofreciendo mecanismos explícitos —ramas y fusiones— para integrar el trabajo de varias personas de forma ordenada y con un registro de quién hizo qué.

### ¿Cuál es la diferencia entre Git y GitHub?

Git es el programa que lleva el historial de cambios; se ejecuta en la propia computadora, funciona sin conexión a internet y es software libre: se podría usar toda la vida sin subir nunca nada a ningún servidor. GitHub, en cambio, es un servicio en línea (una empresa) que aloja repositorios de Git y añade funciones que Git por sí solo no tiene: una interfaz web, control de permisos y colaboradores, gestión de incidencias (*issues*) y, sobre todo, los Pull Request. Existen alternativas equivalentes a GitHub, como GitLab, Bitbucket o Codeberg, porque todas ellas son solo un lugar donde alojar y complementar algo que Git ya hace por sí mismo. En resumen: Git es la herramienta; GitHub es uno de varios sitios donde se puede alojar lo que esa herramienta produce.

### Definiciones con ejemplo

- **Repositorio.** La carpeta del proyecto junto con todo su historial de cambios. Ejemplo: la carpeta `practica1-tc/` de este trabajo, una vez inicializada con `git init`, es un repositorio: contiene tanto el código y los documentos como el registro de cada confirmación hecha sobre ellos.
- **Confirmación (*commit*).** Una fotografía del proyecto en un momento dado, junto con un mensaje que explica qué cambió y por qué. Ejemplo: después de escribir `lenguajes.py`, una confirmación con el mensaje "Implementa prefijos, sufijos y subcadenas" deja registrado ese avance de forma permanente en el historial.
- **Rama (*branch*).** Una línea de desarrollo paralela a la principal (`main`), que permite trabajar en algo nuevo sin arriesgar lo que ya funciona. Ejemplo: crear la rama `practica-1-flet` para desarrollar la interfaz gráfica mientras `main` se mantiene estable.
- **Fusión (*merge*).** El acto de integrar los cambios de una rama en otra. Ejemplo: cuando la interfaz de `practica-1-flet` ya funciona, se fusiona en `main` y a partir de ese momento `main` incluye también esos cambios.
- **Conflicto de fusión.** Ocurre cuando dos ramas modificaron las mismas líneas del mismo archivo de forma distinta y Git no puede decidir por sí solo cuál versión conservar; hay que abrir el archivo, ver ambas versiones marcadas y decidir manualmente cuál se queda (o escribir una tercera). Ejemplo: si `main` y `practica-1-flet` cambiaron ambas la primera línea de `app.py`, al fusionar aparece un conflicto ahí.
- **Pull Request (PR).** Una solicitud, abierta desde GitHub, para fusionar una rama dentro de otra (normalmente dentro de `main`), que además describe qué hace el cambio y permite revisarlo línea por línea antes de integrarlo. Ejemplo: abrir un PR que diga "Añade la aplicación de Flet con las Operaciones 1 y 2" antes de fusionar `practica-1-flet` en `main`.
- **Archivo `.gitignore`.** Una lista de patrones de archivos y carpetas que Git debe ignorar y nunca subir al historial, típicamente por ser regenerables (`__pycache__/`) o por depender de la máquina local (`venv/`). Ejemplo: el `.gitignore` de este repositorio excluye `venv/`, `__pycache__/` y `*.pyc`, pero no excluye los archivos `.jff`, que sí son parte del entregable.
- **Archivo `README.md`.** El documento de portada del repositorio: lo primero que se lee al abrirlo. Debe explicar quién es el autor, qué contiene el proyecto y, sobre todo, el comando exacto para instalarlo y ejecutarlo, de modo que cualquier persona pueda reproducirlo leyendo solo ese archivo.

### ¿Qué es un contenedor y en qué se diferencia de una máquina virtual, en cuanto a arranque, tamaño y aislamiento?

Un contenedor es un entorno aislado que empaqueta un programa junto con exactamente las dependencias que necesita (versión del lenguaje, bibliotecas, herramientas del sistema), pero sin llevar un sistema operativo completo propio: comparte el núcleo (*kernel*) del sistema anfitrión. Una máquina virtual, en cambio, sí incluye un sistema operativo invitado completo, que se ejecuta sobre un hipervisor encima del sistema anfitrión.

Esa diferencia se refleja en tres aspectos concretos:

| Criterio | Máquina virtual | Contenedor |
|---|---|---|
| Arranque | Minutos (arranca un sistema operativo completo) | Segundos (solo arranca el proceso) |
| Tamaño típico | Varios gigabytes | Decenas o cientos de megabytes |
| Aislamiento | Total: núcleo propio, aislamiento estricto | Suficiente para la mayoría de los casos: comparte el núcleo del anfitrión |

En Windows y macOS, Docker sí usa por debajo una máquina virtual ligera (en Windows, WSL 2), pero es una sola, compartida por todos los contenedores que se ejecuten, y no una por cada aplicación como en la virtualización clásica.

### Definiciones: imagen, contenedor, volumen y puerto publicado

- **Imagen.** La plantilla de solo lectura a partir de la cual se crean contenedores: por ejemplo, "Python 3.12 con las bibliotecas del proyecto ya instaladas". Se construye o se descarga una sola vez y se reutiliza. La relación entre imagen y contenedor es la misma que entre una clase y un objeto: de una sola imagen pueden crearse muchos contenedores.
- **Contenedor.** Una instancia en ejecución de una imagen. De la misma imagen `python:3.12-slim` con este proyecto instalado pueden levantarse, por ejemplo, tres contenedores simultáneos (`py311`, `py312`, `py313` en este trabajo), cada uno con su propia versión del intérprete.
- **Volumen.** Una carpeta del disco real que se conecta ("monta") dentro del contenedor, para que los archivos que deben sobrevivir a que el contenedor se borre —código fuente, automatas `.jff`, resultados— sigan existiendo fuera de él. En este proyecto, la línea `- ..:/app` del `compose.yml` es exactamente eso: monta la carpeta del repositorio dentro de `/app` en el contenedor.
- **Puerto publicado.** La conexión entre un puerto de la máquina real y un puerto del contenedor, necesaria para que algo que corre adentro (como la aplicación web de Flet) se pueda abrir desde el navegador de afuera. En este proyecto, `"8550:8550"` en el servicio `py312` publica el puerto 8550 del contenedor hacia el 8550 de la máquina anfitriona.

### ¿Qué es un entorno virtual de Python y por qué un entorno virtual no modifica la versión del intérprete?

Un entorno virtual es una carpeta dentro (o fuera) del proyecto que contiene una copia aislada de las bibliotecas de Python que ese proyecto necesita, independiente de las que estén instaladas para el sistema o para otros proyectos. Se crea con `python -m venv nombre_carpeta` y se activa antes de trabajar; mientras está activo, `pip install` instala paquetes solo ahí dentro.

Un entorno virtual **reutiliza** el intérprete de Python con el que se creó: no instala una copia nueva del lenguaje, solo enlaza al que ya existía en la máquina en ese momento. Por eso un entorno virtual no puede cambiar la versión de Python que usa: si se creó con `py -3.12 -m venv venv`, ese entorno siempre usará Python 3.12, sin importar cuántos paquetes se instalen dentro. Para tener una versión distinta del intérprete (como piden los tres servicios de la Parte C) hace falta, o bien tener esa versión ya instalada en la máquina y crear el entorno virtual con ella, o bien recurrir a un contenedor, que sí puede traer consigo el intérprete completo que se necesite.

### ¿Por qué conviene fijar la versión de la imagen, `python:3.12-slim`, en lugar de emplear `python:latest`?

La etiqueta `latest` no significa "la versión más estable", sino simplemente "la última que se subió al catálogo": hoy puede apuntar a Python 3.12, pero dentro de unos meses el mismo nombre `latest` puede apuntar a una versión distinta (por ejemplo 3.14), y el programa podría dejar de funcionar sin que se haya cambiado una sola línea de código propio. Fijar la versión exacta, como `python:3.12-slim`, hace que la imagen que se descarga hoy sea la misma que se descargará en un año, lo cual es justamente lo que permite que el trabajo siga siendo reproducible después de la fecha de entrega. Es el mismo principio por el que `requirements.txt` fija con `==` las versiones exactas de las bibliotecas de Python, en lugar de dejarlas sin versión.

---

## Parte B. Repositorio

Esta parte se resuelve directamente sobre el repositorio de GitHub (no es un documento): crear la cuenta, el repositorio, el `README.md`, el `.gitignore`, hacer al menos cinco confirmaciones descriptivas y completar el ciclo de rama + Pull Request + fusión. El procedimiento paso a paso, con los comandos exactos, está explicado para que Saúl lo ejecute él mismo en el chat que acompaña este documento (y puede consultarse también resumido más abajo, en la sección "Cómo se hizo" al pie de este archivo). La evidencia que pide el enunciado —dirección del repositorio, captura de `git log --oneline --graph --all` y captura del Pull Request fusionado— se guarda en `evidencias/git/` y se enlaza aquí una vez capturada:

- Dirección del repositorio: `PENDIENTE — pegar aquí la URL una vez creado en GitHub`
- Captura de `git log --oneline --graph --all`: `evidencias/git/log-graph.png` (pendiente)
- Captura del Pull Request fusionado: `evidencias/git/pull-request-fusionado.png` (pendiente)

---

## Parte C. Los tres entornos de Python

### Los tres servicios y por qué esas tres versiones

| Servicio | Imagen base | Motivo de la elección |
|---|---|---|
| `py311` | `python:3.11-slim` | La versión más antigua que sigue recibiendo mantenimiento y que admite la versión de Flet que se instaló en este proyecto (`flet[web]==0.86.5`). |
| `py312` | `python:3.12-slim` | La versión de referencia del curso. Es la que sirve la interfaz gráfica (servicio `py312`, con el puerto publicado). |
| `py313` | `python:3.13-slim` | Una versión reciente, para verificar que el programa no depende de un comportamiento que haya cambiado entre versiones de Python. |

**Justificación con fuentes.** El paquete `flet[web]==0.86.5` que fija `requirements.txt` declara en su metadato `Requires-Python` la condición `>=3.10` (PyPI, [flet 0.86.5](https://pypi.org/project/flet/0.86.5/)), así que en principio Python 3.10 ya cumpliría el requisito. Sin embargo, según el calendario oficial de mantenimiento de CPython, Python 3.10 llega a su fin de vida (*end-of-life*) en octubre de 2026 —es decir, prácticamente al momento de esta entrega—, mientras que Python 3.11 sigue en fase de soporte de seguridad hasta octubre de 2027 (Python Software Foundation, [*Status of Python versions*](https://devguide.python.org/versions/)). Por eso se eligió `python:3.11-slim` como la versión más antigua "viable" para `py311`, en vez de 3.10: es la más vieja que todavía cumple ambas condiciones a la vez (admite Flet **y** sigue recibiendo mantenimiento). `python:3.12-slim` se mantiene porque es la versión que fija el curso, y `python:3.13-slim` se añade como control hacia adelante, para detectar a tiempo si alguna futura versión de Python cambia algo de lo que el programa depende.

### El Dockerfile, línea por línea

```dockerfile
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim
```
`ARG` declara un argumento de construcción con un valor por defecto (3.12); `FROM` parte de la imagen oficial `python` en la variante `slim` (más ligera, sin herramientas de compilación ni documentación) con la versión que llegue como argumento. Es esta línea la que permite que el mismo Dockerfile sirva para las tres versiones: `compose.yml` le pasa un `PYTHON_VERSION` distinto a cada servicio.

```dockerfile
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
```
Crea un entorno virtual dentro de la imagen, en `/opt/venv`, **fuera** de `/app` (donde vive el código). Esto es deliberado: como `compose.yml` monta la carpeta del repositorio completa como volumen en `/app`, cualquier cosa que se hubiera instalado dentro de `/app` quedaría sustituida por el contenido real de la carpeta del proyecto al montar el volumen. Colocar el entorno virtual en `/opt/venv/bin` al principio del `PATH` equivale a tenerlo "activado" permanentemente dentro del contenedor, sin tener que ejecutar `activate` cada vez.

```dockerfile
WORKDIR /app
```
Fija `/app` como la carpeta de trabajo dentro del contenedor: todos los comandos siguientes (y el que se ejecute al arrancar) se ejecutan ahí.

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt
```
Se copia primero **solo** `requirements.txt` y se instalan las dependencias antes de copiar el resto del código. El motivo es el sistema de capas de Docker: si más adelante cambia el código pero no `requirements.txt`, Docker puede reutilizar la capa ya construida con las dependencias instaladas y no repetir esa instalación cada vez que se reconstruye la imagen.

```dockerfile
COPY . .
```
Copia el resto del proyecto a la imagen. (En este proyecto, como además se monta un volumen con la carpeta completa, esta copia queda sustituida en tiempo de ejecución por el volumen; sirve sobre todo para que la imagen sea utilizable también sin volumen, por ejemplo si se publicara sin montar nada.)

```dockerfile
ENV FLET_FORCE_WEB_SERVER=true
ENV FLET_SERVER_PORT=8550
```
Dos variables de entorno que le dicen a Flet cómo comportarse dentro del contenedor: como no hay un escritorio gráfico disponible dentro de un contenedor Linux, `FLET_FORCE_WEB_SERVER=true` obliga a la aplicación a arrancar como servidor web en lugar de intentar abrir una ventana nativa, y `FLET_SERVER_PORT=8550` fija en qué puerto escucha ese servidor.

```dockerfile
CMD ["python", "src/app.py"]
```
El comando que se ejecuta por defecto al arrancar un contenedor de esta imagen. `compose.yml` lo sustituye por `pytest -q` en los servicios `py311` y `py313`, que no necesitan servir la interfaz, solo correr las pruebas.

### El `compose.yml`, clave por clave

- **`build.context`** (`..`, la carpeta que contiene a `entorno/`): desde dónde se construye la imagen, es decir, qué carpeta ve Docker como raíz al copiar archivos con `COPY`.
- **`build.dockerfile`**: qué Dockerfile usar, aquí siempre el mismo (`entorno/Dockerfile`) para los tres servicios.
- **`build.args.PYTHON_VERSION`**: el valor que recibe el `ARG PYTHON_VERSION` del Dockerfile; es lo único que distingue a `py311`, `py312` y `py313` entre sí.
- **`container_name`**: un nombre legible (`tc_p1_py311`, etc.) en lugar del nombre generado automáticamente por Docker.
- **`volumes` (`..:/app`)**: conecta la carpeta del repositorio con `/app` dentro del contenedor, para que el código, los `.jff` y lo que el programa genere sigan siendo archivos reales del repositorio y no se pierdan al borrar el contenedor.
- **`ports` (solo en `py312`, `"8550:8550"`)**: publica el puerto 8550 del contenedor hacia el 8550 de la máquina anfitriona; sin esta línea el contenedor de la interfaz correría, pero el navegador no podría llegar a él. Los otros dos servicios no la necesitan porque solo ejecutan pruebas, no sirven nada por la red.
- **`command`** (en `py311` y `py313`): sustituye al `CMD` del Dockerfile solo para ese servicio; aquí se usa para correr `pytest -q` en vez de levantar la interfaz.

No se incluyó la línea `version: '3.8'` que aparece en tutoriales antiguos: Compose V2 la ignora y advierte que está obsoleta.

### Verificación de que cada contenedor reporta la versión que le corresponde

```bash
cd entorno
docker compose build
docker compose run --rm py311 python --version    # debe imprimir 3.11.x
docker compose run --rm py312 python --version    # debe imprimir 3.12.x
docker compose run --rm py313 python --version    # debe imprimir 3.13.x
```

### Instalación de Docker, paso a paso

1. **Descargar Docker Desktop** desde `docker.com/products/docker-desktop` (Windows, macOS o Linux). En Windows, el instalador activa por debajo WSL 2 (Subsistema de Windows para Linux); si Windows lo pide, hay que reiniciar una vez para terminar de habilitarlo.
2. **Abrir Docker Desktop y esperar el indicador verde** ("Docker is running") antes de usar cualquier comando `docker`. Si un comando responde `Cannot connect to the Docker daemon`, es justamente que Docker Desktop no está abierto o no ha terminado de arrancar todavía.
3. **Comprobar la instalación:**
   ```bash
   docker --version
   docker run --rm hello-world
   ```
   Si el segundo comando descarga la imagen `hello-world` y muestra un mensaje de bienvenida, Docker quedó instalado y funcionando correctamente.
4. **Construir y levantar el entorno de esta práctica** desde la carpeta `entorno/` del repositorio:
   ```bash
   cd entorno
   docker compose build
   docker compose up py312        # levanta la interfaz y abre http://localhost:8550
   docker compose run --rm py311 pytest -q
   docker compose run --rm py313 pytest -q
   docker compose down            # apaga y limpia
   ```
5. **Si se prefiere Podman en lugar de Docker Desktop** (por ejemplo, por no requerir un demonio con privilegios): los mismos comandos funcionan sustituyendo `docker` por `podman` (`podman compose build`, etc.); se indicó así en el `README.md` de este repositorio.

**Diagnóstico rápido de fallas comunes:** primero `docker compose ps` para ver el estado de cada servicio, después `docker compose logs <servicio>` para ver por qué falló. Si `port is already allocated`, algo más en la máquina ya está usando el puerto 8550: cambiar el número de la izquierda en `ports` (por ejemplo `"8551:8550"`).

### Nota sobre el problema del compilador en Visual Studio Code

Python no se compila: es un lenguaje interpretado, así que "el compilador falla" en VS Code casi nunca significa un error de compilación real, sino uno de estos tres problemas, de más a menos frecuente:

1. **El intérprete seleccionado en VS Code no es el correcto.** Con `Ctrl+Shift+P` → `Python: Select Interpreter` se elige explícitamente cuál Python usa el editor; si no se ha creado o seleccionado el entorno virtual del proyecto, VS Code puede estar usando un Python distinto (o ninguno) y todo el resaltado, autocompletado y ejecución fallan como si "no compilara".
2. **Python no quedó en el `PATH` de Windows.** Si `python --version` en una terminal responde "no se reconoce como comando", Python está instalado pero no accesible; se soluciona reinstalando con la casilla "Add python.exe to PATH" marcada, o usando el lanzador `py` en su lugar (`py -0` lista las versiones instaladas, `py -3.12 --version` selecciona una en particular).
3. **La extensión de Python de VS Code no está instalada o quedó desactualizada.** Se instala desde la pestaña de extensiones, buscando "Python" (la oficial, de Microsoft).

La razón por la que este proyecto se apoya en Docker precisamente para el Ejercicio 1 es evitar depender de que el Python y las extensiones de cada máquina estén bien configurados: dentro del contenedor, la versión del intérprete y las dependencias quedan fijadas por el Dockerfile, sin importar qué esté instalado (o mal instalado) en Visual Studio Code en ese momento. Mientras se resuelve el problema local del compilador/intérprete, el programa puede seguir desarrollándose y probándose normalmente dentro de los tres contenedores.
