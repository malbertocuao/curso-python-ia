"""Sesiones 3, 4 y 10: caso de uso "indexar un documento".

- Sesión 3: el servicio recibe el proveedor de embeddings por constructor (inversión de
  dependencias) y lanza errores del dominio, nunca de HTTP.
- Sesión 4: guarda documento y fragmentos en una sola unidad de trabajo (todo o nada).
- Sesión 10: fragmentación por párrafos con el título del documento.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from asistente.domain.models import Chunk, Document
from asistente.domain.ports import EmbeddingProvider, UnitOfWork

Chunking = Literal["chars", "paragraphs"]


@dataclass
class IndexingService:
    embedder: EmbeddingProvider
    uow_factory: Callable[[], UnitOfWork] | None = None
    chunking: Chunking = "chars"

    # taller: s03
    def vectorize(self, doc: Document) -> list[Chunk]:
        """Parte el documento y le asigna a cada fragmento su vector, en una sola llamada.

        Lanza EmptyDocumentError si el documento no tiene texto.
        """
        raise NotImplementedError

    # taller: s04
    def index(self, doc: Document) -> int:
        """Vectoriza y guarda el documento con sus fragmentos; devuelve cuántos son."""
        raise NotImplementedError
