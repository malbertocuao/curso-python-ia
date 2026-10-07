"""Sesiones 2, 4, 5 y 11: puertos (interfaces) del hexágono, expresados como Protocols.

Los adaptadores (OpenAI, Anthropic, Ollama, memoria, Postgres...) los implementan
sin heredar de nada: tipado estructural. El dominio y los servicios solo conocen esto.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from types import TracebackType
from typing import Protocol, Self, runtime_checkable
from uuid import UUID

from asistente.domain.models import Chunk, Document, Message


@runtime_checkable
class LLMProvider(Protocol):
    """Puerto de salida hacia cualquier proveedor de modelos (Strategy, sesión 4)."""

    name: str

    async def complete(self, messages: Sequence[Message], *, temperature: float = 0.2) -> str: ...


@runtime_checkable
class VisionProvider(Protocol):
    """Sesión 11: un proveedor que además lee imágenes."""

    async def describe_image(self, image: bytes, media_type: str, prompt: str) -> str: ...


class EmbeddingProvider(Protocol):
    dimensions: int

    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...


class DocumentRepository(Protocol):
    def add(self, doc: Document) -> None: ...
    def get(self, doc_id: UUID) -> Document | None: ...
    def list(self) -> list[Document]: ...


class VectorStore(Protocol):
    def add(self, chunks: Sequence[Chunk]) -> None: ...

    def search(
        self, vector: Sequence[float], k: int = 4, *, groups: frozenset[str]
    ) -> list[tuple[Chunk, float]]:
        """Los k fragmentos más parecidos entre los que pueden ver `groups` (sesión 13).

        `groups` es obligatorio a propósito: nadie puede olvidar el control de acceso.
        """
        ...


class UnitOfWork(Protocol):
    """Todo o nada: el documento y sus vectores se guardan juntos (sesión 4)."""

    @property
    def documents(self) -> DocumentRepository: ...
    @property
    def chunks(self) -> VectorStore: ...

    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


class DocumentExtractor(Protocol):
    """Sesión 11: convierte un archivo en un Document. Cadena de responsabilidad."""

    def supports(self, path: Path) -> bool: ...
    async def extract(self, path: Path) -> Document: ...
