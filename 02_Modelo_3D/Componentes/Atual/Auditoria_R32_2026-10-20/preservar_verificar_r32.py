import sys,zipfile,json,hashlib
from pathlib import Path
sys.path.append('C:/Users/Elias/AppData/Local/Programs/FreeCAD-1.1.4/lib')
import FreeCAD as App
base=Path('C:/Users/Elias/Documents/PROJETOS/Guedala park/guedala-park/02_Modelo_3D/Componentes/Atual')
src=base/'Consolidacao_R31_2026-10-20/Guedala_Park_R31_Consolidado.FCStd'
dst=base/'Auditoria_R32_2026-10-20/Guedala_Park_R32_Auditoria.FCStd'
# O núcleo sem interface não grava os ViewProviders. Preservar os dados
# gráficos originais byte a byte, pois nenhuma geometria foi alterada.
with zipfile.ZipFile(src) as a,zipfile.ZipFile(dst,'a',compression=zipfile.ZIP_DEFLATED) as b:
 existing=set(b.namelist());copied=[]
 for n in a.namelist():
  if n not in existing:b.writestr(n,a.read(n));copied.append(n)
 assert a.read('GuiDocument.xml')==b.read('GuiDocument.xml')
d=App.openDocument(str(dst));d.recompute()
assert d.getObject('AuditoriaDimensionalR32').get('A21')=='Modulo019'
assert len(d.Objects)==6193
assert not [o.Name for o in d.Objects if any(s in o.State for s in ['Invalid','Error'])]
assert d.getObject('AcessoFolhaR31').ExtracaoBandeja==0
App.closeDocument(d.Name)
report={'reopened':True,'objects':6193,'original_gui_preserved':True,'restored_view_entries':len(copied),'model_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'geometry_changed':False}
(dst.parent/'Reabertura_R32.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
