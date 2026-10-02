"""Fundamentos 2: funciones (sesión 2, unos 35 min). Implemente cada función y ejecute:

uv run pytest fundamentos/test_s02_funciones.py -q
"""

from __future__ import annotations

from collections.abc import Callable, Hashable, Iterable
from typing import Any

FILTROS_PERMITIDOS = frozenset({"area", "anio", "idioma"})


# 1. key= y varias claves ----------------------------------------------------
def ordenar_resultados(resultados: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Ordena por 'puntaje' de mayor a menor; en empate, por 'titulo' alfabético.

    Devuelve una lista nueva: no modifica la recibida.
    """
    raise NotImplementedError


# 2. Funciones como argumentos -----------------------------------------------
def aplicar_pasos(texto: str, *pasos: Callable[[str], str]) -> str:
    """Aplica cada paso al resultado del anterior, en orden. Sin pasos, devuelve el texto."""
    raise NotImplementedError


# 3. Funciones que devuelven funciones ---------------------------------------
def agrupar_por[T, K: Hashable](items: Iterable[T], clave: Callable[[T], K]) -> dict[K, list[T]]:
    """Agrupa los items según clave(item), conservando el orden de llegada en cada grupo."""
    raise NotImplementedError


# 4. Closures ----------------------------------------------------------------
def limitador(maximo: int) -> Callable[[int], bool]:
    """Devuelve consumir(tokens) -> bool.

    True y descuenta si caben en el presupuesto restante; False y no descuenta si no caben.
    Lanza ValueError si tokens es negativo. Cada limitador es independiente.
    """
    raise NotImplementedError


# 5. Firma explícita y lista de permitidos (código seguro) -------------------
def construir_consulta(texto: str, /, *, limite: int = 5, **filtros: str) -> dict[str, Any]:
    """{'texto': ..., 'limite': ..., 'filtros': {...}}.

    `texto` sin espacios a los lados y no vacío; `limite` entre 1 y 50.
    Solo se aceptan filtros de FILTROS_PERMITIDOS; cualquier otro → ValueError
    (nunca se pasan claves desconocidas a la capa de datos).
    """
    raise NotImplementedError
