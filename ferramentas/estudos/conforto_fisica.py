"""Equações auditáveis do estudo; SI, azimute a partir do norte, horário UTC−3.

NOAA (fração anual), Tetens/FAO e volumes finitos implícitos. Os parâmetros
de materiais, ocupação e conforto são hipóteses externas a este módulo.
"""
import math
from datetime import datetime
import numpy as np


def required(mapping, key):
    value = mapping[key]
    if value is None or value == '':
        raise ValueError('Entrada ausente: ' + key)
    return value


def solar(day, hour, lat=-23.60, lon=-46.72, timezone=-3):
    """Altura geométrica e azimute; day=dia do ano; aceita arrays NumPy."""
    gamma = 2*np.pi/365*(np.asarray(day)-1+(np.asarray(hour)-12)/24)
    eq = 229.18*(.000075+.001868*np.cos(gamma)-.032077*np.sin(gamma)
                 -.014615*np.cos(2*gamma)-.040849*np.sin(2*gamma))
    dec = (.006918-.399912*np.cos(gamma)+.070257*np.sin(gamma)
           -.006758*np.cos(2*gamma)+.000907*np.sin(2*gamma)
           -.002697*np.cos(3*gamma)+.00148*np.sin(3*gamma))
    ha = np.radians((np.asarray(hour)*60+eq+4*lon-60*timezone)/4-180)
    phi = np.radians(lat)
    alt = np.arcsin(np.clip(np.sin(phi)*np.sin(dec)+np.cos(phi)*np.cos(dec)*np.cos(ha),-1,1))
    az = (np.degrees(np.arctan2(np.sin(ha),np.cos(ha)*np.sin(phi)-np.tan(dec)*np.cos(phi)))+180)%360
    return np.degrees(alt), az


def day_number(month, day=21, year=2026):
    return datetime(year,month,day).timetuple().tm_yday


def incidence(alt, az, normal):
    return np.where(np.asarray(alt)>0, np.maximum(0,np.cos(np.radians(alt))*np.cos(np.radians(np.asarray(az)-normal))),0)


def local_sun(alt, az, top=245):
    """CAD: x à direita, y para baixo na folha, z para cima."""
    a,b=np.radians(alt),np.radians(az)
    return np.stack([np.cos(a)*np.cos(b-np.radians(top+90)),
                     np.cos(a)*np.cos(b-np.radians(top+180)),np.sin(a)],axis=-1)


def clear_sky(alt):
    """Haurwitz GHI; partição difusa de 15% é hipótese, não parte de Haurwitz."""
    c=np.maximum(np.sin(np.radians(alt)),.0001)
    ghi=np.where(np.asarray(alt)>0,1098*c*np.exp(-.059/c),0)
    dhi=.15*ghi
    dni=np.where(np.asarray(alt)>0,(ghi-dhi)/c,0)
    return ghi,dni,dhi


def plane_irradiance(alt, az, normal, ghi, dni, dhi, visible=1., albedo=.2):
    """Plano vertical: feixe + céu isotrópico + reflexão do chão. W/m²."""
    return np.asarray(dni)*incidence(alt,az,normal)*visible+.5*np.asarray(dhi)+.5*albedo*np.asarray(ghi)


def saturation(t):
    """Tetens, FAO-56 eq.11: pressão de saturação em Pa (faixa meteorológica)."""
    t=np.asarray(t)
    return 610.8*np.exp(17.27*t/(t+237.3))


def dewpoint(t, rh):
    if np.any(np.asarray(rh)<=0) or np.any(np.asarray(rh)>100):
        raise ValueError('UR deve estar em (0,100]')
    return inverse_saturation(saturation(t)*np.asarray(rh)/100)


def inverse_saturation(p):
    log=np.log(np.asarray(p)/610.8)
    return 237.3*log/(17.27-log)


def mixing_ratio(t,rh,pressure=92500):
    p=saturation(t)*np.asarray(rh)/100
    if np.any(p>=pressure) or np.any(np.asarray(rh)<0):raise ValueError('Pressão/UR inválida')
    return .62198*p/(pressure-p)


def rh_from_w(t,w,pressure=92500):
    return 100*pressure*np.asarray(w)/(.62198+np.asarray(w))/saturation(t)


def surface_rh(t,rh,ts):
    """Potencial sem drenar condensado; valores >100 indicam condensação."""
    return np.asarray(rh)*saturation(t)/saturation(ts)


def critical_frsi(t,rh,te,limit=80):
    if t<=te:return math.nan
    critical=inverse_saturation(saturation(t)*rh/limit)
    return float((critical-te)/(t-te))


def moisture_step(w,source_kg_s,flow_m3_s,w_supply,volume,dt=300,density=1.1):
    """Solução exata dw/dt=G/M+Q/V*(ws−w); massa de ar seco constante.

    Retorna w e massa líquida exportada [kg]. Condensação deve ser drenada
    explicitamente pelo chamador, preservando a identidade de massa.
    """
    if min(source_kg_s,flow_m3_s)<0 or min(volume,dt)<=0:raise ValueError('Balanço inválido')
    mass=density*volume
    if flow_m3_s==0:
        end=w+source_kg_s*dt/mass
    else:
        k=flow_m3_s/volume
        equilibrium=w_supply+source_kg_s/(density*flow_m3_s)
        end=equilibrium+(w-equilibrium)*math.exp(-k*dt)
    exported=source_kg_s*dt-mass*(end-w)
    return end,exported


