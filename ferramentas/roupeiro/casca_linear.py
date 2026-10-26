"""Casca plana retangular: membrana Q4, flexao Mindlin e cisalhamento MITC.

Implementacao independente NumPy, pequenas deformacoes, material isotropico.
Rotacao de drilling estabilizada por penalidade pequena e consistente.
Nao e um modelo constitutivo de junta de MDF nem substitui ensaios.
"""
import math,time
import numpy as np

def shape(x,y):
    signs=np.array([[-1,-1],[1,-1],[1,1],[-1,1]],float)
    N=(1+signs[:,0]*x)*(1+signs[:,1]*y)/4
    dx=signs[:,0]*(1+signs[:,1]*y)/4
    dy=signs[:,1]*(1+signs[:,0]*x)/4
    return N,dx,dy

def flat_element(a,b,t,E,nu=.3,drill=1e-4):
    D=E/(1-nu**2)*np.array([[1,nu,0],[nu,1,0],[0,0,(1-nu)/2]])
    A=D*t;B=D*t**3/12;S=5/6*E/(2*(1+nu))*t
    K=np.zeros((24,24));saved=[]
    def shear(x,y,direction):
        N,dx,dy=shape(x,y);dx*=2/a;dy*=2/b;row=np.zeros(24)
        for i in range(4):
            if direction==0:row[6*i+2]=dx[i];row[6*i+4]=N[i]
            else:row[6*i+2]=dy[i];row[6*i+3]=-N[i]
        return row
    for x in [-1/math.sqrt(3),1/math.sqrt(3)]:
        for y in [-1/math.sqrt(3),1/math.sqrt(3)]:
            N,dx,dy=shape(x,y);dx*=2/a;dy*=2/b
            M=np.zeros((3,24));F=np.zeros((3,24));R=np.zeros(24)
            for i in range(4):
                q=6*i;M[0,q]=dx[i];M[1,q+1]=dy[i]
                M[2,q]=dy[i];M[2,q+1]=dx[i]
                F[0,q+4]=dx[i];F[1,q+3]=-dy[i]
                F[2,q+4]=dy[i];F[2,q+3]=-dx[i]
                R[q+5]=N[i];R[q+1]=-.5*dx[i];R[q]=.5*dy[i]
            C=np.vstack([((1-y)*shear(0,-1,0)+(1+y)*shear(0,1,0))/2,
                         ((1-x)*shear(-1,0,1)+(1+x)*shear(1,0,1))/2])
            w=a*b/4
            K+=(M.T@A@M+F.T@B@F+S*C.T@C+drill*E*t*np.outer(R,R))*w
            saved.append((M,F,C))
    return K,(A,B,S,saved)

class System:
    def __init__(self):self.ndof=0;self.blocks=[];self.fixed=set();self.points=[]
    def dofs(self,n):
        r=np.arange(self.ndof,self.ndof+n);self.ndof+=n;return r
    def block(self,ids,K):self.blocks.append((np.array(ids,int),np.array(K,float)))
    def spring(self,row,k):
        ix=np.array(sorted(row));v=np.array([row[i] for i in ix]);self.block(ix,k*np.outer(v,v))
    def matrix(self):
        K=np.zeros((self.ndof,self.ndof))
        for ids,m in self.blocks:K[np.ix_(ids,ids)]+=m
        return K

def combine(*pairs):
    out={}
    for row,scale in pairs:
        for i,v in row.items():out[i]=out.get(i,0)+scale*v
    return {i:v for i,v in out.items() if abs(v)>1e-14}

def dense(row,n):
    v=np.zeros(n)
    for i,a in row.items():v[i]=a
    return v

