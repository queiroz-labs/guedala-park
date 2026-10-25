"""One-DOF planar six-bar linkage inferred from coincident cylindrical STEP axes.

All distances come from the untouched official 40004143 STEP. This is a
reconstruction, not a manufacturer-supplied motion law.
"""
from pathlib import Path
import json
import math
import numpy as np

ROOT=(Path(__file__).resolve().parent / '.').resolve()
data=json.loads(((Path(__file__).resolve().parent / 'Geometria_articulacoes.json').resolve()).read_text())
parts=data['71T7550']['parts']

def shared(i,j,approx):
    candidates=[]
    for c in parts[i]['cylinders_Y']:
        p=np.array([c['center'][0],c['center'][2]])
        for d in parts[j]['cylinders_Y']:
            v=np.array([d['center'][0],d['center'][2]])
            if np.linalg.norm(p-v)<.001:
                candidates.append(p)
    return min(candidates,key=lambda p:np.linalg.norm(p-np.array(approx)))

a=shared(1,4,[-10.45,-9.4984])
b=shared(1,6,[-4.8669,36.822])
c=shared(4,5,[-29.8045,-31.7219])
d=shared(5,6,[-25.0583,16.3167])
e=shared(6,3,[-50.525,10.1413])
f=shared(3,2,[-18.15,40.5])
g=shared(5,2,[5.5,41.7])

def rotation(angle):
    cs,sn=math.cos(angle),math.sin(angle)
    return np.array([[cs,-sn],[sn,cs]])

def arg(p): return math.atan2(p[1],p[0])

def geometry(qs,cup):
    q,s=qs
    C=a+rotation(q)@(c-a)
    D=b+rotation(s)@(d-b)
    E=b+rotation(s)@(e-b)
    t5=arg(D-C)-arg(d-c)
    G=C+rotation(t5)@(g-c)
    F=G+rotation(cup)@(f-g)
    t3=arg(F-E)-arg(f-e)
    return C,D,E,F,G,t5,t3

def residual(qs,cup):
    C,D,E,F,G,t5,t3=geometry(qs,cup)
    return np.array([np.linalg.norm(D-C)-np.linalg.norm(d-c),
                     np.linalg.norm(F-E)-np.linalg.norm(f-e)])

def solve(cup,initial):
    qs=np.array(initial,dtype=float)
    for iteration in range(50):
        r=residual(qs,cup)
        if max(abs(r))<1e-9: return qs
        step=1e-6
        J=np.column_stack([(residual(qs+np.eye(2)[i]*step,cup)-residual(qs-np.eye(2)[i]*step,cup))/(2*step) for i in range(2)])
        change=np.linalg.solve(J,-r)
        # A damped Newton step keeps continuation on the existing assembly branch.
        factor=1.
        while factor>1e-5 and np.linalg.norm(residual(qs+factor*change,cup))>np.linalg.norm(r):
            factor*=.5
        qs+=factor*change
    raise RuntimeError('Linkage closure failed at '+str(math.degrees(cup)))

def transform(angle,p_before,p_after):
    offset=p_after-rotation(angle)@p_before
    return {'theta_xz_rad':float(angle),'translation_xz_mm':offset.tolist()}

def table(sign):
    rows=[];qs=np.zeros(2);max_residual=0
    for opening in np.arange(0,155.0001,.25):
        cup=sign*math.radians(opening)
        old=qs.copy();qs=solve(cup,qs)
        C,D,E,F,G,t5,t3=geometry(qs,cup)
        trans={0:transform(0,a,a),1:transform(0,a,a),
               4:transform(qs[0],a,a),6:transform(qs[1],b,b),
               5:transform(t5,c,C),2:transform(cup,g,G),3:transform(t3,e,E)}
        # Check all seven shared revolute axes independently of the closure equations.
        links=[(1,4,a),(1,6,b),(4,5,c),(5,6,d),(6,3,e),(3,2,f),(5,2,g)]
        def pos(i,p):
            t=trans[i];return rotation(t['theta_xz_rad'])@p+np.array(t['translation_xz_mm'])
        joint_errors=[float(np.linalg.norm(pos(i,p)-pos(j,p))) for i,j,p in links]
        error=max(joint_errors);max_residual=max(max_residual,error)
        if np.linalg.norm(qs-old)>.3: raise RuntimeError('Assembly branch jump')
        rows.append({'alpha_deg':float(opening),'parts':trans,
                     'max_joint_error_mm':error,
                     'cup_center_xz_mm':pos(2,np.array([-6.5,38.5])).tolist()})
    return {'sign':sign,'max_joint_error_mm':max_residual,'poses':rows}

if __name__=='__main__':
    result={'source':'71T7550_40004143.step',
        'joints_xz_mm':{n:p.tolist() for n,p in zip('abcdefg',[a,b,c,d,e,f,g])},
        'parts':{str(i):p['label'] for i,p in enumerate(parts)},
        'model':'6 rigid links, 7 revolute joints, 1 DOF; latch locked to fixed arm',
        'manufacturer_motion_law':False,'branches':[]}
    for sign in [-1,1]:
        try:
            r=table(sign);result['branches'].append(r)
            print(sign,'ok',r['max_joint_error_mm'],[(p['alpha_deg'],p['cup_center_xz_mm']) for p in r['poses'] if p['alpha_deg'] in [0,30,90,92,155]])
        except Exception as exc:
            result['branches'].append({'sign':sign,'error':str(exc)});print(sign,exc)
    ((Path(__file__).resolve().parent / 'Principal_trajetoria.json').resolve()).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
