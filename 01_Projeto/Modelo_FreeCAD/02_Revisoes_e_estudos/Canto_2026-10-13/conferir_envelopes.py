from pathlib import Path
import json
import math
import numpy as np
HERE=(Path(__file__).resolve().parent / '.').resolve()

def panels(alpha,beta):
    a,b=np.radians(alpha),np.radians(beta)
    p=np.broadcast_to([650.,650.],(len(a),2))
    da=np.stack([-np.cos(a),np.sin(a)],axis=1)
    db=np.stack([np.sin(a+b),np.cos(a+b)],axis=1)
    na=18*np.stack([-np.sin(a),-np.cos(a)],axis=1)
    nb=18*np.stack([-np.cos(a+b),np.sin(a+b)],axis=1)
    q=p+400*da
    return np.stack([p,p+400*da,p+400*da+na,p+na],axis=1), np.stack([q,q+400*db,q+400*db+nb,q+nb],axis=1)

def point_distance(poly,point):
    u=poly;v=np.roll(poly,-1,axis=1);dv=v-u
    t=np.clip(np.sum((point-u)*dv,axis=2)/np.sum(dv*dv,axis=2),0,1)
    return np.linalg.norm(u+t[:,:,None]*dv-point,axis=2).min(axis=1)

def rect_distance(poly,rect):
    x0,y0,x1,y1=rect
    q=np.array([[x0,y0],[x1,y0],[x1,y1],[x0,y1]])
    distances=[point_distance(poly,p) for p in q]
    distances.append(np.sqrt(np.maximum(x0-poly[:,:,0],0)**2+np.maximum(poly[:,:,0]-x1,0)**2+
                             np.maximum(y0-poly[:,:,1],0)**2+np.maximum(poly[:,:,1]-y1,0)**2).min(axis=1))
    result=np.min(distances,axis=0)
    # SAT, including contact. Distance is zero for intersecting polygons.
    separated=np.zeros(len(poly),dtype=bool)
    edges=np.roll(poly,-1,axis=1)-poly
    axes=[np.broadcast_to([1.,0.],(len(poly),2)),np.broadcast_to([0.,1.],(len(poly),2))]
    axes += [np.stack([-edges[:,i,1],edges[:,i,0]],axis=1) for i in [0,1]]
    for axis in axes:
        pp=np.sum(poly*axis[:,None,:],axis=2)
        qq=np.einsum('ij,nj->ni',q,axis)
        separated |= (pp.max(axis=1)<qq.min(axis=1)-1e-8)|(qq.max(axis=1)<pp.min(axis=1)-1e-8)
    return np.where(separated,result,0.)

aa,bb=np.meshgrid(np.arange(0,92.00001,.25),np.arange(0,60.00001,.25),indexing='ij')
a,b=aa.ravel(),bb.ravel()
A,B=panels(a,b)
bound=(math.hypot(800,36)+math.hypot(400,18))*math.radians(.125)
cases=[]
for filler in [0,100,120,150,200]:
    width=(1800-filler)/4
    pivot=np.array([250.,1050+filler+width])
    distance=np.minimum(point_distance(A,pivot),point_distance(B,pivot))
    idx=int(np.argmin(distance))
    radius=math.hypot(width,18)
    clear=float(distance[idx]-radius-bound)
    cases.append({'fixed_front_mm':filler,'moving_band_mm':width,
        'first_body_band_mm':filler+width,'neighbour_pivot_mm':pivot.tolist(),
        'separation_sample_mm':round(float(distance[idx]-radius),3),
        'separation_lower_bound_mm':round(clear,3),'critical_alpha_deg':float(a[idx]),
        'critical_beta_deg':float(b[idx]),
        'assumed_displacement_budget_20_plus_20_mm_remaining':round(clear-40,3),
        'assumed_displacement_budget_30_plus_30_mm_remaining':round(clear-60,3)})
maleiro=rect_distance(B,[650,612,2000,650])
idx=int(np.argmin(maleiro))
for deg in [92,110,155]:
    pa,pb=panels(np.array([float(deg)]),np.array([60.]))
    if deg==155:
        back_example={'alpha':deg,'beta':60,'b_distance_to_maleiro_mm':float(rect_distance(pb,[650,612,2000,650])[0]),'tip_mm':pb[0,1].tolist()}
report={'units':'mm','sample_count':len(a),'angle_domain':{'main':[0,92],'fold':[0,60]},
    'sampling_bound_mm':round(bound,3),'fronts':'Conservative nominal 400×18 mm polygons; final cut dimensions not selected',
    'neighbour_envelope':'Full disk enclosing ALL neighbour angles, not a sampled neighbour sweep',
    'cases':cases,'maleiro_B_lower_bound_mm':round(float(maleiro[idx])-bound,3),
    'maleiro_B_critical_pose':{'alpha':float(a[idx]),'beta':float(b[idx])},
    'unlimited_155_counterexample':back_example,
    'displacement_scenarios':'Assumptions for sensitivity only. No documented bound for the complete real linkage was obtained.',
    'fixed_strip_recess_check':{
        'flush_strip_issue':'A 400 mm ideal leaf can enter a coplanar fixed strip during early opening; reproduced separately in native CAD with 394 mm study leaf.',
        'proposed_recess_mm':40,'sheet_thickness_mm':18,
        'analytical_lower_bound_mm':22,
        'proof':'B: min(x) >= 650-400*cos(alpha)-18*max(cos(alpha+beta),0) >=232 mm. Fixed strip at 40 mm recess: max(x)=250-40=210 mm. A min(x)>=249.595 mm over 0..92 deg, also clear.',
        'scope':'Fixed virtual axes only. Real linkage motion and adjustments not covered.'},
    'real_hardware_validation':False}
((Path(__file__).resolve().parent / 'Resultados_envelopes.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
