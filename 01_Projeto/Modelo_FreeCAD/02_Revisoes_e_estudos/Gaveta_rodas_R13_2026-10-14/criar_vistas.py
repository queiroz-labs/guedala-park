from pathlib import Path
import json
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R13_Gaveta_Rodas.FCStd').resolve())
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R13.json').resolve()).read_text(encoding='utf-8'));g=doc.getObject(data['drawer']);reports=[]
for label,pos in [('Fechada',0),('Aberta400',400)]:
 g.Extensao=pos;doc.recompute()
 objects=[doc.getObject(n) for n in data['moving_names']+data['fixed_names']]
 upper=[o for n in ['Modulo004','Modulo005'] for o in doc.getObject(n).Group if o.TypeId=='Part::Box' and o.Label.startswith('Base')]
 preview=App.newDocument('DetalheGavetaRodas'+label+'R13');preview.Label='Gaveta rodas R13 '+label+' - gabaritos e reservas'
 for o in objects+upper:
  s=o.Shape.copy();s.Placement=App.Placement(App.Vector(-4503,-6470,0),App.Rotation()).multiply(o.getGlobalPlacement())
  copy=preview.addObject('Part::Feature','PecaVistaR13');copy.Label=o.Label;copy.Shape=s;copy.ViewObject.ShapeColor=o.ViewObject.ShapeColor
  if o in upper:copy.ViewObject.Transparency=70
 preview.recompute();preview.saveAs(str(root/('Detalhe_rodas_'+label+'_R13.FCStd')))
 reports.append({'label':label,'document':preview.Name,'file':preview.FileName,'extension_mm':pos,'pieces':len(objects)+len(upper)})
g.Extensao=0;doc.recompute();doc.save()
((Path(__file__).resolve().parent / 'Vistas_R13.json').resolve()).write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
first=App.getDocument(reports[0]['document']);App.setActiveDocument(first.Name);Gui.getDocument(first.Name).activeView().viewAxonometric();Gui.updateGui();result=reports
