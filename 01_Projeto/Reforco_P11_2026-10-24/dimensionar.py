"""Reforco P11, estudo R00. Nao modifica FCStd ou libera usinagem.

python dimensionar.py
python dimensionar.py --verificar  # numpy para a conferencia FEM
"""
from pathlib import Path
import csv
import json
import math
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PREVIOUS=ROOT/'01_Projeto/Calculo_P11_2026-10-24'
sys.path.insert(0,str(PREVIOUS))
from calcular_p11 import beam_case, extract_geometry, write_json


def rounded_I(B,H,r):
    c=H/2-r
    removed=(1-math.pi/4)*c*c*r*r+c*r**3/3+(1/3-math.pi/16)*r**4
    return B*H**3/12-4*removed


def rhs_I(B,H,t,r):
    return rounded_I(B,H,r)-rounded_I(B-2*t,H-2*t,max(0,r-t))


def global_case(L,E,I,content,dead,g=9.80665):
    P=content*g;G=dead*g
    return dict(point_deflection_mm=P*L**3/(48*E*I),
                dead_deflection_mm=5*G*L**3/(384*E*I),
                total_deflection_mm=P*L**3/(48*E*I)+5*G*L**3/(384*E*I),
                max_moment_Nmm=P*L/4+G*L/8,
                symmetric_reaction_N=(P+G)/2,
                upper_bound_reaction_N=P+G)


def csv_write(name,rows):
    with (HERE/name).open('w',encoding='utf-8-sig',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=list(rows[0]),delimiter=';')
        w.writeheader();w.writerows(rows)


def inside_rounded(y,z,cy,cz,w,h,r):
    dy=abs(y-cy)-(w/2-r);dz=abs(z-cz)-(h/2-r)
    return max(dy,0)**2+max(dz,0)**2 <= r*r+1e-10 and abs(y-cy)<=w/2+1e-10 and abs(z-cz)<=h/2+1e-10


