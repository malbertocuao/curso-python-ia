"""Fundamentos 4: decoradores (sesión 4, unos 35 min). Implemente y ejecute:

uv run pytest fundamentos/test_s04_decoradores.py -q
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


# 1. Envolver conservando la identidad ---------------------------------------
def contar_llamadas[F: Callable[..., Any]](fn: F) -> F:
    """Decorador: la función decorada tiene un atributo `llamadas` (int) que cuenta
    cuántas veces se llamó, aunque haya lanzado excepción.

    Debe conservar __name__ y __doc__ de la original (functools.wraps).
    """
    raise NotImplementedError


# 2. Decorador con parámetros ------------------------------------------------
def reintentar(
    veces: int = 3,
    *,
    ante: tuple[type[Exception], ...] = (ConnectionError, TimeoutError),
    espera: float = 0.5,
    dormir: Callable[[float], None] = time.sleep,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Reintenta solo ante las excepciones de `ante`, hasta `veces` intentos en total.

    Entre intentos espera espera, 2*espera, 4*espera... usando `dormir` (las pruebas
    lo reemplazan para no esperar de verdad). Otras excepciones se propagan de inmediato.
    `veces` menor que 1 → ValueError al crear el decorador.
    """
    raise NotImplementedError


# 3. Registro con lista de permitidos (código seguro) ------------------------
class Registro:
    """r = Registro();  @r.registrar("eco") class Eco: ...;  r.crear("eco") → Eco()."""

    def __init__(self) -> None:
        self._fabricas: dict[str, Callable[[], Any]] = {}

    def registrar(self, nombre: str) -> Callable[[Callable[[], Any]], Callable[[], Any]]:
        """Decorador que anota la fábrica con el nombre (en minúsculas) y la devuelve intacta.

        Registrar dos veces el mismo nombre → ValueError (nadie suplanta un proveedor).
        """
        raise NotImplementedError

    def crear(self, nombre: str) -> Any:
        """Llama a la fábrica registrada (sin distinguir mayúsculas).

        Nombre desconocido → LookupError con la lista de opciones válidas.
        """
        raise NotImplementedError


# 4. Permisos antes de ejecutar (código seguro) ------------------------------
@dataclass(frozen=True)
class Usuario:
    nombre: str
    permisos: frozenset[str]


def requiere_permiso(permiso: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """La función decorada recibe un Usuario como primer argumento.

    Si no tiene `permiso`, lanza PermissionError SIN ejecutar la función.
    """
    raise NotImplementedError
