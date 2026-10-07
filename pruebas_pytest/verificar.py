"""¿Sus pruebas detectan errores? Ejecutar desde la raíz del proyecto:

uv run python pruebas_pytest/verificar.py

Corre test_calculos.py contra calculos.py, donde todas deben pasar, y contra cada mutante_NN.py,
una copia con un error sembrado, donde al menos una prueba debe fallar ("detectado").
Un mutante "sin detectar" significa que a sus pruebas les falta un caso.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

CARPETA = Path(__file__).resolve().parent


def correr(pruebas: Path, modulo: str) -> int:
    entorno = {**os.environ, "CALCULOS": modulo}
    resultado = subprocess.run(  # noqa: S603  (comando fijo: este mismo Python y pytest)
        [sys.executable, "-m", "pytest", str(pruebas), "-q", "-p", "no:cacheprovider", "-x"],
        env=entorno,
        capture_output=True,
        text=True,
        check=False,
    )
    return resultado.returncode


def main() -> int:
    pruebas = Path(sys.argv[1]) if len(sys.argv) > 1 else CARPETA / "test_calculos.py"
    if correr(pruebas, "calculos") != 0:
        print("Sus pruebas fallan con el código correcto: corríjalas primero.")
        print(f"    uv run pytest {pruebas.relative_to(Path.cwd())} -v")
        return 1
    print("Con el código correcto: todas pasan.\n")
    sin_detectar = []
    for mutante in sorted(CARPETA.glob("mutante_*.py")):
        compile(mutante.read_text(encoding="utf-8"), str(mutante), "exec")  # uno roto no cuenta
        detectado = correr(pruebas, mutante.stem) != 0
        print(f"  {mutante.stem}: {'detectado' if detectado else 'SIN DETECTAR'}")
        if not detectado:
            sin_detectar.append(mutante.stem)
    total = len(list(CARPETA.glob("mutante_*.py")))
    print(f"\nDetectados {total - len(sin_detectar)} de {total}.")
    return 1 if sin_detectar else 0


if __name__ == "__main__":
    sys.exit(main())
