import importlib
import os
import time

import pytest

_m = importlib.import_module(os.getenv("KATAS", "katas"))
Cronometro, Factura, en_lotes = _m.Cronometro, _m.Factura, _m.en_lotes
palabras_por_longitud, reintentar, top_n = _m.palabras_por_longitud, _m.reintentar, _m.top_n


def test_palabras_por_longitud():
    assert palabras_por_longitud("El sol, el mar y la sal.") == {
        1: ["y"],
        2: ["el", "la"],
        3: ["mar", "sal", "sol"],
    }


def test_top_n():
    assert top_n(["b", "a", "b", "c", "a", "d"], 2) == [("a", 2), ("b", 2)]


def test_reintentar():
    intentos = {"n": 0}

    @reintentar(3)
    def fragil():
        intentos["n"] += 1
        if intentos["n"] < 3:
            raise ConnectionError
        return "ok"

    assert fragil() == "ok" and intentos["n"] == 3

    @reintentar(2)
    def siempre_falla():
        raise ValueError("x")

    with pytest.raises(ValueError):
        siempre_falla()


def test_en_lotes_es_perezoso():
    gen = en_lotes(iter(range(7)), 3)
    assert next(gen) == [0, 1, 2]
    assert list(gen) == [[3, 4, 5], [6]]


def test_factura():
    assert Factura(100).total == pytest.approx(119)
    with pytest.raises(ValueError):
        Factura(-1)
    with pytest.raises(ValueError):
        Factura(10, iva=1.5)


def test_cronometro():
    with Cronometro() as c:
        time.sleep(0.05)
    assert 0.04 < c.segundos < 0.5
