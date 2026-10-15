from pathlib import Path
import json
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve();data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R16.json').resolve()).read_text(encoding='utf-8'))
d=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R16_Banco_Simples.FCStd').resolve());m=d.getObject(data['module']);relative=m.getGlobalPlacement().inverse();leaf=d.getObject(data['leaf']);orig=leaf.Placement.copy();reports=[]
def reset():
 for r in data['lids']:
  c=d.getObject(r['control']);c.Abertura=0
  if r['separate_cushion']:c.ElevarAlmofada=0;c.DeslocamentoAlmofada=0
 leaf.Placement=orig
for label in ['BebidasBalde','Folha']:
 reset()
 for r in data['lids'][1:3] if label=='BebidasBalde' else data['lids'][3:]:
  c=d.getObject(r['control']);c.ElevarAlmofada=50;c.DeslocamentoAlmofada=abs(r['parking_source_v']-r['pad_v']);c.Abertura=90
 if label=='Folha':leaf.Placement.Base=App.Vector(orig.Base.x,orig.Base.y+24,800)
 d.recompute();preview=App.newDocument('Banco'+label+'R16');preview.Label='Banco R16 '+label+' - gabaritos e giros ideais'
 objects=[d.getObject(n) for n in data['new']+['Peca406','Peca407','Peca408','Peca421','Peca091','Peca092']]
 for o in objects:
  s=o.Shape.copy();s.Placement=relative.multiply(o.getGlobalPlacement());copy=preview.addObject('Part::Feature','PecaVistaBanco');copy.Label=o.Label;copy.Shape=s;copy.ViewObject.ShapeColor=o.ViewObject.ShapeColor
  kind=o.CategoriaR16 if 'CategoriaR16' in o.PropertiesList else ''
  if o.Name in data['structure']:copy.ViewObject.Transparency=82
  elif o.Name in ['Peca421','Peca091','Peca092']:copy.ViewObject.Transparency=75
  elif kind in ['conteudo','folha_gabarito','reserva_programa']:copy.ViewObject.Transparency=45
 preview.recompute();preview.saveAs(str(root/(label+'_Detalhe_R16.FCStd')));reports.append({'label':label,'document':preview.Name,'file':preview.FileName})
 App.setActiveDocument(preview.Name);Gui.getDocument(preview.Name).activeView().viewAxonometric();Gui.updateGui()
reset();d.recompute();d.save();((Path(__file__).resolve().parent / 'Vistas_R16.json').resolve()).write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8');result=reports
