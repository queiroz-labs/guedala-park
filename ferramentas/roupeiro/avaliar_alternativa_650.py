"""Compara duas folhas672 com650, sem alterar CAD. Requer NumPy/Pillow.

Reutiliza o mecanismo do detalhamento e acrescenta caminho nominal ate P01.
Os resultados nao homologam ferragens, fixacoes, rigidez ou carga de uso.
"""
from pathlib import Path
import hashlib,itertools,json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import detalhar_portas_maleiro as base

ROOT=base.ROOT;OUT=base.OUT;D=base.D;G=9.80665
mm=np.eye(4);mm[2,3]=2132
def doors(width):
 if width==672:
  start,finish,origins=5392.,6738.,[5408.,6722.]
 else:
  # Liner18 + calco3: recobrimento nominal13 comK5, confirmado na tabela.
  start,finish,origins=5413.,6717.,[5426.+3,6704.-3]
 return [dict(door='esquerda',side='left',module_matrix=mm.tolist(),hinge_support_inner_x_mm=origins[0],hinge_origin_y_mm=3346.5,closed_leaf_base=[start,3290,1],front_local_box=[0,0,0,width,18,306]),
  dict(door='direita',side='right',module_matrix=mm.tolist(),hinge_support_inner_x_mm=origins[1],hinge_origin_y_mm=3346.5,closed_leaf_base=[finish,3290,1],front_local_box=[-width,0,0,0,18,306])]
def rectangle_record(bb):
 vol=math.prod(bb[i+3]-bb[i] for i in range(3))
 return dict(bbox_mm=bb,volume_mm3=vol,com_mm=[(bb[i]+bb[i+3])/2 for i in range(3)])
def body_records(width):
 out={n:dict(r,bbox_mm=list(r['bbox_mm'])) for n,r in D['panels'].items() if r['module']=='P03' and not r['door']}
 for n in ['Peca259','Peca260','Peca262','Peca263']:
  bb=out[n]['bbox_mm'];bb[1]+=20;out[n]=dict(out[n],**rectangle_record(bb))
 if width==650:
  for n,bb in [('Liner_esquerdo',[5408,3310,2150,5426,3922,2422]),('Liner_direito',[6704,3310,2150,6722,3922,2422]),
   ('Faixa_esquerda',[5392,3290,2133,5410,3308,2439]),('Faixa_direita',[6720,3290,2133,6738,3308,2439])]:out[n]=rectangle_record(bb)
 return out
def cut_points():
 out=[]
 for face in D['variants']['atual_R52']['contacts']:
  a,b=face['a'],face['b']
  if face['axis']!=2 or abs(face['center_mm'][2]-2132)>1e-6:continue
  mods={D['panels'][a]['module'],D['panels'][b]['module']}
  if mods!={'P01','P03'}:continue
  lower=a if D['panels'][a]['module']=='P01' else b
  bb=list(face['bbox_mm']);bb[1]=max(bb[1],3310.)
  for x,y in itertools.product([bb[0],bb[3]],[bb[1],bb[4]]):out.append(dict(lower=lower,point_mm=[x,y,2132.]))
 return out
pts=cut_points();A=np.array([[1.,(p['point_mm'][0]-6065)/1000,(p['point_mm'][1]-3310)/1000] for p in pts]).T
triples=[];invs=[]
for ix in itertools.combinations(range(len(pts)),3):
 if abs(np.linalg.det(A[:,ix]))>1e-11:triples.append(ix);invs.append(np.linalg.inv(A[:,ix]))
