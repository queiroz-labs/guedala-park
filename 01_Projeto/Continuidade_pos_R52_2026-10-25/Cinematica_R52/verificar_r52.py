"""Read-only validation of the new snapshot against saved/native references."""
from pathlib import Path
import json,sys,math,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
OLD=HERE.parents[1]/'Cinematica_offline_2026-10-25'
sys.path.insert(0,str(OLD))
from cinematica import Engine,Context

engine=Engine(HERE/'Snapshot_R52.json')
old=json.loads((OLD/'Snapshot_R51.json').read_text(encoding='utf-8'))
assert all(engine.data[k]==old[k] for k in ['sheets','controls','leaves'])
reference=json.loads((HERE.parents[1]/'P04_P15_suspensao_2026-10-25/Geometria_e_portas_R51.json').read_text(encoding='utf-8'))
count=0;err=0.
for code,m in reference['modules'].items():
    for door in m['doors']:
        for pose in door['samples']:
            x,y,z=engine.centers(door['leaf'],pose['angle_deg'])[door['name']]
            uvz=[2872-y,7390-x,z-2132] if code=='P04' else [x-3563,7000-y,z-1650]
            err=max(err,max(abs(a-b) for a,b in zip(uvz,pose['center_uvz_mm'])));count+=1
assert count==522 and err<1e-7
extra=json.loads((OLD/'Referencia_nativa_R12.json').read_text(encoding='utf-8'))
extraerr=0.
for p in extra['poses']:
    center=engine.centers(p['leaf'],p['angle_deg'])[p['front']]
    extraerr=max(extraerr,max(abs(a-b) for a,b in zip(center,p['center_world_mm'])))
assert extraerr<1e-7
poses=0
for leaf in engine.leaf_names():
    for angle in range(87):
        mat=engine.placement(leaf,angle)
        assert np.isfinite(mat).all() and np.max(np.abs(mat[:3,:3].T@mat[:3,:3]-np.eye(3)))<1e-10
        assert abs(np.linalg.det(mat[:3,:3])-1)<1e-10;poses+=1
for forbidden in ["__import__('os')","open('arquivo')","(1).__class__"]:
    try:Context(engine,{}).expression(forbidden)
    except ValueError:pass
    else:raise AssertionError(forbidden)
cad=Path(engine.data['cad']);assert hashlib.sha256(cad.read_bytes()).hexdigest()==engine.data['sha256']
report={'source_sha256':engine.data['sha256'],'source_objects':engine.data['source_objects'],
    'R51_inputs_identical':True,'reference_poses':count+len(extra['poses']),'maximum_reference_error_mm':max(err,extraerr),
    'visible_leaves':len(engine.leaf_names()),'rotation_poses':poses,'source_unchanged':True,'passed':True,
    'scope':'R52 dataset validated; reuse of528 independent R51 native references justified by exact identity of all numerical inputs. Native R52 samples are checked separately.'}
(HERE/'Verificacao_offline_R52.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True))
