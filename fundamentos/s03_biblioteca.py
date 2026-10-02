"""Fundamentos 3: biblioteca estándar (sesión 3, unos 30 min). Implemente y ejecute:

uv run pytest fundamentos/test_s03_biblioteca.py -q
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


# 1. pathlib -----------------------------------------------------------------
def listar_documentos(base: Path, extensiones: tuple[str, ...] = (".md", ".txt")) -> list[str]:
    """Rutas relativas a `base`, con '/', de los archivos con esas extensiones.

    Busca también en subcarpetas; la extensión no distingue mayúsculas. Orden alfabético.
    """
    raise NotImplementedError


# 2. Rutas seguras (código seguro) -------------------------------------------
def leer_documento(base: Path, nombre: str) -> str:
    """Lee base/nombre en UTF-8.

    Si la ruta resuelta queda fuera de `base` ('../.env', '/etc/passwd', enlaces simbólicos
    que salen), lanza PermissionError. Si no existe, FileNotFoundError.
    """
    raise NotImplementedError


# 3. json --------------------------------------------------------------------
def cargar_config(texto: str) -> dict[str, Any]:
    """Lee una configuración JSON y la valida.

    Debe ser un objeto con 'modelo' (texto no vacío) y 'temperatura' (número entre 0 y 2;
    un booleano no cuenta). 'max_tokens' es opcional (entero > 0, por defecto 512).
    Cualquier problema, incluido JSON mal formado → ValueError. Devuelve solo esas tres claves.
    """
    raise NotImplementedError


# 4. datetime y zonas horarias -----------------------------------------------
def a_hora_local(iso: str, zona: str = "America/Bogota") -> str:
    """'2026-10-05T12:00:00+00:00' → '2026-10-05 07:00'.

    Una fecha sin zona horaria es ambigua → ValueError.
    """
    raise NotImplementedError


# 5. Registros sin secretos (código seguro) ----------------------------------
def enmascarar_secretos(mensaje: str) -> str:
    """Reemplaza el valor de api_key, token, password y clave por '***'.

    'conectando api_key=sk-123 usuario=ana' → 'conectando api_key=*** usuario=ana'
    Acepta '=' o ':' (con espacios opcionales) y no distingue mayúsculas en el nombre.
    """
    raise NotImplementedError
