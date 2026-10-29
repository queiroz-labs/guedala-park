"""Entrada FreeCADCmd (que importa scripts, sem usar __main__)."""
from pathlib import Path
import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from medir_folgas_cinematica import run

run(Path(os.environ['GP_CINEMATICA_OUT']))
sys.stdout.flush()
sys.stderr.flush()
os._exit(0)
