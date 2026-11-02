"""Pruebas de la práctica de la sesión 2. Ejecutar desde la raíz del proyecto:

uv run pytest poo -v
uv run pytest poo -k cita        # solo un ejercicio
"""

import dataclasses
import importlib
import os
import time
from uuid import uuid4

import pytest

_m = importlib.import_module(os.getenv("PRACTICA", "") + "poo")


# 1. Una dataclass inmutable -------------------------------------------------------------
def test_cita_se_compara_por_contenido():
    assert _m.Cita(1, "15 días") == _m.Cita(1, "15 días")
    assert _m.Cita(1, "15 días") != _m.Cita(2, "15 días")
    assert repr(_m.Cita(1, "x")) == "Cita(fuente=1, extracto='x')"


def test_cita_es_inmutable():
    cita = _m.Cita(fuente=1, extracto="x")
    with pytest.raises(dataclasses.FrozenInstanceError):
        cita.fuente = 2
    assert len({_m.Cita(1, "x"), _m.Cita(1, "x")}) == 1  # inmutable → sirve en un set


# 2. Objeto de valor y entidad -----------------------------------------------------------
def test_mensaje_objeto_de_valor():
    a = _m.Mensaje("user", "hola")
    time.sleep(0.001)
    b = _m.Mensaje("user", "hola")
    assert a.creado != b.creado  # se crearon en momentos distintos...
    assert a == b  # ...y aun así son iguales
    assert a != _m.Mensaje("assistant", "hola")
    with pytest.raises(dataclasses.FrozenInstanceError):
        a.contenido = "otro"


def test_documento_entidad():
    a = _m.Documento("Vacaciones", "15 días")
    b = _m.Documento("Vacaciones", "15 días")
    assert a.fuente == "manual"
    assert a != b  # mismo texto, documentos distintos
    corregido = dataclasses.replace(a, titulo="Vacaciones 2026")
    assert corregido == a  # mismo id: sigue siendo el mismo documento
    assert len({a, b, corregido}) == 2


# 3. Validar al nacer, calcular al pedir --------------------------------------------------
@pytest.mark.parametrize(("texto", "posicion"), [("", 0), ("   ", 0), ("hola", -1)])
def test_fragmento_invalido_no_nace(texto, posicion):
    with pytest.raises(ValueError):
        _m.Fragmento(texto, posicion)


def test_fragmento_propiedades():
    f = _m.Fragmento("quince días hábiles", 0)
    assert f.vectorizado is False
    assert f.palabras == 3
    f.embedding = [0.1, 0.2]
    assert f.vectorizado is True  # se calcula cada vez que se lee


# 4. Que el objeto se comporte como lo que es -----------------------------------------------
def test_conversacion_como_secuencia():
    conv = _m.Conversacion()
    assert not conv
    assert len(conv) == 0
    m = conv.agregar("user", "hola")
    conv.agregar("assistant", "¿en qué le ayudo?")
    assert m == _m.Mensaje("user", "hola")
    assert conv
    assert len(conv) == 2
    assert [x.contenido for x in conv] == ["hola", "¿en qué le ayudo?"]


def test_conversacion_no_entrega_su_lista():
    conv = _m.Conversacion()
    conv.agregar("user", "hola")
    assert isinstance(conv.mensajes, tuple)
    with pytest.raises(AttributeError):
        conv.mensajes.append(_m.Mensaje("user", "intruso"))  # una tupla no tiene append
    assert len(conv) == 1


# 5. Constructores con nombre --------------------------------------------------------------
def test_documento_desde_archivo(tmp_path):
    ruta = tmp_path / "vacaciones.txt"
    ruta.write_text("Quince días hábiles por año.", encoding="utf-8")
    doc = _m.Documento.desde_archivo(ruta)
    assert doc.titulo == "vacaciones"
    assert doc.contenido == "Quince días hábiles por año."
    assert doc.fuente == str(ruta)


def test_desde_archivo_respeta_la_subclase(tmp_path):
    class Manual(_m.Documento):
        pass

    ruta = tmp_path / "manual.txt"
    ruta.write_text("x", encoding="utf-8")
    assert type(Manual.desde_archivo(ruta)) is Manual  # usa cls, no el nombre de la clase