triples=np.array(triples);invs=np.array(invs)
def compression_cut(loads):
 mass=sum(m for m,c in loads);cg=sum((m*np.array(c) for m,c in loads),np.zeros(3))/mass
 rhs=mass*G*np.array([1.,(cg[0]-6065)/1000,(cg[1]-3310)/1000])
 rr=np.einsum('kij,j->ki',invs,rhs);ok=np.min(rr,axis=1)>=-1e-7
 if not np.any(ok):return dict(feasible=False,mass_kg=mass,cg_mm=cg.tolist())
 rr=rr[ok];tt=triples[ok];env={}
 for n in sorted({p['lower'] for p in pts}):
  mask=np.array([p['lower']==n for p in pts]);values=np.sum(rr*mask[tt],axis=1)
  env[n]=dict(min_N=float(values.min()),max_N=float(values.max()))
 witness=[dict(**pts[int(k)],force_z_N=float(v)) for k,v in zip(tt[0],rr[0])]
 # Conferencia do certificado por soma direta, sem usar a matriz inversa.
 ff=sum(p['force_z_N'] for p in witness)
 mx=sum((p['point_mm'][1]-3310)*p['force_z_N'] for p in witness)
 my=sum((p['point_mm'][0]-6065)*p['force_z_N'] for p in witness)
 assert abs(ff-mass*G)<1e-6 and abs(mx-mass*G*(cg[1]-3310))<1e-5 and abs(my-mass*G*(cg[0]-6065))<1e-5
 return dict(feasible=True,mass_kg=mass,cg_mm=cg.tolist(),receivers=env,witness=witness)

variants=[];all_cases=[]
for width in [672,650]:
 rows=doors(width);pp={r['door']:base.polygons(r) for r in rows};parts=body_records(width)
 pair_results=[]
 for n,pol in pp.items():
  for name,neighbor in base.neighbors.items():
   ss=base.separations(pol,neighbor);hit=np.argwhere(ss<-1e-6)
   pair_results.append(dict(pair=[n,name],intersections=len(hit),minimum_axis_gap_mm=float(ss.min())))
 ss=base.separations(*pp.values());pair_results.append(dict(pair=['esquerda','direita'],intersections=int(np.sum(ss<-1e-6)),minimum_axis_gap_mm=float(ss.min())))
 stationary={n:list(r['bbox_mm']) for n,r in D['panels'].items() if not r['door'] and r['module']!='P03'}
 stationary.update({n:r['bbox_mm'] for n,r in parts.items()})
 hits=[]
 for n,pol in pp.items():
  for target,bb in stationary.items():
   if min(2439,bb[5])<=max(2133,bb[2])+1e-6:continue
   ss=base.separations(pol,base.rect(bb)[None,:])[:,0];ii=np.flatnonzero(ss<-1e-6)
   if len(ii):hits.append(dict(door=n,target=target,poses=len(ii),first_angle_deg=float(base.angles[ii[0]])))
 paths=[]
 for x in [5505.,6075.]:
  collisions=[]
  for y in np.arange(2550,3410.001,5.):
   bag=base.rect([x,y,2150,x+550,y+350,2400])[None,:]
   for n,pol in pp.items():
    if base.separations(bag,pol[-1:])[0,0]<-1e-6:collisions.append(dict(y_mm=float(y),obstacle=n))
   for n,bb in stationary.items():
    if min(2400,bb[5])<=max(2150,bb[2])+1e-6:continue
    if base.separations(bag,base.rect(bb)[None,:])[0,0]<-1e-6:collisions.append(dict(y_mm=float(y),obstacle=n))
  paths.append(dict(x_mm=x,collisions=collisions))
 for rho,kg,pose in itertools.product([650,800,900],[0,20,30],['fechadas','esquerda86','direita86','ambas86']):
  aa=[86 if pose in ['esquerda86','ambas86'] else 0,86 if pose in ['direita86','ambas86'] else 0]
  loads=[(r['volume_mm3']*rho/1e9,r['com_mm']) for r in parts.values()]
  for row,angle in zip(rows,aa):
   center=base.polygons(row,[angle])[0].mean(0)
   loads.append((4.,[float(center[0]),float(center[1]),2286.]))
  loads.append((kg,[6065.,3585. if kg!=30 else 3617.,2275.]))
  all_cases.append(dict(width_mm=width,density_hypothesis_kg_m3=rho,finished_each_door_hypothesis_kg=4.,content_total_kg=kg,pose=pose,
   loads=[dict(mass_kg=m,center_mm=list(c)) for m,c in loads],cut=compression_cut(loads)))
 spacing=148 if width==672 else 202
 variants.append(dict(width_mm=width,door_count=2,hinges_each=2 if width==672 else 3,
  plate='173H7100' if width==672 else'173H7130',plate_spacing_mm=0 if width==672 else 3,
  overlay_mm=16 if width==672 else 13,K_mm=5,
  hinges_z_from_leaf_bottom_mm=[79,227] if width==672 else[52,153,254],
  max_hinge_spacing_mm=spacing,extra_parts={n:r for n,r in parts.items() if n.startswith(('Liner','Faixa'))},
  wood_mass_without_moving_leaves_at800_kg=sum(r['volume_mm3']*800/1e9 for r in parts.values()),
  opening_between_liners_mm=1314 if width==672 else 1278,
  pair_results=pair_results,static_hits=hits,bag_paths=paths,
  finished_door4kg_group=dict(vertical_N=4*G,gravity_moment_Nm=4*G*width/2000,
   equivalent_pair_N=4*G*(width/2)/spacing,
   note='Momento total do grupo; nao distribuir por tres fixadores sem compatibilidade.'),
  application_confirmed=False))
