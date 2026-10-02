"""Fundamentos 5: iteradores y generadores (sesión 5, unos 30 min). Implemente y ejecute:

uv run pytest fundamentos/test_s05_generadores.py -q

Todas deben ser perezosas: las pruebas les pasan iterables infinitos o que fallan si se
consumen de más.
"""

from __future__ import annotations

from collections.abc import Callable, Hashable, Iterable, Iterator


# 1. Leer registros ----------------------------------------------------------
def leer_registros(lineas: Iterable[str]) -> Iterator[dict[str, str]]:
    """'area=rrhh; anio=2026' → {'area': 'rrhh', 'anio': '2026'}.

    Ignora líneas vacías y las que empiezan por '#'. Quita espacios alrededor de
    claves y valores. Una línea con un par sin '=' → ValueError con el número de línea.
    """
    raise NotImplementedError


# 2. Ventanas con solapamiento -----------------------------------------------
def ventanas(texto: str, tamano: int, paso: int) -> Iterator[str]:
    """ventanas('abcdefg', 3, 2) → 'abc', 'cde', 'efg'.

    La última ventana puede ser más corta, pero nunca queda una ventana que esté
    contenida completa en la anterior. Texto vacío → nada. tamano o paso < 1, o
    paso > tamano (se perdería texto) → ValueError al llamar la función, no al primer next().
    Pista: una función con yield no ejecuta nada hasta el primer next().
    """
    raise NotImplementedError


# 3. Sin repetidos -----------------------------------------------------------
def sin_repetidos[T](
    items: Iterable[T], clave: Callable[[T], Hashable] | None = None
) -> Iterator[T]:
    """Entrega cada elemento la primera vez que aparece su clave (o el elemento mismo)."""
    raise NotImplementedError


# 4. Tope de recursos (código seguro) ----------------------------------------
def hasta_presupuesto(textos: Iterable[str], max_caracteres: int) -> Iterator[str]:
    """Entrega textos mientras la suma de sus longitudes no supere max_caracteres.

    El primer texto que no cabe detiene todo (no se salta para buscar otros más cortos).
    No debe consumir del iterable más de lo necesario.
    """
    raise NotImplementedError
