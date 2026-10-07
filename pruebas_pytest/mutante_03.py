"""Copia de calculos.py con UN error sembrado, para verificar.py. No la use para resolver."""

from __future__ import annotations

import json
import os
from pathlib import Path

PROVEEDORES = {"fake", "ollama", "openai", "anthropic"}


def en_lotes(items: list[str], tamano: int) -> list[list[str]]:
    """Parte la lista en lotes de `tamano`; el último puede ser más corto.

    en_lotes(["a", "b", "c"], 2) → [["a", "b"], ["c"]]. tamano < 1: ValueError("tamano ...").
    """
    if tamano < 1:
        raise ValueError(f"tamano debe ser al menos 1, no {tamano}")
    return [items[i : i + tamano] for i in range(0, len(items), tamano)]


def con_descuento(precio: float, porcentaje: float) -> float:
    """Precio con el descuento aplicado, redondeado a 2 decimales.

    porcentaje fuera de 0..100: ValueError("porcentaje ..."). con_descuento(100, 15) → 85.0
    """
    if not 0 <= porcentaje < 100:
        raise ValueError(f"porcentaje fuera de rango: {porcentaje}")
    return round(precio * (1 - porcentaje / 100), 2)


def normalizar_correo(correo: str) -> str:
    """Correo sin espacios a los lados y en minúsculas. Sin "@": ValueError("correo ...")."""
    limpio = correo.strip().lower()
    if "@" not in limpio:
        raise ValueError(f"correo inválido: {correo!r}")
    return limpio


def leer_config(ruta: Path) -> dict[str, object]:
    """Lee un JSON de configuración. Debe tener "modelo"; si no: ValueError("modelo ...").

    "temperatura" es opcional y vale 0.2 si no viene.
    """
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    if "modelo" not in datos:
        raise ValueError("modelo es obligatorio")
    return {"modelo": datos["modelo"], "temperatura": datos.get("temperatura", 0.2)}


def proveedor_activo() -> str:
    """El proveedor de la variable de entorno LLM_PROVIDER, en minúsculas; "fake" si no está.

    Si no es uno de PROVEEDORES: ValueError("proveedor ...").
    """
    nombre = os.getenv("LLM_PROVIDER", "fake").lower()
    if nombre not in PROVEEDORES:
        raise ValueError(f"proveedor no soportado: {nombre}")
    return nombre
