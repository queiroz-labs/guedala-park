"""P01: caminho nominal ate o piso, sem tubos, preservando baseZ62/80.
N,mm,MPa,kg. Hipoteses de apoio/material nao sao capacidade liberada.
"""
from pathlib import Path
import json,sys,hashlib,csv
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'Calculo_P11_2026-10-24'))
from calcular_p11 import beam_case
CAD=ROOT/'01_Projeto/Revisao_sem_tubos_R51_2026-10-25/Guedala_Park_R51_Sem_estudo_tubular.FCStd'
SHA='ab5323bb12f8eca40b25bdfe4eadc8a3221c82b0646f354cd1f2832acfb27c16'
assert hashlib.sha256(CAD.read_bytes()).hexdigest()==SHA
G=9.80665
parts=[]
# Quatro longarinas de MDF18 em pe, altura62; duas formam apoio central36.
for tag,y in [('frontal',3290.),('trilho_posterior',3354.),('frente_base',3372.),('traseiro',3904.)]:
 parts.append(dict(id='Soco_'+tag,label='Soco de marcenaria '+tag,origin_mm=[5408.,y,0.],size_mm=[1964.,18.,62.],role='apoio continuo nominal ao piso'))
# Alinhar travessas de marcenaria sob as cinco divisorias e junto das laterais.
xs=[5408.,5763.,6113.,6381.,6649.,6999.,7354.]
for i,x in enumerate(xs,1):
 for tag,y,length in [('frente',3308.,46.),('caixa',3390.,514.)]:
  parts.append(dict(id=f'Soco_transversal_{i}_{tag}',label=f'Travessa soco{i} {tag}',origin_mm=[x,y,0.],size_mm=[18.,length,62.],role='compressao direta sob divisoria ou borda; piso continuo requerido'))
parts.append(dict(id='Calco_fundo',label='Calco continuo18 sob fundo existente',origin_mm=[5408.,3922.,0.],size_mm=[1964.,18.,18.],role='fundoZ18 -> calco18 -> piso; altura final depende do nivel real'))
for x,side in [(5390.,'E'),(7372.,'D')]:
 parts.append(dict(id='Soco_lateral_frontal_'+side,label='Apoio62 da continuacao lateral frontal '+side,origin_mm=[x,3290.,0.],size_mm=[18.,82.,62.],role='continuidade lateral frontal -> soco -> piso'))
area=sum(p['size_mm'][0]*p['size_mm'][1] for p in parts)
volume=sum(p['size_mm'][0]*p['size_mm'][1]*p['size_mm'][2] for p in parts)
contact_base=2*1964*18+7*18*514
contact_extension=2*1964*18+7*18*46
contact_back=1964*18;contact_front_sides=2*18*82
assert abs(area-contact_base-contact_extension-contact_back-contact_front_sides)<1e-8
cells=[]
for b in [50.,550.]:
 for m in [5.,10.,20.]:
  r=beam_case(355,b,17.7,1100,800,m,'point' if b==50 else 'distribuida',mass_thickness_mm=18.3)
  cells.append(dict(effective_width_mm=b,content_kg=m,load=r['type'],self_mass_kg=r['self_mass_kg'],
    deferred_deflection_mm=r['max_deflection_mm'],plus_reserve_mm=r['max_deflection_mm']+.2,
    reaction_each_end_N=r['reaction_left_N'],criterion_mm=355/300,
    note='Triagem entre travessas reais do soco, no maior tramo entre eixos355. Nao e carga aprovada por compartimento; contato e nivel precisam existir.'))
