"""Sesión 3: estadísticas del índice.

Este archivo tiene problemas que no se ven a simple vista. Encuéntrelos con las herramientas:
`uv run ruff check` y `uv run mypy src`. Las pruebas de tests/test_stats.py dicen qué se espera.
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Sequence

from asistente.domain.models import Chunk, Document


def resumen_indice(docs: Sequence[Document], chunks: Sequence[Chunk]) -> dict[str, int]:
    """Cuántos documentos y fragmentos hay, y cuántos documentos quedaron sin fragmentos."""
    por_documento = Counter(c.document_id for c in chunks)
    return {
        "documentos": len(docs),
        "fragmentos": len(chunks),
        "sin_fragmentos": sum(1 for d in docs if por_documento[d.id] == 0),
    }


def promedio_caracteres(chunks):
    """Largo promedio de los fragmentos; 0.0 si no hay ninguno."""
    return sum(len(c.text) for c in chunks) / len(chunks)


def titulo_mas_largo(docs: Sequence[Document]) -> str | None:
    return max((d.title for d in docs), key=len, default=None)


def titulo_destacado(docs: Sequence[Document]) -> str:
    """El título más largo en mayúsculas, para un encabezado; vacío si no hay documentos."""
    return titulo_mas_largo(docs).upper()
