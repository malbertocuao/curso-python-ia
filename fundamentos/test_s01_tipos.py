import importlib
import os
from decimal import Decimal

import pytest

_m = importlib.import_module(os.getenv("FUNDAMENTOS", "") + "s01_tipos")


def test_limpiar_etiquetas():
    assert _m.limpiar_etiquetas("Legal, RRHH ,, legal") == ["legal", "rrhh"]
    assert _m.limpiar_etiquetas("  ") == []


def test_total_con_iva():
    assert _m.total_con_iva(["100", "0.05"]) == Decimal("119.06")
    assert _m.total_con_iva(["10.00"], iva="0") == Decimal("10.00")
    assert _m.total_con_iva([]) == Decimal("0.00")


@pytest.mark.parametrize("malo", [["abc"], ["-1"], ["NaN"]])
def test_total_con_iva_rechaza(malo):
    with pytest.raises(ValueError):
        _m.total_con_iva(malo)


def test_parsear_limite():
    assert _m.parsear_limite(None) == 5
    assert _m.parsear_limite("") == 5
    assert _m.parsear_limite(" 20 ") == 20
    assert _m.parsear_limite("3", defecto=1, maximo=3) == 3


@pytest.mark.parametrize("malo", ["0", "51", "-2", "diez", "2.5", "10**9"])
def test_parsear_limite_rechaza(malo):
    with pytest.raises(ValueError):
        _m.parsear_limite(malo)


def test_leer_lista_enteros():
    assert _m.leer_lista_enteros("[1, 2, 3]") == [1, 2, 3]
    assert _m.leer_lista_enteros("[]") == []


@pytest.mark.parametrize(
    "malo",
    ["(1, 2)", "[1, 'a']", "[True]", "[1.5]", "no es lista", "__import__('os').getcwd()"],
)
def test_leer_lista_enteros_rechaza(malo):
    with pytest.raises(ValueError):
        _m.leer_lista_enteros(malo)


def test_indice_invertido():
    docs = {"d1": "Vacaciones anuales", "d2": "vacaciones"}
    assert _m.indice_invertido(docs) == {"vacaciones": {"d1", "d2"}, "anuales": {"d1"}}


def test_fusionar_config_no_modifica_ni_comparte():
    base = {"modelo": "qwen3", "opciones": {"temperatura": 0.2, "max_tokens": 500}}
    capa = {"opciones": {"temperatura": 0.7}}
    r = _m.fusionar_config(base, capa)
    assert r == {"modelo": "qwen3", "opciones": {"temperatura": 0.7, "max_tokens": 500}}
    assert base["opciones"] == {"temperatura": 0.2, "max_tokens": 500}
    assert capa == {"opciones": {"temperatura": 0.7}}
    r["opciones"]["max_tokens"] = 1  # la copia no comparte el dict anidado
    assert base["opciones"]["max_tokens"] == 500
    assert _m.fusionar_config(base) is not base
