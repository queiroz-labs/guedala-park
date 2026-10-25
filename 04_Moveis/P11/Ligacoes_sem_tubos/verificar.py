"""Verificacoes independentes do modelo ideal, nao da junta fisica."""
from pathlib import Path
import json
import math
import numpy as np
from numpy.polynomial.legendre import Legendre,leggauss
from placa_ritz import setup,back_compliance
from calcular import HERE,ROOT,create_model,write_json


def boundary_solution(n,nu,all_four=True):
    L=661.;B=312.;E=1100.;t=17.7;W=(20+L*B*18.3*800/1e9)*9.80665
    xi,wt=leggauss(n+6);s=Legendre([2/3,0,-2/3])
    X=[Legendre.basis(i)*s for i in range(n+1)]
    Y=[Legendre.basis(i)*(s if all_four else 1) for i in range(n+1)]
    def values(F,d=0):return np.array([f.deriv(d)(xi) for f in F])
    def gram(F,d,G,e):return (values(F,d)*wt)@values(G,e).T
    MX=gram(X,0,X,0);MY=gram(Y,0,Y,0);HX=gram(X,2,X,2);HY=gram(Y,2,Y,2)
    CX=gram(X,2,X,0);CY=gram(Y,2,Y,0);GX=gram(X,1,X,1);GY=gram(Y,1,Y,1)
    D=E*t**3/(12*(1-nu**2));fx=2/L;fy=2/B
    K=D*L*B/4*(fx**4*np.kron(HX,MY)+fy**4*np.kron(MX,HY)+nu*fx*fx*fy*fy*(np.kron(CX,CY.T)+np.kron(CX.T,CY))+2*(1-nu)*fx*fx*fy*fy*np.kron(GX,GY))
    F=W/4*np.kron(values(X)@wt,values(Y)@wt);scale=np.sqrt(np.diag(K))
    u=np.linalg.solve(K/scale[:,None]/scale[None,:],F/scale)/scale
    phi=np.kron([f(0) for f in X],[f(0) for f in Y])
    return float(phi@u)


