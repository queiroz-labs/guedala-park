from pathlib import Path
import json,math
import numpy as np

root=(Path(__file__).resolve().parent / '.').resolve()
params=json.loads(((Path(__file__).resolve().parent / 'Montagem_simples.json').resolve()).read_text(encoding='utf-8'))
j=params['joints'];a,b,c,d=[np.array(j[k],float) for k in 'abcd']
angles=np.arange(0,86.00001,.5)
theta=-np.radians(angles)
R=np.stack([np.stack([np.cos(theta),-np.sin(theta)],axis=-1),np.stack([np.sin(theta),np.cos(theta)],axis=-1)],axis=-2)
Q=b-np.einsum('aij,j->ai',R,d-c)
v=Q-a;dist=np.linalg.norm(v,axis=1);unit=v/dist[:,None]
ell=(np.sum((a-c)**2)-np.sum((b-d)**2)+dist**2)/(2*dist)
height=np.sqrt(np.sum((a-c)**2)-ell**2)
C=a+ell[:,None]*unit+params['branch']*height[:,None]*np.stack([-unit[:,1],unit[:,0]],axis=-1)
T=C-np.einsum('aij,j->ai',R,c)
def poly(rect,frame,mount):
    M=np.array(frame,float);Rw=np.einsum('ij,ajk,kl->ail',M,R,M.T)
    offset=np.array(mount)+T@M.T-np.einsum('aij,j->ai',Rw,mount)
    return np.einsum('aij,pj->api',Rw,np.array(rect,float))+offset[:,None,:]
def distances(P,Q):
    # all ordered angle pairs, exact convex rectangles at each sampled pose
    A=np.repeat(P,len(Q),axis=0);B=np.tile(Q,(len(P),1,1))
    axes=np.concatenate([np.roll(A,-1,axis=1)-A,np.roll(B,-1,axis=1)-B],axis=1)
    axes=np.stack([-axes[:,:,1],axes[:,:,0]],axis=-1)
    ap=np.einsum('npi,nai->nap',A,axes);bp=np.einsum('npi,nai->nap',B,axes)
    separated=np.any((ap.max(axis=2)<bp.min(axis=2))|(bp.max(axis=2)<ap.min(axis=2)),axis=1)
    mins=[]
    for points,edges in [(A,B),(B,A)]:
        delta=np.roll(edges,-1,axis=1)-edges
        dif=points[:,:,None,:]-edges[:,None,:,:]
        t=np.clip(np.sum(dif*delta[:,None,:,:],axis=-1)/np.sum(delta*delta,axis=-1)[:,None,:],0,1)
        mins.append(np.min(np.linalg.norm(dif-t[:,:,:,None]*delta[:,None,:,:],axis=-1),axis=(1,2)))
    dst=np.minimum(*mins);dst[~separated]=0
    idx=int(np.argmin(dst))
    return {'min_gap_sampled_mm':float(dst[idx]),'critical_angles_deg':[float(angles[idx//len(Q)]),float(angles[idx%len(Q)])],'intersecting_samples':int(np.sum(~separated)),'pairs':len(A)}
rows=[]
for strip in range(0,201,5):
    left=251+strip;tip=-651-strip
    P=poly([(left,-650),(647,-650),(647,-632),(left,-632)],[[1,0],[0,-1]],(632,-593.5))
    Q=poly([(232,-1047),(250,-1047),(250,tip),(232,tip)],[[0,1],[-1,0]],(193.5,-1032))
    report=distances(P,Q);report['reduction_mm']=strip;rows.append(report)
    if report['min_gap_sampled_mm']>=10:break
result={'angle_step_deg':.5,'angle_range_deg':[0,86],'comparisons':rows,'scope':'Sólidos retangulares das frentes com movimento de quatro barras do STEP. Sem ferragens, suportes e tolerancias. Minimos amostrados.'}
((Path(__file__).resolve().parent / 'Dimensionamento_faixa.json').resolve()).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
