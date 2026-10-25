"""Somente leitura: madeiras P01/P03/P02 e interfaces superiores emR51."""
from pathlib import Path
import json,hashlib
import FreeCAD as App,FreeCADGui as Gui
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
ref=json.loads((ROOT/'P01_apoios_ao_piso_2026-10-25/Resultados.json').read_text(encoding='utf8'))
cad=Path(ref['cad']);assert hashlib.sha256(cad.read_bytes()).hexdigest()==ref['sha256']
source=next(d for d in App.listDocuments().values() if Path(d.FileName).resolve()==cad.resolve())
assert not Gui.getDocument(source.Name).Modified
old=json.loads((ROOT/'Cargas_e_ligacoes_R50_2026-10-25/Geometria_R50.json').read_text(encoding='utf8'))
def visible(o):
 return bool(o.ViewObject.Visibility) and all(p.ViewObject.Visibility for p in o.InListRecursive if p.isDerivedFrom('App::DocumentObjectGroup'))
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def record(o):
 s=world(o);b=s.BoundBox;solids=s.Solids;v=sum(x.Volume for x in solids)
 assert v>0
 c=sum((x.CenterOfMass*x.Volume for x in solids),App.Vector())/v
 return dict(name=o.Name,label=o.Label,volume_mm3=v,com_global_mm=[c.x,c.y,c.z],bbox_global_mm=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],parents=[p.Name for p in o.InList])
rows={};excluded={}
for code in ('P01','P03','P02'):
 rows[code]=[];excluded[code]=[]
 for n in old['modules'][code]['pieces']:
  o=source.getObject(n)
  wood=(n.startswith('Peca') or (n.startswith('GavetaComum') and not any(t in o.Label for t in ('Trava','Envelope'))) or
        ('CategoriaR14' in o.PropertiesList and o.CategoriaR14=='madeira') or
        n in ['PlacaL','PlacaL001','LateralApoioPrincipal','FrenteSimplesR04','FrenteSimplesR001','ApoioPortaBR04','FaixaQuinaAR04','FaixaQuinaBR04'])
  if visible(o) and wood:rows[code].append(record(o))
  else:excluded[code].append(dict(name=n,label=o.Label,reason='oculto/auxiliar' if not visible(o) else 'ferragem, varao, gabarito ou eixo; massa efetiva pendente'))
z=2132.;contacts=[]
def faces(s):return [f for f in s.Faces if abs(f.BoundBox.ZMin-z)<1e-6 and abs(f.BoundBox.ZMax-z)<1e-6]
for a in rows['P01']:
 if abs(a['bbox_global_mm'][5]-z)>1e-6:continue
 sa=world(source.getObject(a['name']))
 for code in ('P03','P02'):
  for b in rows[code]:
   if abs(b['bbox_global_mm'][2]-z)>1e-6:continue
   sb=world(source.getObject(b['name']));area=sum(f.common(g).Area for f in faces(sa) for g in faces(sb))
   if area>.001:contacts.append(dict(lower=a['name'],upper=b['name'],upper_module=code,Z_mm=z,area_mm2=area))
mirror=record(source.getObject('Peca275'))
assert hashlib.sha256(cad.read_bytes()).hexdigest()==ref['sha256'] and not Gui.getDocument(source.Name).Modified
out=dict(cad=str(cad),sha256=ref['sha256'],wood=rows,excluded=excluded,upper_contacts=contacts,mirror_reservation=mirror,
 drawer_groups={n:dict(extension_mm=float(source.getObject(n).Extensao.Value),nominal_course_mm=float(source.getObject(n).CursoNominal.Value),local_Y_expression=str(source.getObject(n).ExpressionEngine),global_displacement_per_extension_mm=[0,-1,0]) for n in ['Gaveta','Gaveta001','Gaveta002','Gaveta003']},
 scope='Geometria nominal de madeira visivel, sem densidade real/ferragens. Contato superior nao prova partilha de esforcos entreP02/P03/P01. Espelho e reserva, nao item pesado.')
(HERE/'Geometria_R51.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(dict(wood_counts={k:len(v) for k,v in rows.items()},upper_contacts=len(contacts),source_unchanged=True)))
