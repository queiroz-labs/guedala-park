import runpy
import traceback
from pathlib import Path
root=Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD')
try:
    tested=runpy.run_path(str(Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD\\05_Ferramentas_e_registros\\auditar_modelo.py')),init_globals={'FreeCAD':FreeCAD})
    result=tested['result']
except Exception:
    result=traceback.format_exc()
    (Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD\\05_Ferramentas_e_registros\\Falha_auditoria.txt')).write_text(result,encoding='utf-8')
