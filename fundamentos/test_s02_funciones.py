import importlib
import os

import pytest

_m = importlib.import_module(os.getenv("FUNDAMENTOS", "") + "s02_funciones")


def test_ordenar_resultados():
    datos = [
        {"titulo": "b", "puntaje": 0.5},
        {"titulo": "c", "puntaje": 0.9},
        {"titulo": "a", "puntaje": 0.5},
    ]
    copia = list(datos)
    assert [r["titulo"] for r in _m.ordenar_resultados(datos)] == ["c", "a", "b"]
    assert datos == copia


def test_aplicar_pasos():
    assert _m.aplicar_pasos("  Hola ", str.strip, str.lower, lambda t: t + "!") == "hola!"
    assert _m.aplicar_pasos("x") == "x"


def test_agrupar_por():
    palabras = ["sol", "mar", "luna", "río", "cielo"]
    assert _m.agrupar_por(palabras, len) == {
        3: ["sol", "mar", "río"],
        4: ["luna"],
        5: ["cielo"],
    }


def test_limitador():
    consumir = _m.limitador(1000)
    assert [consumir(400), consumir(700), consumir(600), consumir(1)] == [True, False, True, False]
    otro = _m.limitador(10)
    assert otro(10) is True
    with pytest.raises(ValueError):
        otro(-1)


def test_construir_consulta():
    assert _m.construir_consulta("  vacaciones ", limite=3, area="rrhh") == {
        "texto": "vacaciones",
        "limite": 3,
        "filtros": {"area": "rrhh"},
    }
    assert _m.construir_consulta("x")["filtros"] == {}


@pytest.mark.parametrize(
    "kwargs",
    [{"propietario": "otro"}, {"__class__": "x"}, {"limite": 0}, {"limite": 51}],
)
def test_construir_consulta_rechaza(kwargs):
    with pytest.raises(ValueError):
        _m.construir_consulta("x", **kwargs)


def test_construir_consulta_firma():
    with pytest.raises(ValueError):
        _m.construir_consulta("   ")
    with pytest.raises(TypeError):
        _m.construir_consulta("x", 3)  # limite debe ir con nombre
    with pytest.raises(TypeError):
        _m.construir_consulta(texto="x")  # texto es solo posicional
