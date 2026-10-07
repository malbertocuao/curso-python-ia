"""Pruebas de la práctica del anexo A. Ejecutar desde la raíz del proyecto:

uv run pytest tipos_de_datos -v
"""

import importlib
import json
import os

import pytest

_m = importlib.import_module(os.getenv("PRACTICA", "") + "tipos")


# Texto ---------------------------------------------------------------------------------
@pytest.mark.parametrize(
    ("nombre", "esperada"),
    [
        ("Informe.Final.PDF", "pdf"),
        ("foto.jpg", "jpg"),
        ("Makefile", ""),
        (".env", ""),
        ("archivo.", ""),
    ],
)
def test_extension(nombre, esperada):
    assert _m.extension(nombre) == esperada


def test_sin_version_quita_el_prefijo_una_sola_vez():
    assert _m.sin_version("v2-manual") == "manual"
    assert _m.sin_version("v2-v2-manual") == "v2-manual"
    assert _m.sin_version("2v-manual") == "2v-manual"


def test_sin_pdf_quita_el_sufijo_exacto():
    assert _m.sin_pdf("informe.pdf") == "informe"
    assert _m.sin_pdf("spdf.pdf") == "spdf"  # rstrip(".pdf") daría "s"
    assert _m.sin_pdf("notas.txt") == "notas.txt"


def test_palabras():
    assert _m.palabras("  hola   mundo \n") == ["hola", "mundo"]
    assert _m.palabras("") == []


def test_campos_conserva_los_vacios():
    assert _m.campos("a, b,,c ") == ["a", "b", "", "c"]


def test_clave_valor():
    assert _m.clave_valor("modelo = qwen3") == ("modelo", "qwen3")
    assert _m.clave_valor("url=http://x?a=1") == ("url", "http://x?a=1")
    with pytest.raises(ValueError, match="falta"):
        _m.clave_valor("sin igual")


def test_carpeta_y_archivo():
    assert _m.carpeta_y_archivo("rrhh/politicas/vacaciones.pdf") == (
        "rrhh/politicas",
        "vacaciones.pdf",
    )
    assert _m.carpeta_y_archivo("vacaciones.pdf") == ("", "vacaciones.pdf")


def test_unir():
    assert _m.unir([1, 2, 3]) == "1, 2, 3"
    assert _m.unir([1, 2], separador="-") == "1-2"
    assert _m.unir([]) == ""


# Ordenar, máximos y recorridos ---------------------------------------------------------
def test_mejores_por_puntaje_y_empate_alfabetico():
    puntajes = {"viaticos": 0.5, "vacaciones": 0.9, "nomina": 0.5, "horario": 0.1}
    assert _m.mejores(puntajes, 3) == ["vacaciones", "nomina", "viaticos"]
    assert _m.mejores(puntajes, 10) == ["vacaciones", "nomina", "viaticos", "horario"]


def test_mas_largo():
    assert _m.mas_largo(["sol", "luna", "mar"]) == "luna"
    assert _m.mas_largo(["sol", "mar"]) == "sol"  # empate: el primero
    assert _m.mas_largo([]) is None


def test_emparejar_exige_el_mismo_largo():
    assert _m.emparejar(["¿a?", "¿b?"], ["1", "2"]) == [("¿a?", "1"), ("¿b?", "2")]
    with pytest.raises(ValueError):
        _m.emparejar(["¿a?", "¿b?"], ["1"])


def test_primero_mayor():
    assert _m.primero_mayor([1, 5, 3, 9], 4) == 5
    assert _m.primero_mayor([1, 2], 4) is None


# Diccionarios y conjuntos --------------------------------------------------------------
def test_sin_repetidos_conserva_el_primero_y_el_orden():
    assert _m.sin_repetidos(["RRHH", "legal", "rrhh", "Legal", "nomina"]) == [
        "RRHH",
        "legal",
        "nomina",
    ]


def test_por_inicial():
    assert _m.por_inicial(["Sol", "mar", "sal", "Luna"]) == {
        "s": ["Sol", "sal"],
        "m": ["mar"],
        "l": ["Luna"],
    }


def test_mas_frecuentes():
    items = ["legal", "rrhh", "legal", "nomina", "rrhh", "legal"]
    assert _m.mas_frecuentes(items, 2) == [("legal", 3), ("rrhh", 2)]


# Números, fechas, bytes y JSON ---------------------------------------------------------
def test_a_centenas_usa_el_redondeo_de_python():
    assert _m.a_centenas(1349) == 1300
    assert _m.a_centenas(1351) == 1400
    assert _m.a_centenas(1250) == 1200  # mitad exacta: al par
    assert _m.a_centenas(1350) == 1400
    assert isinstance(_m.a_centenas(1349), int)


def test_dias_entre():
    assert _m.dias_entre("2026-12-14", "2027-01-05") == 22
    assert _m.dias_entre("2026-10-07", "2026-10-07") == 0


def test_bytes_utf8():
    assert _m.bytes_utf8("año") == 4
    assert _m.bytes_utf8("ano") == 3


def test_a_json():
    texto = _m.a_json({"año": 2026, "temas": ["tipos"]})
    assert '"año": 2026' in texto  # con tildes legibles
    assert "\n  " in texto  # con sangría de 2 espacios
    assert json.loads(texto) == {"año": 2026, "temas": ["tipos"]}
