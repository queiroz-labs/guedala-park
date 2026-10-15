from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();a=json.loads(((Path(__file__).resolve().parent / 'Montagem_R18.json').resolve()).read_text(encoding='utf-8'));axes=json.loads(((Path(__file__).resolve().parent / '../Apoios_R11_2026-10-14/Eixos_71B3550.json').resolve()).read_text(encoding='utf-8'));p=Path(a['file'])
def record(angle):
 d=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==p)
 for r in a['doors']:d.getObject(r['control']).Abertura=angle
 d.getObject('ControleSimplesR04').set('B2',str(angle)+' deg');d.getObject('ControleSimplesR04').set('B3',str(angle)+' deg');d.recompute()
 def point(o,p):return o.getGlobalPlacement().multiply(o.Placement.inverse()).multVec(App.Vector(p[0],0,p[1]))
 def corners(o):
  pl=o.getGlobalPlacement();w,h=float(o.Length),float(o.Width)
  return [list(pl.multVec(App.Vector(x,y,0))) for x,y in [(0,0),(w,0),(w,h),(0,h)]]
 out={'angle':angle,'fronts':[{ 'door':r['door'],'points_world':corners(d.getObject(r['old_panel']))} for r in a['doors']], 'corner_fronts':[],'joints':[],'invalid':[o.Name for o in d.Objects if 'Invalid' in o.State]}
 for n in ['PainelSimplesR04','PainelSimplesR001']:out['corner_fronts'].append({'name':n,'points_world':corners(d.getObject(n))})
 for r in a['doors']:
  if r['door'] not in a['changed_doors']:continue
  g=d.getObject(r['door']);f=d.getObject(r['front'])
  for hi,h in enumerate(r['hinges']):
   bs={b['index']:d.getObject(b['body']) for b in h['bodies']};errs=[(point(bs[i],axes[k])-point(bs[j],axes[k])).Length for i,j,k in [(1,2,'a'),(1,3,'b'),(2,4,'c'),(3,4,'d')]]
   hole=f.Tool.Shapes[hi];cp=g.getGlobalPlacement().multVec(hole.Placement.Base);native=point(bs[4],[-6.5,38.5])
   out['joints'].append({'door':r['door'],'level':h['level'],'axis_residual':max(errs),'cup_residual':(cp-native).Length})
 (root/('Pose_'+str(angle)+'_R18.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 if angle==0:d.save()
 return {'angle':angle,'invalid':out['invalid'],'axis_residual':max(x['axis_residual'] for x in out['joints']),'cup_residual':max(x['cup_residual'] for x in out['joints'])}