class Wall:
    """Volumes finitos 1D, uma célula por camada, Euler implícito.

    layers = (espessura m, lambda W/mK, capacidade volumétrica J/m³K).
    Fluxos positivos do ar interno para a parede. Sem chuva/umidade de obra.
    """
    def __init__(self,layers,rsi=.13,rse=.04,dt=3600):
        self.layers=np.array(layers,float); self.rsi=rsi; self.rse=rse
        if np.any(self.layers<=0) or min(rsi,rse,dt)<=0:raise ValueError('Parede inválida')
        self.r=self.layers[:,0]/self.layers[:,1]
        cap=self.layers[:,0]*self.layers[:,2]
        n=len(cap); k=np.zeros((n,n))
        self.ge=1/(rse+self.r[0]/2);self.gi=1/(rsi+self.r[-1]/2)
        k[0,0]+=self.ge;k[-1,-1]+=self.gi
        for i in range(n-1):
            conduct=2/(self.r[i]+self.r[i+1])
            k[i,i]+=conduct;k[i+1,i+1]+=conduct
            k[i,i+1]-=conduct;k[i+1,i]-=conduct
        inv=np.linalg.inv(np.diag(cap/dt)+k)
        self.a=inv@np.diag(cap/dt)
        self.be=inv[:,0]*self.ge;self.bi=inv[:,-1]*self.gi

    @property
    def u(self):return float(1/(sum(self.r)+self.rsi+self.rse))

    @property
    def capacity(self):return float(sum(self.layers[:,0]*self.layers[:,2]))

    def step(self,state,te,ti):
        state=self.a@state+self.be*te+self.bi*ti
        q=self.gi*(ti-state[-1])
        return state,float(ti-q*self.rsi)

    def series(self,te,ti,spin=168):
        te=np.asarray(te);ti=np.broadcast_to(ti,te.shape)
        state=np.full(len(self.r),float(ti[0]));out=[]
        for j in range(-min(spin,len(te)),len(te)):
            # Circular spin-up uses the preceding December, not January's future.
            state,ts=self.step(state,float(te[j]),float(ti[j]))
            if j>=0:out.append(ts)
        return np.array(out)


def cavity_surface(ti,te,rwall,back_m,gap_m,vent_fraction=0,rsi=.13):
    """Série resistiva de triagem; ventilação aproxima o fundo à temperatura do ar.

    Não simula sorção, infiltração de chuva, parede úmida ou pontes 2D.
    """
    if not 0<=vent_fraction<=1:raise ValueError('Fração inválida')
    extra=(back_m/.13+min(.18,gap_m*9))*(1-vent_fraction)
    return np.asarray(ti)-(np.asarray(ti)-np.asarray(te))*(rsi+extra)/(rwall+rsi+extra)


def cp(angle):
    """Cp empírico hipotético: +0,6 frontal, −0,3 a sotavento."""
    c=np.cos(np.radians(angle))
    return np.where(c>0,.6*c*c,-.3)


def cross_flow(speed,direction,areas,top=245,cd=.6,path_area=1.):
    """Duas fachadas e gargalo interno em série. Q m³/s e sinal SSE→SW.

    Aeq=[Σ1/A²]^-1/2; Δp=ρv²ΔCp/2; sem tiragem por altura.
    """
    if min(areas)<=0 or path_area<=0:return np.zeros_like(speed,dtype=float),np.zeros_like(speed,dtype=float)
    aeq=1/math.sqrt(sum(1/a**2 for a in (*areas,path_area)))
    delta=cp(np.asarray(direction)-(top-90))-cp(np.asarray(direction)-top)
    return cd*aeq*np.asarray(speed)*np.sqrt(abs(delta)),np.sign(delta)


def rc_step(state,te,tsa,q_solar,q_internal,wall_area,glass_area,capacity,
            conduct_air_mass,wall_u,glass_u,vent_wk,dt=3600,neighbour=24.,party_wk=0.):
    """2 nós por zona: ar + massa. MRT≈massa; Top≈(Tar+Tm)/2.

    Implicit solve. Wall sol-air heats mass; transmitted sun 60% mass,
    40% air, internal gains 40% mass/60% air (hypotheses). No latent load.
    """
    ca,cm=capacity
    h=conduct_air_mass;hw=wall_u*wall_area;hg=glass_u*glass_area
    a=np.array([[ca/dt+h+hg+vent_wk+party_wk,-h],[-h,cm/dt+h+hw]])
    b=np.array([ca/dt*state[0]+(hg+vent_wk)*te+party_wk*neighbour+.4*q_solar+.6*q_internal,
                cm/dt*state[1]+hw*tsa+.6*q_solar+.4*q_internal])
    return np.linalg.solve(a,b)


def adaptive_limit(prevailing):
    """Somente referência hipotética se texto normativo não conferido.

    Linha 0,31*Tm+17,8+3,5; não equivale a conformidade ASHRAE/ISO/NBR.
    """
    t=np.asarray(prevailing)
    return np.where((t>=10)&(t<=33.5),.31*t+21.3,np.nan)