doors=[]
geometry=json.loads((HERE.parent/'Cargas_e_ligacoes_R50_2026-10-25/Geometria_R50.json').read_text(encoding='utf-8'))
woodmass=geometry['parts']['Peca247']['volume_mm3']*800/1e9
for extra in [0.,2.]:
 for b in [10.,20.,50.]:
  r=beam_case(64,b,17.7,1100,800,woodmass+extra,'point',mass_thickness_mm=18.3)
  doors.append(dict(nominal_wood_leaf_mass_kg=woodmass,hardware_mass_sensitivity_kg=extra,effective_contact_width_mm=b,
    entire_leaf_on_one_local_support=True,span_between_runners_mm=64,
    max_deflection_mm=r['max_deflection_mm'],support_each_N=r['reaction_left_N'],
    note='Envelope de ponto no meio do vao transversal, sem credito do aluminio do trilho. Largura efetiva10/20/50 e massa extra2 sao sensibilidades, nao medidas dos carros. Tolerancia de desnivel do sistema ainda por comprovar.'))
floor=[]
for total in [200.,300.,400.,500.]:
 for fraction in [1.,.25,.05]:
  F=total*G;A=area*fraction
  floor.append(dict(total_mass_scenario_kg=total,contact_fraction=fraction,nominal_contact_area_m2=A/1e6,
    average_pressure_kPa=F/A*1000,
    ideal_MDF_axial_shortening_at_E1100_mm=F/A*62/1100,
    note='Massa TOTAL parametrica, nao conteudo autorizado. Pressao nao e tensao admissivel do piso/MDF; desnivel/calcos alteram contato.'))
out=dict(cad=str(CAD),sha256=SHA,units='N,mm,MPa,kg',new_boards=parts,count=len(parts),
 plinth_top_Z_mm=62,original_base_top_Z_mm=80,original_base_underside_Z_mm=62,
 footprint=[5390,3290,7390,3940],total_top_and_floor_nominal_area_mm2=area,
 contact_main_base_mm2=contact_base,contact_front_extension_mm2=contact_extension,
 contact_back_mm2=contact_back,contact_front_sides_mm2=contact_front_sides,
 volume_mm3=volume,mass_nominal_kg_at_rho800=volume*800/1e9,
 cell_beams=cells,door_base_extension=doors,floor_scenarios=floor,
 status='ESTUDO separado de caminho ate o piso; sem modificarR51, sem fixadores ou capacidade liberados.',
 constraints=['Sem tubos/quadro metalico','Altura interna/cursos/cortes existentes preservados no estudo',
 'Face inferior frontal62 passa a ter soco visivel; revisao de aparencia por Elias antes de incorporar',
 'Contato nivelado ao piso e ao fundo da base nao demonstrado por nominal; levantamento/calcos depois das chaves',
 'Reconstituir massa de carcaça, portas, gavetas e conteudo antes de especificar piso/apoios',
 'Nao usar simples apoio para substituir retencao/anti-tombamento do roupeiro'])
(HERE/'Resultados.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (HERE/'Pecas_soco_estudo.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['id','X_mm','Y_mm','Z_mm','L_mm','P_mm','H_mm','status'])
 for p in parts:w.writerow([p['id'],*p['origin_mm'],*p['size_mm'],'ESTUDO - medidas nominais; bordas/nivel/piso/juntas pendentes'])
assert len(parts)==21 and area==250272
assert all(abs(r['reaction_each_end_N']*2-(r['self_mass_kg']+r['content_kg'])*G)<1e-7 for r in cells)
assert hashlib.sha256(CAD.read_bytes()).hexdigest()==SHA
(HERE/'Verificacao_calculo.json').write_text(json.dumps(dict(source_unchanged=True,
 checks=['21 pecas previstas','area nominal topo=piso=soma das interfaces','equilibrio das seis vigas','SHA256R51 preservado'],
 passed=True),indent=2)+'\n',encoding='utf-8')
print(json.dumps({'new_boards':len(parts),'area_m2':area/1e6,'main_base_contact_mm2':contact_base,
 'extension_contact_mm2':contact_extension,'nominal_mass_kg':volume*800/1e9,
 'beams':[(r['effective_width_mm'],r['content_kg'],r['plus_reserve_mm']) for r in cells]}))
