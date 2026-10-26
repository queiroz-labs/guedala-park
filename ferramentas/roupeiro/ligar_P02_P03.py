"""P02/P03 deformaveis, C01 e divisoria/base/socoP01. Estudo sem abrir CAD.

Juntas e piso sao parametros, nao propriedades medidas. Sem capacidade liberada.
"""
import argparse,csv,itertools,json,math,time,os
from pathlib import Path
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
from casca_linear import Panel,combine,dense,solve_spd
from casca_em_L import LPanel
from calcular_caixa_P03 import Model,G,T,ORIGIN,ROOT,OUT,motion

def stations(lo,hi,n):
    for i in range(n):yield lo+(hi-lo)*(i+.5)/n,(hi-lo)/n

class Coupled(Model):
    def __init__(self,soco=True,c01_k=500.,c01_n=4,c01_spread=False,floor_k_area=1.,floor_gap=0.,mesh=1.,lower_mesh=None,full_walls=True,**kwargs):
        super().__init__(closed_back=True,nx=round(8*mesh),ny=round(4*mesh),**kwargs)
        lower_mesh=mesh if lower_mesh is None else lower_mesh
        self.options=dict(soco=soco,c01_k=c01_k,c01_n=c01_n,c01_spread=c01_spread,floor_k_area=floor_k_area,floor_gap=floor_gap,mesh=mesh,lower_mesh=lower_mesh,full_walls=full_walls,**kwargs)
        P=self.panels;s=self.s;E=self.E;n=max(2,round(4*mesh));nz=max(2,round(2*mesh))
        P['P02_base']=LPanel(s,'P02_base',[1350,-400,9],step=140/mesh,E=E)
        P['P02_topo']=LPanel(s,'P02_topo',[1350,-400,299],step=140/mesh,E=E)
        P['P02_lateral']=Panel(s,'P02_lateral',[1359,20,18],[0,1,0],[0,0,1],612,272,n,nz,E=E)
        P['P02_fundo_principal']=Panel(s,'P02_fundo_principal',[1350,641,18],[1,0,0],[0,0,1],632,272,n,nz,E=E)
        P['P02_fundo_retorno']=Panel(s,'P02_fundo_retorno',[1991,-400,18],[0,1,0],[0,0,1],1032,272,round(6*mesh),nz,E=E)
        P['P02_terminal']=Panel(s,'P02_terminal',[1770,-391,18],[1,0,0],[0,0,1],212,272,max(2,round(2*mesh)),nz,E=E)
        for horizontal,z in [('base',18),('topo',290)]:
            a=P['P02_'+horizontal]
            for label,other,points in [
                ('lateral','P02_lateral',[[1359,y,z] for y in [70,230,390,550]]),
                ('principal','P02_fundo_principal',[[x,641,z] for x in [1420,1600,1780,1940]]),
                ('retorno','P02_fundo_retorno',[[1991,y,z] for y in [-350,-150,70,270,470,580]]),
                ('terminal','P02_terminal',[[x,-391,z] for x in [1810,1930]])]:
                for i,point in enumerate(points):self.joint(f'P02_{horizontal}_{label}_{i}',a,P[other],point)
        for z in [68,230]:
            self.joint(f'P02_lateral_principal_{z}',P['P02_lateral'],P['P02_fundo_principal'],[1359,632,z])
            self.joint(f'P02_terminal_retorno_{z}',P['P02_terminal'],P['P02_fundo_retorno'],[1982,-391,z])
        # Nenhuma junta fundo255-fundo256: eles so compartilham aresta.
        self.c01=[]
        ys=[80,572] if c01_n==4 else ([140,356,572] if c01_spread else [80,326,572])
        for i,(y,z) in enumerate(itertools.product(ys,[48,260] if c01_spread else [78,230])):
            point=[1350,y,z];rows=[]
            for axis in np.eye(3):
                row=combine((P['P02_lateral'].displacement_row(point,axis),1),(P['direita'].displacement_row(point,axis),-1))
                s.spring(row,c01_k);rows.append(row)
            self.c01.append(dict(name=f'C01_{i+1}',point_mm=point,rows=rows))
        # Sem atrito: contato normal na face; cisalhamento vem so dos conectores.
        for y,dy in stations(20,632,4):
            for z,dz in stations(18,290,2):
                point=[1350,y,z]
                row=combine((P['P02_lateral'].displacement_row(point,[1,0,0]),1),(P['direita'].displacement_row(point,[1,0,0]),-1))
                self.contact('C01_face',row,self.penalty*dy*dz,dy*dz,point)
        if c01_k==0:
            # So para comparacao sem ligacao positiva. Nao cria apoio vertical.
            s.fixed.update(P['P02_base'].ids[0,:2]);s.fixed.add(int(P['P02_base'].ids[-1,1]))
        # Contato real da baseP02 no topo da lateral direita e sua extensao.
        for lo,hi,count,label in [(0,82,2,'P02_extensao_D'),(82,650,8,'P02_lateral_D')]:
            for y,dy in stations(lo,hi,count):
                for x in [1991-9/math.sqrt(3),1991+9/math.sqrt(3)]:
                    row=combine((P['P02_base'].displacement_row([x,y,0],[0,0,1]),1),(self.root_row('lateral_direita',[x,y,0]),-1))
                    k=self.penalty*9*dy
                    if y<82:k=1/(1/k+1/(4*self.joint_k*dy/82/2))
                    self.contact(label,row,k,9*dy,[x,y,0])
        for x,dx in stations(1350,1982,6):
            for y in [51-31/math.sqrt(3),51+31/math.sqrt(3)]:
                row=combine((P['P02_base'].displacement_row([x,y,0],[0,0,1]),1),(self.beam_row(x,y),-1))
                self.contact('P02_travessa',row,self.penalty*dx*31,dx*31,[x,y,0])
        if self.rear_support:
            for x,dx in stations(1350,1982,6):
                for y in [641-9/math.sqrt(3),641+9/math.sqrt(3)]:
                    row=combine((P['P02_base'].displacement_row([x,y,0],[0,0,1]),1),(self.root_row('fundo_P01_proposto',[x,y,0]),-1))
                    self.contact('P02_fundo_P01',row,self.penalty*dx*9,dx*9,[x,y,0])
        # Base principal e extensao frontal sao duas chapas, ligadas por molas.
        P['P01_base']=Panel(s,'P01_base',[18,82,-2061],[1,0,0],[0,1,0],1964,550,round(14*lower_mesh),round(4*lower_mesh),E=E)
        P['P01_base_frente']=Panel(s,'P01_base_frente',[18,0,-2061],[1,0,0],[0,1,0],1964,82,round(14*lower_mesh),2,E=E)
        s.fixed.update(P['P01_base'].ids[0,:2]);s.fixed.add(int(P['P01_base'].ids[-1,1]))
        for i,x in enumerate([27,382,732,1000,1268,1618,1973]):
            self.joint(f'P01_base_frente_{i}',P['P01_base'],P['P01_base_frente'],[x,82,-2061])
        self.axial_members=[];self.root_ties=[]
        if full_walls:self.add_walls(lower_mesh,soco,floor_k_area)
        # Retira fundacoes supostas da divisoria e das duas laterais superiores.
        # A divisoria agora descarrega por contato na base flexivel.
        for name in ([] if full_walls else ['lateral_esquerda','divisoria','lateral_direita']):
            r=self.roots[name];s.block(r['ids'],-np.diag(r['k']));r['k']*=0
            bottom='pe_divisoria' if name=='divisoria' else ('piso_E' if name.endswith('esquerda') else 'piso_D')
            if name=='divisoria':point=[1000,357,-2052];width=550.;H=2052.;ymin=82.;floor_stiff=np.zeros(3)
            else:
                point=[r['point'][0],366,-2061];width=568.;H=2061.;ymin=82.
                floor_stiff=np.array([E*T*width/71,E*T*width**3/(12*71),E*width*T**3/(12*71)])
            ids=s.dofs(3);s.block(ids,np.diag(floor_stiff))
            self.roots[bottom]=dict(ids=ids,point=np.array(point,float),k=floor_stiff,width=width,H=71 if name!='divisoria' else 0)
            mass_height=2052 if name=='divisoria' else 2132
            self.axial_members.append(dict(top=name,bottom=bottom,mass_kg=width*mass_height*18.3*800/1e9))
            for y,dy in stations(ymin,ymin+width,8):
                for x in [point[0]-T/2/math.sqrt(3),point[0]+T/2/math.sqrt(3)]:
                    p=[x,y,0]
                    row=combine((self.root_row(name,p),1),(self.root_row(bottom,p),-1))
                    s.spring(row,E*(T/2*dy)/H)
            if name=='divisoria':
                for y,dy in stations(82,632,8):
                    for x in [1000-9/math.sqrt(3),1000+9/math.sqrt(3)]:
                        p=[x,y,-2052]
                        row=combine((self.root_row(bottom,p),1),(P['P01_base'].displacement_row(p,[0,0,1]),-1))
                        self.contact('pe_divisoria_base',row,self.penalty*9*dy,9*dy,p)
            else:
                for i,y in enumerate([130,290,450,600]):
                    x=18 if name.endswith('esquerda') else 1982;p=[x,y,-2061]
                    row=combine((P['P01_base'].displacement_row(p,[0,0,1]),1),(self.root_row(bottom,p),-1))
                    s.spring(row,self.joint_k)
                # Ligacoes positivas de extremidade da base frontal as
                # extensoes lateraisP01; tambem hipoteticas, nao apoio fixo.
                for y in [20,60]:
                    p=[x,y,-2061]
                    row=combine((P['P01_base_frente'].displacement_row(p,[0,0,1]),1),(self.root_row(bottom,p),-1))
                    s.spring(row,self.joint_k)
        self.floor_pads=[];self.soco_mass=0
        if soco:
            path=ROOT/'04_Moveis/P01/Apoios_ao_piso/Pecas_soco_estudo.csv'
            with path.open(encoding='utf-8-sig',newline='') as f:pieces=list(csv.DictReader(f,delimiter=';'))
            for r in pieces:
                x=float(r['X_mm'])-ORIGIN[0];y=float(r['Y_mm'])-ORIGIN[1]
                L=float(r['L_mm']);B=float(r['P_mm']);H=float(r['H_mm'])
                self.soco_mass+=L*B*H*800/1e9
                for panel in [P['P01_base'],P['P01_base_frente']]:
                    u,v,_=panel.origin
                    x0=max(x,u);x1=min(x+L,u+panel.L);y0=max(y,v);y1=min(y+B,v+panel.B)
                    if x1<=x0 or y1<=y0 or H!=62:continue
                    area=(x1-x0)*(y1-y0)
                    self.floor_pads.append(dict(name=r['id'],panel=panel.name,area_mm2=area))
                    # E/H da madeira em serie com rigidez por area do piso.
                    ka=1/(H/E+1/floor_k_area)
                    for xx,dx in stations(x0,x1,max(2,math.ceil((x1-x0)/180))):
                        for yy,dy in stations(y0,y1,max(2,math.ceil((y1-y0)/180))):
                            p=[xx,yy,-2070]
                            self.contact('piso_'+r['id'],panel.displacement_row(p,[0,0,1]),ka*dx*dy,dx*dy,p)
                            self.contacts[-1]['gap_mm']=floor_gap if r['id']=='Soco_transversal_4_caixa' else 0.
                            self.contacts[-1]['external_floor']=True
        self.K=s.matrix();self.C=np.array([dense(c['row'],s.ndof) for c in self.contacts]);self.ks=np.array([c['k'] for c in self.contacts])
        self.gaps=np.array([c.get('gap_mm',0.) for c in self.contacts])

    def add_walls(self,mesh,soco,floor_k_area):
        s=self.s;P=self.panels;E=self.E;n=round(4*mesh);nh=round(10*mesh)
        specs=[('lateral_esquerda','P01_lateral_E',[9,82,-2132],568,2132),
               ('lateral_direita','P01_lateral_D',[1991,82,-2132],568,2132),
               ('divisoria','P01_divisoria',[1000,82,-2052],550,2052)]
        for root,name,o,width,H in specs:
            wall=P[name]=Panel(s,name,o,[0,1,0],[0,0,1],width,H,n,nh,E=E)
            r=self.roots[root];s.block(r['ids'],-np.diag(r['k']));r['k']*=0
            for y,dy in stations(82,82+width,8):
                for x in [o[0]-9/math.sqrt(3),o[0]+9/math.sqrt(3)]:
                    point=[x,y,0]
                    row=combine((self.root_row(root,point),1),(wall.displacement_row(point,[0,0,1]),-1))
                    s.spring(row,self.penalty*9*dy)
                    self.root_ties.append(dict(root=root,wall=name,row=row,k=self.penalty*9*dy,point=point))
            if root=='divisoria':
                for y,dy in stations(82,632,8):
                    for x in [1000-9/math.sqrt(3),1000+9/math.sqrt(3)]:
                        p=[x,y,-2052]
                        row=combine((wall.displacement_row(p,[0,0,1]),1),(P['P01_base'].displacement_row(p,[0,0,1]),-1))
                        self.contact('pe_divisoria_base',row,self.penalty*9*dy,9*dy,p)
            else:
                for y,dy in stations(82,650,8):
                    for x in [o[0]-9/math.sqrt(3),o[0]+9/math.sqrt(3)]:
                        p=[x,y,-2132]
                        self.contact('piso_'+name,wall.displacement_row(p,[0,0,1]),floor_k_area*9*dy,9*dy,p)
                        self.contacts[-1]['external_floor']=True
                for i,y in enumerate([130,290,450,600]):
                    x=18 if root.endswith('esquerda') else 1982
                    self.joint(f'P01_base_{name}_{i}',P['P01_base'],wall,[x,y,-2061])
                for y in [20,60]:
                    p=[x,y,-2061];pw=[x,82,-2061]
                    receiver=combine((wall.displacement_row(pw,[0,0,1]),1),(wall.rotation_row(pw,[1,0,0]),y-82))
                    row=combine((P['P01_base_frente'].displacement_row(p,[0,0,1]),1),(receiver,-1))
                    s.spring(row,self.joint_k)
        # Tres referencias horizontais na cota do piso; sem apoio vertical fixo.
        s.fixed.update(P['P01_lateral_E'].ids[0,:2]);s.fixed.add(int(P['P01_lateral_D'].ids[0,1]))
        H=2114 if self.rear_support else 2096
        back=P['P01_fundo']=Panel(s,'P01_fundo',[18,641,-2114],[1,0,0],[0,0,1],1964,H,round(14*mesh),nh,E=E)
        for x,name in [(18,'P01_lateral_E'),(1982,'P01_lateral_D'),(1000,'P01_divisoria')]:
            for i,z in enumerate([-1850,-1300,-750,-150]):
                self.joint(f'P01_fundo_{name}_{i}',back,P[name],[x,641 if name!='P01_divisoria' else 632,z])
        for i,x in enumerate([118,338,558,778,998,1218,1438,1658,1878]):
            self.joint(f'P01_fundo_base_{i}',back,P['P01_base'],[x,632,-2061])
        if self.rear_support:
            r=self.roots['fundo_P01_proposto'];s.block(r['ids'],-np.diag(r['k']));r['k']*=0
            for x,dx in stations(18,1982,12):
                for y in [641-9/math.sqrt(3),641+9/math.sqrt(3)]:
                    p=[x,y,0];row=combine((self.root_row('fundo_P01_proposto',p),1),(back.displacement_row(p,[0,0,1]),-1))
                    s.spring(row,self.penalty*9*dx)
        if soco:
            ka=1/(18/E+1/floor_k_area)
            for x,dx in stations(18,1982,12):
                for y in [641-9/math.sqrt(3),641+9/math.sqrt(3)]:
                    p=[x,y,-2114];self.contact('piso_calco_fundo',back.displacement_row(p,[0,0,1]),ka*9*dx,9*dx,p)
                    self.contacts[-1]['external_floor']=True

    def loads(self):
        F,basecases,masses=super().loads();P=self.panels
        # Inclui o peso axial de laterais e divisoria; demaisP01 nao modelados.
        axial=np.zeros(self.s.ndof)
        for m in self.axial_members:
            for name in [m['top'],m['bottom']]:axial[self.roots[name]['ids'][0]]-=m['mass_kg']*G/2
        # Soco: peso equivalente aplicado na base. Nao credita rigidez extra.
        if self.soco_mass:P['P01_base'].add_pressure_rectangle(axial,[0,0],[1964,550],[0,0,-self.soco_mass*G])
        fixedmass=0.
        for name in ['FaixaQuinaAR04','FaixaQuinaBR04']:
            r=motion.D['panels'][name];m=r['volume_mm3']*800/1e9;fixedmass+=m;cg=np.array(r['com_mm'])-ORIGIN
            ref=np.array([cg[0],max(20.,cg[1]),9.])
            if name=='FaixaQuinaBR04':ref=np.array([1770.,cg[1],9.])
            force=np.array([0,0,-m*G]);P['P02_base'].add_point(axial,ref,force,np.cross(cg-ref,force))
        fs=[];cases=[]
        for k,c in enumerate(basecases):
            for content,packing in [(0,'sem'),(20,'centro'),(20,'ponta')]:
                for pose,angle in [('fechadas',0),('ambas86',86)]:
                    f=F[:,k]+axial
                    for name,panel,ref in [('FrenteSimplesR04','P02_lateral',[1359,57,154]),('FrenteSimplesR001','P02_terminal',[1807,-391,154])]:
                        cg=np.r_[motion.neighbors[name][0 if angle==0 else -1].mean(0),2286]-ORIGIN
                        ref=np.array(ref,float);force=np.array([0,0,-2*G])
                        P[panel].add_point(f,ref,force,np.cross(cg-ref,force))
                    if content:
                        lo,hi=([265,535],[465,735]) if packing=='centro' else ([510,20],[560,40])
                        P['P02_base'].add_pressure_rectangle(f,lo,hi,[0,0,-content*G])
                    fs.append(f);cases.append(dict(P03_pose=c['pose'],P03_packing=c['packing'],P02_content_kg=content,P02_packing=packing,P02_pose=pose))
        masses.update(axial_members_mass_kg=sum(m['mass_kg'] for m in self.axial_members),soco_mass_kg=self.soco_mass,P02_trim_mass_kg=fixedmass,P02_doors_kg=4.)
        return np.array(fs).T,cases,masses

    def virtuals(self):
        vs=[]
        for axis in ['z','rx','ry']:
            v=np.zeros(self.s.ndof)
            for p in self.panels.values():
                for n,(x,y,z) in enumerate(p.coords):
                    if axis=='z':v[p.ids[n,2]]=1
                    if axis=='rx':v[p.ids[n,1]]=-z;v[p.ids[n,2]]=y;v[p.ids[n,3]]=1
                    if axis=='ry':v[p.ids[n,0]]=z;v[p.ids[n,2]]=-x;v[p.ids[n,4]]=1
            for i,x in enumerate(self.front_x):
                if axis=='z':v[self.front_ids[i,0]]=1
                if axis=='rx':v[self.front_ids[i,0]]=41;v[self.front_ids[i,2]]=1
                if axis=='ry':v[self.front_ids[i,0]]=-x;v[self.front_ids[i,1]]=-1
            for r in self.roots.values():
                x,y,_=r['point']
                if axis=='z':v[r['ids'][0]]=1
                if axis=='rx':v[r['ids'][0]]=y;v[r['ids'][1]]=1
                if axis=='ry':v[r['ids'][0]]=-x;v[r['ids'][2]]=1
            vs.append(v)
        return np.array(vs)

    def solve_coupled(self,export_config=0):
        F,cases,masses=self.loads();start=time.time();n=self.s.ndof
        effective=F-self.C.T@(self.ks*self.gaps)[:,None]
        allsol=solve_spd(self.K,np.column_stack([effective,self.C.T]),self.s.fixed)
        U=allsol[:,:F.shape[1]];V=allsol[:,F.shape[1]:];M=self.C@V;g0=self.C@U+self.gaps[:,None]
        vs=self.virtuals();outputs=[];csvrows=[];envelopes={};floorenv={};maxres=np.zeros(3)
        # Corte independente do P02: cargas, contato P01 e ligacaoC01.
        pv=np.zeros((6,n));center=np.array([1350,326,154])
        for name,p in self.panels.items():
            if not name.startswith('P02_'):continue
            for ni,xyz in enumerate(p.coords):
                for axis,e in enumerate(np.eye(3)):
                    pv[axis,p.ids[ni,:3]]=e
                    pv[axis+3,p.ids[ni,:3]]=np.cross(e,xyz-center);pv[axis+3,p.ids[ni,3:]]=e
        maxcut=np.zeros(6);maxdiv=0.
        jointrows=[np.array([dense(row,n) for row in j['rows']]) for j in self.box_joints]
        crows=[np.array([dense(row,n) for row in j['rows']]) for j in self.c01]
        previous_off=[]
        for ic,case in enumerate(cases):
            off=previous_off.copy()
            for iteration in range(400):
                u=U[:,ic].copy();g=g0[:,ic].copy()
                if off:
                    z=np.linalg.solve(np.diag(1/self.ks[off])-M[np.ix_(off,off)],g0[off,ic]);u+=V[:,off]@z;g+=M[:,off]@z
                active=[i for i in range(len(self.ks)) if i not in off];reaction=-self.ks*g;reaction[off]=0
                neg=[i for i in active if reaction[i]<-1e-5]
                if neg:off.append(min(neg,key=lambda i:reaction[i]));continue
                pen=[i for i in off if g[i]<-1e-7]
                if pen:off.remove(min(pen,key=lambda i:g[i]));continue
                break
            else:raise AssertionError('Contatos sem convergencia')
            previous_off=off.copy()
            ground=np.zeros(n)
            for r in self.roots.values():ground[r['ids']]-=r['k']*u[r['ids']]
            residual=self.K@u-effective[:,ic]
            for i in off:residual-=self.ks[i]*self.C[i]*g[i]
            fixed=np.zeros(n)
            for i in self.s.fixed:fixed[i]=residual[i]
            check=vs@(F[:,ic]+ground+fixed+self.C.T@reaction)
            maxres=np.maximum(maxres,np.abs(check));assert abs(check[0])<.001 and max(abs(check[1:]))<.1,check
            linear_ok=bool(max(-min(u[self.panels[k].ids[:,2]]) for k in ['base','P02_base','P01_base'])<T/2)
            c01=[];totalforce=np.zeros(3);totalmoment=np.zeros(3)
            for j,rows in zip(self.c01,crows):
                delta=rows@u;force=-self.options['c01_k']*delta
                totalforce+=force;totalmoment+=np.cross(np.array(j['point_mm'])-[1350,326,154],force)
                row=dict(configuration=export_config,case=ic,**case,joint=j['name'],x_mm=ORIGIN[0]+j['point_mm'][0],y_mm=ORIGIN[1]+j['point_mm'][1],z_mm=ORIGIN[2]+j['point_mm'][2],
                    tension_N=max(0.,-force[0]),Fy_N=force[1],Fz_N=force[2],shear_N=float(np.linalg.norm(force[1:])),resultant_N=float(np.linalg.norm(force)),relative_translation_mm=float(np.linalg.norm(delta)),small_displacement_screen_ok=linear_ok)
                csvrows.append(row);c01.append(row)
            for i,c in enumerate(self.contacts):
                if c['receiver']=='C01_face':
                    force=np.array([reaction[i],0,0]);totalforce+=force;totalmoment+=np.cross(np.array(c['point_mm'])-[1350,326,154],force)
            cut=pv@F[:,ic]+np.r_[totalforce,totalmoment]
            for i,c in enumerate(self.contacts):
                if c['receiver'].startswith('P02_'):
                    force=np.array([0.,0.,reaction[i]])
                    cut+=np.r_[force,np.cross(np.array(c['point_mm'])-center,force)]
            maxcut=np.maximum(maxcut,np.abs(cut));assert max(abs(cut[:3]))<.001 and max(abs(cut[3:]))<.1,cut
            divtop=sum(-j['k']*dense(j['row'],n)@u for j in self.root_ties if j['root']=='divisoria')
            divback=0.
            for j,rows in zip(self.box_joints,jointrows):
                force=-self.joint_k*rows@u;mag=float(np.linalg.norm(force));r=envelopes.setdefault(j['name'],dict(name=j['name'],max_resultant_N=0,critical_case=None))
                if mag>r['max_resultant_N']:r.update(max_resultant_N=mag,critical_case=ic,force_N=force.tolist())
                if j['panels']==['P01_fundo','P01_divisoria']:divback-=force[2]
            floor_force=0;floor_div=0;pressure=0;footforce=0;footmoment=0
            for i,c in enumerate(self.contacts):
                if c.get('external_floor'):
                    floor_force+=reaction[i];p=reaction[i]/c['area_mm2'];pressure=max(pressure,p)
                    if c['receiver']=='piso_Soco_transversal_4_caixa':floor_div+=reaction[i]
                    e=floorenv.setdefault(c['receiver'],dict(max_pressure_MPa=0,max_point_force_N=0))
                    e['max_pressure_MPa']=max(e['max_pressure_MPa'],float(p));e['max_point_force_N']=max(e['max_point_force_N'],float(reaction[i]))
                if c['receiver']=='pe_divisoria_base':footforce+=reaction[i];footmoment+=(c['point_mm'][1]-357)*reaction[i]
            p=self.panels['base'];q=self.panels['P02_base'];b=self.panels['P01_base']
            bprobe=dense(b.displacement_row([1000,357,-2052],[0,0,1]),n)@u
            root=self.roots['divisoria'];rootw=float(u[root['ids'][0]])
            if 'P01_divisoria' in self.panels:
                divmass=masses['panel_mass_kg']['P01_divisoria']
                divres=footforce+divback-divtop-divmass*G;maxdiv=max(maxdiv,abs(divres));assert abs(divres)<.001,divres
            outputs.append(dict(case,case_index=ic,P03_base_down_mm=float(-min(u[p.ids[:,2]])),P02_base_down_mm=float(-min(u[q.ids[:,2]])),
                P01_base_down_mm=float(-min(u[b.ids[:,2]])),P01_base_below_divider_down_mm=float(-bprobe),divider_top_down_mm=-rootw,
                divider_foot_force_N=float(footforce),divider_foot_moment_X_Nm=float(footmoment/1000),
                divider_top_load_N=float(divtop),divider_back_action_on_divider_N=float(divback),
                C01_force_on_P02_N=totalforce.tolist(),C01_moment_at_face_center_Nm=(totalmoment/1000).tolist(),
                max_C01_shear_N=max(r['shear_N'] for r in c01),max_C01_tension_N=max(r['tension_N'] for r in c01),
                floor_total_N=float(floor_force),floor_under_divider_N=float(floor_div),floor_peak_pressure_MPa=float(pressure),
                active_contacts=len(active),iterations=iteration+1,
                small_displacement_screen_ok=linear_ok))
        return dict(options=self.options,unknowns=n,mass_hypotheses=masses,cases=outputs,joint_envelopes=list(envelopes.values()),floor_envelopes=floorenv,
                    equilibrium_max_residual_N_Nmm_Nmm=maxres.tolist(),P02_cut_max_residual_N_Nmm=maxcut.tolist(),divider_vertical_cut_max_residual_N=maxdiv,seconds=time.time()-start),csvrows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--quick',action='store_true');args=ap.parse_args()
    configs=[dict(soco=False),dict(soco=True)]
    if not args.quick:
        configs += [dict(soco=True,base_thickness=25.),dict(soco=True,c01_k=100.),dict(soco=True,c01_k=2000.),
                    dict(soco=True,c01_n=6),dict(soco=True,floor_k_area=.1),dict(soco=True,floor_k_area=10.),
                    dict(soco=True,floor_gap=.2),dict(soco=True,floor_gap=1.),dict(soco=True,mesh=1.5),
                    dict(soco=True,rear_support=True),dict(soco=True,joint_k=100.),
                    dict(soco=True,c01_n=6,c01_spread=True),
                    dict(soco=True,c01_n=6,c01_spread=True,rear_support=True),
                    dict(soco=True,c01_n=6,c01_spread=True,rear_support=True,base_thickness=25.),
                    dict(soco=True,c01_n=6,c01_spread=True,mesh=1.5),
                    dict(soco=True,c01_n=6,c01_spread=True,mesh=2.,lower_mesh=1.5)]
    results=[];export=[]
    for idx,cfg in enumerate(configs):
        r,rows=Coupled(**cfg).solve_coupled(idx);results.append(r);export+=rows
        print(json.dumps(dict(configuration=idx,options=cfg,seconds=r['seconds'],P03_mm=max(c['P03_base_down_mm'] for c in r['cases']),P01_mm=max(c['P01_base_below_divider_down_mm'] for c in r['cases']),C01_shear_N=max(c['max_C01_shear_N'] for c in r['cases']),C01_tension_N=max(c['max_C01_tension_N'] for c in r['cases']),linear_screen_cases=sum(c['small_displacement_screen_ok'] for c in r['cases'])),ensure_ascii=True),flush=True)
    d=dict(source_sha256=motion.D['source_sha256'],source_unchanged=motion.sha(ROOT/motion.D['source'])==motion.D['source_sha256'],configurations=results,
        limitations=['Casca isotropica linear;E1100 e rigidezes de juntas/piso sao hipoteses. Sem ensaio/capacidade homologados.',
            'P02 base/topo em L inteiros;sem junta ficticia no recorte e sem ligacao direta entre fundos que so compartilham aresta.',
            'C014/6 molasXYZ e contato normal sem atrito;nao produto dimensionado ou furo aprovado.',
            'P01 base/frente,laterais,divisoria e fundo como cascas com juntas;receptores superiores ajustados como secoes planas. Extensoes frontais ainda reduzidas a braços/ligacoes positivas hipoteticas. Sem buckling/retencao.',
            'Soco e 21pecas anteriores separados do CAD;contato por areaE/H em serie com piso parametrico. Nivelamento/contato real desconhecidos.',
            'P01: pesos das bases,laterais/divisoria,fundo e travessa superior;demais prateleiras/varoes/gavetas,extensoes laterais e conteudo ainda ausentes. Nao e envelope global de uso.',
            'FundoP01 modelado continuo;formato nao cabe em2750x1850. Fornecimento inteiro ou emenda estrutural/rigidez precisam ser demonstrados.',
            'P02 portas2kg acabadas cada e1kg de acessorios fixos compartilhado entre todasjuntas sao reservas;faixas so entram como peso,sem rigidez.',
            'P03 recebe20kg totais de malas;P02 compara0/20kg em centro/ponta,sem recomendar20kg no retorno.',
            'Sem impacto/manuseio,folgas reais dos conectores,fluencia medida ou verificacao de esmagamento/arrancamento/furos.',
            'Deslocamentos grandes invalidam a hipotese linear;triagem interna nao e criterio de aceitação.'],
        gate='ESTUDO_CONDICIONAL;nao libera20kg oufabricacao;R52 nao aberta/alterada')
    if not args.quick:
        (OUT/'Ligacao_P02_P03.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
        with (OUT/'Ligacao_C01_solicitacoes.csv').open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(export[0]),delimiter=';');w.writeheader();w.writerows(export)

if __name__=='__main__':main()
