"""Práctica del anexo A: los métodos de los tipos de datos, con el argumento correcto.

Cada ejercicio se resuelve en una o dos líneas si se elige bien el método y sus argumentos;
la docstring dice en qué diapositiva del anexo A está. Reemplace `raise NotImplementedError`
y ejecute, desde la raíz del proyecto:

    uv run pytest tipos_de_datos -v
"""

from __future__ import annotations

import json  # noqa: F401  (ejercicio 19)
from collections import Counter  # noqa: F401  (ejercicio 15)
from datetime import date  # noqa: F401  (ejercicio 17)
from typing import Any


# Texto ---------------------------------------------------------------------------------
def extension(nombre: str) -> str:
    """1. La extensión en minúsculas, sin el punto; "" si no tiene.

    "Informe.Final.PDF" → "pdf"   "Makefile" → ""   ".env" → ""   "archivo." → ""
    Diapositiva: split, rsplit, partition (mire rpartition).
    """
    raise NotImplementedError


def sin_version(nombre: str) -> str:
    """2. Quita el prefijo "v2-" una sola vez. "v2-v2-manual" → "v2-manual".

    Diapositiva: strip, lstrip, rstrip, removeprefix, removesuffix.
    """
    raise NotImplementedError


def sin_pdf(nombre: str) -> str:
    """3. Quita el sufijo ".pdf" exacto. "spdf.pdf" → "spdf" (con rstrip(".pdf") daría "s")."""
    raise NotImplementedError


def palabras(texto: str) -> list[str]:
    """4. Las palabras, sin vacíos aunque haya varios espacios seguidos.

    "  hola   mundo " → ["hola", "mundo"]. Diapositiva: split, rsplit, partition.
    """
    raise NotImplementedError


def campos(linea: str) -> list[str]:
    """5. Los campos separados por coma, sin espacios a los lados, CONSERVANDO los vacíos.

    "a, b,,c " → ["a", "b", "", "c"]
    """
    raise NotImplementedError


def clave_valor(linea: str) -> tuple[str, str]:
    """6. Separa en el primer "=" y quita espacios. Sin "=": ValueError con la palabra "falta".

    "url=http://x?a=1" → ("url", "http://x?a=1")
    """
    raise NotImplementedError


def carpeta_y_archivo(ruta: str) -> tuple[str, str]:
    """7. Separa la carpeta del archivo en la última "/". Sin "/", la carpeta es "".

    "rrhh/politicas/vacaciones.pdf" → ("rrhh/politicas", "vacaciones.pdf")
    """
    raise NotImplementedError


def unir(numeros: list[int], separador: str = ", ") -> str:
    """8. Une los números como texto. unir([1, 2, 3]) → "1, 2, 3".

    Diapositiva: join, el inverso de split.
    """
    raise NotImplementedError


# Ordenar, máximos y recorridos ---------------------------------------------------------
def mejores(puntajes: dict[str, float], k: int) -> list[str]:
    """9. Los k nombres de mayor puntaje; si empatan, en orden alfabético.

    Diapositiva: ordenar con sort, sorted y reversed (clave de tupla).
    """
    raise NotImplementedError


def mas_largo(textos: list[str]) -> str | None:
    """10. El texto más largo (si empatan, el primero); None si la lista está vacía.

    Diapositiva: sum, min, max.
    """
    raise NotImplementedError


def emparejar(preguntas: list[str], respuestas: list[str]) -> list[tuple[str, str]]:
    """11. Pares (pregunta, respuesta). Si los largos no coinciden: ValueError.

    Diapositiva: zip y map.
    """
    raise NotImplementedError


def primero_mayor(numeros: list[int], limite: int) -> int | None:
    """12. El primer número mayor que `limite`, o None si no hay.

    Diapositiva: iter y next.
    """
    raise NotImplementedError


# Diccionarios y conjuntos --------------------------------------------------------------
def sin_repetidos(etiquetas: list[str]) -> list[str]:
    """13. Quita repetidos sin importar mayúsculas; conserva la primera forma y el orden.

    ["RRHH", "legal", "rrhh", "Legal", "nomina"] → ["RRHH", "legal", "nomina"]
    Diapositiva: diccionarios, leer y quitar sin fallar (setdefault) y casefold.
    """
    raise NotImplementedError


def por_inicial(palabras: list[str]) -> dict[str, list[str]]:
    """14. Agrupa por la primera letra en minúscula, en el orden en que aparecen.

    ["Sol", "mar", "sal"] → {"s": ["Sol", "sal"], "m": ["mar"]}
    """
    raise NotImplementedError


def mas_frecuentes(items: list[str], n: int) -> list[tuple[str, int]]:
    """15. Los n más frecuentes con su cuenta, de mayor a menor.

    Diapositiva: Counter, defaultdict, deque.
    """
    raise NotImplementedError


# Números, fechas, bytes y JSON ---------------------------------------------------------
def a_centenas(valor: float) -> int:
    """16. Redondea a la centena más cercana y devuelve un int. a_centenas(1351) → 1400.

    Ojo: con la mitad exacta, Python redondea al par (1250 → 1200). Diapositiva: int, float, round.
    """
    raise NotImplementedError


def dias_entre(desde: str, hasta: str) -> int:
    """17. Días entre dos fechas AAAA-MM-DD. ("2026-12-14", "2027-01-05") → 22.

    Diapositiva: fechas.
    """
    raise NotImplementedError


def bytes_utf8(texto: str) -> int:
    """18. Cuántos bytes ocupa el texto en UTF-8. "año" → 4.

    Diapositiva: encode, decode y bytes.
    """
    raise NotImplementedError


def a_json(datos: dict[str, Any]) -> str:
    """19. JSON legible: tildes sin escapar y sangría de 2 espacios.

    Diapositiva: JSON, de texto a datos y de vuelta.
    """
    raise NotImplementedError
