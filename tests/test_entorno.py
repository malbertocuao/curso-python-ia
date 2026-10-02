"""Sesión 1: el entorno está listo. Estas pruebas deben pasar desde el primer día."""

import sys

import asistente


def test_python_312_o_superior():
    assert sys.version_info >= (3, 12)


def test_el_paquete_se_importa():
    assert asistente.__name__ == "asistente"
