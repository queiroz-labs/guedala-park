"""Extracao somente leitura, em FreeCADCmd; nunca salva/recomputa o CAD-fonte."""
from pathlib import Path
import json, hashlib, itertools
import FreeCAD as App, Part
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
SOURCE=PROJECT/'Correcao_integral_R52_2026-10-25/Guedala_Park_R52_Corrigido.FCStd'
GEO=PROJECT/'P01_massas_equilibrio_2026-10-25/Geometria_R51.json'
PLINTH=PROJECT/'P01_apoios_ao_piso_2026-10-25/Resultados.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=sha(SOURCE);geo=json.loads(GEO.read_text(encoding='utf-8'))
oldsha=sha(Path(geo['cad']))
assert oldsha==geo['sha256']
doc=App.openDocument(str(SOURCE))
names=['Peca206','Peca207','Peca208','Peca209','Peca210','ReferenciaCorrerR14','ReferenciaCorrerR001','ReferenciaCorrerR002','ReferenciaCorrerR003']
names += [r['name'] for r in geo['wood']['P03'] if r['name'] not in ['Peca264','Peca265']]
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def record(s):
 b=s.BoundBox;vol=sum(t.Volume for t in s.Solids)
 c=sum((t.CenterOfMass*t.Volume for t in s.Solids),App.Vector())/vol
 return {'bbox_mm':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax], 'volume_mm3':vol,'com_mm':[c.x,c.y,c.z]}
shapes={n:world(doc.getObject(n)) for n in names}
# A caixaP02 e representada por uma resultante agregada; usa-se a base emL
# apenas para extrair as interfaces geometricas, sem substitui-la por seuBBox.
shapes['P02_resultante']=world(doc.getObject('PlacaL'))
records={n:dict(name=n,label=doc.getObject(n).Label if n!='P02_resultante' else 'P02 agregado:10 madeiras',**record(s))for n,s in shapes.items()}
rows=geo['wood']['P02'];vol=sum(r['volume_mm3']for r in rows)
records['P02_resultante']['volume_mm3']=vol
records['P02_resultante']['com_mm']=[sum(r['volume_mm3']*r['com_global_mm'][i]for r in rows)/vol for i in range(3)]
# Confirma individualmente os corpos usados contra inventarioR51, sem assumir
# que a simples comparacao de dois BBox valida um painel nao retangular.
legacy={r['name']:r for group in geo['wood'].values()for r in group}
for n in names:
 a=records[n];b=legacy[n]
 assert abs(a['volume_mm3']-b['volume_mm3'])<.01,(n,'volume')
 assert max(abs(x-y)for x,y in zip(a['bbox_mm'],b['bbox_global_mm']))<1e-6,(n,'bbox')
 assert max(abs(x-y)for x,y in zip(a['com_mm'],b['com_global_mm']))<1e-6,(n,'centro')
plinth=json.loads(PLINTH.read_text(encoding='utf-8'))['new_boards']
def interfaces(shapes):
 out=[]
 for a,b in itertools.combinations(shapes,2):
  sa,sb=shapes[a],shapes[b];aa,bb=record(sa)['bbox_mm'],record(sb)['bbox_mm']
  if any(min(aa[i+3],bb[i+3])-max(aa[i],bb[i]) < -1e-6 for i in range(3)):continue
  overlaps=[min(aa[i+3],bb[i+3])-max(aa[i],bb[i])for i in range(3)]
  flat=[i for i,v in enumerate(overlaps)if abs(v)<1e-6]
  if len(flat)!=1:continue
  axis=flat[0];level=(max(aa[axis],bb[axis])+min(aa[axis+3],bb[axis+3]))/2
  def on_plane(f):
   fb=f.BoundBox;bounds=[fb.XMin,fb.YMin,fb.ZMin,fb.XMax,fb.YMax,fb.ZMax]
   return abs(bounds[axis]-level)<1e-6 and abs(bounds[axis+3]-level)<1e-6
  common_faces=[]
  for fa in sa.Faces:
   if not on_plane(fa):continue
   for fb in sb.Faces:
    if on_plane(fb):common_faces.extend(fa.common(fb).Faces)
  for f in common_faces:
   if f.Area<1e-4:continue
   vs=[[v.Point.x,v.Point.y,v.Point.z] for v in f.Vertexes]
   normal=f.normalAt(0,0)
   axis=max(range(3),key=lambda i:abs([normal.x,normal.y,normal.z][i]))
   assert abs(abs([normal.x,normal.y,normal.z][axis])-1)<1e-8
   out.append({'a':a,'b':b,'area_mm2':f.Area,'center_mm':[f.CenterOfMass.x,f.CenterOfMass.y,f.CenterOfMass.z], 'axis':axis,'vertices_mm':vs})
 return out
variants={}
for label,add_soco,extend in [('R52_sem_soco',False,False),('soco_sem_traseiro',True,False),('soco_e_traseiro',True,True)]:
 ss={k:v.copy()for k,v in shapes.items()}
 if extend:
  ss['Peca208']=Part.makeBox(1964,18,2114,App.Vector(5408,3922,18))
  ss['Peca262']=Part.makeBox(1314,650,18,App.Vector(5408,3290,2132))
 rr={n:dict(records[n],**record(s))for n,s in ss.items()}
 rr['P02_resultante']=records['P02_resultante'].copy()
 if add_soco:
  for p in plinth:
   n=p['id'];ss[n]=Part.makeBox(*p['size_mm'],App.Vector(*p['origin_mm']))
   rr[n]=dict(name=n,label='ESTUDO socoR01: '+n,**record(ss[n]))
 contacts=interfaces(ss)
 floors=[]
 for n,s in ss.items():
  for f in s.Faces:
   b=f.BoundBox
   if abs(b.ZMin)<1e-6 and abs(b.ZMax)<1e-6 and f.Area>.01:
    floors.append({'a':n,'b':'PISO','area_mm2':f.Area,'axis':2,'center_mm':[f.CenterOfMass.x,f.CenterOfMass.y,0], 'vertices_mm':[[v.Point.x,v.Point.y,v.Point.z]for v in f.Vertexes]})
 variants[label]={'bodies':rr,'interfaces':contacts,'floor_faces':floors,'soco':add_soco,'extend':extend}
assert sha(SOURCE)==before and sha(Path(geo['cad']))==oldsha
App.closeDocument(doc.Name)
out={'source':str(SOURCE),'source_sha256':before,'source_unchanged':True,'inventory_R51':str(GEO),'inventory_sha256':sha(GEO),'R51_source_unchanged':True,'verified_original_bodies':names,'doors':geo['wood']['P03'][-2:],'variants':variants,'limitations':['P02 agregado; mecanismo interno e cantilever do retorno nao modelados.','Interfaces sao faces nominais, nao ligacoes ou capacidade demonstrada.','Soco e extensoes so existem nos cenarios separados; nao noCADR52.']}
(HERE/'Geometria_interfaces.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:{'bodies':len(v['bodies']),'interfaces':len(v['interfaces']),'floors':len(v['floor_faces'])}for k,v in variants.items()}))
