"""Revisao independenteP11; placasKirchhoffRitz, conformidadeverticalC8 e apoiofundoV0.
A u-C R=v0, K u+A.T R=F. R positivo=apoio empurra prateleira para cima.
Nao e capacidade liberada. UnidadesN,mm,MPa.
"""
import numpy as np
from numpy.polynomial.legendre import Legendre,leggauss

L=661.;B=312.;THICK=17.7;TMASS=18.3;RHO=800.;GRAVITY=9.80665
SUPPORTS=np.array([(0,60),(0,252),(L,60),(L,252),(72,B),(244,B),(417,B),(589,B)],dtype=float)

class PlateModel:
 def __init__(self,n=18,E=1100,nu=.3,C=None,v0=None,L=L,B=B,t=THICK,supports=SUPPORTS):
  self.n=n;self.E=E;self.nu=nu;self.L=L;self.B=B;self.t=t;self.supports=np.array(supports,float)
  self.fs=[Legendre.basis(i) for i in range(n+1)]
  self.N=(n+1)**2;self.S=len(self.supports)
  self.D=E*t**3/(12*(1-nu*nu))
  q,wt=leggauss(n+3)
  v=np.array([f(q) for f in self.fs]);d1=np.array([f.deriv()(q) for f in self.fs]);d2=np.array([f.deriv(2)(q) for f in self.fs])
  def gram(a,b):return (a*wt)@b.T
  M=gram(v,v);H=gram(d2,d2);X=gram(d2,v);G=gram(d1,d1)
  fx=2/L;fy=2/B
  self.K=self.D*L*B/4*(fx**4*np.kron(H,M)+fy**4*np.kron(M,H)+nu*fx**2*fy**2*(np.kron(X,X.T)+np.kron(X.T,X))+2*(1-nu)*fx**2*fy**2*np.kron(G,G))
  self.A=np.array([self.phi(x,y) for x,y in self.supports])
  self.C=np.zeros((self.S,self.S)) if C is None else np.asarray(C,dtype=float)
  self.v0=np.zeros(self.S) if v0 is None else np.asarray(v0,dtype=float)
  assert self.C.shape==(self.S,self.S) and self.v0.shape==(self.S,)
  assert np.max(np.abs(self.C-self.C.T))<1e-10
  self.Kaug=np.block([[self.K,self.A.T],[self.A,-self.C]])
  self.scale=np.r_[np.sqrt(np.maximum(np.diag(self.K),1.)),np.ones(self.S)]
  self.Kscaled=self.Kaug/self.scale[:,None]/self.scale[None,:]
 def phi(self,x,y):
  return np.kron([f(2*x/self.L-1) for f in self.fs],[f(2*y/self.B-1) for f in self.fs])
 def evaluate(self,coeffs,xs,ys,dx=0,dy=0):
  """Retorna grade len(xs) por len(ys), derivadafisica dx/dy."""
  vx=np.array([f.deriv(dx)(2*np.asarray(xs)/self.L-1)*(2/self.L)**dx for f in self.fs])
  vy=np.array([f.deriv(dy)(2*np.asarray(ys)/self.B-1)*(2/self.B)**dy for f in self.fs])
  return vx.T@np.array(coeffs).reshape(self.n+1,self.n+1)@vy
 def solve(self,mass=10,kind='uniform',cx=None,cy=None,stress=False,grid=(161,101),dead_kg=None):
  cx=self.L/2 if cx is None else cx;cy=self.B/2 if cy is None else cy
  own=self.L*self.B*TMASS*RHO/1e9 if dead_kg is None else dead_kg
  F=np.zeros(self.N);F[0]=(own+(mass if kind=='uniform' else 0))*GRAVITY
  if kind!='uniform':
   assert 25<=cx<=self.L-25 and 30<=cy<=self.B-30
   ix=np.array([f.integ()(2*(cx+25)/self.L-1)-f.integ()(2*(cx-25)/self.L-1) for f in self.fs])*self.L/100
   iy=np.array([f.integ()(2*(cy+30)/self.B-1)-f.integ()(2*(cy-30)/self.B-1) for f in self.fs])*self.B/120
   F+=mass*GRAVITY*np.kron(ix,iy)
  rhs=np.r_[F,self.v0]
  sol=np.linalg.solve(self.Kscaled,rhs/self.scale)/self.scale
  coeffs=sol[:self.N];R=sol[self.N:]
  xs=np.linspace(0,self.L,grid[0]);ys=np.linspace(0,self.B,grid[1])
  W=self.evaluate(coeffs,xs,ys);idx=np.unravel_index(W.argmax(),W.shape)
  equilibrium=dict(force_N=float(R.sum()-(mass+own)*GRAVITY),moment_x_Nmm=float(self.supports[:,0]@R-(mass*GRAVITY*(cx if kind!='uniform' else self.L/2)+own*GRAVITY*self.L/2)),moment_y_Nmm=float(self.supports[:,1]@R-(mass*GRAVITY*(cy if kind!='uniform' else self.B/2)+own*GRAVITY*self.B/2)))
  result=dict(degree=self.n,E_MPa=self.E,nu=self.nu,mass_kg=mass,kind=kind,center_mm=[cx,cy],self_mass_kg=own,max_deflection_mm=float(W.max()),max_at_mm=[float(xs[idx[0]]),float(ys[idx[1]])],min_deflection_mm=float(W.min()),frontmid_mm=float(self.phi(self.L/2,0)@coeffs),center_mm_deflection=float(self.phi(self.L/2,self.B/2)@coeffs),reactions_N=R.tolist(),support_deflection_mm=(self.A@coeffs).tolist(),coefficients=coeffs.tolist(),equilibrium_error=equilibrium,max_constraint_error_mm=float(np.max(np.abs(self.A@coeffs-self.C@R-self.v0))))
  if stress:
   wxx=self.evaluate(coeffs,xs,ys,dx=2);wyy=self.evaluate(coeffs,xs,ys,dy=2);wxy=self.evaluate(coeffs,xs,ys,dx=1,dy=1)
   Mx=-self.D*(wxx+self.nu*wyy);My=-self.D*(wyy+self.nu*wxx);Mxy=-self.D*(1-self.nu)*wxy
   sx=6*Mx/self.t**2;sy=6*My/self.t**2;shear=6*Mxy/self.t**2
   mean=(sx+sy)/2;rad=np.sqrt(((sx-sy)/2)**2+shear**2)
   sp=np.maximum(np.abs(mean+rad),np.abs(mean-rad))
   XX,YY=np.meshgrid(xs,ys,indexing='ij');mask=np.ones(XX.shape,bool)
   for x,y in self.supports:mask &= (XX-x)**2+(YY-y)**2>=30**2
   masked=np.where(mask,sp,-np.inf);im=np.unravel_index(masked.argmax(),masked.shape)
   result['global_stress_screen']=dict(exclusion_radius_mm=30,max_abs_principal_bending_MPa=float(masked.max()),at_mm=[float(xs[im[0]]),float(ys[im[1]])],sigma_x_MPa=float(sx[im]),sigma_y_MPa=float(sy[im]),tau_xy_MPa=float(shear[im]),status='Tensao de triagem do modelo deplaca; nao valida furos, contato, corte doMDF ou junta. Pontosideais singularizam tensoes locais.')
  return result

