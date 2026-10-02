# Fundamentos: Python a fondo

Ejercicios de los bloques "Python a fondo" de las sesiones 1 a 6. Se resuelven fuera de clase
(unos 30 a 40 minutos cada paquete) y las pruebas dicen cuándo están terminados.

| Sesión | Tema | Archivo | Prueba |
|---|---|---|---|
| 1 | Tipos y contenedores | `s01_tipos.py` | `uv run pytest fundamentos/test_s01_tipos.py` |
| 2 | Funciones | `s02_funciones.py` | `uv run pytest fundamentos/test_s02_funciones.py` |
| 3 | Biblioteca estándar | `s03_biblioteca.py` | `uv run pytest fundamentos/test_s03_biblioteca.py` |
| 4 | Decoradores | `s04_decoradores.py` | `uv run pytest fundamentos/test_s04_decoradores.py` |
| 5 | Iteradores y generadores | `s05_generadores.py` | `uv run pytest fundamentos/test_s05_generadores.py` |
| 6 | Excepciones y gestores de contexto | `s06_excepciones.py` | `uv run pytest fundamentos/test_s06_excepciones.py` |

Cada paquete incluye al menos un ejercicio de código seguro: validar entradas, leer datos sin
`eval`, rutas que no salen de su carpeta, registros sin secretos, listas de permitidos, permisos
antes de ejecutar, topes de recursos y archivos temporales que no dejan rastro.

Las soluciones del facilitador (`solucion_s0N_*.py`) están en `.gitignore`: no se publican.
Para verificarlas: `FUNDAMENTOS=solucion_ uv run pytest fundamentos`.
