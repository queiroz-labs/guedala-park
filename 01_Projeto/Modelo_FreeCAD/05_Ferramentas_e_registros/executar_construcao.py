import runpy
from pathlib import Path
import traceback
root = Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD')
try:
    for name in list(FreeCAD.listDocuments()):
        if name.startswith('Guedala_Park_R01'):
            FreeCAD.closeDocument(name)
    built = runpy.run_path(str(Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD\\05_Ferramentas_e_registros\\gerar_modelo.py')))
    result = built['result']
except Exception:
    (Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD\\05_Ferramentas_e_registros\\Falha.txt')).write_text(traceback.format_exc(), encoding='utf-8')
    raise