assert len(all_cases)==72 and all(c['cut']['feasible'] for c in all_cases)
assert all(not v['static_hits'] and all(p['intersections']==0 for p in v['pair_results']) and all(not p['collisions'] for p in v['bag_paths']) for v in variants)

# Requisito da nova ligacao liner-lateral: nao creditar apoio do liner na base.
# Peso proprio e porta inteira sao transmitidos pela face, como caso investigado.
# Nao usa divisao igual entre quatro parafusos nem atribui capacidade ao4x30.
joint_wrenches=[]
parts650=body_records(650)
for row,side,n,face_x in zip(doors(650),['esquerda','direita'],['Liner_esquerdo','Liner_direito'],[5408.,6722.]):
 ref=np.array([face_x,3636.,2286.]);own=parts650[n]
 for rho in [650,800,900]:
  woodmass=own['volume_mm3']*rho/1e9
  for i,ang in enumerate(base.angles):
   cp=base.polygons(row,[ang])[0].mean(0);cg=np.array([cp[0],cp[1],2286.])
   Fdoor=np.array([0.,0.,-4*G]);Fwood=np.array([0.,0.,-woodmass*G])
   force=Fdoor+Fwood
   moment=(np.cross(cg-ref,Fdoor)+np.cross(np.array(own['com_mm'])-ref,Fwood))/1000
   joint_wrenches.append(dict(side=side,density_hypothesis_kg_m3=rho,angle_deg=float(ang),
    force_N=force.tolist(),moment_about_bolt_group_Nm=moment.tolist(),reference_mm=ref.tolist(),
    pure_axial_pair_over132mm_if_My_carried_only_by_normal_forces_N=abs(float(moment[1]))/.132))
result=dict(source_sha256=D['source_sha256'],source_unchanged=base.sha(ROOT/D['source'])==D['source_sha256'],
 variants=variants,cases=all_cases,liner_face_joint_wrenches=joint_wrenches,
 sources=[dict(url='https://ea.blum.com/en/number-of-hinges/',facts=['Regra publicada ate600mm; ate650mm orienta dobradica adicional.','Recomenda em principio altura maior que largura.','Aumentar espacamento dos extremos.']),
  dict(url='https://publications.blum.com/2024/catalogue/en/152/',facts=['173H7130 distancia3, altura11.5; 173H7100 distancia0, altura8.5.']),
  dict(url='https://publications.blum.com/2024/catalogue/en/77/',facts=['Tabela de recobrimento para71B3550; K5/calco3 correspondente nominal13.'])],
 sleeve_joint_proposal=dict(liner_each_mm=[18,612,272],contact_area_each_mm2=612*272,
  fasteners_each_candidate=4,fastener_family='4x30 face a face',nominal_penetration_second_board_mm=12,
  remaining_outer_board_mm=6,stations_yz_mm=[[3410,2220],[3410,2352],[3862,2220],[3862,2352]],
  status='Posicoes/familia de estudo; resistencia, pilotos, espacamento e acesso nao homologados. Caso de junta sem credito do apoio inferior do liner; sem distribuicao por parafuso.'),
 limitations=['Nao e aprovacao automatica da frente baixa650x306: ressalva de proporcao continua.','Calco3 foi tratado como afastamento rigido3 do eixo de montagem; STEP real e regulagens nao ensaiados.',
 'Sem corpos de ferragem, parafusos/pilotos, maos, pessoas, paredes ou tolerancias.','Amostragem0.5grau/5mm nao prova margem continua.','Cortes de compressao so verificam equilibrio necessario; nao incluem P02 acoplado, rigidez/juntas ou pressao local.',
 'Massa4kg por folha e hipotese, massas fixas das ferragens ainda nao incluidas separadamente.','Carga30kg e investigacao, nao capacidade autorizada.','Faixas/liners mudam aparencia, peso e fixacoes; nao aprovados pelo usuario nem incorporados a R52.'],
 integration_gate='NAO_ATENDIDO: proporcao/ferragens e fixacoes/caixa ainda condicionadas; comparar aparencia com Elias.')
