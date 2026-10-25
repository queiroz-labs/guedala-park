from pathlib import Path
from datetime import datetime
import json,shutil
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
src=(Path(__file__).resolve().parent / '../Padronizacao_R08_2026-10-14/Guedala_Park_R08_Gavetas_Comuns.FCStd').resolve()
prev=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==src)
prev.save();dest=(Path(__file__).resolve().parent / 'Guedala_Park_R09_Portas_Comuns.FCStd').resolve()
if dest.exists():dest=dest.with_stem(dest.stem+'_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
shutil.copy2(src,dest);doc=App.openDocument(str(dest));App.setActiveDocument(doc.Name)
doc.Label='Guedala Park - R09 - portas comuns com controles corrigidos'
rows=[]
for name in ['Modulo004','Modulo008','Modulo009','Modulo010','Modulo011','Modulo014']:
 m=doc.getObject(name);doors=[o for o in m.Group if hasattr(o,'Abertura')]
 for i,g in enumerate(doors):
  g.Placement.Rotation.Axis=App.Vector(0,0,1)
  if 'CursoEstudo' not in g.PropertiesList:g.addProperty('App::PropertyAngle','CursoEstudo','Conferencia R09')
  g.CursoEstudo=86
  g.setExpression('Placement.Rotation.Angle',('-' if i==0 else '')+'min(CursoEstudo,max(0 deg,Abertura))')
  front=next(o for o in g.Group if o.TypeId=='Part::Box')
  if i==1:
   g.setExpression('Placement.Base.x',m.PlanilhaDimensoes.Name+'.Comprimento - 1 mm')
   front.setExpression('Placement.Base.x','0 mm - Length')
  g.Movimento='Eixo ideal na lateral externa, estudo86 com70T3553 candidato. Dobradica e batente físicos ainda a conferir. Abertura positiva.'
  rows.append({'module':m.Label,'door':g.Name,'front':front.Name,'side':'left' if i==0 else 'right'})
# O aéreo de cinco folhas permanece ilustrativo, sem novos divisores: corrige só o sinal.
m=doc.getObject('Modulo016')
for g in [o for o in m.Group if hasattr(o,'Abertura')]:
 g.Placement.Rotation.Axis=App.Vector(0,0,1);g.setExpression('Placement.Rotation.Angle','-Abertura')
 g.Movimento='Abertura para fora corrigida; distribuição de folhas e apoios internos ainda proposta, sem ferragem real montada.'
 rows.append({'module':m.Label,'door':g.Name,'front':next(o for o in g.Group if o.TypeId=='Part::Box').Name,'side':'left_illustrative_support_pending'})
doc.recompute();doc.save()
((Path(__file__).resolve().parent / 'Controles_R09.json').resolve()).write_text(json.dumps({'file':str(dest),'doors':rows,'scope':'Correção do sentido/pivôs ideais. Sem homologação de dobradiça, batente, fixação ou carga. Cabeceira/canto físico R04 e portas de correr preservados.'},ensure_ascii=False,indent=2),encoding='utf-8')
result={'file':str(dest),'corrected_doors':len(rows)}
