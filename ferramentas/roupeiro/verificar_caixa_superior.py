"""Verificacao independente: equilibrio dos certificados e geometria das juntas.

Nao importa o resolvedor nem presume capacidade das chapas/conectores.
"""
from pathlib import Path
import hashlib
import json
import math

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_Moveis/Proximas_decisoes/P01_P03'
gp=OUT/'Geometria_P02_individual.json'
D=json.loads(gp.read_text(encoding='utf-8'))
R=json.loads((OUT/'Resultados_topologia.json').read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert R['geometry_sha256']==sha(gp)
assert sha(ROOT/D['source'])==R['source_sha256']==D['source_sha256']
checks=[]

def close(a,b,tol=1e-6):
    assert abs(a-b)<tol,(a,b)


max_force=max_moment=0.
infeasible=coupled=certificates=0
for c in R['cases']:
    for key,loads,total_key in [('P02_compression_only',c['P02_loads'],'P02_total'),
                                ('coupled_necessary_cut',c['P02_loads']+c['P03_loads'],'coupled_total')]:
        sol=c[key]
        mass=sum(r['mass_kg'] for r in loads)
        cg=[sum(r['mass_kg']*r['com_mm'][i] for r in loads)/mass for i in range(3)]
        close(mass,c[total_key]['mass_kg'])
        for i in range(3):close(cg[i],c[total_key]['com_mm'][i])
        if not sol['feasible']:
            assert key=='P02_compression_only'
            points=[p for f in D['variants'][c['variant']]['contacts'] if f['axis']==2 and
                    abs(f['center_mm'][2]-2132)<1e-6 and
                    ((f['a'] in {n for n,r in D['panels'].items() if r['module']=='P02'} and D['panels'][f['b']]['module']=='P01') or
                     (f['b'] in {n for n,r in D['panels'].items() if r['module']=='P02'} and D['panels'][f['a']]['module']=='P01'))
                    for p in f['vertices_mm']]
            ymin=min(p[1] for p in points)
            assert cg[1]<ymin
            close(mass*9.80665*(ymin-cg[1])/1000,sol['minimum_resisting_wrench_about_front_Nm'])
            infeasible+=1
            continue
        force=sum(r['force_z_N'] for r in sol['witness'])
        mx=sum((r['point_mm'][1]-3290)*r['force_z_N'] for r in sol['witness'])
        my=-sum((r['point_mm'][0]-7000)*r['force_z_N'] for r in sol['witness'])
        target=mass*9.80665
        max_force=max(max_force,abs(force-target))
        max_moment=max(max_moment,abs(mx-target*(cg[1]-3290)),abs(my+target*(cg[0]-7000)))
        close(force,target,1e-5)
        close(mx,target*(cg[1]-3290),1e-4)
        close(my,-target*(cg[0]-7000),1e-4)
        for w in sol['witness']:
            assert w['force_z_N']>=-1e-7
            assert any(f['a'] in (w['lower'],w['upper']) and f['b'] in (w['lower'],w['upper']) and
                       any(math.dist(w['point_mm'],p)<1e-6 for p in f['vertices_mm'])
                       for f in D['variants'][c['variant']]['contacts'])
        certificates+=1
        coupled+=key=='coupled_necessary_cut'
assert len(R['cases'])==81 and infeasible==9 and coupled==81 and certificates==153
checks.append('81 casos: 153 certificados compressivos e nove separacoes pelo CG conferidos independentemente')

for v in D['variants'].values():
    assert not v['positive_intersections']
    c01=[c for c in v['contacts'] if {c['a'],c['b']}=={'Peca259','LateralApoioPrincipal'}]
    assert len(c01)==1
    close(c01[0]['area_mm2'],612*272)
    for station in R['C01_study_stations']:
        a,b=station['start_mm'],station['end_mm']
        close(a[0],6722);close(b[0],6758)
        assert 3310<a[1]<3922 and 2150<a[2]<2422
        assert a[1:]==b[1:]
checks.append('C01: quatro eixos dentro da face612x272; sem quantitativo ou usinagem liberados')

for v in D['variants'].values():
    e=[c for c in v['edge_only'] if {c['a'],c['b']}=={'Peca255','Peca256'}]
    assert len(e)==1
    close(e[0]['length_mm'],272)
    assert not any({c['a'],c['b']}=={'Peca255','Peca256'} for c in v['contacts'])
new=D['variants']['caixa_fechada_ESTUDO']
old=D['variants']['traseiro_ESTUDO']
close(new['bodies']['Peca263']['volume_mm3']-old['bodies']['Peca263']['volume_mm3'],1314*18*18)
c=[c for c in new['contacts'] if {c['a'],c['b']}=={'Peca261','Peca263'}]
assert len(c)==1;close(c[0]['area_mm2'],1314*18)
assert not any({c['a'],c['b']}=={'Peca261','Peca263'} for c in old['contacts'])
checks.append('TopoP03: acrescimo18 cria face23652mm2; fundosP02 continuam somente com aresta272')

# Independente do recorte BREP: no y<3290, retorno do L =230x400;
# fundo de retorno =18x400x272; apoio da portaB=212x18x272;
# faixaB e folhaB inteiras. A massa e o momento devem coincidir.
for s in R['return_sections']:
    rho=s['rho_hypothesis_kg_m3'];kg=s['content_tip_kg']
    pp=[(230*400*18,3090.),(230*400*18,3090.),(18*400*272,3090.),
        (212*18*272,2899.)]
    for n in ['FaixaQuinaBR04','FrenteSimplesR001']:
        pp.append((D['panels'][n]['volume_mm3'],D['panels'][n]['com_mm'][1]))
    w=sum(vol*rho/1e9*9.80665 for vol,y in pp)+kg*9.80665
    m=sum(vol*rho/1e9*9.80665*(3290-y)/1000 for vol,y in pp)+kg*9.80665*.370
    close(w,s['weight_forward_N'])
    close(m,s['moment_x_at_cut_Nm'])
checks.append('Nove cortes do retorno conferidos por volumes analiticos e soma de momentos')

out=dict(status='OK',checks=checks,cases=81,compression_certificates=certificates,
         P02_infeasible_compression_only=infeasible,coupled_necessary_cuts=coupled,
         max_force_residual_N=max_force,max_moment_residual_Nmm=max_moment,
         source_unchanged=True,source_sha256=D['source_sha256'],
         limitations=['Aritmetica/geometria verificadas; nao e demonstracao de rigidez/capacidade.',
                      'Novas geometrias verificadas somente contra os22paineis selecionados; demais componentes nao conferidos.'])
(OUT/'Verificacao_topologia.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
