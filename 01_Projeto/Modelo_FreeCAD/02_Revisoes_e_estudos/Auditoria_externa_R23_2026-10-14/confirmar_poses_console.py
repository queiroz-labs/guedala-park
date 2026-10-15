"""Runtime verification only, no collision or previous SAT rerun, no save."""
from pathlib import Path
import json,hashlib
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
a=json.loads(((Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Montagem_R18.json').resolve()).read_text(encoding='utf-8'))
axes=json.loads(((Path(__file__).resolve().parent / '../Apoios_R11_2026-10-14/Eixos_71B3550.json').resolve()).read_text(encoding='utf-8'))
source=Path(json.loads(((Path(__file__).resolve().parent / '../Rotulos_R23_2026-10-14/Rotulos_R23.json').resolve()).read_text(encoding='utf-8'))['file'])
hash_before=hashlib.sha256(source.read_bytes()).hexdigest()
d=App.openDocument(str(source));report={'file':str(source),'gui_up':bool(App.GuiUp),'cases':[]}
changed=[r for r in a['doors'] if r['door'] in a['changed_doors']]
def point(o,p):return o.getGlobalPlacement().multiply(o.Placement.inverse()).multVec(App.Vector(p[0],0,p[1]))
for angle in [0,30,86]:
 for r in a['doors']:d.getObject(r['control']).Abertura=angle
 d.recompute()
 native=json.loads(((Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14').resolve()/('Pose_'+str(angle)+'_R18.json')).read_text(encoding='utf-8'))
 points={r['door']:r['points_world'] for r in native['fronts']}
 for r in changed:
  p=d.getObject(r['old_panel']);pl=p.getGlobalPlacement();w,h=float(p.Length),float(p.Width)
  corners=[pl.multVec(App.Vector(x,y,0)) for x,y in [(0,0),(w,0),(w,h),(0,h)]]
  errs=[(v-App.Vector(*q)).Length for v,q in zip(corners,points[r['door']])]
  hs=[]
  for hi,hinge in enumerate(r['hinges']):
   bs={b['index']:d.getObject(b['body']) for b in hinge['bodies']}
   joint=max((point(bs[i],axes[k])-point(bs[j],axes[k])).Length for i,j,k in [(1,2,'a'),(1,3,'b'),(2,4,'c'),(3,4,'d')])
   hole=d.getObject(r['front']).Tool.Shapes[hi];center=d.getObject(r['door']).getGlobalPlacement().multVec(hole.Placement.Base)
   cup=(center-point(bs[4],[-6.5,38.5])).Length
   hs.append({'group':hinge['group'],'joint_residual_mm':joint,'cup_residual_mm':cup,'body_volume_mm3':[bs[i].Shape.Volume for i in range(5)],'body_global_matrices':[bs[i].getGlobalPlacement().Matrix.A for i in range(5)]})
  report['cases'].append({'door':r['door'],'angle_deg':angle,'native_front_max_difference_mm':max(errs),'hinges':hs})
report['invalid']=[o.Name for o in d.Objects if 'Invalid' in o.State]
App.closeDocument(d.Name)
report['sha256_before']=hash_before;report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest()
report['source_unchanged']=report['sha256_before']==report['sha256_after']
report['ok']=not report['gui_up'] and not report['invalid'] and report['source_unchanged'] and all(r['native_front_max_difference_mm']<1e-6 and all(h['joint_residual_mm']<1e-6 and h['cup_residual_mm']<1e-6 and min(h['body_volume_mm3'])>0 for h in r['hinges']) for r in report['cases'])
((Path(__file__).resolve().parent / 'Validacao_runtime_poses.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('POSE_VALIDATION',report['ok'],max(r['native_front_max_difference_mm'] for r in report['cases']))
