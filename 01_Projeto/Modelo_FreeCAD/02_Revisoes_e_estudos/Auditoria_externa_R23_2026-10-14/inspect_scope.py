from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
source=json.loads(((Path(__file__).resolve().parent / '../Rotulos_R23_2026-10-14/Rotulos_R23.json').resolve()).read_text(encoding='utf-8'))['file']
d=App.openDocument(source)
rows=[]
for mn in ['Modulo016','Modulo003','Modulo001']:
 for o in d.getObject(mn).Group:
  r={'module':mn,'name':o.Name,'label':o.Label,'type':o.TypeId}
  if o.TypeId=='Part::Box':r['dimensions']=[float(o.Length),float(o.Width),float(o.Height)]
  if 'Shape' in o.PropertiesList:r['volume']=o.Shape.Volume
  rows.append(r)
report={'module_children':rows,'corners':[{'name':o.Name,'label':o.Label,'type':o.TypeId} for o in d.Objects if o.Name.startswith(('FrenteSimples','FerragemSimples','ApoioPortaB','FaixaQuina'))]}
((Path(__file__).resolve().parent / 'Escopo_objetos.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
App.closeDocument(d.Name)
print('SCOPE_RESULT',len(rows),len(report['corners']))