# 6. Herencia: una familia de errores --------------------------------------------------------
def test_jerarquia_de_errores():
    assert issubclass(_m.DocumentoNoEncontrado, _m.ErrorAsistente)
    assert issubclass(_m.ProveedorNoDisponible, _m.ErrorAsistente)
    assert not issubclass(_m.DocumentoNoEncontrado, _m.ProveedorNoDisponible)


def test_buscar():
    doc = _m.Documento("Vacaciones", "15 días")
    docs = {doc.id: doc}
    assert _m.buscar(docs, doc.id) is doc
    otro = uuid4()
    with pytest.raises(_m.DocumentoNoEncontrado, match=str(otro)):
        _m.buscar(docs, otro)
    with pytest.raises(_m.ErrorAsistente):  # también se atrapa por la raíz
        _m.buscar(docs, otro)


# 7. Composición: armar con piezas ------------------------------------------------------------
class Inestable:
    """Proveedor falso: falla las primeras `fallas` veces y luego responde."""

    nombre = "inestable"

    def __init__(self, fallas: int, error: type[Exception] | None = None) -> None:
        self.fallas = fallas
        self.error = error
        self.llamadas = 0

    def completar(self, pregunta: str) -> str:
        self.llamadas += 1
        if self.llamadas <= self.fallas:
            raise (self.error or _m.ProveedorNoDisponible)("caído")
        return f"respuesta a {pregunta}"


def test_con_reintentos_se_recupera():
    interno = Inestable(fallas=2)
    proveedor = _m.ConReintentos(interno, intentos=3)
    assert proveedor.nombre == "inestable+reintentos"
    assert proveedor.completar("hola") == "respuesta a hola"
    assert interno.llamadas == 3


def test_con_reintentos_se_rinde():
    interno = Inestable(fallas=5)
    with pytest.raises(_m.ProveedorNoDisponible):
        _m.ConReintentos(interno, intentos=3).completar("hola")
    assert interno.llamadas == 3


def test_con_reintentos_no_reintenta_otros_errores():
    interno = Inestable(fallas=5, error=KeyError)
    with pytest.raises(KeyError):
        _m.ConReintentos(interno).completar("hola")
    assert interno.llamadas == 1
    with pytest.raises(ValueError):
        _m.ConReintentos(interno, intentos=0)


# 8. Interfaces con Protocol --------------------------------------------------------------------
def test_eco_cumple_el_protocolo_sin_heredar():
    eco = _m.Eco()
    assert eco.completar("hola") == "eco: hola"
    assert isinstance(eco, _m.ProveedorLLM)
    assert _m.ProveedorLLM not in type(eco).__mro__  # no hereda de él
    assert not isinstance(object(), _m.ProveedorLLM)
    assert isinstance(_m.ConReintentos(eco), _m.ProveedorLLM)  # la composición también


def test_con_respaldo():
    assert _m.con_respaldo(_m.Eco(), Inestable(0), "hola") == "eco: hola"
    assert _m.con_respaldo(Inestable(9), _m.Eco(), "hola") == "eco: hola"
    with pytest.raises(KeyError):  # otros errores no activan el respaldo
        _m.con_respaldo(Inestable(9, KeyError), _m.Eco(), "hola")


# 9. Código seguro: objetos que se defienden -----------------------------------------------------
def test_config_no_muestra_la_llave():
    cfg = _m.ConfigProveedor("qwen3:14b", "sk-secreta-123")
    assert cfg.temperatura == 0.2
    assert "sk-secreta-123" not in repr(cfg)
    assert "qwen3:14b" in repr(cfg)
    with pytest.raises(dataclasses.FrozenInstanceError):
        cfg.modelo = "otro"


@pytest.mark.parametrize(("api_key", "temperatura"), [("", 0.2), ("k", -0.1), ("k", 2.5)])
def test_config_valida(api_key, temperatura):
    with pytest.raises(ValueError):
        _m.ConfigProveedor("qwen3:14b", api_key, temperatura)
