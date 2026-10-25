from pathlib import Path
import json,sys,hashlib,re,os,traceback
import FreeCAD as App
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'Cinematica_offline_2026-10-25'))
from cinematica import Engine

try:
    e=Engine(HERE/'Snapshot_R52.json');cad=Path(e.data['cad']);sha=hashlib.sha256(cad.read_bytes()).hexdigest()
    assert sha==e.data['sha256'];d=App.openDocument(str(cad));rows=[]
    def world_cg(o):
        s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement)
        v=sum(q.Volume for q in s.Solids)
        return sum((q.CenterOfMass*q.Volume for q in s.Solids),App.Vector())/v
    for n in e.leaf_names():
        control,prop=re.fullmatch(r'(\w+)\.(\w+)',e.data['leaves'][n]['expressions']['Abertura']).groups()
        obj=d.getObject(control);original=getattr(obj,prop).Value
        for angle in [0,45,86]:
            setattr(obj,prop,angle);d.recompute();expected=e.centers(n,angle)
            for front in e.data['leaves'][n]['fronts']:
                c=world_cg(d.getObject(front['name']));actual=[c.x,c.y,c.z];err=max(abs(a-b) for a,b in zip(actual,expected[front['name']]))
                assert err<1e-7,(n,angle,err)
                rows.append({'leaf':n,'front':front['name'],'angle':angle,'error_mm':err})
        setattr(obj,prop,original);d.recompute()
    assert not any('Invalid' in o.State or 'Error' in o.State for o in d.Objects)
    App.closeDocument(d.Name);assert hashlib.sha256(cad.read_bytes()).hexdigest()==sha
    (HERE/'Verificacao_nativa_R52.json').write_text(json.dumps({'source_sha256':sha,'poses':len(rows),'max_error_mm':max(r['error_mm'] for r in rows),'source_unchanged':True,'passed':True,'samples':rows},ensure_ascii=False,indent=2),encoding='utf-8')
except BaseException:(HERE/'Erro_nativo_R52.json').write_text(traceback.format_exc(),encoding='utf-8')
sys.stdout.flush();sys.stderr.flush();os._exit(0)
