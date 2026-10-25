"""Inspeção localizada da R30 em modo sem interface; nunca salva a fonte."""
import sys,json,hashlib,time
from pathlib import Path
sys.path.append('C:/Users/Elias/AppData/Local/Programs/FreeCAD-1.1.4/lib')
import FreeCAD as App

here=Path(__file__).resolve().parent
source=here.parents[1]/'Modelo_FreeCAD/01_Atual/Consistencia_R30_2026-10-14/Guedala_Park_R30_Juntas_Rotulos.FCStd'
start=time.time(); before=hashlib.sha256(source.read_bytes()).hexdigest()
doc=App.openDocument(str(source))
def info(o):
    r={'name':o.Name,'label':o.Label,'type':o.TypeId}
    if hasattr(o,'getGlobalPlacement'):
        p=o.getGlobalPlacement();r['global_placement']=str(p)
    if hasattr(o,'Shape') and not o.Shape.isNull():
        b=o.Shape.BoundBox;r['shape_bbox']=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
        r['valid']=o.Shape.isValid();r['volume']=o.Shape.Volume
    if hasattr(o,'Group'):r['group']=[x.Name for x in o.Group]
    return r
module=doc.getObject('Modulo006')
report={'source':str(source),'sha256':before,'seconds':time.time()-start,
        'module':info(module),'members':[info(o) for o in module.Group],
        'extra':[info(doc.getObject(n)) for n in ['Peca133','Peca134','Peca308','Peca152','Peca357']],
        'object_count':len(doc.Objects)}
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
(here/'Inspecao_R30.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'seconds':report['seconds'],'object_count':report['object_count'],'members':report['members']},ensure_ascii=False))
App.closeDocument(doc.Name)
