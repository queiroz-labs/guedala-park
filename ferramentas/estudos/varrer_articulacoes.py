"""Extensao das amostras a solidos cujo Placement responde a controles reais."""
from pathlib import Path
import argparse,csv,hashlib,json
import numpy as np
from articulacoes_cinematica import XMLPlacements
from varrer_cinematica import transformed_box,distances,FIXED_ENVELOPES


def run(cad,snapshot,out):
    data=json.loads(snapshot.read_text(encoding='utf-8'));assert hashlib.sha256(cad.read_bytes()).hexdigest()==data['sha256']
    model=XMLPlacements(cad);g=data['geometry'];base=model.context({});mat0={};unsupported={}
    for n in g:
        try:mat0[n]=base(n)
        except (ValueError,SyntaxError) as e:unsupported[n]=str(e)
    controls=[tuple(v['expressions']['Abertura'].split('.')) for v in data['leaves'].values() if v['visible_effective']]
    controls += [('ControleCantoR35','AberturaA'),('ControleCantoR35','AberturaB')]
    controls += [(n,'Extensao') for n in data['drawers'] if n!='Gaveta007']
    memberships={};bycontrol={};validation=[];bodies={};deltas={}
    for ctrl in controls:
        maximum=data['drawers'][ctrl[0]]['course_mm'] if ctrl[1]=='Extensao' else 86
        world=model.context({ctrl:maximum});members=[]
        for n,m0 in mat0.items():
            try:changed=not np.allclose(world(n),m0,rtol=0,atol=1e-7)
            except (ValueError,SyntaxError) as e:
                unsupported[n]=str(e);continue
            if changed:members.append(n);memberships.setdefault(n,[]).append(ctrl)
        if not members:raise ValueError('Controle sem solidos moveis: '+'.'.join(ctrl))
        bycontrol['.'.join(ctrl)]=members
        states=list(range(0,int(maximum)+1,10)) if ctrl[1]=='Extensao' else list(range(87))
        if maximum not in states:states.append(maximum)
        matrices={n:[] for n in members}
        for state in states:
            w=model.context({ctrl:state})
            for n in members:matrices[n].append(w(n))
            if state in ([0,100,maximum] if ctrl[1]=='Extensao' else [0,45,86]):
                validation.append(dict(control=list(ctrl),value=state,matrices={n:w(n).reshape(-1).tolist() for n in members}))
        for n in members:
            if len(memberships[n])>1:raise ValueError('Solido depende de controles multiplos: '+n)
            inv=np.linalg.inv(mat0[n])
            deltas[n]=[(m@inv).reshape(-1).tolist() for m in matrices[n]]
            bodies[n]=dict(group='.'.join(ctrl),states=states,unit='mm' if ctrl[1]=='Extensao' else 'grau',
                boxes=np.array([transformed_box(g[n]['box_global_mm'],m@inv) for m in matrices[n]]))
    # Todo hardware de dobradica e da gaveta que nao mudou permanece no estado capturado.
    for n,v in g.items():
        if n not in bodies and (v['module'] is not None or n in FIXED_ENVELOPES or
                n.startswith(('FerragemComum','CalcoComum','FerragemVizinha','FerragemSimples')) or
                any(a in data['drawers'] and a!='Gaveta007' for a in v['ancestors'])):
            if any(a=='Gaveta007' for a in v['ancestors']):continue
            bodies[n]=dict(group='fixo',states=[0],unit='fixo',boxes=np.array([v['box_global_mm']]))
    rows=[];names=sorted(bodies);narrow=[];internal=[]
    for i,na in enumerate(names):
        a=bodies[na]
        for nb in names[i+1:]:
            b=bodies[nb]
            if a['group']=='fixo' and b['group']=='fixo':continue
            if a['group']==b['group']:
                ds=np.linalg.norm(np.maximum(np.maximum(a['boxes'][:,:3]-b['boxes'][:,3:],b['boxes'][:,:3]-a['boxes'][:,3:]),0),axis=1)
                k=int(np.argmin(ds));j=k;minimum=float(ds[k]);count=len(ds)
            else:
                ds=distances(a['boxes'],b['boxes']);k,j=np.unravel_index(np.argmin(ds),ds.shape);minimum=float(ds[k,j]);count=ds.size
            rows.append(dict(objeto_a=na,objeto_b=nb,grupo_a=a['group'],grupo_b=b['group'],
                limite_inferior_mm=round(minimum,6),estado_a=a['states'][k],estado_b=b['states'][j],
                unidade_a=a['unit'],unidade_b=b['unit'],candidato=minimum<1e-8,amostras=int(count)))
            if minimum<1e-8:
                shared=set(g[na]['ancestors']) & set(g[nb]['ancestors'])
                if any(n.startswith('Dobradica') for n in shared):
                    internal.append([na,nb]);continue
                if a['group']==b['group']:
                    indices=[[int(i),int(i)] for i in np.where(ds<1e-8)[0]]
                else:
                    indices=np.argwhere(ds<1e-8).tolist()
                narrow.append(dict(a=na,b=nb,indices=indices))
    out.mkdir(parents=True,exist_ok=True)
    with (out/'Pares_articulacoes.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
    (out/'Validacao_poses.json').write_text(json.dumps(dict(sha256=data['sha256'],poses=validation)),encoding='utf-8')
    (out/'Candidatos_articulados.json').write_text(json.dumps(dict(sha256=data['sha256'],pairs=narrow,internal_hinge_pairs=internal,
        bodies={n:dict(group=v['group'],states=v['states'],unit=v['unit'],deltas=deltas.get(n,[np.eye(4).reshape(-1).tolist()])) for n,v in bodies.items()})),encoding='utf-8')
    summary=dict(source_sha256=data['sha256'],controls=len(controls),bodies=len(bodies),moving_bodies=len(memberships),
        pairs=len(rows),candidates=sum(r['candidato'] for r in rows),unsupported=unsupported,control_members=bycontrol,
        table_sha256=hashlib.sha256((out/'Pares_articulacoes.csv').read_bytes()).hexdigest())
    (out/'Articulacoes_resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return {k:v for k,v in summary.items() if k!='control_members'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cad',type=Path,required=True);p.add_argument('--snapshot',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    assert not a.out.resolve().is_relative_to(Path(__file__).resolve().parents[2])
    print(json.dumps(run(a.cad,a.snapshot,a.out),ensure_ascii=False,indent=2))
