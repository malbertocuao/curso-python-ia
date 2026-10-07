"""Escriba aquí las pruebas de calculos.py. Ejecutar desde la raíz del proyecto:

uv run pytest pruebas_pytest -v               # sus pruebas, contra el código correcto
uv run python pruebas_pytest/verificar.py     # ¿detectan los 10 errores sembrados?

Lea las docstrings de calculos.py: dicen exactamente qué debe hacer cada función. Para detectar
los 10 errores necesitará lo del anexo B:

- pytest.raises(ValueError, match="...") para cada error que documentan las funciones
- @pytest.mark.parametrize para probar varios casos, incluidos los bordes (0, 100, el último lote)
- pytest.approx o valores exactos para los decimales
- tmp_path para escribir el archivo JSON de leer_config
- monkeypatch.setenv y monkeypatch.delenv para LLM_PROVIDER

No cambie las cuatro líneas de abajo: permiten que verificar.py cambie el módulo que se prueba.
"""

import importlib
import os

_m = importlib.import_module(os.getenv("CALCULOS", "calculos"))


def test_en_lotes_parte_en_grupos():  # un ejemplo para empezar
    assert _m.en_lotes(["a", "b", "c", "d"], 2) == [["a", "b"], ["c", "d"]]
