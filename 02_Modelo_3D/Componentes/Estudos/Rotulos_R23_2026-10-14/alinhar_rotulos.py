from pathlib import Path
import json,shutil,hashlib,re
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
src=(Path(__file__).resolve().parent / '../Visibilidade_R22_2026-10-14/Guedala_Park_R22_Visibilidade_Atual.FCStd').resolve();dst=(Path(__file__).resolve().parent / 'Guedala_Park_R23_Rotulos_Consistentes.FCStd').resolve()
assert not dst.exists(),'Revisão existente; não reconstruir'
sha=hashlib.sha256(src.read_bytes()).hexdigest();shutil.copy2(src,dst);d=App.openDocument(str(dst));App.setActiveDocument(d.Name)
snapshot={o.Name:{'parent':o.getParentGeoFeatureGroup().Name if o.getParentGeoFeatureGroup() else None,'placement':list(o.Placement.Matrix.A) if 'Placement' in o.PropertiesList else None,'expressions':[list(x) for x in o.ExpressionEngine] if 'ExpressionEngine' in o.PropertiesList else None,'visibility':o.Visibility if 'Visibility' in o.PropertiesList else None} for o in d.Objects}
changes=[]
def label(n,value):
 o=d.getObject(n)
 if o.Label!=value:changes.append({'object':n,'before':o.Label,'after':value});o.Label=value
for folder,filename in [('Dobradicas_R10_2026-10-14','Montagem_R10.json'),('Banheiro_R12_2026-10-14','Montagem_R12.json'),('Portas_opostas_R18_2026-10-14','Montagem_R18.json')]:
 for r in json.loads((base/'02_Revisoes_e_estudos'/folder/filename).read_text(encoding='utf-8'))['doors']:
  title=re.sub(r'porta(\d)',r'porta \1',d.getObject(r['control']).Label)
  label(r['control'],title);label(r['door'],title+' — folha proposta');label(r['front'],title+' — frente com canecos')
  for h in r['hinges']:label(h['group'],'71B3550 — '+title+' — z'+str(h['level'])+' (proposta)')
sliding=[]
def reflected(v):return App.Vector(-v.x,v.y,v.z)
for r in json.loads(((Path(__file__).resolve().parent / '../Correr_R14_2026-10-14/Montagem_R14.json').resolve()).read_text(encoding='utf-8'))['rows']:
 m=d.getObject(r['module']);out=reflected(m.getGlobalPlacement().Rotation.multVec(App.Vector(0,-1,0)))
 right=App.Vector(0,0,1).cross(out);right.normalize()
 centers=[]
 for n in r['leaves']:
  o=d.getObject(n);p=o.getGlobalPlacement().multVec(App.Vector(float(o.Length)/2,float(o.Width)/2,float(o.Height)/2));p=App.Vector(7400-p.x,p.y,p.z);centers.append(p.dot(right))
 order=sorted(range(2),key=lambda i:centers[i]);sides={order[0]:'esquerda',order[1]:'direita'}
 move=reflected(m.getGlobalPlacement().Rotation.multVec(App.Vector(1,0,0))).dot(right)
 assert abs(move)>.99,'Orientação frontal não planar: não inferir sentido'
 title='Roupeiro' if r['module']=='Modulo' else 'Maleiro'
 for i in range(2):
  direction='direita' if move*(1 if i==0 else -1)>0 else 'esquerda';text=title+' — porta '+sides[i]+' — deslizar para '+direction
  label(r['controls'][i],text);label(r['drivers'][i],text+' — ferragens-gabarito R14');label(r['leaves'][i],text+' — frente proposta')
  sliding.append({'control':r['controls'][i],'driver':r['drivers'][i],'leaf':r['leaves'][i],'physical_side':sides[i],'slide_direction':direction,'basis':'Reflected module frontal normal, world up and projected leaf centers; source local translation signs preserved.'})
for i in range(20):
 m=d.getObject('Modulo'+('%03d'%i if i else ''))
 for o in m.Group:
  if not ('Shape' in o.PropertiesList and o.Visibility):continue
  if o.Label.startswith('Lateral esquerda'):label(o.Name,o.Label.replace('Lateral esquerda','Lateral direita',1))
  elif o.Label.startswith('Lateral direita'):label(o.Name,o.Label.replace('Lateral direita','Lateral esquerda',1))
d.Label='Guedala Park — R23 — espelhado / rótulos consistentes'
d.recompute()
for n,r in snapshot.items():
 o=d.getObject(n);assert (o.getParentGeoFeatureGroup().Name if o.getParentGeoFeatureGroup() else None)==r['parent']
 if r['placement'] is not None:assert max(abs(x-y) for x,y in zip(r['placement'],o.Placement.Matrix.A))<1e-9,n
 if r['expressions'] is not None:assert r['expressions']==[list(x) for x in o.ExpressionEngine],n
 if r['visibility'] is not None:assert o.Visibility==r['visibility'],n
assert not [o.Name for o in d.Objects if 'Invalid' in o.State]
assert hashlib.sha256(src.read_bytes()).hexdigest()==sha
d.save()
report={'file':str(dst),'source':str(src),'source_sha256':sha,'changes':changes,'sliding':sliding,'objects_compared':len(snapshot),'parents_placements_expressions_visibility_unchanged':True,'invalid':[],'scope':'Labels only; object names, controls, formulas, geometry and hardware preserved. Physical side labels refer to the mirrored apartment, not the source numbering.'}
((Path(__file__).resolve().parent / 'Rotulos_R23.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result={k:v for k,v in report.items() if k not in ['changes','sliding']};result['labels_changed']=len(changes)
