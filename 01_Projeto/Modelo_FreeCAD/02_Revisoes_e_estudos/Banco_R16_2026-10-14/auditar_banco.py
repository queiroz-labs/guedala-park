from pathlib import Path
import json,math
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve();data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R16.json').resolve()).read_text(encoding='utf-8'))
d=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R16_Banco_Simples.FCStd').resolve());m=d.getObject(data['module'])
a=json.loads(Path(data['source_files'][0]).read_text(encoding='utf-8'));detail=json.loads(Path(data['source_files'][1]).read_text(encoding='utf-8'))
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def volume(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return a.common(b).Volume
def reset():
 for row in data['lids']:
  c=d.getObject(row['control']);c.Abertura=0
  if row['separate_cushion']:c.ElevarAlmofada=0;c.DeslocamentoAlmofada=0
 d.recompute()
def parked(row):
 c=d.getObject(row['control']);c.ElevarAlmofada=50;c.DeslocamentoAlmofada=row['parking_source_v']-row['pad_v']
def hits(o,targets):
 out=[];s=shape(o)
 for q in targets:
  if q==o:continue
  v=volume(s,shape(q))
  if v>.1:out.append({'moving':o.Name,'target':q.Name,'label':q.Label,'mm3':v})
 return out
room=d.getObject('Ambiente_sala')
external=[o for o in room.Group if o.TypeId=='Part::Box']+list(d.getObject('ParedesInteiras').Group)
external=list({o.Name:o for o in external}.values())
structure=[d.getObject(n) for n in data['structure']]
program=[d.getObject(n) for n in data['content']+data['panels']+data['ledges']+[data['containment'],data['leaf']]]
lids=[d.getObject(row['lid']) for row in data['lids']];pads=[d.getObject(row['cushion']) for row in data['lids']]
reset();internal=[]
solid=structure+program+lids+pads
for i,o in enumerate(solid):
 for q in solid[i+1:]:
  v=volume(shape(o),shape(q))
  if v>.1:internal.append({'pair':[o.Name,q.Name],'labels':[o.Label,q.Label],'mm3':v})
bearing=[]
for row in data['lids']:
 o=d.getObject(row['lid']);s=shape(o);bottom=next(f for f in s.Faces if f.normalAt(0,0).z<-.99 and abs(f.CenterOfMass.z-400)<1e-5)
 contacts=[]
 for q in structure:
  area=bottom.common(shape(q)).Area
  if area>.1:contacts.append({'support':q.Name,'label':q.Label,'area_mm2':area})
 bearing.append({'lid':o.Name,'contacts':contacts,'total_area_mm2':sum(x['area_mm2'] for x in contacts)})
positions=[];cushionRoutes=[]
for row in data['lids']:
 reset();c=d.getObject(row['control']);lid=d.getObject(row['lid']);pad=d.getObject(row['cushion'])
 if row['separate_cushion']:
  # Native v reflection: travel towards kitchen is negative localX.
  stops=[(0,0),(60,0),(60,row['parking_source_v']-row['pad_v']),(50,row['parking_source_v']-row['pad_v'])]
  orig=pad.Placement.Base
  for j,(lift,shift) in enumerate(stops):
   c.ElevarAlmofada=lift;c.DeslocamentoAlmofada=shift;d.recompute();h=hits(pad,external+structure+program+lids+[q for q in pads if q!=pad])
   cushionRoutes.append({'sector':row['id'],'lift_mm':lift,'shift_mm':shift,'hits':h})
  parked(row)
 for angle in [0,15,30,45,60,75,90]:
  c.Abertura=angle;d.recompute();moving=[lid] if row['separate_cushion'] else [lid,pad];other=[q for q in lids+pads if q not in moving]
  h=[e for o in moving for e in hits(o,external+structure+program+other)]
  positions.append({'sector':row['id'],'angle_deg':angle,'hits':h})
reset()
for row in data['lids'][1:3]:parked(row);d.getObject(row['control']).Abertura=90
d.recompute();sim=[e for o in lids+pads for e in hits(o,external+structure+program+[q for q in lids+pads if q!=o])]
# Axis-aligned source box segments become exact swept prisms in native world axes.
# This is geometric continuous translation of fixed-orientation envelopes, not physical handling.
def nodepos(node):
 return App.Vector(1800-10*(node['y']+node['d']),10*node['x'],10*node['z'])
def sweep(o,p1,p2):
 assert sum(abs(getattr(p1,k)-getattr(p2,k))>1e-6 for k in ['x','y','z'])<=1
 pl=o.Placement;o.Placement.Base=p1;d.recompute();b1=shape(o).BoundBox;o.Placement.Base=p2;d.recompute();b2=shape(o).BoundBox
 low=[min(getattr(b1,k+'Min'),getattr(b2,k+'Min')) for k in ['X','Y','Z']];high=[max(getattr(b1,k+'Max'),getattr(b2,k+'Max')) for k in ['X','Y','Z']]
 return Part.makeBox(*[hi-lo for lo,hi in zip(low,high)],App.Vector(*low))
allContent=[d.getObject(n) for n in data['content']+data['panels']];original={o.Name:o.Placement.copy() for o in allContent}
routes=[]
def route(obj,nodes,targets,label):
 segs=[]
 for p1,p2 in zip(nodes,nodes[1:]):
  swept=sweep(obj,p1,p2);h=[]
  for q in targets:
   if q==obj:continue
   v=volume(swept,shape(q))
   if v>.1:h.append({'target':q.Name,'label':q.Label,'mm3':v})
  segs.append({'from_mm':list(p1),'to_mm':list(p2),'hits':h})
 routes.append({'item':label,'name':obj.Name,'segments':segs})
fixed=external+structure+[d.getObject(n) for n in data['ledges']+[data['containment'],data['leaf']]]
for r in detail['middleAlternative']['independentDrinks']:
 reset();row=data['lids'][1];parked(row);d.getObject(row['control']).Abertura=90;d.recompute();o=d.getObject(data['objects'][r['id']])
 route(o,[nodepos(n) for n in r['nodes']],fixed+lids+pads+[q for q in allContent if q!=o],r['id']);o.Placement=original[o.Name]
reset();row=data['lids'][2];parked(row);d.getObject(row['control']).Abertura=90;d.recompute();o=d.getObject(data['objects']['Balde 8 L'])
route(o,[nodepos(n) for n in detail['bucket']['nodes']],fixed+lids+pads+[q for q in allContent if q!=o],'Balde 8 L');o.Placement=original[o.Name]
# Clean compartment in source order: pots, then empty removable panels, then lower groups.
reset();d.getObject(data['lids'][0]['control']).Abertura=90;d.recompute();removed=set()
clean=a['pots']+detail['supports']['boards']+a['lower'][:2]
for r in clean:
 o=d.getObject(data['objects'][r['id']]);p=o.Placement.Base;z=366 if r['id'].startswith('Pote') else 310 if r['id'].startswith('Painel') else 213 if r['id']=='Travessas' else p.z
 nodes=[p,App.Vector(p.x,p.y,z),App.Vector(p.x,80,z),App.Vector(p.x,80,970)]
 route(o,nodes,fixed+lids+pads+[q for q in allContent if q.Name not in removed and q!=o],r['id']);removed.add(o.Name)
for o in allContent:o.Placement=original[o.Name]
reset();d.recompute();d.save()
report={'closed_internal_hits':internal,'bearing_geometry':bearing,'lid_positions':positions,'cushion_nodes':cushionRoutes,'two_daily_sectors_open_hits':sim,'content_routes':routes,'fixed_external_targets':len(external),'invalid':[o.Name for o in solid if not o.Shape.isValid()], 'limits':'Somente banco R16, programa de envelopes propostos/importados. Novos suportes e tampas, sentidos/ordem longitudinal corrigidos. Contato de apoio não comprova resistência; giro de eixos ideais sem ferragem/retencão. Translações de conteúdo por envoltórias, não mão/pega/alças/produtos reais. Almofadas: nós apenas; varredura entre nós a conferir separadamente. Não repete901 poses2D nem testes antigos do apartamento.'}
((Path(__file__).resolve().parent / 'Auditoria_R16.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result={'internal':internal,'lid_positions':len(positions),'lid_hits':[r for r in positions if r['hits']],'cushion_node_hits':[r for r in cushionRoutes if r['hits']],'simultaneous_hits':sim,'content_routes':len(routes),'route_hits':[r for r in routes if any(s['hits'] for s in r['segments'])],'bearing':bearing,'invalid':report['invalid']}
