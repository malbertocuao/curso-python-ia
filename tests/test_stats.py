"""Sesión 3: las estadísticas del índice (y los errores sembrados en el punto de partida)."""

from asistente.domain.models import Document
from asistente.services.stats import (
    promedio_caracteres,
    resumen_indice,
    titulo_destacado,
)

DOCS = [
    Document("Vacaciones", "a " * 500),
    Document("Política de viáticos", "b"),
    Document("Vacía", " "),
]


# taller: s03
def test_resumen_del_indice():
    chunks = [c for d in DOCS for c in d.split(size=400, overlap=50)]
    assert resumen_indice(DOCS, chunks) == {
        "documentos": 3,
        "fragmentos": len(chunks),
        "sin_fragmentos": 1,
    }
    assert promedio_caracteres(chunks) > 0


# taller: s03
def test_casos_vacios_no_revientan():
    assert promedio_caracteres([]) == 0.0
    assert titulo_destacado([]) == ""
    assert titulo_destacado(DOCS) == "POLÍTICA DE VIÁTICOS"
