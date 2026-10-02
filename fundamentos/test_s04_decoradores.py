import importlib
import os

import pytest

_m = importlib.import_module(os.getenv("FUNDAMENTOS", "") + "s04_decoradores")


def test_contar_llamadas():
    @_m.contar_llamadas
    def dividir(a, b):
        """Divide a entre b."""
        return a / b

    assert dividir(6, 3) == 2
    with pytest.raises(ZeroDivisionError):
        dividir(1, 0)
    assert dividir.llamadas == 2
    assert dividir.__name__ == "dividir" and dividir.__doc__ == "Divide a entre b."


def test_reintentar_con_espera_exponencial():
    esperas = []
    intentos = {"n": 0}

    @_m.reintentar(4, espera=0.5, dormir=esperas.append)
    def fragil():
        intentos["n"] += 1
        if intentos["n"] < 4:
            raise ConnectionError
        return "ok"

    assert fragil() == "ok"
    assert esperas == [0.5, 1.0, 2.0]


def test_reintentar_agota_y_propaga():
    esperas = []

    @_m.reintentar(2, dormir=esperas.append)
    def siempre_timeout():
        raise TimeoutError

    with pytest.raises(TimeoutError):
        siempre_timeout()
    assert len(esperas) == 1


def test_reintentar_no_reintenta_otros_errores():
    intentos = {"n": 0}

    @_m.reintentar(5, dormir=lambda s: None)
    def llave_invalida():
        intentos["n"] += 1
        raise PermissionError("401")

    with pytest.raises(PermissionError):
        llave_invalida()
    assert intentos["n"] == 1


def test_reintentar_valida_parametros():
    with pytest.raises(ValueError):
        _m.reintentar(0)


def test_registro():
    r = _m.Registro()

    @r.registrar("Eco")
    class Eco:
        pass

    assert Eco.__name__ == "Eco"  # la clase sigue intacta
    assert isinstance(r.crear("ECO"), Eco)
    with pytest.raises(LookupError, match="eco"):
        r.crear("os.system")
    with pytest.raises(ValueError):
        r.registrar("eco")(lambda: object())


def test_requiere_permiso():
    ejecutadas = []

    @_m.requiere_permiso("documentos:borrar")
    def borrar(usuario, doc_id):
        ejecutadas.append(doc_id)
        return True

    admin = _m.Usuario("ana", frozenset({"documentos:leer", "documentos:borrar"}))
    lector = _m.Usuario("luis", frozenset({"documentos:leer"}))
    assert borrar(admin, "d1") is True
    with pytest.raises(PermissionError):
        borrar(lector, "d2")
    assert ejecutadas == ["d1"]
    assert borrar.__name__ == "borrar"
