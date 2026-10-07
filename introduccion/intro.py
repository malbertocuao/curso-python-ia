"""Práctica de la introducción a Python.

Cada función tiene su firma, una docstring con lo que debe hacer y `raise NotImplementedError`.
Reemplace esa línea por la implementación y ejecute, desde la raíz del proyecto:

    uv run pytest introduccion -v          # todas
    uv run pytest introduccion -k saludo   # solo las de un ejercicio

Los ejercicios siguen el orden de la presentación "Python para quien ya programa".
"""

from __future__ import annotations

import functools  # noqa: F401  (lo necesita el ejercicio 12)
import math  # noqa: F401  (lo necesita el ejercicio 8)
from collections.abc import Callable, Iterator
from dataclasses import dataclass


# 1. Un programa es un archivo ----------------------------------------------------------
def saludo(nombre: str, formal: bool = False) -> str:
    """Saludo para `nombre`, sin los espacios que traiga a los lados.

    saludo("Ana") → "Hola, Ana"        saludo("Ana", formal=True) → "Buenos días, Ana."
    Pista: f-strings y el método strip.
    """
    raise NotImplementedError


def main() -> None:
    """Imprime saludo("mundo"). Al final del archivo ya está el bloque
    `if __name__ == "__main__":` que la llama: pruebe `uv run python introduccion/intro.py`.
    """
    raise NotImplementedError


# 2. Bloques y condiciones --------------------------------------------------------------
def clasificar_temperatura(t: float) -> str:
    """Clasifica la temperatura de un modelo de IA.

    Menor que 0.3 → "precisa"; de 0.3 a 1 (incluido) → "equilibrada"; mayor que 1 → "creativa".
    Si es negativa o mayor que 2: ValueError.
    """
    raise NotImplementedError


# 3. Recorrer y contar ------------------------------------------------------------------
def contar_vocales(texto: str) -> dict[str, int]:
    """Cuántas veces aparece cada vocal (a, e, i, o, u), sin importar mayúsculas.

    Siempre devuelve las cinco claves, aunque alguna valga 0. El texto viene sin tildes.
    contar_vocales("Hola Mundo") → {"a": 1, "e": 0, "i": 0, "o": 2, "u": 1}
    """
    raise NotImplementedError


# 4. Funciones que devuelven varios valores ---------------------------------------------
def resumen(numeros: list[float]) -> tuple[float, float, float]:
    """(mínimo, máximo, promedio) de la lista. Lista vacía: ValueError.

    resumen([4, 1, 7]) → (1, 7, 4.0)
    """
    raise NotImplementedError


# 5. Al llamar, se pasa el objeto -------------------------------------------------------
def agregar_etiqueta(etiquetas: list[str] | None, nueva: str) -> list[str]:
    """Una lista con las etiquetas y `nueva` al final, si no estaba ya.

    No modifica la lista que recibe: devuelve otra. Con None, empieza de una lista vacía.
    agregar_etiqueta(["rrhh"], "legal") → ["rrhh", "legal"]
    """
    raise NotImplementedError


# 6. Comprensiones ----------------------------------------------------------------------
def largos(palabras: list[str]) -> dict[str, int]:
    """Diccionario palabra → largo, sin las palabras vacías o de solo espacios.

    Con una comprensión de diccionario. largos(["sol", "", "luna"]) → {"sol": 3, "luna": 4}
    """
    raise NotImplementedError


# 7. Errores ----------------------------------------------------------------------------
def a_entero(texto: str, defecto: int = 0) -> int:
    """El entero que representa el texto, o `defecto` si no es un entero válido.

    a_entero(" 7 ") → 7     a_entero("4.2") → 0     a_entero("x", defecto=-1) → -1
    Pista: try / except ValueError.
    """
    raise NotImplementedError


# 8. Módulos de la biblioteca estándar --------------------------------------------------
def hipotenusa(a: float, b: float) -> float:
    """La hipotenusa de un triángulo rectángulo, redondeada a 2 decimales.

    Use math.sqrt (el import ya está arriba). hipotenusa(1, 1) → 1.41
    """
    raise NotImplementedError


# 9. Clases -----------------------------------------------------------------------------
class Contador:
    """Contador que solo sube.

    Contador() empieza en 0; Contador(10), en 10. `valor` se lee como atributo (una property)
    y no se puede asignar. incrementar(paso=1) suma; con paso <= 0, ValueError. reiniciar()
    vuelve a 0. repr(c) → "Contador(6)".
    """

    def __init__(self, inicio: int = 0) -> None:
        raise NotImplementedError

    @property
    def valor(self) -> int:
        raise NotImplementedError

    def incrementar(self, paso: int = 1) -> None:
        raise NotImplementedError

    def reiniciar(self) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


# 10. dataclass -------------------------------------------------------------------------
@dataclass(frozen=True)
class Producto:
    """Producto inmutable. Precio negativo: ValueError al crearlo.

    `precio_con_iva` es una property: el precio por 1.19, redondeado a 2 decimales.
    """

    nombre: str
    precio: float
    etiquetas: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        raise NotImplementedError

    @property
    def precio_con_iva(self) -> float:
        raise NotImplementedError


# 11. Generadores -----------------------------------------------------------------------
def lineas_numeradas(texto: str) -> Iterator[str]:
    """Genera "1: texto", "2: texto"… por cada línea no vacía, sin espacios a los lados.

    Las líneas vacías no se cuentan. Debe ser un generador (yield), no devolver una lista.
    list(lineas_numeradas("a\\n\\n b ")) → ["1: a", "2: b"]
    """
    raise NotImplementedError


# 12. Decoradores -----------------------------------------------------------------------
def en_mayusculas(funcion: Callable[..., str]) -> Callable[..., str]:
    """Decorador: la función decorada devuelve su resultado en mayúsculas.

    Debe aceptar cualquier argumento (*args, **kwargs) y conservar el nombre y la docstring
    de la original con functools.wraps (el import ya está arriba).
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