def build():
    s=json.loads((HERE/'Premissas.json').read_text(encoding='utf-8'))
    old=json.loads((ROOT/s['base_calculo']).read_text(encoding='utf-8'))
    geom=extract_geometry(old)
    p=s['perfil'];a=s['apoio'];tol=s['tolerancias_para_sensibilidade_secao'];g=old['gravidade_m_s2']
    own=s['vao_livre_mm']*s['profundidade_mm']*s['espessura_mdf_para_massa_mm']*s['densidade_mdf_kg_m3']/1e9
    dead=own+s['massa_metal_max_calculo_kg']
    # Vao de calculo=672: superior a distancia entre centros reais de apoio.
    metal=global_case(p['comprimento_nominal_mm'],p['E_min_MPa'],p['I_min_mm4'],s['conteudo_total_kg'],dead)
    gap=max(b-a for a,b in zip(p['centros_y_mm'],p['centros_y_mm'][1:]))
    local=beam_case(gap,s['faixa_efetiva_local_mm'],s['espessura_mdf_resistente_mm'],
                    s['E_mdf_MPa']/s['multiplicador_flecha_mdf_sustentada'],s['densidade_mdf_kg_m3'],
                    s['conteudo_total_kg'],'localizada_central',mass_thickness_mm=s['espessura_mdf_para_massa_mm'])
    Gsteel=p['E_min_MPa']/(2*(1+0.3));ecc=p['largura_mm']/2+0.1
    torque=(s['conteudo_total_kg']+dead)*g*ecc
    twist=torque*p['comprimento_nominal_mm']/(4*Gsteel*p['J_torcao_min_mm4'])
    twist_displacement=ecc*twist
    total=metal['total_deflection_mm']+local['max_deflection_mm']+a['acomodacao_total_max_mm']+s['orcamento_torcao_mm']
    sigma=metal['max_moment_Nmm']/(p['I_min_mm4']/(tol['altura_max_mm']/2))
    design_sigma=sigma*s['majoracao_cargas_metal_estudo']
    # Torsao de parede fina e so triagem; rigidez exige anti-giro ajustado nas pontas.
    mid_area=(tol['largura_min_mm']-tol['parede_min_mm'])*(tol['altura_min_mm']-tol['parede_min_mm'])
    tau=torque/(2*mid_area*tol['parede_min_mm'])
    von_mises=math.sqrt(design_sigma**2+3*(tau*s['majoracao_cargas_metal_estudo'])**2)
    limit_stress=p['fy_min_MPa']/s['divisor_resistencia_metal_estudo']
    worst_I=rhs_I(tol['largura_min_mm'],tol['altura_min_mm'],tol['parede_min_mm'],tol['raio_externo_max_em_paredes']*tol['parede_min_mm'])
    nominal_I=rhs_I(p['largura_mm'],p['altura_vertical_mm'],p['parede_nominal_mm'],2*p['parede_nominal_mm'])
    bearing_area=a['sapata_largura_y_mm']*a['embutimento_minimo_efetivo_mm']
    demands=dict(effective_bearing_area_mm2=bearing_area,
                 service_reaction_upper_bound_N=metal['upper_bound_reaction_N'],
                 service_bearing_demand_MPa=metal['upper_bound_reaction_N']/bearing_area,
                 proof_bearing_demand_MPa=a['forca_prova_local_proposta_N']/bearing_area,
                 remaining_side_web_min_mm=a['espessura_lateral_minima_de_estudo_mm']-a['bolso_profundidade_x_mm']-a['tolerancia_profundidade_bolso_mm'],
                 status='Demandas, nao resistencia certificada do MDF. Nao converter MOR em resistencia de apoio.')
    pockets=[]
    for side,part,x0,x1 in [('esquerda','Peca335',-6,0),('direita','Peca334',661,667)]:
        for n,cy in enumerate(p['centros_y_mm'],1):
            pockets.append(dict(id=f'P11-AP-{side}-{n}',part=part,
                                x_min_bay_mm=x0,x_max_bay_mm=x1,
                                y_center_from_front_mm=cy,y_min_mm=cy-a['bolso_largura_y_mm']/2,y_max_mm=cy+a['bolso_largura_y_mm']/2,
                                z_floor_from_shelf_bottom_mm=a['bolso_soleira_z_mm'],z_ceiling_mm=a['bolso_teto_z_mm'],radius_mm=a['raio_interno_bolso_mm'],
                                status='Nominal; nao programa de usinagem. Provar apoio e compatibilizar CAD primeiro'))
    # Confere acomodacao geometrica do tubo, sapata e calcos no contorno R3.
    geometric_checks=[]
    cz=(a['bolso_soleira_z_mm']+a['bolso_teto_z_mm'])/2
    for cy in p['centros_y_mm']:
        for item,w,z0,z1 in [('tubo',35,-15,0),('sapata',35,-17,-15),('calco_inferior',35,-17.5,-17),('antigiro_superior',35,0,0.5)]:
            ok=all(inside_rounded(y,z,cy,cz,43,18,3) for y in [cy-w/2,cy+w/2] for z in [z0,z1])
            assert ok,(item,cy)
            geometric_checks.append(dict(item=item,y_center_mm=cy,inside_nominal_R3=True))
    assert gap==126 and total<s['criterio_flecha_mm']
    assert worst_I>p['I_min_mm4'] and twist_displacement<s['orcamento_torcao_mm']
    assert von_mises<limit_stress
    # Pilotos Minifix ficam9mm acima; bolsos nao invadem cilindroØ5 na lateral.
    min_clearance=min(math.hypot(max(0,abs(y-cy)-43/2),9-a['bolso_teto_z_mm'])-2.5
                      for y in [60,252] for cy in p['centros_y_mm'])
    assert min_clearance>0
    # A sapata avanca14.5mm no vao; caixa deMinifix comeca a26.5mm.
    shoe_cam_gap=34-15/2-(a['sapata_comprimento_x_mm']-a['embutimento_nominal_mm'])
    assert shoe_cam_gap>0
    tube_mass_catalogue=p['quantidade']*p['comprimento_nominal_mm']/1000*p['peso_catalogo_barra6m_kg']/6
    volume_envelope=p['quantidade']*s['vao_livre_mm']*p['largura_mm']*p['altura_vertical_mm']/1e6
    candidates=[]
    for label,b,h,t,count in [('Tubo20x10x1.5',20,10,1.5,3),('Tubo35x15x1.5',35,15,1.5,3),('Tubo35x15x2',35,15,2,3),('Tubo20x20x1.5',20,20,1.5,3),('Barra38.1x12.7',38.1,12.7,0,3)]:
        I=rhs_I(b,h,t,2*t) if t else b*h**3/12
        area=b*h-(b-2*t)*(h-2*t)-(4-math.pi)*((2*t)**2-t*t) if t else b*h
        mass=count*area*p['comprimento_nominal_mm']*p['densidade_aco_kg_m3']/1e9
        row=global_case(p['comprimento_nominal_mm'],200000,I,s['conteudo_total_kg'],own+mass)
        candidates.append(dict(option=label,height_mm=h,ideal_or_rounded_I_mm4=I,metal_mass_kg=mass,
                               global_deflection_only_mm=row['total_deflection_mm'],
                               status='Comparacao nominal, sem validar toda alternativa; a selecionada usaI_min4800 e metal4kg'))
    parts=[dict(id='P11-RF-TUBO',quantity=3,description='Tuboaco35x15x2;15vertical;fy>=200;I>=4800;J>=10000',nominal_dimensions_mm='672x35x15',notes='L_corte=vao_real+11;comprimento nominal672;naousinarMDF18da prateleira'),
           dict(id='P11-RF-SAPATA',quantity=6,description='Sapataaco sobponta',nominal_dimensions_mm='20x35x2',notes='Contato efetivo minimo5x35;semcontar solda como apoiovertical'),
           dict(id='P11-RF-MACICO',quantity=6,description='Inserto macico deacoajustadoao interior naspontas',nominal_dimensions_mm='30x10x20aprox',notes='Chanfros/ajuste ao tubo real;calcar rigidamente para evitar amassamento local;nao soldagem estrutural presumida'),
           dict(id='P11-RF-CALCO-INF',quantity=6,description='Calco inferior metalico rigido',nominal_dimensions_mm='35x5x0.5nominal',notes='Ajustar apos medir;semcunhaMDFouespuma'),
           dict(id='P11-RF-CALCO-SUP',quantity=6,description='Calco superior antigiro metalico',nominal_dimensions_mm='35x5x0.5nominal',notes='Folga residual vertical<=0.05;acomodacao total<=0.2 comprovada'),
           dict(id='P11-RF-BOLSO',quantity=6,description='Cavidade internaR3 naslaterais;naoprofuroexterno',nominal_dimensions_mm='43x18x6',notes='Soleira17.5abaixo da prateleira; teto0.5acima;3porlateral;usinagempendente')]
    result=dict(revision='R00',date=s['data'],settings=s,source_cad_sha256=geom['sha256'],
                self_mass_mdf_kg=own,metal_mass_catalogue_tubes_kg=tube_mass_catalogue,metal_mass_calculation_kg=s['massa_metal_max_calculo_kg'],
                steel_global=metal,mdf_transverse=local,
                effective_I_nominal_rounded_mm4=nominal_I,tolerance_sensitivity_I_mm4=worst_I,
                assembly_budget_mm=a['acomodacao_total_max_mm'],torsion_budget_mm=s['orcamento_torcao_mm'],
                torsion_elastic_estimate_mm=twist_displacement,combined_upper_estimate_mm=total,criterion_mm=s['criterio_flecha_mm'],
                residual_margin_mm=s['criterio_flecha_mm']-total,
                metal_stress=dict(service_bending_MPa=sigma,study_design_von_mises_MPa=von_mises,study_limit_MPa=limit_stress,status='Triagem de material e modelo, nao declaracao normativa ou verificacao completa das pontas'),
                support_demands=demands,nominal_geometry_checks=geometric_checks,
                minifix_pilot_nominal_clearance_mm=min_clearance,shoe_to_cam_nominal_gap_mm=shoe_cam_gap,
                profile_envelope_volume_litres=volume_envelope,lower_bay_clearance_below_profile_mm=258-15,
                local_clearance_below_end_mm=258-17.5,nominal_pockets=pockets,candidates=candidates,
                manufacturing_status='CONDICIONAL: dimensionamento global e detalhe nominal, sem corteCAD ou ensaio; provar apoios/MDF/encaixes e suspensao antes de liberar20kg no armario',
                excluded=['CreditarMinifix/fundo no apoiovertical','Dividir20kgpor3','SomarEI doMDFao metal','Carga em contato menor50x60mm','Pessoas,impacto,umidadeanormal','Certificar longo prazo pelo ensaio curto'])
    write_json(HERE/'Resultados.json',result)
    csv_write('Comparacao_perfis.csv',candidates);csv_write('Pecas_reforco.csv',parts);csv_write('Bolsos_nominais.csv',pockets)
    return result