def setup(n=18,E=1100,nu=.3,C=None,v0=None,**kwargs):return PlateModel(n,E,nu,C,v0,**kwargs)

def back_compliance(E=1100,Kg=500.,L=L,h=100.,t=17.7,back_positions=(72,244,417,589),self_mass_kg=None):
 """Viga verticalequivalenteh100 e peso dotodo fundo, nao recorte.
 Kvjunta traseiraNAO incluido; adicionar diagonalprateleira independentemente.
 """
 I=t*h**3/12;A=t*h;G=E/(2*(1+.3));kGA=5/6*G*A
 def green(x,a):
  bb=L-a
  bend=bb*x*(L*L-bb*bb-x*x)/(6*L*E*I) if x<=a else a*(L-x)*(L*L-a*a-(L-x)**2)/(6*L*E*I)
  shear=min(x,a)*(L-max(x,a))/(L*kGA)
  end=((1-x/L)*(1-a/L)+(x/L)*(a/L))/Kg
  return bend+shear+end
 positions=np.asarray(back_positions,float)
 C=np.array([[green(x,a) for a in positions] for x in positions])
 self_mass=L*574*18.3*800/1e9 if self_mass_kg is None else self_mass_kg
 W=self_mass*GRAVITY;q=W/L
 v=np.array([q*x*(L**3-2*L*x*x+x**3)/(24*E*I)+q*x*(L-x)/(2*kGA)+W/(2*Kg) for x in positions])
 return C,v,dict(E_MPa=E,I_mm4=I,area_mm2=A,kGA_N=kGA,end_group_K_N_mm=Kg,self_mass_kg=self_mass,positions_mm=positions.tolist())

