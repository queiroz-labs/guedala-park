from pathlib import Path
import json,math,itertools
import numpy as np
root=(Path(__file__).resolve().parent / '.').resolve()
data=json.loads(((Path(__file__).resolve().parent / 'Dados_plano_R18.json').resolve()).read_text(encoding='utf-8'))
axes=json.loads(Path(data['axes_file']).read_text(encoding='utf-8'))
a,b,c,d=[np.array(axes[k],float) for k in ['a','b','c','d']]
def circle(A,B,r1,r2,sign):
 v=B-A;dd=np.linalg.norm(v);ll=(r1*r1-r2*r2+dd*dd)/(2*dd);hh=math.sqrt(max(0,r1*r1-ll*ll))
 return A+ll*v/dd+sign*hh*np.array([-v[1],v[0]])/dd
sg=min([-1,1],key=lambda sign:np.linalg.norm(circle(a,b-d+c,np.linalg.norm(a-c),np.linalg.norm(b-d),sign)-c))
angles=np.arange(0,86.0001,.5)
def polygons(row):
 mm=np.array(row['module_matrix']);rot_module=mm[:2,:2];mb=mm[:2,3]
 origin=np.array([row['hinge_support_inner_x_mm'],56.5]);start=np.array(row['closed_leaf_base'][:2])
 bb=row['front_local_box'];rect=np.array([[bb[0],0],[bb[3],0],[bb[3],bb[4]],[bb[0],bb[4]]]);items=[]
 for angle in angles:
  th=-math.radians(angle);R=np.array([[math.cos(th),-math.sin(th)],[math.sin(th),math.cos(th)]])
  cp=circle(a,b-R@(d-c),np.linalg.norm(a-c),np.linalg.norm(b-d),sg);trans=cp-R@c
  phi=th if row['side']=='left' else -th;rr=np.array([[math.cos(phi),-math.sin(phi)],[math.sin(phi),math.cos(phi)]])
  shift=np.array([-trans[0] if row['side']=='left' else trans[0],-trans[1]])
  base=origin+shift+rr@(start-origin);items.append((rect@rr.T+base)@rot_module.T+mb)
 return np.array(items)
rows=data['rows'];head=next(r for r in rows if r['module']=='Modulo003');hm=np.array(head['module_matrix'])
rows+= [dict(door='PainelSimplesR001',module='Modulo001',side='left',module_matrix=hm.tolist(),hinge_support_inner_x_mm=1818,closed_leaf_base=[1803,0,1],front_local_box=[0,0,0,271,18,306],front_height=306)]
cm=np.eye(4);cm[:2,:2]=[[0,1],[-1,0]];cm[:2,3]=[2200,-126]
rows+= [dict(door='PainelSimplesR04',module='Modulo001',side='right',module_matrix=(hm@cm).tolist(),hinge_support_inner_x_mm=256,closed_leaf_base=[271,0,1],front_local_box=[-271,0,0,0,18,306],front_height=306)]
polys=[polygons(r) for r in rows]
agreement=[]
for angle in [0,30,86]:
 native=json.loads((root/f'Pose_{angle}_R18.json').read_text(encoding='utf-8'));ref={r['door']:r['points_world'] for r in native['fronts']};ref.update({r['name']:r['points_world'] for r in native['corner_fronts']})
 for row,pp in zip(rows,polys):
  expected=np.array(ref[row['door']])[:,:2];actual=pp[int(angle*2)]
  # Compare point sets; local panel ordering differs for the normalized corner A.
  err=max(np.linalg.norm(actual[:,None]-expected[None,:],axis=2).min(axis=0));assert err<1e-6,(row['door'],angle,err)
  agreement.append({'door':row['door'],'angle':angle,'max_error_mm':float(err)})
def norm(p):
 e=p[:,[1,2],:]-p[:,[0,1],:];n=np.stack([-e[:,:,1],e[:,:,0]],axis=2);return n/np.linalg.norm(n,axis=2)[:,:,None]
normals=[norm(p) for p in polys]
def separation(A,B,na,nb):
 aa=np.einsum('aek,avk->aev',na,A);ba=np.einsum('aek,bvk->abev',na,B)
 bb=np.einsum('bek,bvk->bev',nb,B);ab=np.einsum('bek,avk->abev',nb,A)
 gapA=np.maximum(aa.min(axis=2)[:,None,:]-ba.max(axis=3),ba.min(axis=3)-aa.max(axis=2)[:,None,:])
 gapB=np.maximum(bb.min(axis=2)[None,:,:]-ab.max(axis=3),ab.min(axis=3)-bb.max(axis=2)[None,:,:])
 return np.maximum(gapA.max(axis=2),gapB.max(axis=2))
