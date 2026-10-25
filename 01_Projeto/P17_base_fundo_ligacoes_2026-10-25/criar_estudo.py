"""Estudo parcial P17; fonte nunca editada. Executar no FreeCAD."""
from pathlib import Path
import json,hashlib
import FreeCAD as App,FreeCADGui as Gui,Part
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'Resultados.json').read_text(encoding='utf8'))
cad=Path(data['cad']);assert hashlib.sha256(cad.read_bytes()).hexdigest()==data['sha256']
source=next(d for d in App.listDocuments().values() if Path(d.FileName).resolve()==cad.resolve())
assert not Gui.getDocument(source.Name).Modified
name='P17_fundo_inteiro_ligacoes_ESTUDO'
target=HERE/(name+'.FCStd');assert not target.exists()
module=source.getObject('Modulo016');placement=module.getGlobalPlacement()
names=['Peca384','Peca385','Peca386','Peca387','Peca388','ApoioComumR11','ApoioComumR001','ApoioComumR002','ApoioOpostoR18']
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def shape_local(dim,pos):
 s=Part.makeBox(*dim,App.Vector(*pos));s.Placement=placement.multiply(s.Placement);return s
if name in App.listDocuments():
 doc=App.getDocument(name)
 # Retomada exata da criacao interrompida antes de gravar ou gerar marcadores.
 assert not doc.FileName and len(doc.Objects)==10 and doc.getObject('Madeiras')
 assert all(doc.getObject('Estudo_'+n) for n in names)
else:doc=App.newDocument(name)
App.setActiveDocument(doc.Name);doc.Label='P17 fundo inteiro e ligacoes positivas - ESTUDO condicionado'
group=doc.getObject('Madeiras') or doc.addObject('App::DocumentObjectGroup','Madeiras');objects={}
for old in names:
 original=source.getObject(old);o=doc.getObject('Estudo_'+old) or doc.addObject('PartDesign::Feature','Estudo_'+old);group.addObject(o)
 o.Label=old+' - '+('fundo18 altura550 proposto' if old=='Peca386' else original.Label+' preservado')
 o.Shape=shape_local((1964,18,550),(-1982,332,0)) if old=='Peca386' else world(original)
 o.ViewObject.ShapeColor=(.23,.61,.48) if old=='Peca386' else original.ViewObject.ShapeColor
 o.ViewObject.Transparency=25 if old=='Peca386' else 0
 if 'Situacao' not in o.PropertiesList:o.addProperty('App::PropertyString','Situacao')
 o.Situacao='Estudo separado. Juntas, painel, acesso, acabamento e suspensao pendentes; nao fabricar.'
 objects[old]=o
def area(a,b):
 return sum(f.common(g).Area for f in a.Shape.Faces for g in b.Shape.Faces)
contacts=[]
def contact(a,b,expected):
 ar=area(objects[a],objects[b]);assert abs(ar-expected)<.01,(a,b,ar,expected)
 contacts.append(dict(a=a,b=b,area_mm2=ar,expected_mm2=expected))
divs=[n for n in names if n.startswith('Apoio')]
for n in divs:
 contact(n,'Peca387',18*312);contact(n,'Peca388',18*312);contact(n,'Peca386',18*514)
for n in ('Peca384','Peca385'):contact(n,'Peca386',18*550)
for n in ('Peca387','Peca388'):contact(n,'Peca386',1964*18)
marks=doc.addObject('App::DocumentObjectGroup','Eixos_nominais');rows=[]
def mark(interface,p,axis):
 u,y,z=p;v=placement.multVec(App.Vector(-1982+u,20+y,z));code='P17_E%02d'%(len(rows)+1)
 o=doc.addObject('PartDesign::Feature',code);o.Label=code+' eixo nominal - nao CNC';marks.addObject(o)
 o.Shape=Part.makeSphere(2,v);o.ViewObject.ShapeColor=(.85,.16,.10)
 rows.append(dict(id=code,interface=interface,study_uyz_mm=p,module_xyz_mm=[-1982+u,20+y,z],global_xyz_mm=[v.x,v.y,v.z],axis_in_module=axis,
  family_candidate='Confirmat7x50 proposto; nao produto escolhido',status='Reconciliar com ferragens existentes; nao quantidade adicional, furo ou capacidade aprovada.'))
for u in (473,973,991,1473):
 for y in (72,240):
  for z in (0,550):mark('base/divisoria ou tampo/divisoria',(u,y,z),'Z')
for j in range(12):
 for z in (9,541):mark('base/fundo ou tampo/fundo',(72+j*(1964-144)/11,321,z),'Y')
for u in (473,973,991,1473):
 for z in (88,275,462):mark('divisoria/fundo',(u,321,z),'Y')
for u in (0,1964):
 for z in (70,275,480):mark('lateral/fundo',(u,321,z),'X')
marks.ViewObject.Visibility=False
assert len(rows)==58 and len(contacts)==16
added=[shape_local((1964,18,18),(-1982,332,z)) for z in (0,532)]
def visible(o):
 if not o.ViewObject.Visibility:return False
 return all(p.ViewObject.Visibility for p in o.InListRecursive if p.isDerivedFrom('App::DocumentObjectGroup'))
interferences=[];tested=0
for o in source.Objects:
 if o.Name=='Peca386' or not o.isDerivedFrom('Part::Feature') or o.Shape.isNull() or not visible(o):continue
 s=world(o);tested+=1
 for i,a in enumerate(added):
  if a.BoundBox.intersect(s.BoundBox):
   volume=a.common(s).Volume
   if volume>1e-3:interferences.append(dict(object=o.Name,band=i,volume_mm3=volume))
assert not interferences,interferences
doc.recompute();view=Gui.activeDocument().activeView()
view.viewLeft();view.fitAll()
view.saveImage(str(HERE/'P17_estudo.png'),1400,700,'White')
doc.saveAs(str(target))
assert hashlib.sha256(cad.read_bytes()).hexdigest()==data['sha256'] and not Gui.getDocument(source.Name).Modified
out=dict(study=str(target),study_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),source_sha256=data['sha256'],wood_count=9,
 contacts=contacts,nominal_axes=rows,added_material_interferences=interferences,visible_source_shapes_tested=tested,source_unchanged=True,
 scope='Somente estudo parcial nominal de caixa: oito formas copiadas e fundo514 para550. Sem portas/ferragens. Interferencias dos acrescimos na pose atual; nao ensaio de movimento. Armazenamento e cotas exteriores preservados. Eixos nao sao CNC nem compra.')
(HERE/'Conferencia_geometrica.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
App.setActiveDocument(source.Name)
print(json.dumps(dict(study=str(target),contacts=len(contacts),axes=len(rows),tested=tested,source_unchanged=True)))
