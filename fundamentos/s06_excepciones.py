"""Fundamentos 6: excepciones y gestores de contexto (sesión 6, unos 30 min). Ejecute:

uv run pytest fundamentos/test_s06_excepciones.py -q
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any


class ErrorAsistente(Exception):
    """Raíz de los errores del dominio."""


class EntradaInvalida(ErrorAsistente):
    pass


class ProveedorNoDisponible(ErrorAsistente):
    pass


# 1. Traducir y encadenar ----------------------------------------------------
def leer_temperatura(texto: str) -> float:
    """'0.7' → 0.7. Debe estar entre 0 y 2.

    Texto que no es número → EntradaInvalida encadenada al ValueError original
    (raise ... from ...). Fuera de rango → EntradaInvalida sin causa.
    """
    raise NotImplementedError


# 2. Unidad de trabajo en pequeño --------------------------------------------
@contextmanager
def transaccion(destino: dict[str, Any]) -> Iterator[dict[str, Any]]:
    """with transaccion(datos) as borrador: ...

    Entrega una copia de `destino`. Si el bloque termina bien, `destino` queda igual
    al borrador (incluidas claves borradas). Si hay excepción, `destino` no cambia y
    la excepción se propaga.
    """
    raise NotImplementedError
    yield {}  # para que sea un generador; bórrelo al implementar


# 3. Archivo temporal sin rastro (código seguro) -----------------------------
@contextmanager
def archivo_temporal(contenido: bytes, sufijo: str = ".pdf") -> Iterator[Path]:
    """Escribe `contenido` en un archivo temporal y entrega su ruta.

    Solo el dueño puede leerlo (permisos 0o600) y se borra al salir, aunque el bloque
    falle. Pista: tempfile.mkstemp.
    """
    raise NotImplementedError
    yield Path()  # para que sea un generador; bórrelo al implementar


# 4. Tiempo límite asíncrono -------------------------------------------------
async def con_limite[T](operacion: Callable[[], Awaitable[T]], segundos: float) -> T:
    """Ejecuta operacion() con tiempo máximo.

    Si se agota → ProveedorNoDisponible encadenada al TimeoutError.
    Cualquier otra excepción se propaga sin cambios.
    """
    raise NotImplementedError
