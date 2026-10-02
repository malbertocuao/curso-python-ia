import importlib
import itertools
import os
from types import GeneratorType

import pytest

_m = importlib.import_module(os.getenv("FUNDAMENTOS", "") + "s05_generadores")


def explota_despues(items, n):
    """Entrega n elementos y luego falla: prueba que nadie consume de más."""
    yield from items[:n]
    raise AssertionError("se consumió más de lo necesario")


def test_leer_registros():
    lineas = ["# encabezado", "", " area = rrhh ; anio=2026 ", "area=legal"]
    assert list(_m.leer_registros(lineas)) == [
        {"area": "rrhh", "anio": "2026"},
        {"area": "legal"},
    ]


def test_leer_registros_es_perezoso_y_reporta_linea():
    gen = _m.leer_registros(explota_despues(["a=1", "b=2"], 1))
    assert isinstance(gen, GeneratorType)
    assert next(gen) == {"a": "1"}
    with pytest.raises(ValueError, match="3"):
        list(_m.leer_registros(["a=1", "", "sin igual"]))


def test_ventanas():
    assert list(_m.ventanas("abcdefg", 3, 2)) == ["abc", "cde", "efg"]
    assert list(_m.ventanas("abcdefgh", 3, 2)) == ["abc", "cde", "efg", "gh"]
    assert list(_m.ventanas("ab", 5, 2)) == ["ab"]
    assert list(_m.ventanas("", 3, 1)) == []


@pytest.mark.parametrize(("tamano", "paso"), [(0, 1), (3, 0), (3, 4)])
def test_ventanas_valida(tamano, paso):
    with pytest.raises(ValueError):
        _m.ventanas("abc", tamano, paso)


def test_sin_repetidos():
    assert list(_m.sin_repetidos([3, 1, 3, 2, 1])) == [3, 1, 2]
    palabras = ["Sol", "mar", "SOL", "Mar", "luna"]
    assert list(_m.sin_repetidos(palabras, clave=str.lower)) == ["Sol", "mar", "luna"]
    infinito = _m.sin_repetidos(itertools.cycle([1, 2, 3, 4]))
    assert list(itertools.islice(infinito, 4)) == [1, 2, 3, 4]


def test_hasta_presupuesto():
    assert list(_m.hasta_presupuesto(["abc", "de", "fgh", "i"], 6)) == ["abc", "de"]
    assert list(_m.hasta_presupuesto(["muy largo"], 3)) == []
    infinito = itertools.repeat("x" * 10)
    assert len(list(_m.hasta_presupuesto(infinito, 95))) == 9
    assert list(_m.hasta_presupuesto(explota_despues(["ab", "cdef"], 2), 3)) == ["ab"]
