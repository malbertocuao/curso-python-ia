"""Sesiones 5 y 10: adaptadores de embeddings + Factory.

HashingEmbedding: sin red, sin costo, determinístico. Sirve para pruebas y para que
el pipeline funcione desde el día uno; captura similitud léxica, no semántica.
OllamaEmbedding / OpenAICompatibleEmbedding: semánticos, por API. Regla de oro: indexar y
consultar con el mismo modelo (los vectores de modelos distintos no son comparables).
"""

from __future__ import annotations

import hashlib
import math
import os
import re
from collections.abc import Callable, Sequence

from asistente.domain.errors import ProviderUnavailableError, UnknownProviderError
from asistente.domain.ports import EmbeddingProvider

_TOKEN = re.compile(r"\w+", re.UNICODE)
_STOP = frozenset(
    [
        "el",
        "la",
        "los",
        "las",
        "un",
        "una",
        "de",
        "del",
        "y",
        "o",
        "a",
        "en",
        "por",
        "para",
        "con",
        "se",
        "me",
        "te",
        "que",
        "es",
        "al",
        "lo",
        "le",
        "su",
        "sus",
        "mi",
        "cuantos",
        "cuanta",
        "cuántos",
        "cuánta",
        "cómo",
        "como",
        "qué",
        "cual",
        "cuál",
    ]
)


class HashingEmbedding:
    def __init__(self, dimensions: int = 512) -> None:
        self.dimensions = dimensions

    def _one(self, text: str) -> list[float]:
        vec = [0.0] * self.dimensions
        for token in _TOKEN.findall(text.lower()):
            if token in _STOP or len(token) < 3:
                continue
            h = int(hashlib.md5(token.encode(), usedforsecurity=False).hexdigest(), 16)
            vec[h % self.dimensions] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._one(t) for t in texts]


class SentenceTransformerEmbedding:
    """Embeddings semánticos locales (CPU-bound → ProcessPool en la sesión 5)."""

    def __init__(self, model: str = "paraphrase-multilingual-MiniLM-L12-v2") -> None:
        from sentence_transformers import SentenceTransformer  # import perezoso

        self._model = SentenceTransformer(model)
        self.dimensions = int(self._model.get_sentence_embedding_dimension() or 0)

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [
            list(map(float, v)) for v in self._model.encode(list(texts), normalize_embeddings=True)
        ]


class OpenAICompatibleEmbedding:
    """Embeddings vía API (I/O-bound → ThreadPool o asyncio en la sesión 5)."""

    def __init__(
        self,
        model: str,
        dimensions: int,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 60,
    ) -> None:
        from openai import OpenAI

        self._client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout, max_retries=2)
        self._model = model
        self.dimensions = dimensions

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        import openai

        try:
            resp = self._client.embeddings.create(model=self._model, input=list(texts))
        except (openai.APIConnectionError, openai.RateLimitError, openai.InternalServerError) as e:
            raise ProviderUnavailableError(f"embeddings no disponibles: {type(e).__name__}") from e
        return [d.embedding for d in resp.data]


# taller: s10
def OllamaEmbedding(  # noqa: N802 (se usa como una clase: OllamaEmbedding(...))
    model: str = "qwen3-embedding:0.6b", dimensions: int = 1024, base_url: str | None = None
) -> OpenAICompatibleEmbedding:
    """Sesión 10: Ollama expone /v1/embeddings compatible con OpenAI; basta con la base_url."""
    raise NotImplementedError


class SlowEmbedding:
    """Sesión 5: envuelve otro proveedor y simula la latencia de una API (patrón decorador)."""

    def __init__(self, inner: EmbeddingProvider, delay: float = 0.2) -> None:
        self.inner = inner
        self.delay = delay
        self.dimensions = inner.dimensions

    # taller: s05
    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """Espera `delay` segundos (como una llamada de red) y delega en el proveedor interno."""
        raise NotImplementedError


_EMBEDDERS: dict[str, Callable[[], EmbeddingProvider]] = {
    "hashing": lambda: HashingEmbedding(),
    "ollama": lambda: OllamaEmbedding(os.getenv("OLLAMA_EMBED_MODEL", "qwen3-embedding:0.6b")),
    "sentence": lambda: SentenceTransformerEmbedding(),
    "openai": lambda: OpenAICompatibleEmbedding(
        os.environ["OPENAI_EMBED_MODEL"], int(os.getenv("OPENAI_EMBED_DIMENSIONS", "1536"))
    ),
}


def build_embedder(provider: str | None = None) -> EmbeddingProvider:
    """Proveedor de embeddings según `provider` o EMBEDDING_PROVIDER (por defecto, hashing)."""
    key = (provider or os.getenv("EMBEDDING_PROVIDER") or "hashing").lower()
    try:
        factory = _EMBEDDERS[key]
    except KeyError:
        raise UnknownProviderError(
            f"Embeddings no soportados: {key}. Opciones: {sorted(_EMBEDDERS)}"
        ) from None
    return factory()
