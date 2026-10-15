from pathlib import Path
import json
import numpy as np
from resolver_principal import a,b,c,d,e,f,g,geometry,rotation,arg

root=(Path(__file__).resolve().parent / '.').resolve()
poses=json.loads(((Path(__file__).resolve().parent / 'Principal_trajetoria.json').resolve()).read_text())['branches'][0]['poses']

def intersections(A,B,r1,r2):
    u=B-A;dist=np.linalg.norm(u);u=u/dist
    l=(r1*r1-r2*r2+dist*dist)/(2*dist)
    h=np.sqrt(max(0,r1*r1-l*l));v=np.array([-u[1],u[0]])
    return A+l*u+h*v,A+l*u-h*v

C=c;D=d;E=e;F=f;G=g
di=intersections(C,b,np.linalg.norm(d-c),np.linalg.norm(d-b))
fi=intersections(E,G,np.linalg.norm(f-e),np.linalg.norm(f-g))
sd=1 if np.linalg.norm(di[0]-d)<np.linalg.norm(di[1]-d) else -1
sf=1 if np.linalg.norm(fi[0]-f)<np.linalg.norm(fi[1]-f) else -1
maxerr=0
for p in poses:
    q=p['parts']['4']['theta_xz_rad']
    C=a+rotation(q)@(c-a)
    D=intersections(C,b,np.linalg.norm(d-c),np.linalg.norm(d-b))[0 if sd==1 else 1]
    s=arg(D-b)-arg(d-b)
    E=b+rotation(s)@(e-b)
    t5=arg(D-C)-arg(d-c)
    G=C+rotation(t5)@(g-c)
    F=intersections(E,G,np.linalg.norm(f-e),np.linalg.norm(f-g))[0 if sf==1 else 1]
    tcup=arg(F-G)-arg(f-g)
    difference=tcup-p['parts']['2']['theta_xz_rad']
    maxerr=max(maxerr,abs(np.arctan2(np.sin(difference),np.cos(difference))))

subset=[p for p in poses if p['alpha_deg']<=92]
s=np.array([p['alpha_deg']/92 for p in subset])
q=np.array([-p['parts']['4']['theta_xz_rad']*180/np.pi for p in subset])
coeff=np.polynomial.polynomial.polyfit(s[1:-1],(q[1:-1]-q[-1]*s[1:-1])/(s[1:-1]*(s[1:-1]-1)),10)
estimated=q[-1]*s+s*(s-1)*np.polynomial.polynomial.polyval(s,coeff)
report={'circle_branch_D':sd,'circle_branch_F':sf,
    'forward_matches_inverse_max_rad':maxerr,
    'drive_fit_max_q_error_deg':float(max(abs(estimated-q))),
    'q_at_92_deg':float(q[-1]),'drive_polynomial_coefficients':coeff.tolist(),
    'equation':'q_positive_deg=q92*s+s*(s-1)*sum(c_i*s^i); s=clamp(alpha,0,92)/92',
    'branch_test_domain':[0,155], 'joints':{n:p.tolist() for n,p in zip('abcdefg',[a,b,c,d,e,f,g])}}
((Path(__file__).resolve().parent / 'Parametros_expressões.json').resolve()).write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
