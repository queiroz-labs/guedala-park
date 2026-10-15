from pathlib import Path
import json,math
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R15.json').resolve()).read_text(encoding='utf-8'))
d=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R15_Cesto_Simples.FCStd').resolve())
c=d.getObject(data['control']);m=d.getObject(data['module']);driver=d.getObject(data['driver'])
if 'RetiradaConjunto' not in c.PropertiesList:c.addProperty('App::PropertyLength','RetiradaConjunto','Estudo R15')
c.RetiradaConjunto=0;driver.setExpression('Placement.Base.y','70 mm - '+c.Name+'.RetiradaConjunto')
c.Sequencia+='; manutenção ilustrativa: saco fora/conjunto sustentado e retenções liberadas, RetiradaConjunto0→400; não representa liberação mecânica validada.'
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def volume(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return a.common(b).Volume
room=next(o for o in m.InList if o.Name=='Ambiente_lavanderia')
targets=[o for o in room.Group if o.TypeId=='Part::Box' and not o.Label.startswith('Histórico oculto')]
targets+=[d.getObject(n) for n in ['Peca352','Peca353','Peca354']+data['fixed']+data['hydraulic']]
targets+=list(d.getObject('ParedesInteiras').Group)
for other in ['Modulo004','Modulo005','Modulo006','Modulo014']:
 targets += [o for o in d.getObject(other).Group if o.TypeId=='Part::Box']
targets=list({o.Name:o for o in targets}.values());cached=[(o,shape(o)) for o in targets]
objects=[d.getObject(n) for n in data['moving']];bag=d.getObject(data['bag']);frame=[d.getObject(n) for n in data['frame']]
def check(moving,exclude=None):
 hits=[];exclude=set() if exclude is None else exclude
 for o in moving:
  a=shape(o)
  for q,b in cached:
   if q.Name==o.Name or (o.CategoriaR15=='pino_gabarito' and q.CategoriaR15=='apoio_pivo_gabarito' if 'CategoriaR15' in q.PropertiesList else False) or q.Name in exclude:continue
   v=volume(a,b)
   if v>.1:hits.append({'moving':o.Name,'target':q.Name,'label':q.Label,'mm3':v})
 return hits
giro=[];c.RetiradaSaco=0;c.EndireitarSaco=0;c.RetiradaPainelSuperior=0
for angle in list(range(0,56,5))+[math.degrees(math.atan(250/450))]:
 c.Abertura=angle;d.recompute();hits=check(objects+[bag]);bagframe=[]
 for o in frame:
  v=volume(shape(bag),shape(o))
  if v>.1:bagframe.append({'pair':[bag.Name,o.Name],'mm3':v})
 bb=shape(d.getObject(data['front'])).BoundBox;fbbs=[shape(o).BoundBox for o in frame]
 giro.append({'angle_deg':angle,'hits':hits,'bag_frame_hits':bagframe,'front_floor_min_mm':bb.ZMin,'frame_max_height_mm':max(b.ZMax for b in fbbs)})
c.Abertura=55;c.RetiradaSaco=0;c.EndireitarSaco=0;withdrawal=[]
for distance in [0,100,200,300,400,445]:
 c.RetiradaSaco=distance;d.recompute();hits=check([bag]);framehits=[]
 for o in frame+[d.getObject(data['front'])]:
  v=volume(shape(bag),shape(o))
  if v>.1:framehits.append({'pair':[bag.Name,o.Name],'mm3':v})
 bb=shape(bag).BoundBox;withdrawal.append({'phase':'axial','distance_mm':distance,'hits':hits,'frame_hits':framehits,'bbox_world_mm':[bb.XMin,bb.XMax,bb.YMin,bb.YMax,bb.ZMin,bb.ZMax]})
for angle in [0,10,20,30,40,50,55]:
 c.EndireitarSaco=angle;d.recompute();hits=check([bag]);framehits=[]
 for o in frame+[d.getObject(data['front'])]:
  v=volume(shape(bag),shape(o))
  if v>.1:framehits.append({'pair':[bag.Name,o.Name],'mm3':v})
 bb=shape(bag).BoundBox;withdrawal.append({'phase':'upright','angle_deg':angle,'hits':hits,'frame_hits':framehits,'bbox_world_mm':[bb.XMin,bb.XMax,bb.YMin,bb.YMax,bb.ZMin,bb.ZMax]})
# Maintenance assumes daily bag already removed and all retaining fasteners safely released.
# It is a geometric path, not a tool-free release, weight handling or support demonstration.
bag.Visibility=False;maintenance=[];upper=d.getObject(data['upper'])
for dist in [0,50,100,200]:
 c.RetiradaPainelSuperior=dist;d.recompute();hits=check([upper])
 for o in objects:
  v=volume(shape(upper),shape(o))
  if v>.1:hits.append({'moving':upper.Name,'target':o.Name,'mm3':v})
 maintenance.append({'phase':'upper_panel','distance_mm':dist,'hits':hits})
c.RetiradaPainelSuperior=200
for dist in [0,100,200,300,400]:
 c.RetiradaConjunto=dist;d.recompute();maintenance.append({'phase':'released_frame','distance_mm':dist,'hits':check(objects,exclude={data['upper']})})
for field in ['Abertura','RetiradaSaco','EndireitarSaco','RetiradaPainelSuperior','RetiradaConjunto']:setattr(c,field,0)
bag.Visibility=True;bag.ViewObject.Transparency=65;d.recompute()
internal=[]
for i,o in enumerate(objects):
 if o.CategoriaR15=='pino_gabarito':continue
 for q in objects[i+1:]:
  if q.CategoriaR15=='pino_gabarito':continue
  v=volume(shape(o),shape(q))
  if v>.1:internal.append({'pair':[o.Name,q.Name],'mm3':v})
frontVol=d.getObject(data['front']).Shape.Volume
report={'giro':giro,'bag_withdrawal':withdrawal,'maintenance':maintenance,'internal_hits_except_pins':internal,'targets':len(targets),'invalid':[o.Name for o in objects+[bag]+[d.getObject(n) for n in data['new']] if not o.Shape.isValid()], 'front_wood_volume_mm3':frontVol,'front_panel_mass750_kg':frontVol*750/1e9,'front_panel_mass900_kg':frontVol*900/1e9,'scope':'Giro de armação/frontais/gabaritos R15 e retirada13poses de corpo400x200x400. Não repetir prova2D5501/1442; novo CAD3D. Pinos idealizados/apoios são reservas, interpenetração de montagem excluída; não ferragem, carga, retenção55, deformação, mãos/pessoa/alças, hidráulica real, apoio/remoção física. Tanque/vazios/reservas condicionaisR08, não levantamento.'}
((Path(__file__).resolve().parent / 'Auditoria_R15.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');data['maintenance_controls']=['RetiradaPainelSuperior','RetiradaConjunto'];((Path(__file__).resolve().parent / 'Montagem_R15.json').resolve()).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');d.save()
result={'giro_positions':len(giro),'giro_hits':[r for r in giro if r['hits'] or r['bag_frame_hits']],'withdrawal_positions':len(withdrawal),'withdrawal_hits':[r for r in withdrawal if r['hits'] or r['frame_hits']],'maintenance':maintenance,'internal_hits':internal,'targets':len(targets),'invalid':report['invalid']}
