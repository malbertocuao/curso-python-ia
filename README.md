# Python transversal para soluciones con IA

Repositorio del curso de 40 horas. A lo largo de las sesiones vamos a construir un solo proyecto:
un **asistente documental empresarial** que responde preguntas sobre las políticas y manuales de
una empresa, citando de dónde sacó cada respuesta.

El repositorio crece con el curso: antes de cada sesión se publica su punto de partida.

## Primeros pasos

Requisitos: [uv](https://docs.astral.sh/uv/) y Git. Más adelante: Docker (sesión 7) y
[Ollama](https://ollama.com) (sesión 8).

1. En GitHub, botón **Use this template → Create a new repository**: cada uno trabaja en su propio
   repositorio, y su pareja revisa sus Pull Requests.
2. Clone **su** repositorio y prepare el entorno:

   ```bash
   git clone git@github.com:<su-usuario>/<su-repositorio>.git
   cd <su-repositorio>
   uv sync
   uv run pre-commit install
   uv run pytest            # debe quedar en verde
   ```

3. Conecte este repositorio como `upstream`, para recibir cada sesión:

   ```bash
   git remote add upstream https://github.com/malbertocuao/curso-python-ia.git
   ```

## Al comenzar cada sesión

```bash
git fetch upstream --tags
git switch main
git merge s02-inicio          # el número de la sesión que empieza
uv sync
uv run pytest                 # las pruebas del taller nuevo aparecen en rojo
```

El taller consiste en ponerlas en verde, en una rama y con Pull Request:

```bash
git switch -c taller-s02
# ... implementar ...
git push -u origin taller-s02  # y abrir el Pull Request para que lo revise su pareja
```

Las funciones del taller traen su documentación y el cuerpo `raise NotImplementedError`. Las pruebas
son la especificación: léalas antes de escribir código.

### Si se atrasó o algo no le funciona

Al comienzo de la sesión siguiente se publica la solución de referencia, `sNN-fin`. Para seguir con
el grupo, tome la versión de referencia de los archivos que necesite:

```bash
git fetch upstream --tags
git checkout s02-fin -- src/asistente/domain/models.py
```

Lo propio de su proyecto (su tarea, sus documentos, sus casos de evaluación) póngalo en archivos
aparte, por ejemplo `src/asistente/services/su_tarea.py` y `data/`, para que no choque con lo que
se publica en cada sesión.

## Ejercicios

| Carpeta | Para qué |
|---|---|
| `diagnostico/` | Prueba diagnóstica de la sesión 1: `uv run pytest diagnostico` |
| `fundamentos/` | Ejercicios de "Python a fondo", sesiones 1 a 6 (ver `fundamentos/README.md`) |

## Reglas del repositorio

- El archivo `.env` (llaves de API) **nunca** se sube: copie `.env.example` a `.env` y complételo.
- `pre-commit` revisa estilo y busca llaves antes de cada commit; la integración continua repite
  esas revisiones, más `mypy` y las pruebas, en cada Pull Request.
- Use datos anonimizados: nada de nombres, cédulas ni documentos confidenciales reales.
