"""Práctica de la sesión 2: clases y objetos, un ejercicio por tema.

Cada ejercicio dice qué hacer y en qué diapositiva se vio. Las pruebas están en
`poo/test_poo.py` y son la especificación. Ejecute, desde la raíz del proyecto:

    uv run pytest poo -v           # todas
    uv run pytest poo -k cita      # solo las de un ejercicio

Los ejercicios siguen el orden de la clase: no se adelante, cada uno usa lo que se explicó
justo antes.
"""

from __future__ import annotations

from collections.abc import Iterator  # noqa: F401  (lo necesita el ejercicio 4)
from dataclasses import dataclass, field  # noqa: F401
from datetime import UTC, datetime
from pathlib import Path  # noqa: F401  (lo necesita el ejercicio 5)
from typing import Protocol, Self, runtime_checkable  # noqa: F401
from uuid import UUID, uuid4  # noqa: F401


def ahora() -> datetime:
    """Fecha y hora actual en UTC. Úsela como `default_factory` (ejercicio 2)."""
    return datetime.now(UTC)


# 1. Una dataclass inmutable -------------------------------------------------------------
# Diapositiva "La misma clase, dos veces".
class Cita:
    """Referencia a un fragmento usado en una respuesta: `[1]` en "15 días hábiles [1]".

    Conviértala en una dataclass inmutable (frozen) con dos campos, en este orden:
        fuente: int        número de la fuente, el 1 de "[1]"
        extracto: str      el texto citado

    Cita(1, "15 días") == Cita(1, "15 días")   → True
    repr(Cita(1, "x"))                          → "Cita(fuente=1, extracto='x')"
    cita.fuente = 2                             → dataclasses.FrozenInstanceError
    """


# 2. Objeto de valor y entidad -----------------------------------------------------------
# Diapositivas "Dos tipos de objetos en el dominio" y "En código, la diferencia es una línea".
class Mensaje:
    """Objeto de valor: dataclass inmutable con tres campos, en este orden:
    rol: str
    contenido: str
    creado: datetime   por defecto `ahora()` (con default_factory) y que NO cuente al
                       comparar: dos mensajes iguales creados en momentos distintos
                       son iguales.
    """


class Documento:
    """Entidad: dataclass (no inmutable) con cuatro campos, en este orden:
        titulo: str
        contenido: str
        fuente: str = "manual"
        id: UUID           por defecto uuid4() (con default_factory)

    Dos documentos son iguales solo si tienen el mismo `id`, aunque el texto sea idéntico.
    Escriba `__eq__` (compara solo el id) y `__hash__` (devuelve hash(self.id)), para que
    un documento se pueda usar en un set.
    """


# 3. Validar al nacer, calcular al pedir --------------------------------------------------
# Diapositiva "Validar al nacer, calcular al pedir".
@dataclass
class Fragmento:
    texto: str
    posicion: int
    embedding: list[float] | None = None

    # Agregue __post_init__: ValueError si posicion < 0 o si el texto está vacío o es solo
    # espacios.

    # Agregue dos propiedades (@property), que se leen sin paréntesis:
    #   vectorizado → True si embedding no es None
    #   palabras    → cuántas palabras tiene el texto (separadas por espacios)


# 4. Que el objeto se comporte como lo que es -----------------------------------------------
# Diapositiva "Que el objeto se comporte como lo que es".
@dataclass
class Conversacion:
    _mensajes: list[Mensaje] = field(default_factory=list)

    def agregar(self, rol: str, contenido: str) -> Mensaje:
        """Crea un Mensaje, lo agrega al final y lo devuelve."""
        raise NotImplementedError

    # Agregue:
    #   __len__   → cuántos mensajes hay:          len(conv)
    #   __iter__  → recorre los mensajes en orden: for m in conv
    #   __bool__  → False si no hay mensajes:      if not conv
    #   mensajes  → propiedad que devuelve una TUPLA con los mensajes, para que desde
    #               afuera nadie pueda agregar ni quitar (ejercicio de código seguro)


# 5. Constructores con nombre --------------------------------------------------------------
# Diapositiva "Constructores con nombre". No hay función nueva: vaya a la clase Documento
# del ejercicio 2 y agréguele el método de clase
#
#     @classmethod
#     def desde_archivo(cls, ruta: Path) -> Self:
#
# titulo = el nombre del archivo sin extensión (ruta.stem), contenido = el texto del archivo
# leído en utf-8, fuente = la ruta como texto (str(ruta)).


# 6. Herencia: una familia de errores --------------------------------------------------------
# Diapositiva "Herencia: cuando de verdad «es un»".
class ErrorAsistente(Exception):
    """Raíz de los errores del asistente."""


# Defina aquí DocumentoNoEncontrado y ProveedorNoDisponible, los dos hijos de ErrorAsistente.


def buscar(documentos: dict[UUID, Documento], id_doc: UUID) -> Documento:
    """El documento con ese id. Si no está: DocumentoNoEncontrado, con el id en el mensaje."""
    raise NotImplementedError


# 7. Composición: armar con piezas ------------------------------------------------------------
# Diapositiva "Composición: armar con piezas".
class ConReintentos:
    """Envuelve a otro proveedor y reintenta cuando falla con ProveedorNoDisponible.

    ConReintentos(interno, intentos=3):
        - ValueError si intentos < 1
        - guarda `interno` e `intentos`
        - nombre = f"{interno.nombre}+reintentos"
    completar(pregunta) llama a interno.completar(pregunta) hasta `intentos` veces.
    Si un intento funciona, devuelve su respuesta. Si el último también falla, deja salir
    el error (`raise` sin nada más). Otros errores no se reintentan: salen de una vez.
    """

    def __init__(self, interno: ProveedorLLM, intentos: int = 3) -> None:
        raise NotImplementedError

    def completar(self, pregunta: str) -> str:
        raise NotImplementedError


# 8. Interfaces con Protocol --------------------------------------------------------------------
# Diapositiva "Interfaces: Protocol en lugar de herencia".
@runtime_checkable
class ProveedorLLM(Protocol):
    """Cualquier cosa que tenga un atributo `nombre: str` y un método
    `completar(self, pregunta: str) -> str`. Escriba esas dos líneas aquí (el método termina
    en `: ...`, sin cuerpo) y borre esta docstring si quiere.
    """


class Eco:
    """Proveedor de prueba: NO hereda de nada. nombre = "eco";
    completar(pregunta) devuelve f"eco: {pregunta}".
    """


def con_respaldo(principal: ProveedorLLM, respaldo: ProveedorLLM, pregunta: str) -> str:
    """Pregunta al principal; si falla con ProveedorNoDisponible, pregunta al respaldo."""
    raise NotImplementedError


# 9. Código seguro: objetos que se defienden -----------------------------------------------------
# Diapositiva "Código seguro: objetos que se defienden".
class ConfigProveedor:
    """Dataclass inmutable con tres campos, en este orden:
        modelo: str
        api_key: str          que NO aparezca en repr() (los repr terminan en los logs)
        temperatura: float = 0.2

    Valide en __post_init__, con if y raise (no con assert):
        - api_key vacía          → ValueError
        - temperatura fuera de 0..2 → ValueError
    """
