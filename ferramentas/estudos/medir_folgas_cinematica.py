"""Menor distancia BREP nas amostras, usando caixas como limites inferiores.

Nao garante trajetoria continua; nao mede profundidade de penetracao.
"""
from pathlib import Path
import argparse
import csv
import functools
import hashlib
import json
import time
import numpy as np
from varrer_cinematica import transformed_box, distances

ROOT = Path(__file__).resolve().parents[2]


def oriented_lower_bound(box_a, transforms_a, box_b, transforms_b, synchronized=False):
    """Separacao projetada nos seis eixos das caixas orientadas: limite inferior."""
    a,b=np.asarray(box_a),np.asarray(box_b)
    ma,mb=np.asarray(transforms_a).reshape(-1,4,4),np.asarray(transforms_b).reshape(-1,4,4)
    ea,eb=(a[3:]-a[:3])/2,(b[3:]-b[:3])/2
    ca=np.einsum('nij,j->ni',ma[:,:3,:3],(a[3:]+a[:3])/2)+ma[:,:3,3]
    cb=np.einsum('nij,j->ni',mb[:,:3,:3],(b[3:]+b[:3])/2)+mb[:,:3,3]
    ra,rb=ma[:,:3,:3],mb[:,:3,:3]
    if synchronized:
        delta=cb-ca
        rotation=np.abs(np.einsum('nik,nil->nkl',ra,rb))
        ga=np.abs(np.einsum('ni,nik->nk',delta,ra))-ea-np.einsum('nkl,l->nk',rotation,eb)
        gb=np.abs(np.einsum('ni,nil->nl',delta,rb))-eb-np.einsum('nkl,k->nl',rotation,ea)
    else:
        delta=cb[None,:,:]-ca[:,None,:]
        rotation=np.abs(np.einsum('nik,mil->nmkl',ra,rb))
        ga=np.abs(np.einsum('nmi,nik->nmk',delta,ra))-ea-np.einsum('nmkl,l->nmk',rotation,eb)
        gb=np.abs(np.einsum('nmi,mil->nml',delta,rb))-eb-np.einsum('nmkl,k->nml',rotation,ea)
    return np.maximum(0,np.maximum(ga.max(axis=-1),gb.max(axis=-1))-1e-6)


def bounded_search(bounds, evaluate, tolerance=1e-7, max_calls=None, max_seconds=None):
    """Intervalo certificado; limite de tempo cooperativo entre chamadas nativas."""
    flat = np.asarray(bounds).reshape(-1)
    if not len(flat) or not np.all(np.isfinite(flat)) or np.any(flat < 0):
        raise ValueError('Limites invalidos')
    best, index, calls = float('inf'), None, 0
    started=time.monotonic();complete=True;lower=None
    for i in np.argsort(flat):
        if flat[i] >= best - tolerance:
            break
        if calls and ((max_calls is not None and calls>=max_calls) or
                      (max_seconds is not None and time.monotonic()-started>=max_seconds)):
            complete=False;lower=min(best,float(flat[i]));break
        value = float(evaluate(int(i)))
        if not np.isfinite(value) or value < -tolerance or value + tolerance < flat[i]:
            raise ValueError('Distancia invalida ou menor que limite conservador')
        calls += 1
        if value < best:
            best, index = max(0.0, value), int(i)
        if best <= tolerance:
            break
    return dict(upper=best,index=index,calls=calls,complete=complete,lower=best if complete else lower)


def bounded_minimum(bounds, evaluate, tolerance=1e-7):
    result=bounded_search(bounds,evaluate,tolerance)
    return result['upper'],result['index'],result['calls']


