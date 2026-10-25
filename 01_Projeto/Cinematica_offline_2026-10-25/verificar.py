"""Compara com522 poses nativas independentes ja salvas, sem chamarFreeCAD."""
from pathlib import Path
import json,math,time,hashlib
import numpy as np
from cinematica import Engine,Context
HERE=Path(__file__).resolve().parent
engine=Engine();refpath=HERE.parent/'P04_P15_suspensao_2026-10-25/Geometria_e_portas_R51.json'
ref=json.loads(refpath.read_text(encoding='utf8'))
assert engine.data['sha256']==ref['sha256']
maxerr=0.;checks=0;closederr=0.
for n,leaf in engine.data['leaves'].items():
 actual=engine.centers(n,0.,include_hidden=True)
 for f in leaf['fronts']:
  closederr=max(closederr,max(abs(a-b) for a,b in zip(actual[f['name']],f['source_global_center_mm'])))
for code,module in ref['modules'].items():
 for door in module['doors']:
  for pose in door['samples']:
   x,y,z=engine.centers(door['leaf'],pose['angle_deg'])[door['name']]
   uvz=[2872-y,7390-x,z-2132] if code=='P04' else [x-3563,7000-y,z-1650]
   maxerr=max(maxerr,max(abs(a-b) for a,b in zip(uvz,pose['center_uvz_mm'])));checks+=1
assert checks==522 and maxerr<1e-7 and closederr<1e-7,(checks,maxerr,closederr)
extra_path=HERE/'Referencia_nativa_R12.json';extra=json.loads(extra_path.read_text(encoding='utf8'))
assert extra['source_sha256']==engine.data['sha256']
extra_error=0.
for p in extra['poses']:
 c=engine.centers(p['leaf'],p['angle_deg'])[p['front']]
 extra_error=max(extra_error,max(abs(a-b) for a,b in zip(c,p['center_world_mm'])))
assert len(extra['poses'])==6 and extra_error<1e-7
# Todas as22 folhas visiveis, incluindo as nao pertencentes ao comparativo522.
poses=0
for n in engine.leaf_names():
 for angle in range(87):
  mat=engine.placement(n,angle)
  assert np.isfinite(mat).all()
  assert np.max(np.abs(mat[:3,:3].T@mat[:3,:3]-np.eye(3)))<1e-10
  assert abs(np.linalg.det(mat[:3,:3])-1)<1e-10;poses+=1
# Recusar comandos/atributosPython fora da aritmetica extraida.
for forbidden in ["__import__('os')","open('arquivo')","(1).__class__"]:
 try:Context(engine,{}).expression(forbidden)
 except ValueError:pass
 else:raise AssertionError('Expressao nao aritmetica foi aceita')
times=[]
for repeat in range(3):
 t=time.perf_counter()
 for m in ref['modules'].values():
  for door in m['doors']:
   for pose in door['samples']:engine.centers(door['leaf'],pose['angle_deg'])
 times.append(time.perf_counter()-t)
source=Path(engine.data['cad']);assert hashlib.sha256(source.read_bytes()).hexdigest()==engine.data['sha256']
report=dict(native_reference_poses=checks,max_native_CG_error_mm=maxerr,
 R12_extra_native_poses=6,max_R12_CG_error_mm=extra_error,
 source_closed_leaves=24,max_closed_CG_error_mm=closederr,
 visible_leaves=len(engine.leaf_names()),hidden_historical_leaves=2,visible_pose_rotation_checks=poses,
 arithmetic_rejection_checks=3,offline_522_pose_seconds=times,offline_median_seconds=float(np.median(times)),
 source_sha256=engine.data['sha256'],source_unchanged=True,FreeCAD_required_for_recalculation=False,
 inputs_sha256={'Snapshot_R51.json':hashlib.sha256((HERE/'Snapshot_R51.json').read_bytes()).hexdigest(),
  'Referencia_nativa_R12.json':hashlib.sha256(extra_path.read_bytes()).hexdigest(),
  str(refpath.relative_to(HERE.parent)):hashlib.sha256(refpath.read_bytes()).hexdigest()},
 scope='Equivalencia do CG/transformacao das folhas neste snapshot, nao resistencia ou colisao comercial. Nao mede tempo de abertura daR51.',passed=True)
(HERE/'Verificacao.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
