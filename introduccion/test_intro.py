"""Pruebas de la práctica de la introducción. Ejecutar desde la raíz del proyecto:

uv run pytest introduccion -v
"""

import importlib
import os
import runpy

import pytest

_m = importlib.import_module(os.getenv("PRACTICA", "") + "intro")


# 1. Un programa es un archivo ----------------------------------------------------------
def test_saludo():
    assert _m.saludo("Ana") == "Hola, Ana"
    assert _m.saludo("  Ana ") == "Hola, Ana"
    assert _m.saludo("Ana", formal=True) == "Buenos días, Ana."
    assert _m.saludo(formal=True, nombre="Luis") == "Buenos días, Luis."


def test_main_solo_al_ejecutar_el_archivo(capsys):
    runpy.run_path(_m.__file__, run_name="__main__")
    assert capsys.readouterr().out == "Hola, mundo\n"
    runpy.run_path(_m.__file__, run_name="importado")
    assert capsys.readouterr().out == ""


# 2. Bloques y condiciones --------------------------------------------------------------
@pytest.mark.parametrize(
    ("t", "esperado"),
    [(0, "precisa"), (0.29, "precisa"), (0.3, "equilibrada"), (1, "equilibrada"), (2, "creativa")],
)
def test_clasificar_temperatura(t, esperado):
    assert _m.clasificar_temperatura(t) == esperado


@pytest.mark.parametrize("t", [-0.1, 2.1])
def test_clasificar_temperatura_fuera_de_rango(t):
    with pytest.raises(ValueError):
        _m.clasificar_temperatura(t)


# 3. Recorrer y contar ------------------------------------------------------------------
def test_contar_vocales():
    assert _m.contar_vocales("Hola Mundo") == {"a": 1, "e": 0, "i": 0, "o": 2, "u": 1}
    assert _m.contar_vocales("") == {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}


# 4. Funciones que devuelven varios valores ---------------------------------------------
def test_resumen():
    menor, mayor, promedio = _m.resumen([4, 1, 7])
    assert (menor, mayor) == (1, 7)
    assert promedio == pytest.approx(4)
    with pytest.raises(ValueError):
        _m.resumen([])


# 5. Al llamar, se pasa el objeto -------------------------------------------------------
def test_agregar_etiqueta_no_modifica_la_lista_recibida():
    originales = ["rrhh"]
    nuevas = _m.agregar_etiqueta(originales, "legal")
    assert nuevas == ["rrhh", "legal"]
    assert originales == ["rrhh"]  # la de afuera no cambió
    assert _m.agregar_etiqueta(None, "legal") == ["legal"]
    assert _m.agregar_etiqueta(["legal"], "legal") == ["legal"]  # sin repetir


# 6. Comprensiones ----------------------------------------------------------------------
def test_largos():
    assert _m.largos(["sol", "", "luna", "  "]) == {"sol": 3, "luna": 4}


# 7. Errores ----------------------------------------------------------------------------
def test_a_entero():
    assert _m.a_entero("42") == 42
    assert _m.a_entero(" 7 ") == 7
    assert _m.a_entero("4.2") == 0
    assert _m.a_entero("x", defecto=-1) == -1


# 8. Módulos de la biblioteca estándar --------------------------------------------------
def test_hipotenusa():
    assert _m.hipotenusa(3, 4) == 5
    assert _m.hipotenusa(1, 1) == 1.41


# 9. Clases -----------------------------------------------------------------------------
def test_contador():
    c = _m.Contador()
    c.incrementar()
    c.incrementar(5)
    assert c.valor == 6
    assert repr(c) == "Contador(6)"
    c.reiniciar()
    assert c.valor == 0
    assert _m.Contador(10).valor == 10
    with pytest.raises(ValueError):
        c.incrementar(0)
    with pytest.raises(AttributeError):
        c.valor = 3  # valor es de solo lectura


# 10. dataclass -------------------------------------------------------------------------
def test_producto():
    p = _m.Producto("Licencia", 100)
    assert p == _m.Producto("Licencia", 100, ())
    assert p.precio_con_iva == 119
    assert _m.Producto("x", 20).precio_con_iva == pytest.approx(23.8)
    with pytest.raises(ValueError):
        _m.Producto("Gratis", -1)
    with pytest.raises(AttributeError):
        p.precio = 1  # frozen=True


# 11. Generadores -----------------------------------------------------------------------
def test_lineas_numeradas():
    gen = _m.lineas_numeradas("primera\n\n  segunda  \n")
    assert next(gen) == "1: primera"
    assert list(gen) == ["2: segunda"]


def test_lineas_numeradas_es_perezoso():
    gen = _m.lineas_numeradas("a\nb")
    assert not isinstance(gen, list)
    assert next(gen) == "1: a"


# 12. Decoradores -----------------------------------------------------------------------
def test_en_mayusculas():
    @_m.en_mayusculas
    def presentar(nombre: str, cargo: str = "analista") -> str:
        """Presenta a una persona."""
        return f"{nombre}, {cargo}"

    assert presentar("ana") == "ANA, ANALISTA"
    assert presentar("luis", cargo="gerente") == "LUIS, GERENTE"
    assert presentar.__name__ == "presentar"
    assert presentar.__doc__ == "Presenta a una persona."
