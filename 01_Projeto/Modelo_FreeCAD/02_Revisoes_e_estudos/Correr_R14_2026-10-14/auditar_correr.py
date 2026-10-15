from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
d=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R14_Correr_Simples.FCStd').resolve())
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R14.json').resolve()).read_text(encoding='utf-8'))
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def hit(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return a.common(b).Volume
def descendants(o):
 out=[]
 for q in getattr(o,'Group',[]):out.append(q);out+=descendants(q)
 return out
def visible(o,seen=None):
 seen=set() if seen is None else seen
 if o.Name.startswith('Ambiente_'):return True
 if o.Name in seen:return True
 seen.add(o.Name)
 if hasattr(o,'Visibility') and not o.Visibility:return False
 return all(visible(a,seen) for a in o.InList if a.TypeId in ['App::Part','App::DocumentObjectGroup'])
room=d.getObject('Modulo').InList[0]
moving=[];tracknames=[];drivers=[];inputs=[]
for row in data['rows']:
 moving += [d.getObject(n) for n in row['leaves']+row['moving']]
 tracknames+=row['tracks'];drivers += [d.getObject(n) for n in row['drivers']];inputs += [d.getObject(n) for n in row['controls']]
excluded={o.Name for o in moving}|set(tracknames)
obstacles=[o for o in descendants(room) if 'Shape' in o.PropertiesList and o.Shape.Volume>0 and o.Name not in excluded and visible(o)]
obstacles += list(d.getObject('ParedesInteiras').Group)
# R13 stored all current R04 solids hidden in the kitchen display; display state is
# not a valid reason to omit their geometry. Select the explicit current namespace,
# excluding boolean input boxes/cylinders, and the four current carcass results.
knowncorner=[o for o in descendants(d.getObject('CantoSimplesR04')) if 'Shape' in o.PropertiesList and o.Name.startswith(('FrenteSimples','FerragemSimples','ApoioPortaB','FaixaQuina'))]
knowncorner += [d.getObject(n) for n in ['PlacaL','PlacaL001','Peca255','Peca256','LateralApoioPrincipal']]
obstacles += knowncorner
obstacles=list({o.Name:o for o in obstacles}.values())
cached=[(o,shape(o)) for o in obstacles]
courses=[]
for row in data['rows']:
 for leafindex,cname in enumerate(row['controls']):
  control=d.getObject(cname)
  leafnames=set(o.Name for o in descendants(d.getObject(row['drivers'][leafindex])))
  own=[o for o in moving if o.Name in leafnames];other=[o for o in moving if o.Name not in leafnames]
  for pct in [0,.125,.25,.375,.5,.625,.75,.875,1]:
   for c in inputs:c.Deslocamento=0
   control.Deslocamento=pct*row['course'];d.recompute();hits=[]
   for o in own:
    a=shape(o)
    for q,b in cached+[(q,shape(q)) for q in other]:
     v=hit(a,b)
     if v>.1:hits.append({'moving':o.Name,'target':q.Name,'label':q.Label,'mm3':v})
   courses.append({'control':cname,'position_mm':float(control.Deslocamento),'hits':hits})
# The two planes are parallel. Check both sets together and access of changed wardrobe openings.
sim=[]
for pct in [.25,.5,1]:
 for row in data['rows']:
  for n in row['controls']:d.getObject(n).Deslocamento=pct*row['course']
 d.recompute();hits=[]
 for i,o in enumerate(moving):
  for q in moving[i+1:]:
   if o.getParentGeoFeatureGroup()==q.getParentGeoFeatureGroup():continue
   v=hit(shape(o),shape(q))
   if v>.1:hits.append({'pair':[o.Name,q.Name],'mm3':v})
 sim.append({'fraction':pct,'hits':hits})
access=[];wardrow=data['rows'][0]
for side,drawerNames,which in [('esquerda',['Gaveta','Gaveta001'],0),('direita',['Gaveta002','Gaveta003'],1)]:
 for c in inputs:c.Deslocamento=0
 d.getObject(wardrow['controls'][which]).Deslocamento=wardrow['course']
 for n in drawerNames:
  g=d.getObject(n)
  for pos in [0,100,200,300,400]:
   g.Extensao=pos;d.recompute();hits=[]
   for o in descendants(g):
    if 'Shape' not in o.PropertiesList or not visible(o) or o.Shape.Volume<=0:continue
    for q in moving+[d.getObject(n) for n in data['fixed']]:
     v=hit(shape(o),shape(q))
     if v>.1:hits.append({'moving':o.Name,'target':q.Name,'mm3':v})
   access.append({'side':side,'drawer':n,'extension_mm':pos,'hits':hits})
  g.Extensao=0
for c in inputs:c.Deslocamento=0
d.recompute()
fixedhits=[]
for n in data['fixed']:
 o=d.getObject(n)
 for q,b in cached:
  if q.Name in data['fixed']:continue
  v=hit(shape(o),b)
  if v>.1:fixedhits.append({'new':n,'target':q.Name,'label':q.Label,'mm3':v})
report={'courses':courses,'simultaneous':sim,'drawer_access':access,'fixed_hits':fixedhits,'targets':len(obstacles),'explicit_corner_targets':len(knowncorner),'invalid':[o.Name for o in moving+[d.getObject(n) for n in data['new']] if not o.Shape.isValid()], 'scope':'Somente mudanças R14; poses discretas de gabaritos hipotéticos, não hardware real/engrenamento/retenção/continuidade/tolerância/carga. Trilhos e contatos de guiamento excluídos das colisões, pois envelopes de seção/altura não são sólidos reais. Quatro gavetas apenas contra novas portas/apoios; não repetição da auditoria R08. R04 vigente selecionada por namespace, pois visibilidade de display herdada era falsa.'}
((Path(__file__).resolve().parent / 'Auditoria_R14.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');d.save()
result={'courses':len(courses),'course_hits':[r for r in courses if r['hits']],'simultaneous':sim,'drawer_positions':len(access),'drawer_hits':[r for r in access if r['hits']],'fixed_hits':fixedhits,'targets':len(obstacles),'invalid':report['invalid']}
