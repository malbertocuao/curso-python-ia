"""Sesiones 3, 4 y 10: el caso de uso de indexación."""

import pytest

from asistente.adapters.embeddings.providers import HashingEmbedding
from asistente.domain.errors import AssistantError, EmptyDocumentError
from asistente.domain.models import Document
from asistente.services.indexing import IndexingService

TEXTO = "Política de vacaciones. " * 60  # unos 1 400 caracteres


class EmbeddingQueSeQuedaCorto:
    dimensions = 3

    def embed(self, texts):
        return [[1.0, 0.0, 0.0]]  # siempre uno, aunque le pidan varios


# taller: s03
def test_vectorize_asigna_un_vector_a_cada_fragmento():
    chunks = IndexingService(HashingEmbedding()).vectorize(Document("t", TEXTO))
    assert len(chunks) > 1
    assert all(c.embedding and len(c.embedding) == 512 for c in chunks)


# taller: s03
def test_documento_vacio_es_un_error_del_dominio():
    with pytest.raises(EmptyDocumentError):
        IndexingService(HashingEmbedding()).vectorize(Document("t", "   "))
    assert issubclass(EmptyDocumentError, AssistantError)


# taller: s03
def test_si_faltan_vectores_falla_en_vez_de_callar():
    with pytest.raises(ValueError):
        IndexingService(EmbeddingQueSeQuedaCorto()).vectorize(Document("t", TEXTO))