def heights(r):
 z=r['module_matrix'][2][3]+r['closed_leaf_base'][2];return z,z+r['front_height']
pairs=[];changed=set(data['changed_doors'])
for i,j in itertools.combinations(range(len(rows)),2):
 if not ({rows[i]['door'],rows[j]['door']}&changed):continue
 z1,z2=heights(rows[i]),heights(rows[j])
 if min(z1[1],z2[1])<=max(z1[0],z2[0]):continue
 A,B=polys[i],polys[j];g=np.maximum(A.min(axis=(0,1))-B.max(axis=(0,1)),B.min(axis=(0,1))-A.max(axis=(0,1)))
 if max(g)>=0:
  pairs.append({'pair':[rows[i]['door'],rows[j]['door']],'method':'sampled envelope','gap_mm':float(max(g)),'intersections':0});continue
 sep=separation(A,B,normals[i],normals[j]);hits=np.argwhere(sep<-1e-6)
 pairs.append({'pair':[rows[i]['door'],rows[j]['door']],'method':'SAT independent angles','gap_mm':float(sep.min()),'intersections':len(hits),'first_hits':[[float(angles[x]),float(angles[y])] for x,y in hits[:5]]})
def hull(points):
 pp=sorted(set(map(tuple,points)))
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lo=[];hi=[]
 for p in pp:
  while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=1e-10:lo.pop()
  lo.append(p)
 for p in reversed(pp):
  while len(hi)>=2 and cross(hi[-2],hi[-1],p)<=1e-10:hi.pop()
  hi.append(p)
 return np.array(lo[:-1]+hi[:-1])
stationary=[]
for target in data['targets']:
 if target['name']=='DivisorApoioVizinhaR03':continue # Explicitly retired source support, not adopted R18.
 dim=target['dimensions'];m=np.array(target['matrix']);pts=np.array([m@np.array([x,y,z,1]) for x,y,z in itertools.product([0,dim[0]],[0,dim[1]],[0,dim[2]])]);p=hull(pts[:,:2])
 if len(p)<3:continue
 stationary.append((target,p,float(pts[:,2].min()),float(pts[:,2].max())))
hits_static=[];tested=0
for r,A,na in zip(rows,polys,normals):
 if r['door'] not in changed:continue
 z1=heights(r)
 for t,B,zlo,zhi in stationary:
  if min(z1[1],zhi)<=max(z1[0],zlo)+1e-6:continue
  gap=np.maximum(A.min(axis=(0,1))-B.max(axis=0),B.min(axis=0)-A.max(axis=(0,1)))
  if max(gap)>=0:continue
  edges=np.roll(B,-1,axis=0)-B;nb=np.stack([-edges[:,1],edges[:,0]],axis=1);nb/=np.linalg.norm(nb,axis=1)[:,None]
  axes_all=np.concatenate([na,np.broadcast_to(nb,(len(A),len(nb),2))],axis=1)
  ap=np.einsum('aek,avk->aev',axes_all,A);bp=np.einsum('aek,vk->aev',axes_all,B)
  sep=np.maximum(ap.min(axis=2)-bp.max(axis=2),bp.min(axis=2)-ap.max(axis=2)).max(axis=1);hits=np.where(sep<-1e-6)[0];tested+=len(A)
  if len(hits):hits_static.append({'door':r['door'],'target':t['name'],'label':t['label'],'poses_hit':len(hits),'first_angles':[float(angles[h]) for h in hits[:5]],'minimum_axis_gap_mm':float(sep.min())})
report={'step_deg':.5,'positions_each':len(angles),'native_agreement':agreement,'pairs':pairs,'static_targets':len(stationary),'static_narrowphase_poses':tested,'static_hits':hits_static,'pair_hits':[p for p in pairs if p['intersections']], 'method':'External numpy SAT of rectangular front envelopes, checked against native FreeCAD positions 0/30/86. Ten fronts include current R04 A/B explicitly. Only pairs and static encounters affected by four R18 changes checked. Planar sweep with height overlap; conservative 2.5D projection of stationary boxes. Excludes retired DivisorApoioVizinhaR03. Not continuous proof, fitting-body collision audit, load, fixation, mechanical stop or tolerance validation. Whole-apartment reflection preserves these ideal geometric distances.'}
((Path(__file__).resolve().parent / 'Varredura_frentes_R18.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['native_agreement','pairs','method']},ensure_ascii=True))
