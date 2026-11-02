"""Sesión 2: entidades del dominio (POO: dataclasses, composición, propiedades).

El dominio NO importa nada de infraestructura (ni FastAPI, ni SDKs de IA, ni BD).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

PUBLIC = frozenset({"todos"})
"""Grupo por defecto: lo que puede ver cualquier usuario autenticado (sesión 13)."""


class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True, slots=True)
class Message:
    """Objeto de valor: inmutable, se compara por contenido."""

    role: Role
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC), compare=False)


@dataclass(slots=True)
class Chunk:
    document_id: UUID
    text: str
    position: int
    embedding: list[float] | None = None
    groups: frozenset[str] = PUBLIC  # quién puede verlo, heredado del documento (sesión 13)


@dataclass(slots=True)
class Document:
    """Entidad: tiene identidad propia (id) que no cambia aunque cambie el contenido."""

    title: str
    content: str
    source: str = "manual"
    metadata: dict[str, str] = field(default_factory=dict)
    groups: frozenset[str] = PUBLIC
    id: UUID = field(default_factory=uuid4)

    @property
    def is_empty(self) -> bool:
        return not self.content.strip()

    def _chunk(self, text: str, position: int) -> Chunk:
        return Chunk(document_id=self.id, text=text, position=position, groups=self.groups)

    # taller: s02
    def split(self, size: int = 800, overlap: int = 100) -> list[Chunk]:
        """Divide el documento en fragmentos con solapamiento (se usa en RAG, sesión 10)."""
        raise NotImplementedError

    # taller: s10
    def split_paragraphs(self, max_chars: int = 1200) -> list[Chunk]:
        """Sesión 10: fragmentos por párrafos, con el título del documento al inicio de cada uno.

        Junta párrafos consecutivos mientras quepan en `max_chars`; un párrafo más largo que
        el límite se parte con `split`. El título da contexto a fragmentos como "se solicitan
        con 30 días de anticipación", que solos no dicen de qué hablan.
        """
        raise NotImplementedError


@dataclass(slots=True)
class Conversation:
    """Composición: una conversación *tiene* mensajes (sesión 9: manejo de contexto)."""

    system_prompt: str
    id: UUID = field(default_factory=uuid4)
    summary: str = ""
    _messages: list[Message] = field(default_factory=list)

    @property
    def messages(self) -> tuple[Message, ...]:
        return tuple(self._messages)

    # taller: s02
    def add(self, role: Role, content: str) -> Message:
        """Agrega un turno de usuario o de asistente; el de sistema se fija al crearla."""
        raise NotImplementedError

    def _system(self) -> str:
        if not self.summary:
            return self.system_prompt
        return f"{self.system_prompt}\n\nResumen de la conversación hasta ahora:\n{self.summary}"

    # taller: s02
    def window(self, max_chars: int = 12_000) -> list[Message]:
        """Ventana de contexto: system + los turnos más recientes que quepan en el presupuesto.

        Aproximación didáctica: ~4 caracteres ≈ 1 token.
        """
        raise NotImplementedError

    # taller: s09
    def replace_history(self, summary: str, recent: list[Message]) -> None:
        """Sesión 9: reemplaza los turnos antiguos por un resumen y conserva los recientes."""
        raise NotImplementedError