def run(out):
    import FreeCAD as App
    import os
    near_threshold = float(os.environ.get('GP_FOLGA_MAX_MM','25'))
    part = int(os.environ.get('GP_FOLGA_PART','0'))
    parts = int(os.environ.get('GP_FOLGA_PARTS','1'))
    max_calls=int(os.environ.get('GP_FOLGA_CALLS','32'))
    max_seconds=float(os.environ.get('GP_FOLGA_SECONDS','2'))
    assert max_calls>=1 and max_seconds>=0
    assert 0 <= part < parts
    resume_path = os.environ.get('GP_FOLGA_RESUME')
    resume_keys = set()
    if resume_path:
        with Path(resume_path).open(encoding='utf-8',newline='') as f:
            resume_keys = {(r['objeto_a'],r['objeto_b']) for r in csv.DictReader(f,delimiter=';')}
    out = out.resolve()
    assert not out.is_relative_to(ROOT)
    release = json.loads((ROOT/'ferramentas/site/current_release.json').read_text())
    cad = ROOT/release['cadPath']
    before = hashlib.sha256(cad.read_bytes()).hexdigest()
    blocked_path=out/'Folgas_bloqueadas.json'
    blocked=json.loads(blocked_path.read_text(encoding='utf-8-sig')) if blocked_path.exists() else []
    if isinstance(blocked,dict):blocked=[blocked]
    assert all(p['source_sha256']==before for p in blocked)
    blocked_keys={(p['a'],p['b']) for p in blocked}
    if resume_path:
        resume_meta=json.loads(Path(resume_path+'.json').read_text())
        assert resume_meta['source_sha256']==before
        assert resume_meta['file_sha256']==hashlib.sha256(Path(resume_path).read_bytes()).hexdigest()
    data = json.loads((out/'Candidatos_articulados.json').read_text())
    snapshot = json.loads((out/'Snapshot.json').read_text())
    brep = json.loads((out/'BREP_articulacoes.json').read_text())
    native = json.loads((out/'Validacao_nativa_articulacoes.json').read_text())
    assert before == data['sha256'] == snapshot['sha256'] == brep['source_sha256'] == native['source_sha256']
    assert native['complete'] and native['maximum_error'] < 1e-6
    bodies = data['bodies']
    for body in bodies.values():
        rotations=np.asarray(body['deltas']).reshape(-1,4,4)[:,:3,:3]
        assert np.all(np.isfinite(rotations))
        assert np.allclose(np.einsum('nik,nil->nkl',rotations,rotations),np.eye(3),rtol=0,atol=1e-10)
        assert np.allclose(np.linalg.det(rotations),1,rtol=0,atol=1e-10)
    boxes = {n: np.array([transformed_box(snapshot['geometry'][n]['box_global_mm'], np.array(m).reshape(4,4))
                         for m in b['deltas']]) for n,b in bodies.items()}
    excluded = {tuple(sorted(p)) for p in data['internal_hinge_pairs']}
    witnesses = {}
    for p in brep['pairs']:
        if p['initial_intersection_mm3'] > 0.01:
            witnesses[p['a'], p['b']] = (0, 0)
        elif p['first_positive']:
            witnesses[p['a'], p['b']] = (p['first_positive']['state_a'], p['first_positive']['state_b'])
    doc = App.openDocument(str(cad))
    bases = {}
    active_path=out/('Folga_ativa_%s.json'%part)
    def active(phase, **extra):
        active_path.write_text(json.dumps(dict(pid=os.getpid(),partition=part,source_sha256=before,phase=phase,time=time.time(),**extra)),encoding='utf-8')

    @functools.lru_cache(maxsize=2048)
    def shape(name, index):
        if name not in bases:
            o = doc.getObject(name)
            s = o.Shape.copy()
            s.Placement = o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement)
            bases[name] = s
        s = bases[name].copy()
        s.Placement = App.Placement(App.Matrix(*bodies[name]['deltas'][index])).multiply(s.Placement)
        return s

    def native_distance(a,ia,b,ib):
        active('native_distance',a=a,b=b,state_a=bodies[a]['states'][ia],state_b=bodies[b]['states'][ib])
        value=float(shape(a,ia).distToShape(shape(b,ib))[0])
        active('between_calls',a=a,b=b)
        return value

    started = time.time()
    count = calls = zeros = omitted = exact_count = interval_count = near_processed = 0
    result = out/('Folgas_BREP.csv' if parts == 1 else 'Folgas_parte_%s.csv' % part)
    try:
        with (out/'Pares_articulacoes.csv').open(newline='') as source, result.open('w',newline='',encoding='utf-8') as target:
            writer = csv.writer(target, delimiter=';')
            writer.writerow(['objeto_a','objeto_b','distancia_minima_amostrada_mm','estado_a','unidade_a','estado_b','unidade_b','avaliacoes_BREP','prova_zero','limite_inferior_caixas_mm','cobertura','limite_inferior_certificado_mm','limite_superior_amostrado_mm'])
            for ordinal,row in enumerate(csv.DictReader(source, delimiter=';')):
                a,b = row['objeto_a'],row['objeto_b']
                if ordinal % parts != part or (a,b) in resume_keys:continue
                if tuple(sorted((a,b))) in excluded:
                    omitted += 1
                    continue
                if (a,b) in blocked_keys:
                    writer.writerow([a,b,'',row['estado_a'],row['unidade_a'],row['estado_b'],row['unidade_b'],0,'',row['limite_inferior_mm'],'pendente: chamada nativa excedeu 60 s',max(0,float(row['limite_inferior_mm'])-1e-6),''])
                    target.flush();count+=1
                    continue
                if float(row['limite_inferior_mm']) > near_threshold:
                    writer.writerow([a,b,'',row['estado_a'],row['unidade_a'],row['estado_b'],row['unidade_b'],0,'',row['limite_inferior_mm'],'somente limite inferior AABB',max(0,float(row['limite_inferior_mm'])-1e-6),''])
                    count += 1
                    continue
                witness = witnesses.get((a,b))
                complete=True
                if witness is not None:
                    minimum, sa, sb, ncall = 0.0, *witness, 0
                elif bodies[a]['group'] == bodies[b]['group'] and bodies[a]['deltas'] == bodies[b]['deltas']:
                    # Mesma isometria em cada amostra conserva a distancia relativa.
                    minimum = native_distance(a,0,b,0)
                    sa,sb,ncall = bodies[a]['states'][0],bodies[b]['states'][0],1
                else:
                    ba,bb = boxes[a],boxes[b]
                    synchronized = bodies[a]['group'] == bodies[b]['group']
                    if synchronized:
                        bounds = np.linalg.norm(np.maximum(np.maximum(ba[:,:3]-bb[:,3:],bb[:,:3]-ba[:,3:]),0),axis=1)
                    else:
                        bounds = distances(ba,bb)
                    obb=oriented_lower_bound(snapshot['geometry'][a]['box_global_mm'],bodies[a]['deltas'],
                                             snapshot['geometry'][b]['box_global_mm'],bodies[b]['deltas'],synchronized)
                    bounds=np.maximum(bounds,obb)
                    def indices(k):
                        return (k,k) if synchronized else np.unravel_index(k,bounds.shape)
                    def evaluate(k):
                        ia,ib = indices(k)
                        return native_distance(a,int(ia),b,int(ib))
                    search=bounded_search(bounds,evaluate,max_calls=max_calls,max_seconds=max_seconds)
                    minimum,k,ncall=search['upper'],search['index'],search['calls']
                    complete=search['complete'];lower=search['lower']
                    ia,ib = indices(k)
                    sa,sb = bodies[a]['states'][ia],bodies[b]['states'][ib]
                if complete:lower=minimum
                writer.writerow([a,b,format(minimum,'.9f') if complete else '',sa,bodies[a]['unit'],sb,bodies[b]['unit'],ncall,'volume comum confirmado' if witness else '',row['limite_inferior_mm'],'minimo BREP amostrado' if complete else 'intervalo: limite de tempo/avaliacoes',format(lower,'.9f'),format(minimum,'.9f')])
                target.flush();active('pair_done',a=a,b=b)
                count += 1
                exact_count += complete
                interval_count += not complete
                near_processed += 1
                calls += ncall
                zeros += complete and minimum <= 1e-7
                if near_processed % 25 == 0:
                    target.flush()
                    print('Folgas: %s pares; %s minimos; %s distancias BREP; %s intervalos' % (count,exact_count,calls,interval_count),flush=True)
    finally:
        App.closeDocument(doc.Name)
    assert hashlib.sha256(cad.read_bytes()).hexdigest() == before
    summary = dict(source_sha256=before, source_unchanged=True, pairs=count, exact_distance_calls=calls,
                   partition=part,partitions=parts,resume_sha256=hashlib.sha256(Path(resume_path).read_bytes()).hexdigest() if resume_path else None,
                   pairs_with_exact_minimum=exact_count, near_pair_threshold_mm=near_threshold,
                   pairs_with_interval=interval_count,max_calls_per_pair=max_calls,cooperative_seconds_per_pair=max_seconds,
                   zero_distance_pairs=zeros, internal_hinge_pairs_excluded=omitted, seconds=time.time()-started,
                   tolerance_mm=1e-7, table_sha256=hashlib.sha256(result.read_bytes()).hexdigest(),
                   limit='Minimos certificados ou intervalos nos pares proximos; demais conservam limite inferior. Busca limitada a 32 avaliacoes/2 s entre chamadas; chamada nativa interrompida por supervisor apos 60 s fica pendente. Amostras 1 grau/10 mm, sem continuidade.')
    summary_path=out/('Folgas_resumo.json' if parts == 1 else 'Folgas_parte_%s.json' % part)
    summary_path.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    active('complete')
    print(json.dumps(summary,ensure_ascii=False),flush=True)


if __name__ == '__main__':
    import os
    run(Path(os.environ['GP_CINEMATICA_OUT']))
    os._exit(0)