(OUT/'Comparacao_portas.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

im=Image.new('RGB',(1800,1320),'white');dr=ImageDraw.Draw(im)
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),n)
def tx(x,y,t,n=24,b=False,c='#233d4d'):dr.text((x,y),t,font=font(n,b),fill=c)
tx(60,35,'Maleiro P03 — comparação das portas',38,True)
tx(60,95,'Mesma altura e profundidade externa • duas malas 55 × 35 × 25 cm como referência',25)
sx=1.;ox=160
for row,yy in [(672,235),(650,735)]:
 tx(60,yy-90,'A. Duas folhas de 67,2 cm' if row==672 else'B. Duas folhas de 65 cm + faixas fixas de 1,8 cm',29,True)
 tx(60,yy-45,'Grupo de duas dobradiças sem confirmação para esta largura.' if row==672 else'Três dobradiças por folha; reforço interno de madeira de 1,8 cm.',23)
 specs=doors(row)
 if row==650:
  for x1,x2 in [(5392,5410),(6720,6738)]:dr.rectangle([ox+x1-5392,yy,ox+x2-5392,yy+306],fill='#8b7659',outline='#3f5360',width=2)
 for r in specs:
  cc=base.polygons(r,[0])[0];lo,hi=cc[:,0].min(),cc[:,0].max()
  dr.rectangle([ox+lo-5392,yy,ox+hi-5392,yy+306],fill='#d6bd94',outline='#3f5360',width=3)
  xx=lo+22.5 if r['side']=='left' else hi-22.5
  for z in ([79,227] if row==672 else[52,153,254]):
   X=ox+xx-5392;Y=yy+306-z
   dr.ellipse([X-17.5,Y-17.5,X+17.5,Y+17.5],fill='#f1f2ef',outline='#3f5360',width=2)
  tx(ox+lo-5392+200,yy+130,str(row/10).replace('.',',')+' cm',27,True)
 tx(65,yy+326,'Vão entre suportes: 131,4 cm • junta central 2 mm' if row==672 else'Vão entre reforços: 127,8 cm • junta central 4 mm • juntas laterais 3 mm',23)
tx(60,1155,'B acrescenta 4,95 kg de madeira fixa a 800 kg/m³ e uma ligação por face a dimensionar em cada lado.',23)
tx(60,1200,'Há orientação publicada para largura/quantidade em B; a proporção baixa ainda exige confirmação.',23,True)
tx(60,1245,'Nenhuma foi incorporada ao CAD. Fixações, corpos das ferragens e capacidade continuam em estudo.',23)
im.save(OUT/'Comparacao_portas.png')
print(json.dumps(dict(variants=2,cuts=len(all_cases),cuts_feasible=sum(c['cut']['feasible'] for c in all_cases),
 pair_hits=sum(p['intersections'] for v in variants for p in v['pair_results']),bag_hits=sum(len(p['collisions']) for v in variants for p in v['bag_paths']),
 wood_delta_B_minus_A_kg=variants[1]['wood_mass_without_moving_leaves_at800_kg']-variants[0]['wood_mass_without_moving_leaves_at800_kg']),ensure_ascii=False))
