from pathlib import Path
import json
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve();p=(Path(__file__).resolve().parent / 'Guedala_Park_R17_Equipamentos.FCStd').resolve()
d=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==p)
a=json.loads(((Path(__file__).resolve().parent / 'Conferencia_R17.json').resolve()).read_text(encoding='utf-8'));reports=[]
fronts=json.loads(((Path(__file__).resolve().parent / '../Dobradicas_R10_2026-10-14/Montagem_R10.json').resolve()).read_text(encoding='utf-8'))['doors']
for title,modules,names,prefix in [('MicroPurificador',['Modulo009','Modulo010','Modulo011','Modulo012'],['Peca140','Peca351','Peca138','Peca308','Peca141'],['ME23P','PE12G']),('E21Lavanderia',['Modulo014','Modulo008'],['Peca155','Peca156','Peca152','Peca154','Peca157','Peca357','Peca043'],['E21'])]:
 out=root/(title+'_Detalhe_R17.FCStd');assert not out.exists()
 chosen=list(names)
 for n in modules:chosen.extend(c.Name for c in d.getObject(n).Group if c.TypeId=='Part::Box' and c.Name!='Peca321')
 chosen.extend(r['front'] for r in fronts if r['module'] in modules)
 chosen.extend(z['name'] for z in a['zones'] if any(z['label'].startswith(k) for k in prefix))
 preview=App.newDocument(title+'R17');preview.Label=title+' R17 - reservas documentais, não instalação'
 for n in dict.fromkeys(chosen):
  o=d.getObject(n);s=o.Shape.copy();s.Placement=o.getGlobalPlacement()
  c=preview.addObject('Part::Feature','ReferenciaVista');c.Label=o.Label;c.Shape=s;c.ViewObject.ShapeColor=o.ViewObject.ShapeColor
  if n in [z['name'] for z in a['zones']]:c.ViewObject.Transparency=80
  elif n in names:c.ViewObject.Transparency=72 if n in ['Peca308','Peca357','Peca043'] else 0
  else:c.ViewObject.Transparency=85
 preview.recompute();preview.saveAs(str(out));App.setActiveDocument(preview.Name)
 Gui.getDocument(preview.Name).activeView().viewAxonometric();Gui.updateGui()
 reports.append({'document':preview.Name,'file':str(out),'label':title})
((Path(__file__).resolve().parent / 'Vistas_R17.json').resolve()).write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8');result=reports
