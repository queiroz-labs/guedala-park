from pathlib import Path
import json
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve()
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R14.json').resolve()).read_text(encoding='utf-8'))
d=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R14_Correr_Simples.FCStd').resolve())
records=[]
for row,title in zip(data['rows'],['Roupeiro','Maleiro']):
 for n in row['controls']:d.getObject(n).Deslocamento=0
 d.getObject(row['controls'][0]).Deslocamento=row['course'];d.recompute()
 m=d.getObject(row['module']);wood=[o for o in m.Group if o.TypeId=='Part::Box']+[d.getObject(n) for n in data['fixed'] if d.getObject(n).getParentGeoFeatureGroup()==m]
 objects=list({o.Name:o for o in wood+[d.getObject(n) for n in row['leaves']+row['moving']+row['tracks']]}.values())
 preview=App.newDocument('Correr'+title+'R14');preview.Label=title+' R14 - carro/guia/trilho são reservas hipotéticas'
 for o in objects:
  s=o.Shape.copy();s.Placement=App.Placement(-m.getGlobalPlacement().Base,App.Rotation()).multiply(o.getGlobalPlacement())
  copy=preview.addObject('Part::Feature','PecaVista');copy.Label=o.Label;copy.Shape=s;copy.ViewObject.ShapeColor=o.ViewObject.ShapeColor
  if o in wood:copy.ViewObject.Transparency=80
  elif o.Name in row['leaves']:copy.ViewObject.ShapeColor=(.84,.78,.65) if o.Name==row['leaves'][0] else (.73,.78,.81)
  else:copy.ViewObject.Transparency=30
 preview.recompute();preview.saveAs(str(root/(title+'_Detalhe_R14.FCStd')));records.append({'title':title,'document':preview.Name,'file':preview.FileName})
 App.setActiveDocument(preview.Name);Gui.getDocument(preview.Name).activeView().viewAxonometric();Gui.updateGui()
for row in data['rows']:
 for n in row['controls']:d.getObject(n).Deslocamento=0
d.recompute();d.save();((Path(__file__).resolve().parent / 'Vistas_R14.json').resolve()).write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8');result=records