def verify():
    s=json.loads((HERE/'Premissas.json').read_text(encoding='utf-8'))
    saved=json.loads((HERE/'Resultados.json').read_text(encoding='utf-8'))
    model,meta=create_model(s,2,degree=18)
    # Navier: controle4bordas apoiadas; esse NAO e o apoio doP11.
    L=661.;B=312.;E=1100.;t=17.7;nu=.3;W=(20+L*B*18.3*800/1e9)*9.80665
    D=E*t**3/(12*(1-nu*nu));q=W/L/B
    navier=16*q/(math.pi**6*D)*sum((-1)**((m+n-2)//2)/(m*n*((m/L)**2+(n/B)**2)**2) for m in range(1,202,2) for n in range(1,202,2))
    numerical=boundary_solution(10,.3,True)
    navier_error=abs(numerical/navier-1);assert navier_error<2e-6
    beam=5*W*L**3/(384*E*(B*t**3/12))
    beam_error=abs(boundary_solution(4,0,False)-beam);assert beam_error<1e-9
    # Fundo: integracao do trabalho virtual, independente da formulaGreen.
    cb,v0,back=back_compliance(E=1100,Kg=500)
    xs=[72,244,417,589];EI=1100*17.7*100**3/12;kgA=back['kGA_N'];KG=500
    nodes,weights=leggauss(6)
    def integrate(fun,breaks):
        return sum((hi-lo)/2*sum(w*fun((lo+hi)/2+(hi-lo)/2*x) for x,w in zip(nodes,weights)) for lo,hi in zip(breaks,breaks[1:]) if hi>lo)
    def moment(x,a):return (L-a)/L*x-max(x-a,0)
    def shear(x,a):return (L-a)/L-(1 if x>a else 0)
    error_c=0;error_v=0;G=back['self_mass_kg']*9.80665;qb=G/L
    for i,x in enumerate(xs):
        for j,a in enumerate(xs):
            actual=integrate(lambda z:moment(z,x)*moment(z,a)/EI+shear(z,x)*shear(z,a)/kgA,sorted(set([0,x,a,L])))
            actual+=((1-x/L)*(1-a/L)+(x/L)*(a/L))/KG
            error_c=max(error_c,abs(cb[i,j]-actual))
        own=integrate(lambda z:moment(z,x)*(qb*z*(L-z)/2)/EI+shear(z,x)*qb*(L/2-z)/kgA,sorted(set([0,x,L])))+G/(2*KG)
        error_v=max(error_v,abs(v0[i]-own))
    assert error_c<1e-12 and error_v<1e-12
    # Alternativa independente por eliminacao: molas apenas, semfundo acoplado.
    test=setup(10,E=1100,C=np.eye(8)/250)
    F=np.zeros(test.N);F[0]=W
    K=test.K+250*test.A.T@test.A;scale=np.sqrt(np.diag(K))
    direct=np.linalg.solve(K/scale[:,None]/scale[None,:],F/scale)/scale
    augmented=test.solve(20,'uniform')
    spring_error=float(np.max(np.abs(direct-augmented['coefficients'])));assert spring_error<1e-9
    # Convergencia na configuracao efetiva doP11.
    higher,_=create_model(s,2,degree=22)
    row18=model.solve(10,'uniform');row22=higher.solve(10,'uniform')
    conv=abs(row22['max_deflection_mm']-row18['max_deflection_mm']);assert conv<.002
    # Equilibrio do conjunto: chapa/conteudo+fundo, semduplicarRtraseiras.
    for row in saved['cases']:
        total=sum(row['reactions_N'][:4])+sum(row['back_side_group_reactions_N'])
        expected=(row['mass_kg']+saved['self_mass_shelf_kg']+back['self_mass_kg'])*9.80665
        assert abs(total-expected)<1e-6
        assert max(abs(v) for v in row['equilibrium_error'].values())<1e-6
        assert row['max_constraint_error_mm']<1e-7
    # Sensibilidadehomogenea2: seEetodasKcaemmetade, flechasduplicam.
    for row in saved['summary']:assert abs(row['sustained_sensitivity_mm']-2*row['instant_mm'])<1e-9
    # Esforcos propostos atendem REQUISITOS, nao capacidades de catalogo.
    demand=saved['connection_demands']
    assert 2*demand['lateral_max_abs_service_N']<=100
    assert 2*demand['rear_max_abs_service_N']<=100
    assert 2*demand['back_side_group_max_abs_service_N']<=150
    assert saved['mixed_case']['comparison_pass'] is False
    # Limites de geom nominal (nao testeBREP).
    rx=[72,244,417,589]
    assert min(rx[0],661-rx[-1])>=70
    assert min(abs(x-edge) for x in rx for edge in [34,627])>15/2+7/2
    for z in [90,305,520]:assert min(z-18,592-z)>=70
    assert min(abs(z-285) for z in [90,305,520])>=20
    old=json.loads((ROOT/s['base_geometrica']).read_text(encoding='utf-8'))
    import hashlib
    assert hashlib.sha256((ROOT/old['cad']).read_bytes()).hexdigest()==old['sha256_cad_esperado']
    report=dict(status='PASS',navier_control_relative_error=navier_error,beam_control_error_mm=beam_error,
                back_virtual_work_C_error_mm_N=error_c,back_virtual_work_self_error_mm=error_v,
                independent_spring_solver_error_mm=spring_error,degree18_to22_deflection_difference_mm=conv,
                equilibrium_cases=len(saved['cases']),CAD_unchanged=True,
                limits='Validacao do metodo e coordenadas nominais, sem prova fisica, colisaoBREP ou liberacao da carga')
    write_json(HERE/'Verificacao.json',report)
    print(json.dumps(report,ensure_ascii=True))


if __name__=='__main__':verify()
