from pathlib import Path
import json,math,numpy as np
root=(Path(__file__).resolve().parent / '.').resolve()
rows=json.loads(((Path(__file__).resolve().parent / 'Frentes_plano_R12.json').resolve()).read_text(encoding='utf-8'))
ax=json.loads(((Path(__file__).resolve().parent / 'Eixos_71B3550.json').resolve()).read_text(encoding='utf-8'));a,b,c,d=[np.array(ax[k],float) for k in ['a','b','c','d']]
def circle(A,B,r1,r2,sign):
 v=B-A;dd=np.linalg.norm(v);ll=(r1*r1-r2*r2+dd*dd)/(2*dd);hh=math.sqrt(r1*r1-ll*ll)
 return A+ll*v/dd+sign*hh*np.array([-v[1],v[0]])/dd
Q=b-d+c;sg=min([-1,1],key=lambda sign:np.linalg.norm(circle(a,Q,np.linalg.norm(a-c),np.linalg.norm(b-d),sign)-c))
angles=np.arange(0,86.0001,.5);polys=[];norms=[]
for row in rows:
 yaw=math.radians(row['module_yaw_deg']);cw,sw=math.cos(yaw),math.sin(yaw);module_rotation=np.array([[cw,-sw],[sw,cw]])
 mx=row['hinge_inner_x_mm'];my=row['hinge_y_mm'];origin=np.array([mx,my]);start=np.array(row['closed_leaf_base'][:2]);mb=np.array(row['module_base'][:2])
 bb=row['front_local_box'];rect=np.array([[bb[0],bb[1]],[bb[3],bb[1]],[bb[3],bb[4]],[bb[0],bb[4]]]);items=[]
 for angle in angles:
  th=-math.radians(angle);co,si=math.cos(th),math.sin(th);R=np.array([[co,-si],[si,co]]);q=b-R@(d-c);cp=circle(a,q,np.linalg.norm(a-c),np.linalg.norm(b-d),sg);trans=cp-R@c
  phi=th if row['side']=='left' else -th;cc,ss=math.cos(phi),math.sin(phi);rot=np.array([[cc,-ss],[ss,cc]])
  shift=np.array([-trans[0] if row['side']=='left' else trans[0],-trans[1]])
  base=origin+shift+rot@(start-origin)
  items.append(((rect@rot.T)+base)@module_rotation.T+mb)
 verts=np.array(items);polys.append(verts)
 edges=verts[:,[1,2],:]-verts[:,[0,1],:];norm=np.stack([-edges[:,:,1],edges[:,:,0]],axis=2);norm/=np.linalg.norm(norm,axis=2)[:,:,None];norms.append(norm)
cases=[];tested=0;broad=[]
for i,one in enumerate(rows):
 for j,two in enumerate(rows[i+1:],i+1):
  lo1=one['module_base'][2]+one['closed_leaf_base'][2];hi1=lo1+one['front_height'];lo2=two['module_base'][2]+two['closed_leaf_base'][2];hi2=lo2+two['front_height']
  if min(hi1,hi2)<=max(lo1,lo2):continue
  A,B=polys[i],polys[j]
  gap=np.maximum(A.min(axis=(0,1))-B.max(axis=(0,1)),B.min(axis=(0,1))-A.max(axis=(0,1)))
  if np.any(gap>=0):
   broad.append({'pair':[one['door'],two['door']],'sampled_envelope_axis_gaps_mm':gap.tolist(),'positive_separation_mm':float(max(gap))});continue
  aa=np.einsum('aek,avk->aev',norms[i],A);ba=np.einsum('aek,bvk->abev',norms[i],B)
  bb=np.einsum('bek,bvk->bev',norms[j],B);ab=np.einsum('bek,avk->abev',norms[j],A)
  gapA=np.maximum(aa.min(axis=2)[:,None,:]-ba.max(axis=3),ba.min(axis=3)-aa.max(axis=2)[:,None,:])
  gapB=np.maximum(bb.min(axis=2)[None,:,:]-ab.max(axis=3),ab.min(axis=3)-bb.max(axis=2)[None,:,:])
  separation=np.maximum(gapA.max(axis=2),gapB.max(axis=2));hits=np.argwhere(separation<-1e-6);idx=np.unravel_index(np.argmin(separation),separation.shape)
  tested+=len(angles)**2
  cases.append({'pair':[one['door'],two['door']],'positions_each':len(angles),'intersections':int(len(hits)),'minimum_separating_axis_gap_mm':float(separation[idx]),'worst_angles_deg':[float(angles[idx[0]]),float(angles[idx[1]])],'first_hits_deg':[[float(angles[x]),float(angles[y])] for x,y in hits[:5]]})
module_by_door={r['door']:r['module'] for r in rows}
same=[r['positive_separation_mm'] for r in broad if module_by_door[r['pair'][0]]==module_by_door[r['pair'][1]]]
cross=[r['positive_separation_mm'] for r in broad if module_by_door[r['pair'][0]]!=module_by_door[r['pair'][1]]]
report={'step_deg':.5,'positions_each_leaf':len(angles),'height_overlapping_pairs_separated_by_sampled_envelopes':len(broad),'broadphase_pairs':broad,
 'minimum_same_module_sampled_envelope_separation_mm':min(same) if same else None,
 'minimum_cross_module_sampled_envelope_separation_mm':min(cross) if cross else None,
 'minimum_sampled_envelope_separation_mm':min(r['positive_separation_mm'] for r in broad) if broad else None,
 'pairs_examined_after_broadphase':len(cases),'angle_combinations_tested':tested,'pairs':cases,
 'method':'SAT de retângulos externos de frente no plano, movimento de quatro barras comparado à auditoria nativa. Menor separação projetada positiva prova separação nas amostras; não é distância euclidiana nem prova contínua/tolerância. Pares sem sobreposição das envoltórias gerais ou altura excluídos.'}
((Path(__file__).resolve().parent / 'Varredura_frentes_R12.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['broadphase_pairs','method']},ensure_ascii=True))
