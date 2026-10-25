"""Duas alteracoes nominais de marcenaria, separadas daR51."""
from pathlib import Path
import json,hashlib
import FreeCAD as App,FreeCADGui as Gui,Part
HERE=Path(__file__).resolve().parent
geo=json.loads((HERE.parent/'P01_massas_equilibrio_2026-10-25/Geometria_R51.json').read_text(encoding='utf8'))
cad=Path(geo['cad']);assert hashlib.sha256(cad.read_bytes()).hexdigest()==geo['sha256']
source=next(d for d in App.listDocuments().values() if Path(d.FileName).resolve()==cad.resolve())
assert not Gui.getDocument(source.Name).Modified
name='P01_P03_apoio_traseiro_ESTUDO';path=HERE/(name+'.FCStd')
assert name not in App.listDocuments() and not path.exists()
doc=App.newDocument(name);doc.Label='P01-P03: caminho traseiro de madeira - ESTUDO condicionado'
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
names=['Peca206','Peca207','Peca208','Peca209','Peca210','ReferenciaCorrerR003','PlacaL']+[r['name']for r in geo['wood']['P03']]
objects={};changed=[]
for n in names:
 original=source.getObject(n);o=doc.addObject('PartDesign::Feature','Estudo_'+n);o.Label=n+' - '+original.Label
 if n=='Peca208':o.Shape=Part.makeBox(1964,18,2114,App.Vector(5408,3922,18))
 elif n=='Peca262':o.Shape=Part.makeBox(1314,650,18,App.Vector(5408,3290,2132))
 else:o.Shape=world(original)
 if n in ('Peca208','Peca262'):
  old=world(original);assert abs(old.common(o.Shape).Volume-old.Volume)<.001
  changed.append(dict(object=n,old_volume_mm3=old.Volume,new_volume_mm3=o.Shape.Volume,added_mm3=o.Shape.Volume-old.Volume))
 o.ViewObject.ShapeColor=(.22,.61,.47) if n in ('Peca208','Peca262') else original.ViewObject.ShapeColor
 o.ViewObject.Transparency=35 if n in ('Peca206','Peca207','Peca210','Peca208') else 0
 o.addProperty('App::PropertyString','Situacao').Situacao='Estudo nominal separado; nao aprova capacidade, juntas, montagem ou piso. Sem incorporacao.'
 objects[n]=o
calco=doc.addObject('PartDesign::Feature','Calco_fundo_estudo_R01');calco.Label='Calco18 do estudo de socoR01; nao presente na fonte'
calco.Shape=Part.makeBox(1964,18,18,App.Vector(5408,3922,0));calco.ViewObject.ShapeColor=(.25,.56,.43)
objects['Calco_fundo']=calco
contacts=[]
def horizontal(a,b,z,expected):
 def faces(s):return [f for f in s.Faces if abs(f.BoundBox.ZMin-z)<1e-6 and abs(f.BoundBox.ZMax-z)<1e-6]
 area=sum(f.common(g).Area for f in faces(objects[a].Shape) for g in faces(objects[b].Shape))
 assert abs(area-expected)<.01,(a,b,area,expected)
 contacts.append(dict(a=a,b=b,Z_mm=z,area_mm2=area))
horizontal('Peca208','Peca262',2132,1314*18)
horizontal('Peca208','PlacaL',2132,632*18)
horizontal('Peca262','Peca261',2150,1314*18)
horizontal('Peca208','Calco_fundo',18,1964*18)
bands=[Part.makeBox(1964,18,18,App.Vector(5408,3922,2114)),Part.makeBox(1314,18,18,App.Vector(5408,3922,2132))]
def visible(o):return bool(o.ViewObject.Visibility) and all(p.ViewObject.Visibility for p in o.InListRecursive if p.isDerivedFrom('App::DocumentObjectGroup'))
overlaps=[];tested=0
for o in source.Objects:
 if o.Name in ('Peca208','Peca262') or not o.isDerivedFrom('Part::Feature') or o.Shape.isNull() or not visible(o):continue
 s=world(o);b=s.BoundBox;tested+=1
 for i,a in enumerate(bands):
  q=a.BoundBox
  if all(min(v,w)-max(x,y)>1e-6 for v,w,x,y in [(q.XMax,b.XMax,q.XMin,b.XMin),(q.YMax,b.YMax,q.YMin,b.YMin),(q.ZMax,b.ZMax,q.ZMin,b.ZMin)]):
   volume=a.common(s).Volume
   if volume>.001:overlaps.append(dict(band=i,object=o.Name,volume_mm3=volume))
assert not overlaps,overlaps
doc.recompute();view=Gui.activeDocument().activeView();view.viewFront();view.fitAll();view.saveImage(str(HERE/'P01_P03_estudo.png'),1000,1100,'White')
doc.saveAs(str(path))
out=dict(study=str(path),study_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source_sha256=geo['sha256'],changed=changed,
 contacts=contacts,visible_source_shapes_tested=tested,added_material_interferences=overlaps,
 added_nominal_mass_800_kg=sum(r['added_mm3']for r in changed)*800/1e9,
 scope='FundoP01 +18 em altura e baseP03 +18 de profundidade para tras, mantendo envelope e espaco interno. CalcoR01 so contexto separado. Sem portas animadas ou ensaio de caixa; nao libera capacidade.')
assert not Gui.getDocument(source.Name).Modified and hashlib.sha256(cad.read_bytes()).hexdigest()==geo['sha256']
(HERE/'Conferencia_geometrica.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
App.setActiveDocument(source.Name)
print(json.dumps(dict(study=str(path),contacts=len(contacts),added_kg=out['added_nominal_mass_800_kg'],source_unchanged=True)))
