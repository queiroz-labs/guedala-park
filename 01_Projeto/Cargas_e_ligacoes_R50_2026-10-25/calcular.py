"""Cargas nominais R50. Unidades N, mm, MPa, kg. Nao modifica CAD.

python calcular.py -- rapido (vigas/tubos/mecanismos/matriz)
python calcular.py --placas -- inclui Ritz e convergencia (numpy)
Nenhuma hipotese de material, junta ou ensaio equivale a carga liberada.
"""
from pathlib import Path
import sys, json, math, csv, hashlib
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'Calculo_P11_2026-10-24'))
sys.path.insert(0,str(HERE.parent/'P11_ligacoes_sem_tubos_2026-10-24'))
from calcular_p11 import beam_case
from placa_ritz import PlateModel
G=9.80665
E=2200.;T=17.7;TM=18.3;RHO=800.
geo=json.loads((HERE/'Geometria_R50.json').read_text(encoding='utf-8'))
CAD=ROOT/geo['cad']
assert hashlib.sha256(CAD.read_bytes()).hexdigest()==geo['sha256']

def save(name,data):
 (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def csvout(name,rows):
 if not rows:return
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (HERE/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,keys,delimiter=';');w.writeheader();w.writerows(rows)

def beam(L,EI,q=0.,points=(),supports=(0.,),step=12.):
 """Euler-Bernoulli FE. q N/mm, points=(x,N), supports verticais bilaterais.
 Hermite cubico com carga consistente e nos em todas as descontinuidades.
 R>0 apoia para cima, R<0 exige retencao; nao elimina tracao automaticamente.
 """
 xs=np.unique(np.r_[np.linspace(0,L,max(4,math.ceil(L/step))+1),supports,[x for x,p in points]])
 nn=len(xs);K=np.zeros((2*nn,2*nn));F=np.zeros(2*nn)
 for i,l in enumerate(np.diff(xs)):
  ix=np.arange(2*i,2*i+4)
  k=EI/l**3*np.array([[12,6*l,-12,6*l],[6*l,4*l*l,-6*l,2*l*l],[-12,-6*l,12,-6*l],[6*l,2*l*l,-6*l,4*l*l]])
  K[np.ix_(ix,ix)]+=k
  F[ix]+=q*l/12*np.array([6,l,6,-l])
 for x,p in points:F[2*int(np.argmin(abs(xs-x)))]+=p
 fixed=[2*int(np.argmin(abs(xs-x))) for x in supports]
 free=np.setdiff1d(np.arange(2*nn),fixed)
 # Diagonal scaling only, no artificial springs.
 scale=np.sqrt(np.maximum(np.diag(K),1.))
 u=np.zeros(2*nn);u[free]=np.linalg.solve(K[np.ix_(free,free)]/scale[free,None]/scale[None,free],F[free]/scale[free])/scale[free]
 R=F-K@u
 return dict(max_deflection_mm=float(u[::2].max()),min_deflection_mm=float(u[::2].min()),
             max_abs_deflection_mm=float(abs(u[::2]).max()),at_mm=float(xs[np.argmax(abs(u[::2]))]),
             supports_mm=list(supports),reactions_N=[float(R[i]) for i in fixed],
             force_error_N=float(sum(R[fixed])-sum(F[::2])),
             moment_error_Nmm=float(np.dot(np.array(supports),R[fixed])-q*L*L/2-sum(x*p for x,p in points)),
             element_max_mm=float(np.diff(xs).max()))

def rectangular_screen(name,L,B,mass,kind='distribuida',Em=E):
 r=beam_case(L,B,T,Em,RHO,mass,kind,mass_thickness_mm=TM)
 return dict(id=name,**r,deferred_sensitivity_mm=2*r['max_deflection_mm'],
             deferred_plus_reserve_mm=2*r['max_deflection_mm']+.2,criterion_mm=L/300,
             status='Triagem da chapa, apoios simples bilaterais ideais; nao capacidade do movel')

def tube(L,D,t,mass,kind='uniform',central=False):
 A=math.pi*(D*D-(D-2*t)**2)/4;I=math.pi*(D**4-(D-2*t)**4)/64
 own=A*L*7850/1e9
 supports=(0.,L/2,L) if central else (0.,L)
 q=(own+(mass if kind=='uniform' else 0))*G/L
 point=() if kind=='uniform' else ((L/4 if central else L/2,mass*G),)
 r=beam(L,200000*I,q,point,supports)
 # Sem apoio central, tensao bruta exata; com central nao atribuir tensao apenas por vao cortado.
 moment=(own+mass)*G*L/8 if kind=='uniform' else own*G*L/8+mass*G*L/4
 return dict(L_mm=L,D_mm=D,wall_mm=t,content_kg=mass,kind=kind,central_support=central,
             own_kg=own,A_mm2=A,I_mm4=I,**r,
             gross_stress_simple_only_MPa=None if central else moment/(I/(D/2)),criterion_mm=L/300)

def build():
 result={'cad':geo['cad'],'sha256':geo['sha256'],'units':'N, mm, MPa, kg',
  'hypotheses':dict(E_instant_MPa=E,E_adverse_MPa=1600,nu=.3,structural_t_mm=T,mass_t_mm=TM,
   rho_kg_m3=RHO,deferred_multiplier=2,extra_deflection_reserve_mm=.2,criterion='L/300 escolhido pelo projeto',
   material_status='Referencia condicional; confirmar fabricante/substrato/espessura resistente. Mult.2 e E1600 sao sensibilidades, sem previsao de prazo.'),
  'P11':'Mantida decisao sem tubos e memoria existente; 10kg distribuidos condicionais, nao capacidade liberada'}
 rows=[]
 for L,B,name in [(799,312,'P15_base'),(1764,212,'P04_base_sem_transferencia_divisorias'),(878.5,212,'P04_maior_entre_centros_condicional'),(355,400,'P01_sapateira'),(705,550,'P01_prateleira_sem_apoio_intermedio')]:
  for m in [5,10,20]:
   for kind in ['distribuida','localizada_central']:
    rows.append(rectangular_screen(name,L,B,m,kind))
 result['beams']=rows;csvout('Triagem_chapas.csv',rows)
 result['adverse_material_beams']=[rectangular_screen(name,L,B,m,Em=1600.) for name,L,B,m in [('P15_base',799,312,20),('P04_maior_entre_centros_condicional',878.5,212,5),('P01_sapateira',355,400,20)]]

 # P01: so a divisoria interna sobrepoe a face inferior da prateleira.
 # Extremidade oposta a lateral so encontra o topo da divisoria pela aresta.
 wardrobe=[]
 for name,supports in [('Peca245',(341.,705.)),('Peca246',(0.,364.))]:
  L=705.;B=550.;own=L*B*TM*RHO/1e9;I=B*T**3/12
  for m in [5,10,20]:
   for kind in ['uniform','free_end']:
    # Localizacao longitudinal apenas; largura inteira ativa na viga, sem validar carga pequena na frente.
    xpos=0. if name=='Peca245' else L
    q=(own+(m if kind=='uniform' else 0))*G/L
    points=() if kind=='uniform' else ((xpos,m*G),)
    r=beam(L,E*I,q,points,supports)
    wardrobe.append(dict(piece=name,content_kg=m,kind=kind,self_mass_kg=own,**r,
      deferred_plus_reserve_mm=2*r['max_abs_deflection_mm']+.2,criterion_mm=364/300,
      criterion_note='364/300 escolhido para triagem do tramo; balanco341 requer verificacao propria',
      note='Lateral com junta de cortante + divisoria em compressao; canto oposto sem apoio positivo'))
 result['P01_overhangs']=wardrobe;csvout('P01_prateleiras_apoios_reais.csv',wardrobe)
 rods=[tube(L,20,.7,m,k,c) for L in [973.,332.] for m in [10,20,30] for k in ['uniform','point'] for c in ([False,True] if L==973 else [False])]
 result['P01_rods']=rods;csvout('P01_varoes.csv',rods)

 # Tubos P15 cancelados expressamente por Elias25/10; historico separado.
 result['P15_tubes_status']={'status':'CANCELADO - exige autorizacao previa de Elias para qualquer proposta futura','history':'Historico_tubos_P15_cancelado.json','active_alternative':'../Solucoes_marcenaria_sem_tubos_2026-10-25/README.md'}

 # P04: demandas nominais por tramo entre eixos, sem contar o fundo.
 p04=[]
 for L,m in [(878.5,5),(434.75,2.5),(434.75,2.5)]:
  r=rectangular_screen('P04_tramo_condicional',L,212,m)
  r['upward_reaction_per_joint_group_N']=r['reaction_left_N']
  r['vertical_joint_K_min_for_0_2mm_N_mm']=r['reaction_left_N']/.2
  p04.append(r)
 result['P04_span_demands']=p04

 # P20 eixo R50 x102,z420: CM local (224,y,-10), rotacao-Y negativa.
 lids=[];curve=[]
 for name in ['BancoR43_Painel1','BancoR43_Painel2']:
  p=geo['parts'][name];L=p['bbox_local_mm'][4];vol=p['volume_mm3'];cg=p['center_of_mass_local_mm']
  assert abs(cg[0]-224)<1e-6 and abs(cg[2]+10)<1e-6
  for rho in [650.,800.]:
   mass=vol*rho/1e9;maxlever=math.hypot(cg[0],cg[2]);peakangle=math.degrees(math.atan2(-cg[2],cg[0]))
   lids.append(dict(piece=name,length_mm=L,depth_mm=448,thickness_mm=20,density_kg_m3=rho,wood_mass_kg=mass,
    local_CG_mm=cg,world_CG_closed_mm=p['center_of_mass_global_mm'],
    peak_closing_moment_Nm=mass*G*maxlever/1000,peak_at_deg=peakangle,
    added_mass_kg_per_peak_Nm=1/(G*maxlever/1000),
    note='Apenas chapa; somar folha movel da piano, parafusos, revestimentos e partes moveis dos articuladores por CG real. Almofada retirada.'))
   for angle in [0.,2.556,15.,30.,45.,60.,75.,85.,90.]:
    a=math.radians(angle);moment=mass*G*(cg[0]*math.cos(a)-cg[2]*math.sin(a))
    curve.append(dict(piece=name,density_kg_m3=rho,wood_mass_kg=mass,angle_deg=angle,
      closing_moment_Nm=moment/1000,ideal_tangential_hand_N=moment/448,
      ideal_vertical_hand_N=None if angle==90 else moment/(448*math.cos(a)),
      one_support_force_at_effective_lever_20mm_N=moment/20,
      one_support_force_at_effective_lever_40mm_N=moment/40,
      one_support_force_at_effective_lever_60mm_N=moment/60))
 result['P20_lids']=lids;result['P20_moment_curve']=curve;csvout('P20_momento_e_esforcos.csv',curve)

 # Exigencias de conjunto, sem fatores de seguranca nem resistencia publicada inventada.
 demands=[]
 for code in ['P04','P15']:
  ps=[p for p in geo['parts'].values() if p['module']==code and p['visible_effective'] and p.get('box_mm') and min(p['box_mm'])>=17.7]
  # Somente caixa nominal conferida, exclui frentes/ferragens; nao soma conjunto com reservas.
  ids=['Peca359','Peca360','Peca361','Peca362','Peca363'] if code=='P15' else ['Peca266','Peca267','Peca268','Peca269','Peca270','ApoioComumR003','ApoioComumR004','ApoioOpostoR001','ApoioOpostoR002']
  mass=sum(geo['parts'][n]['volume_mm3']*RHO/1e9 for n in ids)
  contents=20 if code=='P15' else 10
  axis=1 if code=='P15' else 0
  wall=7000. if code=='P15' else 7390.
  base_id='Peca362' if code=='P15' else 'Peca269'
  box_moment=sum(geo['parts'][n]['volume_mm3']*RHO/1e9*G*(wall-geo['parts'][n]['center_of_mass_global_mm'][axis])/1000 for n in ids)
  content_lever=(wall-geo['parts'][base_id]['center_of_mass_global_mm'][axis])/1000
  # Contagem parcial explicitamente nao inclui portas/elementos desconhecidos.
  W=(mass+contents)*G;M=box_moment+contents*G*content_lever
  demands.append(dict(module=code,box_ids=ids,nominal_box_mass_kg=mass,content_kg=contents,
   partial_weight_N=W,partial_overturning_Nm=M,box_moment_Nm=box_moment,content_lever_from_wall_m=content_lever,
   tension_at_lever200mm_N=M/.2,tension_at_lever400mm_N=M/.4,
   note='Somente caixa+conteudo nominal. Somar portas/ferragens/reforco e CG real. Alavancas200/400 sao parametros;400 nao cabe no P04H308. Reacao total da interface, nao por bucha.'))
 result['suspension_partial_requirements']=demands
 save('Resultados.json',result)

 # Mapa de caminhos e dependencias. Cada linha diferencia demanda de capacidade.
 matrix=[]
 def add(i,mod,pieces,path,demand,action,dep):
  matrix.append(dict(id=i,module=mod,pieces=pieces,load_path=path,demand=demand,
   next_action=action,dependency=dep,status='Nominal calculado; capacidade e fabricacao nao liberadas'))
 add('P15-J01','P15','Peca362 <> Peca359/360','base -> laterais -> caixa',
     'Reacoes da triagem, inclui peso proprio; Minifix existentes4 da base, dentro dos8 da caixa',
     'Provar rigidez/cortante/retencao da junta; calcular demanda com frente concentrada antes de detalhar furos','produto+oficina')
 add('P15-J02','P15','Peca362 <> Peca361','base -> reforco traseiro -> fundo',
     'Contato R50 so aresta, area de face nula; fundo nao recebe apoio creditado',
     'Detalhar suporte positivo; nao copiar Confirmat horizontal do P11','projeto agora')
 add('P15-R01','P15','base/fundo da caixa de marcenaria','base -> ligacoes/fundo -> caixa',
     'Tubos CANCELADOS. Estudar composicao integral da base e fundo com face positiva',
     'Seguir novo estudo sem tubos e comprovar composicao/juntas; nao retomar longarinas','projeto+produto+oficina')
 add('P04-J01','P04','Peca269 <> divisorias internas','base -> uniao em tracao -> divisoria -> tampo/fundo -> suspensao',
     'Vao livre851.5; entre eixos878.5. Contato em cima da base nao sustenta a base para cima',
     'Detalhar tracao e transferencia ate suspensao; dupla36 nao dispensa fixacao','projeto agora+produto+oficina')
 add('P04-J02','P04','Peca269 <> Peca268','base -> fundo',
     'Aresta, sem apoio positivo no modelo',
     'Detalhar T resistente ou suporte; recalcular placa com juntas finitas','projeto agora')
 for n in ['Peca245','Peca246']:
  add('P01-'+n,'P01',n+' <> divisoria interna/lateral','prateleira -> compressao no divisor + junta lateral -> caixa',
      'Balanco341, tramo364. Extremidade junto ao outro divisor so toca em aresta. Carga localizada pode exigir retencao',
      'Estudo723 cria apoio sobre a divisoria existente. Incorporar apos conferir juntas, deformacao da caixa e fichas; ver arquivoP01_estudo_apoios_723','projeto agora+produto+oficina')
 add('P01-V01','P01','Varao/Varao001 <> terminais/central','roupas -> tubo -> suportes -> MDF -> caixa',
     '973mm, tubo20x0.7; central ideal calculado. Distancia montagem-eixo82mm no superior; suporte63total nao resolve',
     'Obter cota face-eixo e capacidade/rigidez do suporte; detalhar caminho ate a base do maleiro','produto+projeto agora')
 add('P01-V02','P01','Varao002/Varao003 <> terminais','roupas -> tubo332 -> terminais -> divisorias18',
     '332mm tubo20x0.7; forca por terminal nos CSV. Distancia montagem-eixo52mm',
     'Desencontrar furos nas divisorias compartilhadas e provar carga dos terminais','produto+oficina')
 add('P20-M01','P20','BancoR43_Painel1/2 <> piano/articuladores','peso movel -> eixo+articulador -> caixa',
     'Curva0a90, CG224/-10, momento residual90 e caso um articulador recebe todo momento',
     'Somar ferragens moveis por CG, desenhar terminais e alavanca efetiva por angulo, provar trava/retorno','produto+projeto agora+oficina')
 add('P20-A01','P20','tampas <> frente/fundo/divisorias','pessoa -> tampa fechada -> apoios positivos -> corpo -> piso',
     '9 contatos horizontais tampa-corpo confirmados em12 pares testados; nao usar articuladores como suporte de assento',
     'Dimensionar carga de pessoas/assimetria, contato e apoios reais do assento; nao concluido nesta rodada','projeto agora+oficina')
 csvout('Matriz_ligacoes_prioritarias.csv',matrix)
 # Reconciliacao146 contatos -- mantem IDs e natureza, nao fabrica conectores.
 source=json.loads((HERE/'Contatos_reconciliados.json').read_text(encoding='utf-8'))
 csvout('Contatos_reconciliados.csv',[{k:v for k,v in r.items() if k not in ['bbox_overlap_mm','global_normal_axis']} for r in source['contacts']])
 return result

def plates(result):
 cases=[];convergence=[]
 for name,L,B,m in [('P15',799.,312.,20.),('P04_878_5',878.5,212.,5.)]:
  for n in [8,10,12,14]:
   pts=sorted(set([(0.,float(y)) for y in np.linspace(0,B,n+1)]+[(L,float(y)) for y in np.linspace(0,B,n+1)]+[(float(x),B) for x in np.linspace(0,L,n+1)]))
   model=PlateModel(n=n,E=E/2,L=L,B=B,t=T,supports=pts)
   r=model.solve(mass=m,dead_kg=L*B*TM*RHO/1e9,grid=(241,81))
   convergence.append(dict(case=name,degree=n,max_deflection_mm=r['max_deflection_mm'],
    equilibrium_error=r['equilibrium_error'],constraint_error_mm=r['max_constraint_error_mm']))
  del r['coefficients'];del r['reactions_N'];del r['support_deflection_mm']
  cases.append(dict(case=name,L_mm=L,B_mm=B,content_kg=m,**r,
   criterion_mm=L/300,plus_reserve_mm=r['max_deflection_mm']+.2,
   status='Comparacao ideal: apoio vertical continuo em3bordas, frente livre, rotacao livre. Nao e junta existente. Fundo/laterais sem acomodacao.'))
 result['ideal_plates']=cases;result['plate_convergence']=convergence
 # P01 prototipo de ligacoes: traseira4+laterais2 com molas verticais,
 # divisoria interna so comprime. Fundo tratado como referencia fixa nesta etapa.
 p01=[]
 for config,L,xbs in [('R50_705_sem_apoio_da_ponta',705.,[341.]),('estudo_723_cobrindo_divisoria',723.,[9.,359.])]:
  for mass,kind,cx,cy in [(5.,'uniform',None,None),(10.,'uniform',None,None),(20.,'uniform',None,None),(5.,'patch',25.,30.)]:
   joints=[(72.,550.),((L-144)/3+72,550.),(2*(L-144)/3+72,550.),(L-72,550.),(L,70.),(L,480.)]
   bearing=[(x,y) for x in xbs for y in [70.,275.,480.]]
   active=list(bearing)
   for iteration in range(8):
    pts=joints+active;C=np.diag([1/500.]*len(joints)+[0.]*len(active))
    model=PlateModel(n=14,E=1100,L=L,B=550.,t=T,supports=pts,C=C)
    r=model.solve(mass=mass,kind=kind,cx=cx,cy=cy,dead_kg=L*550*TM*RHO/1e9,grid=(181,121))
    negative=[k for k,v in enumerate(r['reactions_N'][len(joints):]) if v<-.000001]
    if not negative:break
    active=[v for k,v in enumerate(active) if k not in negative]
   else:raise AssertionError('P01 contato unilateral nao convergiu')
   del r['coefficients'];del r['support_deflection_mm']
   p01.append(dict(config=config,content_kg=mass,**r,joint_positions_mm=joints,active_bearings_mm=active,
    criterion_mm=364/300,remaining_background_settlement_budget_mm=364/300-.2-r['max_deflection_mm'],
    note='Proposta para Peca245; Peca246 espelhada. Juntas iniciaisK1000/diferidas500 requeridas. Apoios so comprimem. Fundo/lateral como referencia; orcamento remanescente deve cobrir suas deformacoes. Nao capacidade liberada.'))
 result['P01_rear_joint_proposal']=p01
 save('Resultados.json',result);save('Convergencia_placas.json',convergence)

def verify(result):
 checks=[]
 for kind in ['distribuida','point']:
  a=beam_case(799,312,T,E,RHO,20,kind,mass_thickness_mm=TM)
  q=(a['self_mass_kg']+(20 if kind=='distribuida' else 0))*G/799
  p=() if kind=='distribuida' else ((799/2,20*G),)
  b=beam(799,E*312*T**3/12,q,p,(0.,799.))
  err=abs(b['max_deflection_mm']/a['max_deflection_mm']-1)
  checks.append(dict(test='FE versus formula viga '+kind,relative_error=err,pass_=bool(err<.001)))
 for name in ['P01_overhangs','P01_rods']:
  rows=result[name];err=max(abs(r['force_error_N']) for r in rows);mom=max(abs(r['moment_error_Nmm']) for r in rows)
  checks.append(dict(test=name+' equilibrio',max_force_error_N=err,max_moment_error_Nmm=mom,pass_=bool(err<1e-5 and mom<.01)))
 # P20: derivada de energia potencial U=m*g*(224sen(a)-10cos(a)).
 da=1e-6;errors=[]
 for r in result['P20_moment_curve']:
  a=math.radians(r['angle_deg']);m=r['wood_mass_kg']
  f=lambda t:m*G*(224*math.sin(t)-10*math.cos(t))/1000
  errors.append(abs((f(a+da)-f(a-da))/(2*da)-r['closing_moment_Nm']))
 checks.append(dict(test='P20 torque por energia potencial',max_error_Nm=max(errors),pass_=max(errors)<1e-6))
 if 'plate_convergence' in result:
  for name in sorted(set(r['case'] for r in result['plate_convergence'])):
   rs=[r for r in result['plate_convergence'] if r['case']==name];er=abs(rs[-1]['max_deflection_mm']/rs[-2]['max_deflection_mm']-1)
   checks.append(dict(test=name+' Ritz14vs12',relative_error=er,pass_=bool(er<.01)))
  # Controle independente: solucao Navier para placa de quatro bordas apoiadas.
  L=799.;B=312.;n=12
  pts=sorted(set([(0.,float(y)) for y in np.linspace(0,B,n+1)]+[(L,float(y)) for y in np.linspace(0,B,n+1)]+[(float(x),0.) for x in np.linspace(0,L,n+1)]+[(float(x),B) for x in np.linspace(0,L,n+1)]))
  model=PlateModel(n=n,E=1100,L=L,B=B,t=T,supports=pts)
  pr=model.solve(mass=20,dead_kg=L*B*TM*RHO/1e9,grid=(121,61))
  q=(20+L*B*TM*RHO/1e9)*G/(L*B)
  navier=16*q/(math.pi**6*model.D)*sum(math.sin(i*math.pi/2)*math.sin(j*math.pi/2)/(i*j*((i/L)**2+(j/B)**2)**2) for i in range(1,102,2) for j in range(1,102,2))
  err=abs(pr['center_mm_deflection']/navier-1)
  checks.append(dict(test='Ritz versus serie independente Navier101 placa4bordas',Ritz_mm=pr['center_mm_deflection'],Navier_mm=navier,relative_error=err,pass_=bool(err<.001)))
  rs=result['P01_rear_joint_proposal']
  err=max(max(abs(v) for v in r['equilibrium_error'].values()) for r in rs)
  compression=min(v for r in rs for v in r['reactions_N'][len(r['joint_positions_mm']):])
  checks.append(dict(test='P01 placas equilibrio e contato sem tracao',max_equilibrium_residual=err,min_contact_reaction_N=compression,pass_=bool(err<1e-5 and compression>=-1e-6)))
  r=next(x for x in rs if x['config'].startswith('estudo_723') and x['content_kg']==20 and x['kind']=='uniform')
  pts=r['joint_positions_mm']+r['active_bearings_mm'];C=np.diag([1/500.]*6+[0.]*(len(pts)-6))
  model=PlateModel(n=16,E=1100,L=723,B=550,t=T,supports=pts,C=C)
  probe=model.solve(mass=20,dead_kg=723*550*TM*RHO/1e9,grid=(181,121))
  err=abs(probe['max_deflection_mm']/r['max_deflection_mm']-1)
  checks.append(dict(test='P01 estudo723 Ritz16vs14',degree16_deflection_mm=probe['max_deflection_mm'],relative_error=err,pass_=bool(err<.01)))
 assert hashlib.sha256(CAD.read_bytes()).hexdigest()==geo['sha256']
 save('Verificacao_numerica.json',{'checks':checks,'passed':all(r['pass_'] for r in checks),'CAD_unchanged':True,
      'scope':'Verificacao numerica das hipoteses, sem ensaio e sem validar materiais/juntas reais.'})
 assert all(r['pass_'] for r in checks),checks
 print(json.dumps({'checks':len(checks),'passed':True,'plates':'ideal_plates' in result}))

if __name__=='__main__':
 r=build()
 if '--placas' in sys.argv:plates(r)
 verify(r)