class Panel:
    def __init__(self,system,name,origin,eu,ev,L,B,nx,ny,t=17.7,E=1100.,nu=.3):
        self.s=system;self.name=name;self.origin=np.array(origin,float)
        self.eu=np.array(eu,float);self.ev=np.array(ev,float);self.en=np.cross(self.eu,self.ev)
        self.R=np.vstack([self.eu,self.ev,self.en]);self.L=L;self.B=B;self.nx=nx;self.ny=ny;self.t=t;self.E=E;self.nu=nu
        self.coords=np.array([self.origin+self.eu*(i*L/nx)+self.ev*(j*B/ny) for j in range(ny+1) for i in range(nx+1)])
        self.ids=system.dofs(6*len(self.coords)).reshape(-1,6)
        Q=np.zeros((24,24))
        for i in range(4):
            Q[6*i:6*i+3,6*i:6*i+3]=self.R;Q[6*i+3:6*i+6,6*i+3:6*i+6]=self.R
        ke,self.constitutive=flat_element(L/nx,B/ny,t,E,nu)
        self.Q=Q;self.element_ids=[]
        for j in range(ny):
            for i in range(nx):
                ids=[j*(nx+1)+i,j*(nx+1)+i+1,(j+1)*(nx+1)+i+1,(j+1)*(nx+1)+i]
                gd=self.ids[ids].flatten();self.element_ids.append(gd);system.block(gd,Q.T@ke@Q)
    def interp(self,point):
        p=np.array(point)-self.origin;x=float(p@self.eu);y=float(p@self.ev)
        if not (-1e-7<=x<=self.L+1e-7 and -1e-7<=y<=self.B+1e-7):raise ValueError((self.name,point,x,y))
        x=min(max(x,0),self.L);y=min(max(y,0),self.B)
        i=min(int(x/self.L*self.nx),self.nx-1);j=min(int(y/self.B*self.ny),self.ny-1)
        xi=(x-i*self.L/self.nx)/(self.L/self.nx)*2-1;eta=(y-j*self.B/self.ny)/(self.B/self.ny)*2-1
        N,*_=shape(xi,eta)
        nodes=[j*(self.nx+1)+i,j*(self.nx+1)+i+1,(j+1)*(self.nx+1)+i+1,(j+1)*(self.nx+1)+i]
        projected=self.origin+x*self.eu+y*self.ev
        return N,nodes,np.array(point)-projected
    def displacement_row(self,point,direction):
        N,nodes,off=self.interp(point);direction=np.array(direction,float)
        coeff=np.r_[direction,np.cross(off,direction)];row={}
        for q,n in zip(N,nodes):
            for i,v in zip(self.ids[n],coeff):
                if abs(q*v)>1e-14:row[int(i)]=float(q*v)
        return row
    def add_point(self,f,point,force,moment=(0,0,0)):
        N,nodes,off=self.interp(point);force=np.array(force,float);moment=np.array(moment,float)+np.cross(off,force)
        for q,n in zip(N,nodes):f[self.ids[n]]+=q*np.r_[force,moment]
    def rotation_row(self,point,direction):
        N,nodes,_=self.interp(point);row={}
        for q,n in zip(N,nodes):
            for i,v in zip(self.ids[n,3:],direction):
                if abs(q*v)>1e-14:row[int(i)]=float(q*v)
        return row
    def add_pressure_rectangle(self,f,lo,hi,total_force):
        # Integra a intersecao de cada celula com o retangulo carregado.
        total_force=np.array(total_force,float);area=(hi[0]-lo[0])*(hi[1]-lo[1])
        for j in range(self.ny):
            for i in range(self.nx):
                x0=max(lo[0],i*self.L/self.nx);x1=min(hi[0],(i+1)*self.L/self.nx)
                y0=max(lo[1],j*self.B/self.ny);y1=min(hi[1],(j+1)*self.B/self.ny)
                if x1<=x0 or y1<=y0:continue
                # Bilinear: valor medio por retangulo e valor no centro.
                point=self.origin+self.eu*((x0+x1)/2)+self.ev*((y0+y1)/2)
                self.add_point(f,point,total_force*(x1-x0)*(y1-y0)/area)
    def own_weight(self,f,rho=800.,mass_thickness=18.3):
        mass=self.L*self.B*mass_thickness*rho/1e9
        self.add_pressure_rectangle(f,(0,0),(self.L,self.B),(0,0,-mass*9.80665));return mass
    def stress(self,u):
        A,B,S,ops=self.constitutive;maxnormal=0.;maxshear=0.
        for ids in self.element_ids:
            v=self.Q@u[ids]
            for M,F,C in ops:
                membrane=A@(M@v)/self.t;bending=B@(F@v)*6/self.t**2
                maxnormal=max(maxnormal,float(np.max(np.abs(membrane+bending))),float(np.max(np.abs(membrane-bending))))
                maxshear=max(maxshear,float(np.max(np.abs(S*(C@v)/self.t))))
        return dict(nominal_max_combined_MPa=maxnormal,nominal_transverse_shear_MPa=maxshear)

