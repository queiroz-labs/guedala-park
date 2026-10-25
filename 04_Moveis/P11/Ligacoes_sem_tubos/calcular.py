"""P11 sem tubos: placa com8juntas e fundo flexivel. UnidadesN,mm,MPa.

python calcular.py (requer numpy)
Capacidade proposta condicional, sem alterarCAD ou liberar fabricacao.
"""
from pathlib import Path
import csv
import json
import math
import sys
import numpy as np
from placa_ritz import setup,back_compliance

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'01_Projeto/Calculo_P11_2026-10-24'))
from calcular_p11 import extract_geometry,write_json


def create_model(s,factor=2,kv_instant=None,degree=18):
    p=s['prateleira'];b=s['fundo']
    E=p['E_instantaneo_MPa']/factor
    kv=(s['rigidez_vertical_inst_requerida_N_mm'] if kv_instant is None else kv_instant)/factor
    kg=s['rigidez_grupo_fundo_lateral_inst_requerida_N_mm']/factor
    points=s['conectores_prateleira']['laterais']['pontos_x_y_mm']+s['conectores_prateleira']['fundo']['pontos_x_y_mm']
    back_x=[v[0] for v in s['conectores_prateleira']['fundo']['pontos_x_y_mm']]
    back_mass=b['largura_mm']*b['altura_mm']*b['espessura_para_massa_mm']*b['densidade_kg_m3']/1e9
    cb,vb,meta=back_compliance(E=E,Kg=kg,L=p['vao_x_mm'],h=b['altura_faixa_analitica_mm'],t=b['espessura_resistente_mm'],back_positions=back_x,self_mass_kg=back_mass)
    C=np.eye(len(points))/kv;C[4:,4:]+=cb;v0=np.r_[np.zeros(4),vb]
    model=setup(degree,E=E,nu=p['poisson_hipotese'],C=C,v0=v0,L=p['vao_x_mm'],B=p['profundidade_y_mm'],t=p['espessura_resistente_mm'],supports=points)
    return model,dict(factor=factor,connector_effective_K_N_mm=kv,back_group_effective_K_N_mm=kg,back=meta,C_mm_N=C.tolist(),v0_mm=v0.tolist())


def simplify(row):
    return {k:v for k,v in row.items() if k!='coefficients'}


def add_back_groups(row,s):
    xs=np.array([p[0] for p in s['conectores_prateleira']['fundo']['pontos_x_y_mm']]);L=s['prateleira']['vao_x_mm']
    b=s['fundo'];G=b['largura_mm']*b['altura_mm']*b['espessura_para_massa_mm']*b['densidade_kg_m3']/1e9*9.80665
    back=np.asarray(row['reactions_N'])[4:]
    row['back_side_group_reactions_N']=[float((1-xs/L)@back+G/2),float((xs/L)@back+G/2)]
    return row


def csv_write(path,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)


def nominal_maps(s):
    # Datum: xesquerda do vao, yfrenteprateleira, zfaceinferior da prateleira.
    points=s['conectores_prateleira'];rows=[]
    for n,(x,y) in enumerate(points['laterais']['pontos_x_y_mm'],1):
        rows.append(dict(id=f'P11-LAT-{n}',family='Minifix15+S100 existente',from_part='Peca335' if x==0 else 'Peca334',to_part='Peca339',x_mm=x,y_mm=y,z_mm=9,axis='X',quantity=1,notes='Posicao existente;caixaB34acessoinferior;nao somar aos12conjuntos ja listados'))
    for n,(x,y) in enumerate(points['fundo']['pontos_x_y_mm'],1):
        rows.append(dict(id=f'P11-TRAS-{n}',family='Confirmat7x50',from_part='Peca336',to_part='Peca339',x_mm=x,y_mm=y,z_mm=9,axis='Y',quantity=1,notes='Pela face posterior;insercao geometrica32mm nao roscaefetiva garantida;cabeca rente'))
    for n,x in enumerate(points['cavilhas_traseiras']['x_mm'],1):
        rows.append(dict(id=f'P11-CAV-{n}',family='Cavilha8x30',from_part='Peca336',to_part='Peca339',x_mm=x,y_mm=312,z_mm=9,axis='Y',quantity=1,notes='10no fundo+20prateleira;semcredito resistente adicional;controlarfolgaaxialepontabroca'))
    for side,x in [('esquerda',0),('direita',661)]:
        for n,z in enumerate(s['grupos_fundo_laterais']['z_desde_base_do_modulo_mm'],1):
            rows.append(dict(id=f'P11-FL-{side}-{n}',family='Confirmat7x50',from_part='Peca335' if side=='esquerda' else 'Peca334',to_part='Peca336',x_mm=x,y_mm=321,z_mm=z-276,axis='X',quantity=1,notes='Passagem na lateral para aresta dofundo;cabeca rente nafaceexterna;validarligamento juntoaresta traseira'))
    # Comprimentos de furacao so nominais; diametro piloto requer nucleo do parafuso real.
    csv_write(HERE/'Mapa_ligacoes_nominais.csv',rows)
    return rows


