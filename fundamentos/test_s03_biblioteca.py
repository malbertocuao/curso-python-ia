import importlib
import os

import pytest

_m = importlib.import_module(os.getenv("FUNDAMENTOS", "") + "s03_biblioteca")


@pytest.fixture
def base(tmp_path):
    (tmp_path / "rrhh").mkdir()
    (tmp_path / "rrhh" / "vacaciones.md").write_text("Quince días hábiles.", encoding="utf-8")
    (tmp_path / "legal.TXT").write_text("Contrato", encoding="utf-8")
    (tmp_path / "foto.png").write_bytes(b"\x89PNG")
    (tmp_path.parent / "secreto.env").write_text("API_KEY=sk-123", encoding="utf-8")
    return tmp_path


def test_listar_documentos(base):
    assert _m.listar_documentos(base) == ["legal.TXT", "rrhh/vacaciones.md"]
    assert _m.listar_documentos(base, (".png",)) == ["foto.png"]


def test_leer_documento(base):
    assert _m.leer_documento(base, "rrhh/vacaciones.md") == "Quince días hábiles."
    with pytest.raises(FileNotFoundError):
        _m.leer_documento(base, "no-existe.md")


@pytest.mark.parametrize("nombre", ["../secreto.env", "rrhh/../../secreto.env", "/etc/hosts"])
def test_leer_documento_no_sale_de_base(base, nombre):
    with pytest.raises(PermissionError):
        _m.leer_documento(base, nombre)


def test_leer_documento_enlace_que_sale(base):
    (base / "atajo.md").symlink_to(base.parent / "secreto.env")
    with pytest.raises(PermissionError):
        _m.leer_documento(base, "atajo.md")


def test_cargar_config():
    assert _m.cargar_config('{"modelo": "qwen3:14b", "temperatura": 0.2, "extra": 1}') == {
        "modelo": "qwen3:14b",
        "temperatura": 0.2,
        "max_tokens": 512,
    }
    assert (
        _m.cargar_config('{"modelo": "m", "temperatura": 1, "max_tokens": 20}')["max_tokens"] == 20
    )


@pytest.mark.parametrize(
    "texto",
    [
        "no es json",
        "[1, 2]",
        '{"temperatura": 0.2}',
        '{"modelo": " ", "temperatura": 0.2}',
        '{"modelo": "m", "temperatura": 3}',
        '{"modelo": "m", "temperatura": true}',
        '{"modelo": "m", "temperatura": "0.2"}',
        '{"modelo": "m", "temperatura": 0.2, "max_tokens": 0}',
    ],
)
def test_cargar_config_rechaza(texto):
    with pytest.raises(ValueError):
        _m.cargar_config(texto)


def test_a_hora_local():
    assert _m.a_hora_local("2026-10-05T12:00:00+00:00") == "2026-10-05 07:00"
    assert _m.a_hora_local("2026-10-05T12:00:00Z", zona="Europe/Madrid") == "2026-10-05 14:00"
    with pytest.raises(ValueError):
        _m.a_hora_local("2026-10-05T12:00:00")


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("conectando api_key=sk-123 usuario=ana", "conectando api_key=*** usuario=ana"),
        ("TOKEN: abc.def.ghi", "TOKEN: ***"),
        ("password = hunter2, clave=1234", "password = ***, clave=***"),
        ("sin secretos aquí", "sin secretos aquí"),
    ],
)
def test_enmascarar_secretos(entrada, esperado):
    assert _m.enmascarar_secretos(entrada) == esperado
