"""Sesión 3: errores del dominio.

Cada capa habla su idioma: los servicios lanzan estos errores y solo la API los traduce a
códigos HTTP (ver los manejadores en api/main.py, sesión 6). Nada de HTTPException aquí.
"""

from __future__ import annotations


class AssistantError(Exception):
    """Raíz de los errores del asistente: permite atraparlos todos en un solo lugar."""


class EmptyDocumentError(AssistantError):
    """El documento no tiene texto que indexar."""


class DocumentNotFoundError(AssistantError):
    """No existe un documento con ese id."""


class ProviderUnavailableError(AssistantError):
    """El proveedor de IA no respondió o falló de forma transitoria: se puede reintentar."""


class UnknownProviderError(AssistantError, ValueError):
    """Se pidió un proveedor que no está registrado (lista de permitidos, sesión 4)."""


class UnsupportedFormatError(AssistantError):
    """El archivo no es de un formato que el asistente sepa leer (sesión 11)."""


class FileTooLargeError(AssistantError):
    """El archivo supera el tamaño máximo permitido (sesión 11)."""
