"""BREP em copias rigidas validadas, fora do interior de uma mesma dobradica."""
from pathlib import Path
import hashlib,json,os,sys,time
import FreeCAD as App
from resumir_articulacoes import native_pairs
ROOT=Path(__file__).resolve().parents[2];OUT=Path(os.environ['GP_CINEMATICA_OUT']).resolve()
assert not OUT.is_relative_to(ROOT)
data=json.loads((OUT/'Candidatos_articulados.json').read_text());valid=json.loads((OUT/'Validacao_nativa_articulacoes.json').read_text())
assert valid['complete'] and valid['maximum_error']<1e-6 and valid['source_sha256']==data['sha256']
release=json.loads((ROOT/'ferramentas/site/current_release.json').read_text());cad=ROOT/release['cadPath']
before=hashlib.sha256(cad.read_bytes()).hexdigest();assert before==data['sha256']
native=json.loads((OUT/'Retrato_nativo_R54.json').read_text());assert native['sha256']==before
old=native_pairs(native,before)
previous={};previous_inputs={};cache_hash=None;reused=0
if os.environ.get('GP_CINEMATICA_CACHE'):
    path=Path(os.environ['GP_CINEMATICA_CACHE'])
    cached=json.loads(path.read_text(encoding='utf-8'))
    assert cached['source_sha256']==before==cached['inputs']['sha256']
    previous={(p['a'],p['b']):p for p in cached['pairs']}
    previous_inputs=cached['inputs']
    previous_candidates={(p['a'],p['b']):p for p in previous_inputs['pairs']}
    cache_hash=hashlib.sha256(path.read_bytes()).hexdigest()
doc=App.openDocument(str(cad));base={};cache={};start=time.time();results=[]


def shape(name,index):
    key=(name,index)
    if key in cache:return cache[key]
    if name not in base:
        o=doc.getObject(name);s=o.Shape.copy()
        s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);base[name]=s
    s=base[name].copy();matrix=App.Matrix(*data['bodies'][name]['deltas'][index])
    s.Placement=App.Placement(matrix).multiply(s.Placement);cache[key]=s
    return s


try:
    for pair in data['pairs']:
        a,b=pair['a'],pair['b']
        if ((a,b) in previous and previous_candidates[a,b]==pair and
            all(previous_inputs['bodies'][n]==data['bodies'][n] for n in (a,b))):
            results.append(previous[a,b]);reused+=1
            continue
        initial=abs(shape(a,0).common(shape(b,0)).Volume)
        first=None;checked=0;touch=None
        if initial<=0.01:
            for ia,ib in pair['indices']:
                sa,sb=shape(a,ia),shape(b,ib);gap=float(sa.distToShape(sb)[0]);checked+=1
                if gap>1e-7:continue
                volume=abs(sa.common(sb).Volume)
                if volume>0.01:
                    first=dict(state_a=data['bodies'][a]['states'][ia],state_b=data['bodies'][b]['states'][ib],intersection_mm3=volume);break
                if touch is None:touch=[data['bodies'][a]['states'][ia],data['bodies'][b]['states'][ib]]
        results.append(dict(a=a,b=b,initial_intersection_mm3=initial,first_positive=first,
            checked_candidate_states=checked,candidate_states=len(pair['indices']),contact_sample=touch,
            pair_already_native=tuple(sorted([a,b])) in old,
            new_pair=bool(first and tuple(sorted([a,b])) not in old)))
        if len(results) % 25 == 0:
            progress=dict(complete=False,source_sha256=before,seconds=time.time()-start,pairs=results,total_pairs=len(data['pairs']))
            (OUT/'BREP_articulacoes_parcial.json').write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
            print('Pares conferidos: %s/%s' % (len(results),len(data['pairs'])),flush=True)
finally:App.closeDocument(doc.Name)
assert hashlib.sha256(cad.read_bytes()).hexdigest()==before
report=dict(source_sha256=before,source_unchanged=True,seconds=time.time()-start,pairs=results,
    reused_pairs_with_identical_inputs=reused,previous_cache_sha256=cache_hash,
    internal_hinge_pairs_excluded=len(data['internal_hinge_pairs']),
    limitation='Intersecoes ja presentes no estado inicial nao reavaliadas; pares internos da mesma dobradica excluidos. Para demais pares, encerra ao confirmar primeira penetracao amostrada; nao mede maxima penetracao nem continuidade.')
(OUT/'BREP_articulacoes.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(pairs=len(results),initial=sum(r['initial_intersection_mm3']>0.01 for r in results),
    positive=sum(bool(r['first_positive']) for r in results),new=sum(r['new_pair'] for r in results),seconds=report['seconds'],source_unchanged=True)),flush=True)
sys.stdout.flush();sys.stderr.flush();os._exit(0)
