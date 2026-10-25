"""Conferencia independente por elementos finitos 1D e regressao historica.

Nao valida o movel real: testa a implementacao do modelo ideal.
Requer numpy, ja disponivel no ambiente de trabalho.
"""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
from calcular_p11 import HERE, ROOT, beam_case, build, limit_by_deflection, write_json


def fem(L,b,t,E,rho,m,kind,a_ratio=0.5,n=40,mass_thickness_mm=None):
    I=b*t**3/12
    ell=L/n
    mass_thickness_mm=t if mass_thickness_mm is None else mass_thickness_mm
    q=(L*b*mass_thickness_mm*rho/1e9)*9.80665/L
    if kind=='distribuida':
        q+=m*9.80665/L
    stiff=np.array([[12,6*ell,-12,6*ell], [6*ell,4*ell**2,-6*ell,2*ell**2],
                    [-12,-6*ell,12,-6*ell], [6*ell,2*ell**2,-6*ell,4*ell**2]],dtype=float)*E*I/ell**3
    force=np.array([q*ell/2,q*ell**2/12,q*ell/2,-q*ell**2/12])
    K=np.zeros((2*(n+1),2*(n+1)));F=np.zeros(2*(n+1))
    for i in range(n):
        ids=[2*i,2*i+1,2*i+2,2*i+3]
        K[np.ix_(ids,ids)]+=stiff
        F[ids]+=force
    if kind!='distribuida':
        index=round(n*a_ratio)
        assert math.isclose(index/n,a_ratio)
        F[2*index]+=m*9.80665
    fixed=[0,2*n]
    free=[i for i in range(len(F)) if i not in fixed]
    u=np.zeros(len(F));u[free]=np.linalg.solve(K[np.ix_(free,free)],F[free])
    residual=K@u-F
    return u[::2],-residual[0],-residual[2*n],np.max(np.abs(residual[free]))


def verify():
    results=build()
    verification=[]
    for E,t,rho,mass_t in [(2100,18,750,18),(2200,17.7,800,18.3),(1600,17.7,800,18.3)]:
        for mass in [0,5,10,20]:
            for kind,a in [('distribuida',0.5),('localizada_central',0.5),('localizada_quarto',0.25),('localizada_proxima_lateral',0.05)]:
                row=beam_case(661,312,t,E,rho,mass,kind,a_ratio=a,mass_thickness_mm=mass_t)
                displacements,left,right,residual=fem(661,312,t,E,rho,mass,kind,a,mass_thickness_mm=mass_t)
                # Compara todos os nos contra solucao por funcoes de Green e UDL.
                own=661*312*mass_t*rho/1e9*9.80665
                q=(own+(mass*9.80665 if kind=='distribuida' else 0))/661
                P=0 if kind=='distribuida' else mass*9.80665
                point=661*a;I=312*t**3/12;analytical=[]
                for x in np.linspace(0,661,len(displacements)):
                    udl=q*x*(661**3-2*661*x*x+x**3)/(24*E*I)
                    if x<=point:
                        concentrated=P*(661-point)*x*(661**2-(661-point)**2-x*x)/(6*661*E*I)
                    else:
                        concentrated=P*point*(661-x)*(661**2-point**2-(661-x)**2)/(6*661*E*I)
                    analytical.append(udl+concentrated)
                err=float(np.max(np.abs(displacements-analytical)))
                assert err<1e-7,(kind,err)
                assert abs(left-row['reaction_left_N'])<1e-7
                assert abs(right-row['reaction_right_N'])<1e-7
                assert abs(left+right-row['total_force_N'])<1e-7
                verification.append(dict(E_MPa=E,t_mm=t,rho_kg_m3=rho,content_kg=mass,type=kind,max_nodal_difference_mm=err,max_free_dof_residual_N_or_Nmm=float(residual)))
    # Comparacao com resultados historicos publicados arredondados a3 casas.
    for mass,rounded in [(5,0.901),(10,1.481),(20,2.639)]:
        value=beam_case(661,312,18,2100,750,mass,'distribuida')['max_deflection_mm']
        assert abs(value-rounded)<=0.0005
    for kind in ['distribuida','localizada_central']:
        limit=limit_by_deflection(661,312,17.7,2200,800,2,300,kind,18.3)
        value=beam_case(661,312,17.7,2200,800,limit,kind,mass_thickness_mm=18.3)['max_deflection_mm']*2
        assert abs(value-661/300)<1e-10
    # A formula da EPF escrita em massa deve coincidir com a implementacao.
    row=beam_case(661,312,18,2100,750,20,'distribuida')
    epf=5*(20+row['self_mass_kg'])*661**3*9.80665/(32*2100*312*18**3)
    assert abs(epf-row['max_deflection_mm'])<1e-12
    # Caso pontual sem peso proprio: PL3/(48EI) e simetria de reacoes.
    point=beam_case(661,312,18,2100,0,20,'localizada_central')
    assert abs(point['max_deflection_mm']-20*9.80665*661**3/(48*2100*point['I_mm4']))<1e-12
    # O ramo proximo da lateral deve produzir reacao maior que a central.
    edge=beam_case(661,312,17.7,2200,800,20,'localizada_proxima_lateral',a_ratio=0.05,mass_thickness_mm=18.3)
    assert edge['reaction_left_N']>200 and edge['reaction_right_N']<25
    # Casos mistos: soma de vetores FEM com peso proprio descontado uma vez.
    for mixed in results['mixed_load_cases']:
        dist=mixed['distributed_content_kg'];point=mixed['localized_content_kg']
        ud=fem(661,312,17.7,2200,800,dist,'distribuida',mass_thickness_mm=18.3)[0]
        up=fem(661,312,17.7,2200,800,point,'localizada_central',mass_thickness_mm=18.3)[0]
        u0=fem(661,312,17.7,2200,800,0,'distribuida',mass_thickness_mm=18.3)[0]
        assert abs((ud+up-u0)[20]-mixed['max_deflection_mm'])<1e-7
    assert results['mixed_load_cases'][0]['deflection_multiplier_2_mm']>661/300
    assert results['mixed_load_cases'][1]['deflection_multiplier_2_mm']<661/300
    settings=results['assumptions']
    assert hashlib.sha256((ROOT/settings['cad']).read_bytes()).hexdigest()==settings['sha256_cad_esperado']
    report=dict(status='PASS',fem_cases=len(verification),additional_mixed_cases=2,mesh_elements=40,
                method='Elementos de viga Euler-Bernoulli, matriz de rigidez e cargas consistentes; deslocamentos nodais e reacoes comparados com solucao analitica',
                max_nodal_difference_mm=max(x['max_nodal_difference_mm'] for x in verification),
                checks=['Regressao historica 5/10/20kg','Equacao EPF','PL3/48EI sem peso proprio','Equilibrio de forcas e assimetria','Inversao de limite L/300','Superposicao de casos mistos sem duplicar peso proprio','SHA256 CAD intacto'],cases=verification,
                scope='Conferencia do modelo matematico 1D, nao ensaio de chapa, conector, movel ou parede')
    write_json(HERE/'Verificacao_numerica.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},ensure_ascii=True))


if __name__=='__main__':
    verify()