def solve_spd(K,F,fixed):
    free=np.array([i for i in range(len(K)) if i not in fixed]);A=K[np.ix_(free,free)]
    scale=np.sqrt(np.maximum(np.diag(A),1e-20))
    x=np.linalg.solve(A/np.outer(scale,scale),F[free]/(scale[:,None] if F.ndim==2 else scale))
    x=x/(scale[:,None] if F.ndim==2 else scale)
    out=np.zeros_like(F);out[free]=x
    return out

def validate():
    E=2200.;nu=.3;t=18.;a=100.;b=80.
    K,ops=flat_element(a,b,t,E,nu);coords=np.array([[0,0,0],[a,0,0],[a,b,0],[0,b,0]])
    rigid=[]
    for axis in np.eye(3):
        d=np.array([np.r_[np.cross(axis,r),axis] for r in coords]).flatten()
        rigid.append(float(abs(d@K@d)/max(np.linalg.norm(K)*np.linalg.norm(d)**2,1)))
    eps=np.array([.001,.002,.0005]);v=[]
    for x,y,z in coords:v+=list([eps[0]*x+eps[2]/2*y,eps[1]*y+eps[2]/2*x,0,0,0,0])
    v=np.array(v);D=E/(1-nu**2)*np.array([[1,nu,0],[nu,1,0],[0,0,(1-nu)/2]])
    expected=a*b*t*(eps@D@eps);membrane_error=abs(v@K@v/expected-1)
    kappa=.0001;v=np.array([np.r_[0,0,kappa*x*x/2,0,-kappa*x,0] for x,y,z in coords]).flatten()
    expected=a*b*E*t**3/(12*(1-nu**2))*kappa**2
    bending_error=abs(v@K@v/expected-1)
    cantilever=[]
    for nx in [12,24]:
        s=System();p=Panel(s,'test',[0,0,0],[1,0,0],[0,1,0],1000,100,nx,2,t,E,nu)
        for n,r in enumerate(p.coords):
            if r[0]==0:s.fixed.update(p.ids[n])
        f=np.zeros(s.ndof);p.add_point(f,[1000,50,0],[0,0,-10])
        u=solve_spd(s.matrix(),f,s.fixed);tip=float(dense(p.displacement_row([1000,50,0],[0,0,1]),s.ndof)@u)
        exact=-10*1000**3/(3*E*(100*t**3/12))
        cantilever.append(dict(nx=nx,tip_mm=tip,beam_reference_mm=exact,relative=abs(tip/exact-1)))
    assert max(rigid)<1e-12 and membrane_error<1e-10 and bending_error<1e-10
    assert cantilever[-1]['relative']<.05,cantilever
    return dict(rigid_rotation_normalized_energy=rigid,membrane_energy_error=membrane_error,
                constant_curvature_energy_error=bending_error,cantilever=cantilever,
                limitation='Validacao numerica de casca plana;nao valida MDF, juntas,apoios ou caixa real.')

if __name__=='__main__':
    import json
    print(json.dumps(validate()))
