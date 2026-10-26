"""P08: limites estaticos de reacoes, sem presumir rigidez ou seis contatos iguais."""
from pathlib import Path
import csv, gzip, hashlib, itertools, json
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_Moveis/P08'
G=9.80665

def sha(p):return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n') if p.suffix in {'.py','.json','.md','.csv'} else p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    basepath=ROOT/'02_Modelo_3D/Base_verificacao.json.gz'
    base=json.loads(gzip.decompress(basepath.read_bytes()));objects=base['objetos']
    release=read(ROOT/'ferramentas/site/current_release.json')
    assert sha(ROOT/release['cadPath'])==base['sha256']
    woodnames=['PecaBaixaR13']+[f'PecaBaixaR{i:03}' for i in range(1,6)]
    wheel_names=[f'PecaBaixaR{i:03}' for i in [10,15,20,25,30,35]]
    wood=[]
    for name in woodnames:
        o=objects[name];b=o['caixa_global'];dims=np.array(b[3:])-b[:3]
        assert abs(float(np.prod(dims))-o['forma']['volume'])<1e-4
        wood.append({'name':name,'volume_mm3':o['forma']['volume'],'center_mm':((np.array(b[:3])+b[3:])/2).tolist(),'box_mm':b})
    wheels=[]
    for i,name in enumerate(wheel_names):
        b=objects[name]['caixa_global'];assert b[2]==0 and b[5]==30
        wheels.append({'id':f'R{i+1}','name':name,'contact_XY_mm':[(b[0]+b[3])/2,(b[1]+b[4])/2]})
    xy=np.array([w['contact_XY_mm'] for w in wheels]);origin=xy.mean(axis=0)
    # Coordenadas em metros e centradas evitam condicionamento numerico ruim.
    A=np.vstack([np.ones(6),((xy-origin)/1000).T])
    volume=sum(p['volume_mm3'] for p in wood)
    center=sum(np.array(p['center_mm'])*p['volume_mm3'] for p in wood)/volume
    # Limites do vao util: origem local X invertida em relacao ao global.
    positions={'centro':[2285.5,6709.0], 'frente_esquerda':[1692.,6506.],
               'frente_direita':[2879.,6506.], 'tras_esquerda':[1692.,6912.], 'tras_direita':[2879.,6912.]}
    cases=[]
    for rho in [650,800,900]:
        mass=volume*rho/1e9
        for load in [0,5,10,20]:
            for label,pos in positions.items():
                if load==0 and label!='centro':continue
                W=(mass+load)*G;cg=(mass*center[:2]+load*np.array(pos))/(mass+load)
                rhs=np.r_[W,W*(cg-origin)/1000]
                for removed in [None,*range(6)]:
                    available=[i for i in range(6) if i!=removed];vertices=[]
                    for triple in itertools.combinations(available,3):
                        m=A[:,triple]
                        if abs(np.linalg.det(m))<1e-10:continue
                        reaction=np.linalg.solve(m,rhs)
                        if min(reaction)<-1e-8:continue
                        v=np.zeros(6);v[list(triple)]=np.maximum(reaction,0)
                        if not any(np.max(np.abs(v-old))<1e-7 for old in vertices):vertices.append(v)
                    arr=np.array(vertices)
                    cases.append({'id':len(cases)+1,'rho_kg_m3':rho,'wood_mass_kg':mass,'payload_kg':load,
                        'payload_position':label,'payload_XY_mm':pos,'total_weight_N':W,'center_XY_mm':cg.tolist(),
                        'removed_contact':None if removed is None else wheels[removed]['id'],
                        'feasible_nonnegative_equilibrium':bool(vertices),
                        'min_reaction_N':None if not vertices else arr.min(axis=0).tolist(),
                        'max_reaction_N':None if not vertices else arr.max(axis=0).tolist(),
                        'vertices_N':[v.tolist() for v in vertices]})
    result={'scope':'Corpo rigido e contatos pontuais verticais; limites de equilibrio, nao previsao de reparticao ou capacidade',
        'cad_sha256':base['sha256'],'inputs':{basepath.relative_to(ROOT).as_posix():sha(basepath),Path(__file__).relative_to(ROOT).as_posix():sha(Path(__file__))},
        'wood':wood,'wood_volume_mm3':volume,'wood_center_mm':center.tolist(),'wheels':wheels,
        'unknown_masses':['rodizios','espacadores','fixadores','acabamentos adicionais','objetos reais'],
        'load_scope':'0/5/10/20 kg sao sensibilidades; nenhuma carga de uso definida ou aprovada',
        'cases':cases,'physical_tests_executed':0,'capacity_demonstrated':False}
    OUT.mkdir(exist_ok=True)
    (OUT/'Apoios.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (OUT/'Reacoes.csv').open('w',encoding='utf-8-sig',newline='') as f:
        fields=['caso','densidade','conteudo_kg','posicao','contato_excluido','equilibrio']+[f'R{i}_{bound}_N' for i in range(1,7) for bound in ['min','max']]
        w=csv.writer(f,delimiter=';');w.writerow(fields)
        for c in cases:
            values=[]
            for i in range(6):
                for bound in ['min','max']:values.append('' if c[f'{bound}_reaction_N'] is None else round(c[f'{bound}_reaction_N'][i],6))
            w.writerow([c['id'],c['rho_kg_m3'],c['payload_kg'],c['payload_position'],c['removed_contact'] or '',c['feasible_nonnegative_equilibrium'],*values])
    print(json.dumps({'cases':len(cases),'without_equilibrium':sum(not c['feasible_nonnegative_equilibrium'] for c in cases),'wood_volume_L':volume/1e6,'center':center.tolist(),'largest_reaction_N':max(max(c['max_reaction_N']) for c in cases if c['max_reaction_N'])}))

if __name__=='__main__':main()