def build():
    s=json.loads((HERE/'Premissas.json').read_text(encoding='utf-8'))
    old=json.loads((ROOT/s['base_geometrica']).read_text(encoding='utf-8'))
    geometry=extract_geometry(old)
    p=s['prateleira'];own=p['vao_x_mm']*p['profundidade_y_mm']*p['espessura_para_massa_mm']*p['densidade_kg_m3']/1e9
    cases=[];models={};metas={}
    for factor in [1,2]:
        model,meta=create_model(s,factor);models[factor]=model;metas[str(factor)]=meta
        for mass in s['conteudo_kg']:
            for kind,cx,cy in [('uniform',330.5,156),('center',330.5,156),('front',330.5,30),('frontside',25,30)]:
                row=model.solve(mass,kind,cx,cy,stress=True,dead_kg=own)
                row['factor']=factor
                row['with_additional_reserve_mm']=row['max_deflection_mm']+p['reserva_adicional_mm']
                row['comparison_pass']=row['with_additional_reserve_mm']<=p['criterio_flecha_mm']
                add_back_groups(row,s);cases.append(simplify(row))
    model=models[2]
    # Propostas sao alternativas, nao pesos cumulativos.
    proposed=[]
    for mass,kind,cx,cy in [(10,'uniform',330.5,156),(6,'center',330.5,156),(3,'front',330.5,30),(3,'frontside',25,30)]:
        row=model.solve(mass,kind,cx,cy,stress=True,dead_kg=own);add_back_groups(row,s)
        row['with_additional_reserve_mm']=row['max_deflection_mm']+p['reserva_adicional_mm']
        row['comparison_pass']=row['with_additional_reserve_mm']<=p['criterio_flecha_mm']
        proposed.append(simplify(row))
        assert row['comparison_pass']
    # Caso misto: 3kgfrente+7kgdistribuidos, peso proprio/fundo contados uma vez.
    a=model.solve(7,'uniform',dead_kg=own);b=model.solve(3,'front',cy=30,dead_kg=own);zero=model.solve(0,'uniform',dead_kg=own)
    coeff=np.array(a['coefficients'])+b['coefficients']-zero['coefficients']
    W=model.evaluate(coeff,np.linspace(0,661,161),np.linspace(0,312,101))
    mixed=dict(distributed_kg=7,front_kg=3,total_content_kg=10,max_deflection_mm=float(W.max()),with_reserve_mm=float(W.max())+.2,comparison_pass=float(W.max())+.2<=p['criterio_flecha_mm'])
    # Limitesmatematicos: maxdeformacao e monotona neste carregamento positivo.
    limits=[]
    for kind,cy in [('uniform',156),('center',156),('front',30)]:
        lo,hi=0.,30.
        for _ in range(30):
            mid=(lo+hi)/2;res=model.solve(mid,kind,cy=cy,dead_kg=own)
            if res['max_deflection_mm']+.2<=p['criterio_flecha_mm']:lo=mid
            else:hi=mid
        limits.append(dict(kind=kind,content_limit_deflection_only_kg=(lo+hi)/2,status='Cruzamento dehipoteses; nao capacidade liberada'))
    sensitivity=[]
    for kv in [200,500,1000,2000]:
        mm,meta=create_model(s,2,kv_instant=kv,degree=16)
        row=mm.solve(10,'uniform',dead_kg=own)
        sensitivity.append(dict(instant_connector_K_N_mm=kv,effective_connector_K_N_mm=kv/2,back_group_effective_K_N_mm=meta['back_group_effective_K_N_mm'],deflection_mm=row['max_deflection_mm'],with_reserve_mm=row['max_deflection_mm']+.2))
    # Requisitosforcas: arredondar demandasmajoradas; nao afirmar resistencia de catalogo.
    force_values=np.array([x['reactions_N'] for x in proposed])
    group_values=np.array([x['back_side_group_reactions_N'] for x in proposed])
    demands=dict(lateral_max_abs_service_N=float(np.max(np.abs(force_values[:,:4]))),rear_max_abs_service_N=float(np.max(np.abs(force_values[:,4:]))),back_side_group_max_abs_service_N=float(np.max(np.abs(group_values))),
                 required_lateral_reversible_design_N=100,required_rear_reversible_design_N=100,required_back_side_group_design_N=150,
                 study_load_multiplier=2,inst_connector_K_required_N_mm=1000,inst_back_side_group_K_required_N_mm=1000,
                 source='Requisitos deprojeto a comprovar; nao resistencia publicada da ferragem')
    assert demands['lateral_max_abs_service_N']*2<=100
    assert demands['rear_max_abs_service_N']*2<=100
    assert demands['back_side_group_max_abs_service_N']*2<=150
    maps=nominal_maps(s)
    eq=max(max(abs(v) for v in row['equilibrium_error'].values()) for row in cases)
    assert eq<1e-6
    summary=[]
    for row in cases:
        if row['factor']==2 and row['kind']=='uniform':
            first=next(x for x in cases if x['factor']==1 and x['kind']=='uniform' and x['mass_kg']==row['mass_kg'])
            summary.append(dict(content_kg=row['mass_kg'],instant_mm=first['max_deflection_mm'],sustained_sensitivity_mm=row['max_deflection_mm'],with_reserve_mm=row['with_additional_reserve_mm'],comparison_pass=row['comparison_pass']))
    csv_write(HERE/'Resumo_cargas.csv',summary)
    reacs=[]
    for row in proposed:
        for i,R in enumerate(row['reactions_N']):
            reacs.append(dict(case=row['kind'],content_kg=row['mass_kg'],support=i+1,x_mm=model.supports[i,0],y_mm=model.supports[i,1],force_N=R,sign='Empurra para cima' if R>=0 else 'Retem para baixo'))
    csv_write(HERE/'Reacoes_propostas.csv',reacs)
    result=dict(revision='R00',settings=s,source_cad_sha256=geometry['sha256'],self_mass_shelf_kg=own,models=metas,cases=cases,summary=summary,proposed_cases=proposed,mixed_case=mixed,deflection_limits=limits,stiffness_sensitivity=sensitivity,connection_demands=demands,nominal_connections=maps,max_equilibrium_error=eq,
                decision='P11SEM TUBOS. Proposta condicional10kgdistribuidos,6kgcentraisou3kgfrente; modelosnao substituem dados da chapa/ligacoes e provaoficina',
                fabrication_released=False,cad_modified=False,
                limits=['Rigidezvertical1000N/mm e capacidades sao requisitossemcomprovacao na junta real','E/F2/nu sao hipoteses, sem garantia temporal','Apoiospontuais bilateralmente retidos; tensoeslocais singulares nao validadas','Ligacoes fundo-laterais e suas cabecas/passagens precisam de compatibilizacao','Nao contem suspensao,portas,conteudosoutrosnemancoragemparede'])
    write_json(HERE/'Resultados.json',result)
    return result,models


if __name__=='__main__':
    r,_=build()
    print(json.dumps({'summary':r['summary'],'limits':r['deflection_limits'],'proposed':[(x['mass_kg'],x['kind'],x['with_additional_reserve_mm']) for x in r['proposed_cases']],'connection_demands':r['connection_demands'],'released':False},ensure_ascii=True))
