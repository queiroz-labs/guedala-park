"""Detalhe nominal e varredura externa P03; sem FreeCAD ou alteracao do modelo.

Reusa quatro barras nativas71B3550 da R04/R11/R18. Requer NumPy/Pillow.
Nao comprova capacidade de ferragem, parafuso, chapa ou margem continua.
"""
from pathlib import Path
import hashlib,itertools,json,math,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/P03'
D=json.loads((ROOT/'04_Moveis/Proximas_decisoes/P01_P03/Geometria_P02_individual.json').read_text(encoding='utf-8'))
S=ROOT/'04_Moveis/Proximas_decisoes/Cinematica/Snapshot_R52.json'
sys.path.insert(0,str(ROOT/'ferramentas/cinematica'))
from cinematica import Engine
E=Engine(S)
LEGACY=ROOT/'02_Modelo_3D/Componentes/Estudos/Portas_opostas_R18_2026-10-14'
L=json.loads((LEGACY/'Dados_plano_R18.json').read_text(encoding='utf-8'))
AX=json.loads((ROOT/'02_Modelo_3D/Componentes/Estudos/Apoios_R11_2026-10-14/Eixos_71B3550.json').read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(ROOT/D['source'])==D['source_sha256']
a,b,c,d=[np.array(AX[k],float) for k in ['a','b','c','d']]
angles=np.arange(0,86.0001,.5)

def circle(A,B,r1,r2,sign):
 v=B-A;dd=np.linalg.norm(v);ll=(r1*r1-r2*r2+dd*dd)/(2*dd)
 return A+ll*v/dd+sign*math.sqrt(max(0,r1*r1-ll*ll))*np.array([-v[1],v[0]])/dd
sg=min([-1,1],key=lambda s:np.linalg.norm(circle(a,b-d+c,np.linalg.norm(a-c),np.linalg.norm(b-d),s)-c))
def polygons(row,aa=angles):
 mm=np.array(row['module_matrix']);origin=np.array([row['hinge_support_inner_x_mm'],row.get('hinge_origin_y_mm',56.5)])
 start=np.array(row['closed_leaf_base'][:2]);bb=row['front_local_box']
 rect=np.array([[bb[0],0],[bb[3],0],[bb[3],bb[4]],[bb[0],bb[4]]]);items=[]
 for ang in aa:
  th=-math.radians(ang);R=np.array([[math.cos(th),-math.sin(th)],[math.sin(th),math.cos(th)]])
  cp=circle(a,b-R@(d-c),np.linalg.norm(a-c),np.linalg.norm(b-d),sg);trans=cp-R@c
  phi=th if row['side']=='left' else -th;rr=np.array([[math.cos(phi),-math.sin(phi)],[math.sin(phi),math.cos(phi)]])
  shift=np.array([-trans[0] if row['side']=='left' else trans[0],-trans[1]])
  items.append((rect@rr.T+origin+shift+rr@(start-origin))@mm[:2,:2].T+mm[:2,3])
 return np.array(items)
def normals(pp):
 ed=np.roll(pp,-1,axis=-2)-pp
 nn=np.stack([-ed[...,1],ed[...,0]],axis=-1)
 return nn/np.linalg.norm(nn,axis=-1)[...,None]
def separations(A,B):
 na,nb=normals(A)[:,:2],normals(B)[:,:2]
 aa=np.einsum('aek,avk->aev',na,A);ba=np.einsum('aek,bvk->abev',na,B)
 bb=np.einsum('bek,bvk->bev',nb,B);ab=np.einsum('bek,avk->abev',nb,A)
 ga=np.maximum(aa.min(2)[:,None,:]-ba.max(3),ba.min(3)-aa.max(2)[:,None,:])
 gb=np.maximum(bb.min(2)[None,:,:]-ab.max(3),ab.min(3)-bb.max(2)[None,:,:])
 return np.maximum(ga.max(2),gb.max(2))
def rect(bounds):
 x,y,z,X,Y,Z=bounds
 return np.array([[x,y],[X,y],[X,Y],[x,Y]])

# Valida a implementacao contra as seis poses do canto da extracao nativa R18.
hm=np.array(next(r['module_matrix'] for r in L['rows'] if r['module']=='Modulo003'))
cm=np.eye(4);cm[:2,:2]=[[0,1],[-1,0]];cm[:2,3]=[2200,-126]
corner_rows=[dict(door='PainelSimplesR001',side='left',module_matrix=hm.tolist(),hinge_support_inner_x_mm=1818,closed_leaf_base=[1803,0,1],front_local_box=[0,0,0,271,18,306]),
 dict(door='PainelSimplesR04',side='right',module_matrix=(hm@cm).tolist(),hinge_support_inner_x_mm=256,closed_leaf_base=[271,0,1],front_local_box=[-271,0,0,0,18,306])]
native_errors=[]
for angle in [0,30,86]:
 native=json.loads((LEGACY/f'Pose_{angle}_R18.json').read_text(encoding='utf-8'))
 refs={q['name']:np.array(q['points_world'])[:,:2] for q in native['corner_fronts']}
 for row in corner_rows:
  pp=polygons(row,[angle])[0];ref=refs[row['door']]
  err=max(np.linalg.norm(pp[:,None]-ref[None,:],axis=2).min(0));assert err<1e-6
  native_errors.append(float(err))
# R20 espelhou globalX; os referenciais locais dos modulos foram depois
# consolidados, portanto nao inferir o espelhamento pela matriz do grupo P04.
# Determinar a translacao pela propria frenteA e conferir ambas as caixas0.
old_a=polygons(corner_rows[1],[0])[0]
T=np.eye(4);T[0,0]=-1
T[0,3]=float(old_a[:,0].max()+D['panels']['FrenteSimplesR04']['bbox_mm'][0])
neighbors={}
for row,name in zip(corner_rows,['FrenteSimplesR001','FrenteSimplesR04']):
 r=dict(row,module_matrix=(T@np.array(row['module_matrix'])).tolist());pp=polygons(r)
 bb=D['panels'][name]['bbox_mm'];actual=[*pp[0].min(0),*pp[0].max(0)]
 assert np.max(np.abs(np.array(actual)-np.array([bb[0],bb[1],bb[3],bb[4]])))<1e-6,(name,actual,bb)
 neighbors[name]=pp
for leaf,w in [('Folha',439.75),('Folha001',439.75),('Folha002',440.25),('VizinhaComumR18',441.75)]:
 neg=E.data['leaves'][leaf]['fronts'][0]['leaf_local_center_mm'][0]<0
 xx=[-w,0] if neg else [0,w]
 pts=np.array([[xx[0],0,0,1],[xx[1],0,0,1],[xx[1],18,0,1],[xx[0],18,0,1]])
 neighbors[leaf]=np.array([(pts@E.placement(leaf,float(ang)).T)[:,:2] for ang in angles])

def main():
 mm=np.eye(4);mm[2,3]=2132
 rows=[dict(door='P03_esquerda',side='left',module_matrix=mm.tolist(),hinge_support_inner_x_mm=5408,
     hinge_origin_y_mm=3346.5,closed_leaf_base=[5392,3290,1],front_local_box=[0,0,0,672,18,306]),
  dict(door='P03_direita',side='right',module_matrix=mm.tolist(),hinge_support_inner_x_mm=6722,
     hinge_origin_y_mm=3346.5,closed_leaf_base=[6738,3290,1],front_local_box=[-672,0,0,0,18,306])]
 polys={r['door']:polygons(r) for r in rows}
 pairs=[]
 for name,pp in polys.items():
  for other,qq in neighbors.items():
   sep=separations(pp,qq);hit=np.argwhere(sep<-1e-6)
   pairs.append(dict(a=name,b=other,independent_angle_pairs=int(sep.size),minimum_axis_gap_mm=float(sep.min()),
       intersections=len(hit),first_angles_deg=[[float(angles[i]),float(angles[j])] for i,j in hit[:5]]))
 sep=separations(*polys.values());hit=np.argwhere(sep<-1e-6)
 pairs.append(dict(a=rows[0]['door'],b=rows[1]['door'],independent_angle_pairs=int(sep.size),
  minimum_axis_gap_mm=float(sep.min()),intersections=len(hit),first_angles_deg=[[float(angles[i]),float(angles[j])] for i,j in hit[:5]]))

 static_results=[]
 for recess in [0,20]:
  hits=[];bounds={n:list(r['bbox_mm']) for n,r in D['panels'].items() if not r['door']}
  if recess:
   for n in ['Peca259','Peca260','Peca262','Peca263']:bounds[n][1]+=recess
  for name,pp in polys.items():
   for n,bb in bounds.items():
    if min(2439,bb[5])<=max(2133,bb[2])+1e-6:continue
    ss=separations(pp,rect(bb)[None,:])[:,0];idx=np.flatnonzero(ss<-1e-6)
    if len(idx):hits.append(dict(door=name,target=n,poses_hit=len(idx),minimum_axis_gap_mm=float(ss.min()),
       first_angles_deg=[float(angles[i]) for i in idx[:5]]))
  static_results.append(dict(recess_body_front_mm=recess,static_hits=hits,
     new_side_depth_mm=650-recess,new_base_top_depth_mm=632-recess,
     storage_internal_mm=[1314,632-recess,272]))

 # Insercao reta em86: malas centralizadas, sem depender de vao lateral estreito.
 bags=[];paths=[]
 for i,x in enumerate([5505.,6075.]):
  final=[x,3410.,2150.,x+550,3760.,2400.];bad=[]
  for y in np.arange(2550,3410.001,5.):
   pp=rect([x,y,2150,x+550,y+350,2400.])
   for name,pol in polys.items():
    if separations(pp[None,:],pol[-1:])[0,0]<-1e-6:bad.append(dict(y_mm=float(y),door=name))
  bags.append(dict(id=i+1,bbox_mm=final));paths.append(dict(bag=i+1,step_mm=5.,start_y_mm=2550.,end_y_mm=3410.,front_hits=bad))
 assert not any(p['front_hits'] for p in paths)
 drill=[]
 for side,x in [('esquerda',5414.5),('direita',6715.5)]:
  for z in [2212.,2360.]:
   drill.append(dict(leaf=side,cup_center_mm=[x,3308.,z],cup_diameter_mm=35.,cup_depth_mm=13.,
       nominal_front_skin_mm=5.,K_mm=5.,plate_setback_from_new_side_front_mm=37.,
       plate_hole_row_y_mm=3347.,screw_family='609.1500 3.5x15; piloto depende da chapa',
       status='ESTUDO de geometria; quantidade e aplicacao em672 de largura nao confirmadas'))
 volume=672*306*18-2*math.pi*17.5**2*13
 weight=volume*900/1e9
 load=dict(wood_mass_at_hypothetical_density900_kg=weight,hypothetical_finished_door_kg=4.,hinge_spacing_mm=148.,
     vertical_group_N=4*9.80665,gravity_moment_at_336mm_Nm=4*9.80665*.336,
     equivalent_148mm_force_pair_N=4*9.80665*.336/.148,
     note='Demandas do grupo, nao capacidades ou forca por parafuso; nao divide peso por dois como homologacao.')
 report=dict(source_sha256=D['source_sha256'],source_unchanged=sha(ROOT/D['source'])==D['source_sha256'],
     leaf_dimensions_mm=[672,306,18],outer_gaps_mm=dict(sides=2,center=2,top_bottom=1),
     closed_bboxes_mm={name:[*pp[0].min(0),*pp[0].max(0)] for name,pp in polys.items()},
     angle_step_deg=.5,angles_each=len(angles),legacy_native_validation_max_error_mm=max(native_errors),
     planar_pairs=pairs,static_variants=static_results,bag_entry_fronts_only=paths,bag_final_positions=bags,
     drilling_nominal=drill,door_group_load=load,
     manufacturer_condition=dict(url='https://ea.blum.com/en/number-of-hinges/',chart_door_width_limit_mm=600,
         extra_hinge_guidance_up_to_width_mm=650,principle_height_greater_than_width=True,
         proposed_door_width_mm=672,quantity_approved=False),
     integration_gate='NAO_ATENDIDO: fabricante nao confirma quantidade/aplicacao672; fixacoes, corpos de ferragem e base de comparacao pendentes.',
     limitations=['SAT de envoltorias retangulares e amostrado, nao margem continua.',
         'Seis vizinhas moveis e22paineis selecionados; nao e auditoria de todas as formas da R52.',
         'Nao varre STEP das dobradicas nem verifica ancoragem, parafusos, resistencia, deformacao ou espaco da mao.',
         'Insercao verifica somente as duas frentes abertas86, sem demais ferragens/pessoas/tolerancias.',
         'Recuo20 alteraria quatro madeiras e seus apoios: nao e troca apenas de portas.',
         'Modelo principal nao aberto no FreeCAD nem alterado.'])
 (OUT/'Detalhamento_portas.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 im=Image.new('RGB',(1800,1150),'white');dr=ImageDraw.Draw(im)
 def f(s,b=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),s)
 def tx(x,y,t,s=23,b=False,c='#233d4d'):dr.text((x,y),t,font=f(s,b),fill=c)
 tx(55,30,'P03 — detalhe nominal de duas portas de abrir',36,True)
 tx(55,85,'Proposta em conferência • 672 × 306 × 18 mm por folha • sem montante central',25)
 sx=.94;ox=100;oy=210
 for x in [0,674]:
  dr.rectangle([ox+x*sx,oy,ox+(x+672)*sx,oy+306*sx],fill='#d3ba91',outline='#354f61',width=3)
 for x in [22.5,1323.5]:
  for z in [79,227]:
   X=ox+x*sx;Y=oy+(306-z)*sx;r=17.5*sx
   dr.ellipse([X-r,Y-r,X+r,Y+r],fill='#edf0ed',outline='#38596a',width=2)
 tx(ox+170,oy+110,'Porta esquerda',28,True);tx(ox+805,oy+110,'Porta direita',28,True)
 tx(100,540,'Canecos Ø35 × 13 • K5 • centros a 79/227 mm da base da folha',26,True)
 tx(100,585,'Entre dobradiças: 148 mm • sobram 5 mm na face do painel de 18 mm.',24)
 tx(100,635,'Calços: linha de furação 37 mm atrás da nova frente da lateral.',24)
 tx(100,700,'Para preservar a profundidade externa de 650 mm:',28,True)
 tx(100,746,'recuar 20 mm nas laterais, base e topo; frentes ocupam 18 + folga de 2 mm.',24)
 tx(100,791,'Laterais: 650 → 630; base/topo: 632 → 612. Isso muda apoios e massas.',24)
 tx(100,864,'PENDÊNCIA QUE IMPEDE APLICAÇÃO',27,True,c='#a33e2c')
 tx(100,909,'Guia: até 600 mm; até 650 com dobradiça extra. A proposta tem 672 mm.',24,c='#a33e2c')
 tx(100,953,'É preciso confirmar o grupo de dobradiças para a folha de 672 × 306 mm.',24,c='#a33e2c')
 tx(100,1040,'Dimensões nominais para consulta técnica, não gabarito de usinagem ou liberação de carga.',22)
 im.save(OUT/'Detalhamento_portas.png')
 print(json.dumps(dict(pair_hits=sum(p['intersections'] for p in pairs),static=[dict(recess=v['recess_body_front_mm'],hits=len(v['static_hits'])) for v in static_results],
     native_error_mm=max(native_errors),entry_front_hits=sum(len(p['front_hits']) for p in paths),gate=report['integration_gate']),ensure_ascii=False))


if __name__=='__main__':
 main()
