from pathlib import Path
import json
import FreeCAD as App, FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R12_Banheiro_Simples.FCStd').resolve())
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R12.json').resolve()).read_text(encoding='utf-8'));reports=[]
for label,angle in [('Fechado',0),('Aberto60',60)]:
 for r in data['doors']:
  c=doc.getObject(r['control']);c.Abertura=angle
  doc.getObject(r['door']).setEditorMode('Abertura',1)
 doc.getObject('PortaEntradaBanheiroR12').Abertura=0;doc.recompute()
 objects=[o for name in ['Modulo017','Modulo018'] for o in doc.getObject(name).Group if o.TypeId=='Part::Box']
 for r in data['doors']:
  objects.append(doc.getObject(r['front']))
  if 'mirror' in r:objects.append(doc.getObject(r['mirror']))
  objects.extend(doc.getObject(b['body']) for h in r['hinges'] for b in h['bodies'])
  objects.extend(doc.getObject(h['plate']) for h in r['hinges'])
 objects.extend(doc.getObject(name) for name in ['Peca185','Peca186','Peca187','Peca188','Peca189','Peca399'])
 preview=App.newDocument('DetalheBanheiro'+label+'R12');preview.Label='Banheiro R12 '+label+' - proposta e volumes de referência'
 for o in objects:
  s=o.Shape.copy();s.Placement=App.Placement(App.Vector(-4040,-4840,0),App.Rotation()).multiply(o.getGlobalPlacement())
  copy=preview.addObject('Part::Feature','PecaVistaR12');copy.Label=o.Label;copy.Shape=s;copy.ViewObject.ShapeColor=o.ViewObject.ShapeColor
 preview.recompute();preview.saveAs(str(root/('Detalhe_Banheiro_'+label+'_R12.FCStd')))
 reports.append({'label':label,'document':preview.Name,'file':preview.FileName,'angle_deg':angle,'pieces':len(objects)})
for r in data['doors']:doc.getObject(r['control']).Abertura=0
doc.getObject('PortaEntradaBanheiroR12').Abertura=90;doc.recompute();doc.save()
((Path(__file__).resolve().parent / 'Vistas_R12.json').resolve()).write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
first=App.getDocument(reports[0]['document']);App.setActiveDocument(first.Name);Gui.getDocument(first.Name).activeView().viewAxonometric();Gui.updateGui();result=reports
