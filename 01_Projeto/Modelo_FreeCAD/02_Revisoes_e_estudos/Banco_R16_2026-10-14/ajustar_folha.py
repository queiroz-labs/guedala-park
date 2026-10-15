from pathlib import Path
import json,math
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve();data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R16.json').resolve()).read_text(encoding='utf-8'));assert 'leaf_remedy' not in data,'Correção já realizada'
d=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R16_Banco_Simples.FCStd').resolve())
row=data['lids'][3];c=d.getObject(row['control']);driver=d.getObject(row['driver']);lid=d.getObject(row['lid']);pad=d.getObject(row['cushion']);m=d.getObject(data['module'])
def worldshape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
before=[list(worldshape(o).BoundBox.getPoint(i)) for o in [lid,pad] for i in range(8)]
c.Abertura=0;d.recompute();p=driver.Placement;p.Base.z=420;driver.Placement=p;lid.Placement.Base.z=-20
driver.removeObject(pad);m.addObject(pad);pad.Placement=App.Placement(App.Vector(0,0,420),App.Rotation())
for field in ['ElevarAlmofada','DeslocamentoAlmofada']:c.addProperty('App::PropertyLength',field,'Estudo R16');setattr(c,field,0)
pad.setExpression('Placement.Base.z','420 mm + '+c.Name+'.ElevarAlmofada');pad.setExpression('Placement.Base.x',c.Name+'.DeslocamentoAlmofada')
c.Sequencia='PROPOSTA NOVA: elevar60, deslocar873 rumo ao sofá, baixar elevação50; almofada sobre os três setores fechados. Abrir tampa90; recuar folha24 e levantar. Não acessar outros setores enquanto a almofada ocupa seus assentos. Devolver em ordem inversa.'
driver.Label='Folha/aspirador/jogos - tampa fina/almofada removível, proposta nova';row['separate_cushion']=True;row['parking_source_v']=100;row['parking_shift_sign']=1
data['leaf_remedy']='Nova proposta funcional: almofada também removível no setor da folha, estacionada sobre os três setores fechados/v100–927/Z470; tampa20 ideal90. A folha800x350x70 recua24 antes de subir. Sem aceitar rotina/carga/pega automaticamente.'
data['proposals'][1]='Primeiro assento integral70 eixo448/470 ideal; outros três tampa20 eixo448/420 e almofada removível. Rotina do último setor é NOVA proposta para liberar folha, não aceite de09/10.'
d.recompute();after=[list(worldshape(o).BoundBox.getPoint(i)) for o in [lid,pad] for i in range(8)]
delta=max(abs(x-y) for aa,bb in zip(before,after) for x,y in zip(aa,bb))
def vol(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return a.common(b).Volume
external=[o for o in d.getObject('Ambiente_sala').Group if o.TypeId=='Part::Box']+list(d.getObject('ParedesInteiras').Group)
fixed=external+[d.getObject(n) for n in data['structure']+data['content']+data['panels']+data['ledges']+[data['containment'],data['leaf']]]
other=[d.getObject(r[n]) for r in data['lids'][:3] for n in ['lid','cushion']]
def sweep_bounds(b1,b2):
 mins=[min(getattr(b1,k+'Min'),getattr(b2,k+'Min')) for k in ['X','Y','Z']];maxs=[max(getattr(b1,k+'Max'),getattr(b2,k+'Max')) for k in ['X','Y','Z']]
 return Part.makeBox(*[hi-lo for lo,hi in zip(mins,maxs)],App.Vector(*mins))
parkNodes=[(0,0),(60,0),(60,873),(50,873)];park=[]
for start,end in zip(parkNodes,parkNodes[1:]):
 c.ElevarAlmofada,c.DeslocamentoAlmofada=start;d.recompute();b1=worldshape(pad).BoundBox;c.ElevarAlmofada,c.DeslocamentoAlmofada=end;d.recompute();swept=sweep_bounds(b1,worldshape(pad).BoundBox)
 hits=[]
 for q in fixed+other+[lid]:
  v=vol(swept,worldshape(q))
  if v>.1:hits.append({'target':q.Name,'mm3':v})
 park.append({'start':start,'end':end,'hits':hits})
poses=[]
for angle in [0,15,30,45,60,75,90]:
 c.Abertura=angle;d.recompute();hits=[]
 for q in fixed+other+[pad]:
  v=vol(worldshape(lid),worldshape(q))
  if v>.1:hits.append({'target':q.Name,'mm3':v})
 poses.append({'angle_deg':angle,'hits':hits})
leaf=d.getObject(data['leaf']);orig=leaf.Placement.copy();p=orig.Base;nodes=[p,App.Vector(p.x,p.y+24,p.z),App.Vector(p.x,p.y+24,970)];route=[]
for p1,p2 in zip(nodes,nodes[1:]):
 leaf.Placement.Base=p1;d.recompute();b1=worldshape(leaf).BoundBox;leaf.Placement.Base=p2;d.recompute();swept=sweep_bounds(b1,worldshape(leaf).BoundBox);hits=[]
 for q in fixed+other+[lid,pad]:
  if q==leaf:continue
  v=vol(swept,worldshape(q))
  if v>.1:hits.append({'target':q.Name,'mm3':v})
 route.append({'from':list(p1),'to':list(p2),'hits':hits})
leaf.Placement=orig;c.Abertura=0;c.ElevarAlmofada=0;c.DeslocamentoAlmofada=0;d.recompute();d.save()
report={'closed_lid_pad_bbox_delta_mm':delta,'new_last_cushion_continuous_route':park,'new_last_lid_poses':poses,'leaf_back24_then_lift':route,'nominal_aperture_depth_mm':378,'leaf_depth_mm':350,'leaf_to_table_and_open_lid_gap_mm':14,'parking_source_v_interval_mm':[100,927],'source_of_correction':'Complemento_R16: subida direta com assento70 bateu mesa; tampas finas nos outros setores já fazem parte da direção. Nova rotina no setor da folha é proposta, não aceite anterior. Não repetiu28 poses/13 percursos nem alterou tamanho da folha.','limits':'Caminho de gabarito rígido, não ferragem/estrutura/material/pega/manuseio/pessoa/folha real. Almofada bloqueia os três outros acessos enquanto estacionada; controlar sequência de uso.'}
((Path(__file__).resolve().parent / 'Folha_solucao_R16.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');((Path(__file__).resolve().parent / 'Montagem_R16.json').resolve()).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');result=report
