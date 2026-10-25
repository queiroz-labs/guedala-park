"""BREP/CG atuais e cinematica copiada em documento temporario proprio.
Nenhum controlador da R51 e movido; nao copia o modelo inteiro.
"""
from pathlib import Path
import json,re,hashlib
import FreeCAD as App
HERE=Path(__file__).resolve().parent
src=App.getDocument('Guedala_Park_R51_Sem_estudo_tubular')
active=App.ActiveDocument.Name;temp_name='Temporario_P04P15_cinematica_suspensao'
assert temp_name not in App.listDocuments()
spec={
 'P04':dict(module='Modulo003',width=1764.,depth=230.,height=308.,
  doors=['FrenteComumR015','FrenteComumR016','FrenteComumR017','FrenteVizinhaR18'],
  leaves=['Folha','Folha001','Folha002','VizinhaComumR18'],
  body=['Peca266','Peca267','Peca268','Peca269','Peca270','ApoioComumR003','ApoioComumR004','ApoioOpostoR001','ApoioOpostoR002','FaixaFixaEstudo']),
 'P15':dict(module='Modulo014',width=799.,depth=330.,height=580.,
  doors=['FrenteComumR010','FrenteComumR011'],leaves=['Folha014','Folha015'],
  body=['Peca359','Peca360','Peca361','Peca362','Peca363'])}
def canonical(code,c):
 return [2872-c.y,7390-c.x,c.z-2132] if code=='P04' else [c.x-3563,7000-c.y,c.z-1650]
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def cg_volume(s):
 v=sum(q.Volume for q in s.Solids);c=sum((q.CenterOfMass*q.Volume for q in s.Solids),App.Vector())/v;return c,v
def part(code,n):
 o=src.getObject(n);s=world(o);c,v=cg_volume(s)
 return dict(name=n,label=o.Label,volume_mm3=v,center_uvz_mm=canonical(code,c),visible_local=o.ViewObject.Visibility)
cells={};refs={}
for n in ['CinematicaComumR10','CinematicaComumR11','CinematicaComumR18']:
 o=src.getObject(n);cells[n]=[]
 for addr in o.getNonEmptyCells():
  content=o.getContents(addr);alias=o.getAlias(addr)
  cells[n].append(dict(cell=addr,content=content,alias=alias))
  for name,prop in re.findall(r'([A-Za-z_]\w*)\.([A-Za-z_]\w*)',content):
   if name.startswith('Controle'):refs.setdefault(name,set()).add(prop)
states={n:{p:float(getattr(src.getObject(n),p).Value) for p in props} for n,props in refs.items()}
temp=App.newDocument(temp_name)
try:
 for n,props in refs.items():
  o=temp.addObject('App::FeaturePython',n)
  for p in props:
   o.addProperty('App::PropertyAngle',p);setattr(o,p,states[n][p])
 for n,rows in cells.items():
  o=temp.addObject('Spreadsheet::Sheet',n)
  for r in rows:
   o.set(r['cell'],r['content'])
   if r['alias']:o.setAlias(r['cell'],r['alias'])
 for code,sp in spec.items():
  for n in sp['leaves']:
   old=src.getObject(n);o=temp.addObject('App::Part',n)
   for p in ('LocalX','LocalY','LocalZ'):
    o.addProperty('App::PropertyLength',p);setattr(o,p,getattr(old,p))
   for p in ('GiroLocal','Abertura','CursoEstudo'):
    o.addProperty('App::PropertyAngle',p);setattr(o,p,getattr(old,p) if p in old.PropertiesList else 86.)
   o.Placement=old.Placement
   for prop,expr in old.ExpressionEngine:o.setExpression(prop,expr)
 temp.recompute()
 result_modules={}
 for code,sp in spec.items():
  body=[part(code,n) for n in sp['body']];doors=[]
  module_placement=src.getObject(sp['module']).getGlobalPlacement()
  for n,leafname in zip(sp['doors'],sp['leaves']):
   leaf=src.getObject(leafname);s=world(src.getObject(n));c,v=cg_volume(s)
   local_cg=leaf.getGlobalPlacement().inverse().multVec(c)
   doors.append(dict(name=n,leaf=leafname,volume_mm3=v,center_closed_uvz_mm=canonical(code,c),
    leaf_local_center_mm=[local_cg.x,local_cg.y,local_cg.z],samples=[]))
  result_modules[code]=dict(width_mm=sp['width'],body_depth_mm=sp['depth'],height_mm=sp['height'],body=body,doors=doors)
 # Amostras0..86°; todos os controles temporarios sincronizados por conveniencia.
 for angle in range(87):
  for n,props in refs.items():
   if 'Abertura' in props:temp.getObject(n).Abertura=angle
  temp.recompute()
  for code,sp in spec.items():
   mp=src.getObject(sp['module']).getGlobalPlacement()
   for door in result_modules[code]['doors']:
    p=temp.getObject(door['leaf']).Placement;c=App.Vector(*door['leaf_local_center_mm'])
    uvz=canonical(code,mp.multVec(p.multVec(c)))
    if angle==0:assert max(abs(x-y) for x,y in zip(uvz,door['center_closed_uvz_mm']))<1e-7
    door['samples'].append(dict(angle_deg=angle,center_uvz_mm=uvz))
 data=dict(cad=src.FileName,sha256=hashlib.sha256(Path(src.FileName).read_bytes()).hexdigest(),modules=result_modules,
  source_controller_states=states,source_controllers_unchanged=True,
  kinematics_source='Tres planilhas de quatro barras e expressoes de seis folhas copiadas em documento temporario. Fonte nao movida.',
  datums=dict(P04='u=2872-Y, v=7390-X, z=Z-2132',P15='u=X-3563, v=7000-Y, z=Z-1650'),
  caveat='86° e curso de estudo existente, nao batente comercial comprovado. Ferragens sem massa real e capacidade da parede pendentes.')
 assert states=={n:{p:float(getattr(src.getObject(n),p).Value) for p in props} for n,props in refs.items()}
 (HERE/'Geometria_e_portas_R51.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 result=dict(modules={c:dict(body=len(m['body']),doors=len(m['doors']),max_depth_CG_mm=max(q['center_uvz_mm'][1] for d in m['doors'] for q in d['samples'])) for c,m in result_modules.items()},source_unchanged=True)
finally:
 # Fecha apenas o documento temporario criado por este script, sem arquivos do usuario.
 App.closeDocument(temp_name)
 if active in App.listDocuments():App.setActiveDocument(active)
