"""Ejecuta la generación de figuras y logs para las pruebas 1 a 3."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS = [
    "generate_prueba_slam.py",
    "generate_prueba_path_planning.py",
    "generate_prueba_localizacion.py",
]


def main() -> int:
    root = Path(__file__).resolve().parent
    for name in SCRIPTS:
        script = root / name
        print(f"\n=== {name} ===")
        rc = subprocess.call([sys.executable, str(script)], cwd=str(root))
        if rc != 0:
            return rc
    print("\nTodos los assets generados correctamente.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
