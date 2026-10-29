"""Valida as matrizes offline em poses nativas; restaura controles, nao salva."""
from pathlib import Path
import hashlib,json,os,sys,time
import FreeCAD as App
ROOT=Path(__file__).resolve().parents[2];OUT=Path(os.environ['GP_CINEMATICA_OUT']).resolve()
assert not OUT.is_relative_to(ROOT)
data=json.loads((OUT/'Validacao_poses.json').read_text());release=json.loads((ROOT/'ferramentas/site/current_release.json').read_text())
cad=ROOT/release['cadPath'];before=hashlib.sha256(cad.read_bytes()).hexdigest();assert before==data['sha256']
doc=App.openDocument(str(cad));results=[];start=time.time()
volumes={n:abs(doc.getObject(n).Shape.Volume) for p in data['poses'] for n in p['matrices']}
try:
    for pose in data['poses']:
        name,prop=pose['control'];o=doc.getObject(name);old=getattr(o,prop)
        try:
            setattr(o,prop,pose['value']);doc.recompute()
            errors=[]
            for n,expected in pose['matrices'].items():
                actual=doc.getObject(n).getGlobalPlacement().toMatrix().A
                error=max(abs(x-y) for x,y in zip(actual,expected))
                if abs(abs(doc.getObject(n).Shape.Volume)-volumes[n])>1e-5:
                    raise ValueError('Forma nao rigida durante movimento: '+n)
                errors.append((error,n))
            worst=max(errors,default=(0,None))
            results.append(dict(control=name+'.'+prop,value=pose['value'],matrices=len(errors),maximum_error=worst[0],worst_object=worst[1]))
        finally:
            setattr(o,prop,old);doc.recompute()
        if worst[0]>1e-6:break
finally:App.closeDocument(doc.Name)
assert hashlib.sha256(cad.read_bytes()).hexdigest()==before
report=dict(source_sha256=before,source_unchanged=True,poses=results,complete=len(results)==len(data['poses']),
    maximum_error=max((r['maximum_error'] for r in results),default=0),seconds=time.time()-start)
(OUT/'Validacao_nativa_articulacoes.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='poses'}),flush=True)
sys.stdout.flush();sys.stderr.flush();os._exit(0 if report['complete'] and report['maximum_error']<=1e-6 else 1)
