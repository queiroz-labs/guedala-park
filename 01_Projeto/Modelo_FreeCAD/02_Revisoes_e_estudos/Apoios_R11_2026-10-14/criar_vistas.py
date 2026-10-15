import FreeCAD as App, FreeCADGui as Gui
from pathlib import Path
import json
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R11_Apoios_Simples.FCStd').resolve())
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R11.json').resolve()).read_text(encoding='utf-8'))
for r in data['doors']:
 c=doc.getObject(r['control']);c.Abertura=60
 for name in ['JuntaEsquerdaProposta','JuntaDireitaProposta']:c.setEditorMode(name,1)
 doc.getObject(r['door']).setEditorMode('Abertura',1)
doc.getObject('ControleCanto').set('B4','60 deg');doc.recompute()
reports=[]
for name,label in [('Modulo016','Escritorio'),('Modulo003','Cabeceira')]:
 m=doc.getObject(name);inv=m.getGlobalPlacement().inverse()
 objects=[o for o in m.Group if o.TypeId=='Part::Box']
 for r in data['doors']:
  if r['module']!=name:continue
  objects.append(doc.getObject(r['front']))
  objects.extend(doc.getObject(b['body']) for h in r['hinges'] for b in h['bodies'])
  objects.extend(doc.getObject(h['plate']) for h in r['hinges'])
 if name=='Modulo003':
  objects.extend(doc.getObject(n) for n in ['VizinhaComCanecosR03','DivisorApoioVizinhaR03'])
  for group in [o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('71B3650 - quatro barras')]:
   objects.extend(o for o in group.Group if o.TypeId=='Part::Feature')
 preview=App.newDocument('Detalhe'+label+'R11');preview.Label=label+' R11 - vista estática60 - proposta'
 for o in objects:
  s=o.Shape.copy();s.Placement=inv.multiply(o.getGlobalPlacement())
  copy=preview.addObject('Part::Feature','PecaVistaR11');copy.Label=o.Label;copy.Shape=s
  copy.ViewObject.ShapeColor=o.ViewObject.ShapeColor
 preview.recompute();preview.saveAs(str(root/('Detalhe_'+label+'_R11.FCStd')))
 reports.append({'label':label,'document':preview.Name,'file':preview.FileName,'pieces':len(objects)})
for r in data['doors']:doc.getObject(r['control']).Abertura=0
doc.getObject('ControleCanto').set('B4','0 deg');doc.recompute();doc.save()
((Path(__file__).resolve().parent / 'Vistas_R11.json').resolve()).write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
first=App.getDocument(reports[0]['document']);App.setActiveDocument(first.Name);Gui.getDocument(first.Name).activeView().viewAxonometric();Gui.updateGui()
result=reports
