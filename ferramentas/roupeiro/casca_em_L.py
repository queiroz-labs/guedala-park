"""Malha retangular recortada: uma chapaL continua, sem junta ficticia na quina."""
import math
import numpy as np
from casca_linear import Panel,flat_element,shape

class LPanel(Panel):
    def __init__(self,system,name,origin,step=140.,t=17.7,E=1100.,nu=.3):
        self.s=system;self.name=name;self.origin=np.array(origin,float)
        self.eu=np.array([1.,0,0]);self.ev=np.array([0.,1,0]);self.en=np.array([0.,0,1]);self.R=np.eye(3)
        self.t=t;self.E=E;self.nu=nu;self.L=650.;self.B=1050.
        def split(a,b):return np.linspace(a,b,math.ceil((b-a)/step)+1)
        self.xs=np.r_[split(0,420)[:-1],split(420,650)]
        self.ys=np.r_[split(0,420)[:-1],split(420,1050)]
        self.cells={};nodes={};coords=[]
        for j in range(len(self.ys)-1):
            for i in range(len(self.xs)-1):
                if self.xs[i]<420-1e-8 and self.ys[j]<420-1e-8:continue
                nn=[]
                for ij in [(i,j),(i+1,j),(i+1,j+1),(i,j+1)]:
                    if ij not in nodes:
                        nodes[ij]=len(coords);coords.append(self.origin+[self.xs[ij[0]],self.ys[ij[1]],0])
                    nn.append(nodes[ij])
                self.cells[i,j]=nn
        self.coords=np.array(coords);self.ids=system.dofs(6*len(coords)).reshape(-1,6)
        self.element_ids=[];self.area=0
        for (i,j),nn in self.cells.items():
            a=self.xs[i+1]-self.xs[i];b=self.ys[j+1]-self.ys[j];self.area+=a*b
            ke,_=flat_element(a,b,t,E,nu);gd=self.ids[nn].flatten();self.element_ids.append(gd);system.block(gd,ke)
        assert abs(self.area-506100)<1e-7
    def interp(self,point):
        x,y,z=np.array(point)-self.origin
        if x<-1e-7 or x>650+1e-7 or y<-1e-7 or y>1050+1e-7:raise ValueError((self.name,point))
        x=float(np.clip(x,0,650));y=float(np.clip(y,0,1050))
        i=min(max(np.searchsorted(self.xs,x,side='right')-1,0),len(self.xs)-2)
        j=min(max(np.searchsorted(self.ys,y,side='right')-1,0),len(self.ys)-2)
        if (i,j) not in self.cells:
            if (i+1,j) in self.cells and abs(x-self.xs[i+1])<1e-7:i+=1
            elif (i,j+1) in self.cells and abs(y-self.ys[j+1])<1e-7:j+=1
            else:raise ValueError(('Ponto no recorteL',point,x,y))
        N,*_=shape(2*(x-self.xs[i])/(self.xs[i+1]-self.xs[i])-1,2*(y-self.ys[j])/(self.ys[j+1]-self.ys[j])-1)
        return N,self.cells[i,j],np.array([0.,0.,z])
    def add_pressure_rectangle(self,f,lo,hi,total_force):
        pieces=[]
        for i,j in self.cells:
            x0=max(lo[0],self.xs[i]);x1=min(hi[0],self.xs[i+1]);y0=max(lo[1],self.ys[j]);y1=min(hi[1],self.ys[j+1])
            if x1>x0 and y1>y0:pieces.append(((x0+x1)/2,(y0+y1)/2,(x1-x0)*(y1-y0)))
        area=sum(r[2] for r in pieces)
        assert area>0
        for x,y,a in pieces:self.add_point(f,self.origin+[x,y,0],np.array(total_force)*a/area)
    def own_weight(self,f,rho=800.,mass_thickness=18.3):
        mass=self.area*mass_thickness*rho/1e9
        self.add_pressure_rectangle(f,[0,0],[650,1050],[0,0,-mass*9.80665]);return mass
