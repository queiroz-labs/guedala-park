import runpy
import traceback
from pathlib import Path
root=Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD\\02_Revisoes_e_estudos\\Canto_2026-10-13')
try:
    done=runpy.run_path(str(Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD\\02_Revisoes_e_estudos\\Canto_2026-10-13\\detalhar_freecad.py')))
    result=done['result']
except Exception:
    result=traceback.format_exc()
    (Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD\\02_Revisoes_e_estudos\\Canto_2026-10-13\\Falha.txt')).write_text(result,encoding='utf-8')