def verify(result):
    from verificar_p11 import fem
    p=result['settings']['perfil'];L=p['comprimento_nominal_mm'];I=p['I_min_mm4'];E=p['E_min_MPa']
    # Uma secao equivalente, sem massa propria, reproduzI para conferir a viga.
    t=15.;b=12*I/t**3
    dead=result['self_mass_mdf_kg']+result['metal_mass_calculation_kg']
    uniform=fem(L,b,t,E,0,dead,'distribuida')[0]
    point=fem(L,b,t,E,0,20,'localizada_central')[0]
    err=abs((uniform+point)[20]-result['steel_global']['total_deflection_mm'])
    assert err<1e-7
    local=result['mdf_transverse']
    u,*_=fem(126,50,17.7,1100,800,20,'localizada_central',mass_thickness_mm=18.3)
    local_err=abs(u[20]-local['max_deflection_mm'])
    assert local_err<1e-7
    # Independente: quadratura numerica do contornoarredondado.
    import numpy as np
    B,H,t,r=34.8,14.8,1.75,5.25
    z=(np.arange(200000)+.5)*H/200000-H/2
    def widths(B,H,r,z):
        az=np.abs(z);out=np.zeros_like(z);inside=az<=H/2
        dy=np.maximum(0,az-(H/2-r))
        out[inside]=B-2*r+2*np.sqrt(np.maximum(0,r*r-dy[inside]**2))
        return out
    numeric=float(np.sum((widths(B,H,r,z)-widths(B-2*t,H-2*t,r-t,z))*z*z)*H/200000)
    section_err=abs(numeric-result['tolerance_sensitivity_I_mm4'])
    assert section_err<.05,(numeric,section_err)
    checks=dict(status='PASS',beam_FEM_error_mm=float(err),mdf_strip_FEM_error_mm=float(local_err),rounded_section_quadrature_error_mm4=section_err,
                geometry_nominal_checks=len(result['nominal_geometry_checks']),
                tests=['Modelo metalico sem acao composta','MDFtransversal comEefetivo','Secaoarredondada por quadratura','ContornoR3 e sapatas/calcos','FolgasnominaisMinifix','SHA256R49conferido'],
                limitations='Nao e ensaio fisico, teste de interferenciaBREP ou comprovacao da resistencia do apoiofresado')
    write_json(HERE/'Verificacao.json',checks)
    return checks


if __name__=='__main__':
    data=build()
    if '--verificar' in sys.argv:print(json.dumps(verify(data),ensure_ascii=True))
    print(json.dumps({k:data[k] for k in ['combined_upper_estimate_mm','criterion_mm','residual_margin_mm','metal_mass_catalogue_tubes_kg','manufacturing_status']},ensure_ascii=True))
