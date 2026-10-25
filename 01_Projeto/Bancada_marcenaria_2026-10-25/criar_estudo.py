"""Bancada de estudo com laterais/pedestal em marcenaria, sem tubos.
Mantem tampo30, topo750 e geometria de contexto das gavetas/equipamentos.
"""
from pathlib import Path
import json,hashlib,csv
import FreeCAD as App,FreeCADGui as Gui,Part
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'Resultados.json').read_text(encoding='utf-8'))
cad=Path(data['cad']);assert hashlib.sha256(cad.read_bytes()).hexdigest()==data['sha256']
src=next(d for d in App.listDocuments().values() if Path(d.FileName).resolve()==cad.resolve())
assert not Gui.getDocument(src.Name).Modified
assert data['panels'][3]['origin_mm'][1]==70
assert 'Bancada_marcenaria_pedestal_ESTUDO' not in App.listDocuments()
doc=App.newDocument('Bancada_marcenaria_pedestal_ESTUDO');doc.Label='Bancada - paineis de marcenaria, estudo condicionado'
context=doc.addObject('App::DocumentObjectGroup','Contexto');context.Label='Gavetas/equipamentos atuais, apenas contexto congelado'
structure=doc.addObject('App::DocumentObjectGroup','Marcenaria');structure.Label='Cinco paineis propostos, nenhum tubo'
points=doc.addObject('App::DocumentObjectGroup','Eixos_nominais');points.Label='Referencias de uniao, nao programa CNC'
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def bbox(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
inventory=json.loads((HERE.parent/'Cargas_e_ligacoes_R50_2026-10-25/Geometria_R50.json').read_text(encoding='utf-8'))
context_ids=[n for n in inventory['modules']['P16']['pieces'] if inventory['parts'][n]['visible_effective'] and n not in ['Peca367','Peca368']]
context_ids+=['Peca110']+[f'Peca{i}' for i in range(113,122)]
for n in dict.fromkeys(context_ids):
 original=src.getObject(n);o=doc.addObject('PartDesign::Feature','Ref_'+n);o.Label=original.Label;o.Shape=world(original);context.addObject(o)
 o.ViewObject.ShapeColor=original.ViewObject.ShapeColor
 if n=='Peca110':o.ViewObject.Transparency=60
new=[];added=[]
for p in data['panels']:
 o=doc.addObject('PartDesign::Feature',p['id']);o.Label=p['role'];o.Shape=Part.makeBox(*p['size_mm'],App.Vector(*p['origin_mm']));structure.addObject(o)
 o.ViewObject.ShapeColor=(.30,.57,.45);o.ViewObject.Transparency=20
 o.addProperty('App::PropertyString','Situacao').Situacao='ESTUDO: aparencia e apoios alterados; material/retencao/fixadores e estabilidade nao aprovados'
 new.append(o)
 if p['source_replaces'] in ['Peca367','Peca368']:
  original=world(src.getObject(p['source_replaces']))
  assert abs(o.Shape.common(original).Volume-original.Volume)<1e-5
  added.append((o.Name,o.Shape.cut(original)))
 else:added.append((o.Name,o.Shape))
top=world(src.getObject('Peca110'));contacts=[]
def area_plane(sa,sb,axis,value):
 def fs(s):
  return [f for f in s.Faces if abs(bbox(f)[axis]-value)<1e-6 and abs(bbox(f)[axis+3]-value)<1e-6]
 return sum(f.common(g).Area for f in fs(sa) for g in fs(sb))
for o in new:
 area=area_plane(o.Shape,top,2,720)
 assert area>0
 contacts.append(dict(a=o.Name,b='Peca110',horizontal_area_mm2=area,normal='Z',status='apoio geometrico; retencao por comprovar'))
for side in ['Apoio_esquerdo','Pedestal_lateral_E']:
 o=doc.getObject(side);x=2738 if side=='Apoio_esquerdo' else 4300
 area=area_plane(o.Shape,doc.getObject('Travessa_traseira').Shape,0,x)
 assert abs(area-18*180)<1e-5
 contacts.append(dict(a=side,b='Travessa_traseira',vertical_area_mm2=area,normal='X',status='junta de cortante, nao simples apoio por gravidade'))
rows=[]
for tag,x in [('E',2738.),('D',4300.)]:
 for k,z in enumerate([612.,648.],1):
  rows.append(dict(id=f'BT-J01-{tag}-{k}',a='Travessa_traseira',b='Apoio_esquerdo' if tag=='E' else 'Pedestal_lateral_E',
   family='Confirmat7x50 candidato',X_mm=x,Y_mm=79.,Z_mm=z,axis='X',quantity=1,
   status='Interface nominal; grupo K1000 inicial requerido. Piloto/cabeca/ligacao real por provar; naoCNC'))
 rows.append(dict(id=f'BT-J01-{tag}-POS',a='Travessa_traseira',b='Apoio_esquerdo' if tag=='E' else 'Pedestal_lateral_E',
  family='Cavilha8x30 posicionamento, sem credito resistente',X_mm=x,Y_mm=79.,Z_mm=630.,axis='X',quantity=1,
  status='Interface nominal; profundidades e tolerancias por conferir; naoCNC'))
for r in rows:
 o=doc.addObject('PartDesign::Feature',r['id'].replace('-','_'));o.Label=r['id']+' - referencia nominal'
 o.Shape=Part.makeSphere(2,App.Vector(r['X_mm'],r['Y_mm'],r['Z_mm']));points.addObject(o);o.ViewObject.ShapeColor=(.8,.15,.10)
points.ViewObject.Visibility=False
parents={o.Name:[p for p in o.InList if 'Group' in p.PropertiesList and o in p.Group] for o in src.Objects};memo={}
def visible(o):
 if o.Name not in memo:memo[o.Name]=bool(o.ViewObject.Visibility) and all(visible(p) for p in parents[o.Name])
 return memo[o.Name]
overlaps=[];candidates=[];screened=0
for original in src.Objects:
 if original.Name in ['Peca111','Peca112','Peca367','Peca368']:continue
 if not original.isDerivedFrom('Part::Feature') or original.Shape.isNull() or not visible(original):continue
 screened+=1;s=world(original);bb=bbox(s)
 for name,sh in added:
  ba=bbox(sh)
  if all(min(ba[k+3],bb[k+3])-max(ba[k],bb[k])>1e-6 for k in range(3)):
   vol=sh.common(s).Volume;candidates.append([name,original.Name,vol])
   if vol>1e-5:overlaps.append([name,original.Name,vol])
self_inter=[]
for i,a in enumerate(new):
 for b in new[i+1:]:
  ba,bb=bbox(a.Shape),bbox(b.Shape)
  if all(min(ba[k+3],bb[k+3])-max(ba[k],bb[k])>1e-6 for k in range(3)):
   vol=a.Shape.common(b.Shape).Volume
   if vol>1e-5:self_inter.append([a.Name,b.Name,vol])
report=dict(contacts=contacts,new_panels=5,retired_in_study=['Peca111','Peca112','Peca367','Peca368'],
  retained_drawer_original_volume_in_new_sides=True,source_visible_shapes_screened=screened,
  source_interference_candidates=candidates,source_positive_interferences=overlaps,self_interferences=self_inter,
  clear_chair_span_mm=1562,source_unchanged=True,source_sha256=data['sha256'],
  scope='Contexto estatico de estudo; nao testa movimento nem ferramenta. Aparencia/espaco sob o gaveteiro mudam, para revisao de Elias. Nao e capacidade liberada.')
(HERE/'Conferencia_geometrica.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not overlaps and not self_inter,(overlaps,self_inter)
doc.recompute();Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
v=Gui.activeDocument().activeView();v.setCameraOrientation(App.Rotation(App.Vector(0,0,1),180).multiply(v.getCameraOrientation()).Q);v.fitAll()
Gui.activeDocument().activeView().saveImage(str(HERE/'Bancada_marcenaria_estudo.png'),1400,1000,'White')
doc.saveAs(str(HERE/'Bancada_marcenaria_pedestal_ESTUDO.FCStd'))
with (HERE/'Junta_travessa_nominal.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
assert hashlib.sha256(cad.read_bytes()).hexdigest()==data['sha256']
App.setActiveDocument(src.Name)
print(json.dumps({'file':doc.FileName,'contacts':len(contacts),'new_interferences':overlaps,'visible_source_shapes':screened}))
