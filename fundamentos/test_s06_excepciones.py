import asyncio
import importlib
import os
import stat

import pytest

_m = importlib.import_module(os.getenv("FUNDAMENTOS", "") + "s06_excepciones")


def test_leer_temperatura():
    assert _m.leer_temperatura(" 0.7 ") == pytest.approx(0.7)
    with pytest.raises(_m.EntradaInvalida) as info:
        _m.leer_temperatura("caliente")
    assert isinstance(info.value.__cause__, ValueError)
    with pytest.raises(_m.EntradaInvalida) as info:
        _m.leer_temperatura("5")
    assert info.value.__cause__ is None
    assert issubclass(_m.EntradaInvalida, _m.ErrorAsistente)


def test_transaccion_confirma():
    datos = {"a": 1, "b": 2}
    with _m.transaccion(datos) as borrador:
        borrador["a"] = 10
        del borrador["b"]
        assert datos == {"a": 1, "b": 2}  # nada cambia antes de terminar
    assert datos == {"a": 10}


def test_transaccion_descarta_si_falla():
    datos = {"a": 1}
    with pytest.raises(LookupError), _m.transaccion(datos) as borrador:
        borrador["a"] = 99
        raise LookupError("falló la vectorización")
    assert datos == {"a": 1}


def test_archivo_temporal():
    with _m.archivo_temporal(b"%PDF-1.7 secreto") as ruta:
        assert ruta.read_bytes() == b"%PDF-1.7 secreto"
        assert ruta.suffix == ".pdf"
        assert stat.S_IMODE(ruta.stat().st_mode) == 0o600
    assert not ruta.exists()


def test_archivo_temporal_se_borra_aunque_falle():
    with pytest.raises(ValueError), _m.archivo_temporal(b"x", ".png") as ruta:
        raise ValueError
    assert not ruta.exists()


async def test_con_limite():
    async def rapida():
        return "ok"

    async def lenta():
        await asyncio.sleep(5)

    async def rota():
        raise KeyError("x")

    assert await _m.con_limite(rapida, 1) == "ok"
    with pytest.raises(_m.ProveedorNoDisponible) as info:
        await _m.con_limite(lenta, 0.05)
    assert isinstance(info.value.__cause__, TimeoutError)
    with pytest.raises(KeyError):
        await _m.con_limite(rota, 1)
