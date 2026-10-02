"""Fundamentos 1: tipos y contenedores (sesión 1, unos 40 min). Implemente cada función y ejecute:

    uv run pytest fundamentos/test_s01_tipos.py -q

Las pruebas son la especificación: léalas antes de empezar. Solo biblioteca estándar.
"""

from __future__ import annotations

from decimal import Decimal


# 1. Texto -------------------------------------------------------------------
def limpiar_etiquetas(texto: str) -> list[str]:
    """'Legal, RRHH ,, legal' → ['legal', 'rrhh'].

    Separa por comas, quita espacios, pasa a minúsculas (casefold), descarta vacías
    y elimina repetidas conservando el orden de la primera aparición.
    """
    raise NotImplementedError


# 2. Números y dinero --------------------------------------------------------
def total_con_iva(precios: list[str], iva: str = "0.19") -> Decimal:
    """Suma precios escritos como texto y aplica el IVA.

    Redondea a 2 decimales, con la mitad hacia arriba.

    Lanza ValueError si algún precio no es un número válido o es negativo.
    """
    raise NotImplementedError


# 3. Validar entradas (código seguro) ----------------------------------------
def parsear_limite(valor: str | None, *, defecto: int = 5, maximo: int = 50) -> int:
    """Convierte el parámetro 'limite' que llega de una petición.

    None o texto vacío → defecto. Texto que no es entero → ValueError.
    Fuera de 1..maximo → ValueError. Ojo: "0" es un valor explícito, no vacío.
    """
    raise NotImplementedError


# 4. Datos, no código (código seguro) ----------------------------------------
def leer_lista_enteros(texto: str) -> list[int]:
    """'[1, 2, 3]' → [1, 2, 3], sin usar eval.

    Lanza ValueError si el texto no es una lista o si algún elemento no es entero
    (los booleanos tampoco cuentan como enteros).
    """
    raise NotImplementedError


# 5. Diccionarios y conjuntos ------------------------------------------------
def indice_invertido(docs: dict[str, str]) -> dict[str, set[str]]:
    """Cada palabra (en minúsculas, separada por espacios) apunta a los ids que la contienen.

    {'d1': 'Vacaciones anuales', 'd2': 'vacaciones'}
    → {'vacaciones': {'d1', 'd2'}, 'anuales': {'d1'}}
    """
    raise NotImplementedError


# 6. Copias y mutabilidad ----------------------------------------------------
def fusionar_config(base: dict[str, object], *capas: dict[str, object]) -> dict[str, object]:
    """Une configuraciones anidadas: cada capa sobrescribe a la anterior, clave por clave.

    Si en ambas un valor es dict, se fusionan recursivamente. No debe modificar
    `base` ni las capas, ni compartir con ellas diccionarios anidados.
    """
    raise NotImplementedError
