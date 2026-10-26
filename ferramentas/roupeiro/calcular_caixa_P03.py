"""P03/A: paineis acoplados, juntas discretas e receptores flexiveis P01.

Pequenas deformacoes, casca MITC retangular e molas de estudo. Sem CAD.
Numeros sao condicionais: nenhuma rigidez/capacidade de junta e homologada.
"""
import argparse,csv,hashlib,json,math,time
from pathlib import Path
import numpy as np
from casca_linear import System,Panel,combine,dense,solve_spd,validate
import detalhar_portas_maleiro as motion

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/P03'
G=9.80665;ORIGIN=np.array([5390.,3290.,2132.]);T=17.7
joint_axes=np.eye(3)

class Model:
    def __init__(self,closed_back=False,nx=12,ny=6,E=1100.,joint_k=500.,root_k=1000.,front_rotation_k=1e5,penalty=100.,rear_support=False,box_rotation_k=0.,front_rail_height=0.,base_thickness=18.):
        self.s=System();self.closed_back=closed_back;self.nx=nx;self.ny=ny;self.E=E;self.joint_k=joint_k
        self.root_k=root_k;self.front_rotation_k=front_rotation_k;self.penalty=penalty
        self.rear_support=rear_support
        self.box_rotation_k=box_rotation_k
        self.front_rail_height=front_rail_height
        self.base_thickness=base_thickness;self.base_z=base_thickness/2
        assert not rear_support or closed_back
        nz=max(2,ny//2);P=self.panels={};depth=630. if closed_back else 612.
        P['base']=Panel(self.s,'base',[18,20,self.base_z],[1,0,0],[0,1,0],1314,depth,nx,ny,t=base_thickness-.3,E=E*(2100/2200 if base_thickness==25 else 1))
        P['topo']=Panel(self.s,'topo',[18,20,299],[1,0,0],[0,1,0],1314,depth,nx,ny,E=E)
        P['fundo']=Panel(self.s,'fundo',[18,641,base_thickness],[1,0,0],[0,0,1],1314,290-base_thickness,nx,nz,E=E)
        P['esquerda']=Panel(self.s,'esquerda',[9,20,0],[0,1,0],[0,0,1],630,308,ny,nz,E=E)
        P['direita']=Panel(self.s,'direita',[1341,20,0],[0,1,0],[0,0,1],630,308,ny,nz,E=E)
        # Tres restricoes exclusivamente horizontais removem modos rigidos.
        # Todas na cota0; nao criam apoio vertical ou momento horizontal.
        self.s.fixed.update(P['esquerda'].ids[0,:2]);self.s.fixed.add(int(P['direita'].ids[0,1]))
        self.box_joints=[]
        for side,x in [('esquerda',18),('direita',1332)]:
            for horizontal,z in [('base',self.base_z),('topo',299)]:
                for i,y in enumerate([70,230,390,550]):self.joint(f'{horizontal}_{side}_{i+1}',P[horizontal],P[side],[x,y,z])
            for i,z in enumerate([68,230]):self.joint(f'fundo_{side}_{i+1}',P['fundo'],P[side],[x,641,z])
        if closed_back:
            for horizontal,z in [('base',base_thickness),('topo',290)]:
                for i,x in enumerate([118,338,558,778,998,1218]):self.joint(f'{horizontal}_fundo_{i+1}',P[horizontal],P['fundo'],[x,641,z])
        # P01 reduzido: mesmo receptor recebe simultaneamente contato direto,
        # travessa frontal e extensao. A divisoria inclui uma complacencia de raiz.
        self.roots={};self.ground=[]
        for name,x,y,width,H in [('lateral_esquerda',9,366,568,2132),('divisoria',1000,357,550,2052),('lateral_direita',1991,366,568,2132)]:
            ids=self.s.dofs(3);ka=E*T*width/H
            kw=1/(1/ka+1/root_k) if name=='divisoria' else ka
            stiff=[kw,E*T*width**3/(12*H),E*width*T**3/(12*H)]
            self.s.block(ids,np.diag(stiff));self.roots[name]=dict(ids=ids,point=np.array([x,y,0.]),k=np.array(stiff),width=width,H=H)
            self.ground.append((ids,np.array(stiff)))
        if rear_support:
            ids=self.s.dofs(3);width=1964.;H=2114.
            stiff=np.array([E*T*width/H,E*width*T**3/(12*H),E*T*width**3/(12*H)])
            self.s.block(ids,np.diag(stiff))
            self.roots['fundo_P01_proposto']=dict(ids=ids,point=np.array([1000.,641.,0.]),k=stiff,width=width,H=H)
        self.front_n=24;self.front_x=np.linspace(9,1991,self.front_n+1);self.front_ids=self.s.dofs(3*len(self.front_x)).reshape(-1,3)
        # Viga frontal P01: flexao longitudinal + torcaoSaintVenant.
        b=82.;I=b*T**3/12+T*front_rail_height**3/12
        J=b*T**3/3*(1-.63*T/b+.052*(T/b)**5);GG=E/(2*1.3)
        if front_rail_height:
            J+=front_rail_height*T**3/3*(1-.63*T/front_rail_height+.052*(T/front_rail_height)**5)
        for i in range(self.front_n):
            h=self.front_x[i+1]-self.front_x[i]
            ke=E*I/h**3*np.array([[12,6*h,-12,6*h],[6*h,4*h*h,-6*h,2*h*h],[-12,-6*h,12,-6*h],[6*h,2*h*h,-6*h,4*h*h]])
            self.s.block(self.front_ids[[i,i+1],:2].flatten(),ke)
            self.s.block(self.front_ids[[i,i+1],2],GG*J/h*np.array([[1,-1],[-1,1]]))
        self.front_joints=[]
        for name in ['lateral_esquerda','divisoria','lateral_direita']:
            x=self.roots[name]['point'][0]
            vert=combine((self.beam_row(x,82),1),(self.root_row(name,[x,82,0]),-1))
            rot=combine((self.beam_rotation_row(x),1),({int(self.roots[name]['ids'][1]):1},-1))
            self.s.spring(vert,joint_k);self.s.spring(rot,front_rotation_k)
            self.front_joints.append(dict(receiver=name,vertical_row=vert,rotation_row=rot))
        self.contacts=[]
        def points(lo,hi,n):
            for i in range(n):yield lo+(hi-lo)*(i+.5)/n,(hi-lo)/n
        # Areas reais, inclusive largura18 e frentes remanescentes62 aposrecuo20.
        for lo,hi,n,label in [(20,82,2,'extensao_frontal_esquerda'),(82,650,8,'lateral_esquerda')]:
            for y,dy in points(lo,hi,n):
                for x in [9-9/math.sqrt(3),9+9/math.sqrt(3)]:
                    row=combine((P['esquerda'].displacement_row([x,y,0],[0,0,1]),1),(self.root_row('lateral_esquerda',[x,y,0]),-1))
                    area=9*dy;k=penalty*area
                    if y<82:k=1/(1/k+1/(4*joint_k*dy/62/2))
                    self.contact(label,row,k,area,[x,y,0])
        for y,dy in points(82,632,8):
            for x in [1000-9/math.sqrt(3),1000+9/math.sqrt(3)]:
                row=combine((P['base'].displacement_row([x,y,0],[0,0,1]),1),(self.root_row('divisoria',[x,y,0]),-1))
                self.contact('divisoria',row,penalty*9*dy,9*dy,[x,y,0])
        for x,dx in points(18,1332,12):
            for y in [51-31/math.sqrt(3),51+31/math.sqrt(3)]:
                row=combine((P['base'].displacement_row([x,y,0],[0,0,1]),1),(self.beam_row(x,y),-1))
                self.contact('travessa_frontal_base',row,penalty*31*dx,31*dx,[x,y,0])
        for y,dy in points(20,82,2):
            for x in [1341-9/math.sqrt(3),1341+9/math.sqrt(3)]:
                row=combine((P['direita'].displacement_row([x,y,0],[0,0,1]),1),(self.beam_row(x,y),-1))
                self.contact('travessa_frontal_lateral_direita',row,penalty*9*dy,9*dy,[x,y,0])
        if rear_support:
            for x,dx in points(18,1332,12):
                for y in [641-9/math.sqrt(3),641+9/math.sqrt(3)]:
                    row=combine((P['base'].displacement_row([x,y,0],[0,0,1]),1),(self.root_row('fundo_P01_proposto',[x,y,0]),-1))
                    self.contact('fundo_P01_proposto_base',row,penalty*9*dx,9*dx,[x,y,0])
            for x in [1341-9/math.sqrt(3),1341+9/math.sqrt(3)]:
                for y in [641-9/math.sqrt(3),641+9/math.sqrt(3)]:
                    row=combine((P['direita'].displacement_row([x,y,0],[0,0,1]),1),(self.root_row('fundo_P01_proposto',[x,y,0]),-1))
                    self.contact('fundo_P01_proposto_lateral_direita',row,penalty*81,81,[x,y,0])
        self.K=self.s.matrix();self.C=np.array([dense(r['row'],self.s.ndof) for r in self.contacts]);self.ks=np.array([r['k'] for r in self.contacts])
    def root_row(self,name,point):
        root=self.roots[name];dx,dy,_=np.array(point)-root['point'];i=root['ids']
        return {int(i[0]):1.,int(i[1]):float(dy),int(i[2]):float(-dx)}
    def beam_shapes(self,x):
        i=min(int((x-9)/(1991-9)*self.front_n),self.front_n-1);h=self.front_x[i+1]-self.front_x[i];r=(x-self.front_x[i])/h
        return i,h,r,np.array([1-3*r*r+2*r**3,h*(r-2*r*r+r**3),3*r*r-2*r**3,h*(-r*r+r**3)])
    def beam_row(self,x,y=41):
        i,h,r,N=self.beam_shapes(x);row={int(j):float(v) for j,v in zip(self.front_ids[[i,i+1],:2].flatten(),N)}
        row[int(self.front_ids[i,2])]=(y-41)*(1-r);row[int(self.front_ids[i+1,2])]=(y-41)*r
        return {k:v for k,v in row.items() if abs(v)>1e-15}
    def beam_rotation_row(self,x):
        i,h,r,N=self.beam_shapes(x);return {int(self.front_ids[i,2]):1-r,int(self.front_ids[i+1,2]):r}
    def joint(self,name,a,b,point):
        rows=[]
        for e in joint_axes:
            row=combine((a.displacement_row(point,e),1),(b.displacement_row(point,e),-1));self.s.spring(row,self.joint_k);rows.append(row)
        direction=np.array([1,0,0] if b.name=='fundo' else ([0,0,1] if a.name=='fundo' else [0,1,0]))
        rotation=combine((a.rotation_row(point,direction),1),(b.rotation_row(point,direction),-1))
        if self.box_rotation_k:self.s.spring(rotation,self.box_rotation_k)
        self.box_joints.append(dict(name=name,panels=[a.name,b.name],point_mm=list(point),rows=rows,rotation_row=rotation,rotation_axis=direction.tolist()))
    def contact(self,label,row,k,area,point):
        self.s.spring(row,k);self.contacts.append(dict(receiver=label,row=row,k=k,area_mm2=area,point_mm=list(point)))
    def loads(self):
        fs=[];cases=[]
        own=np.zeros(self.s.ndof);mass={p.name:p.own_weight(own,mass_thickness=self.base_thickness+.3 if p.name=='base' else 18.3) for p in self.panels.values()}
        frontmass=1964*(82+self.front_rail_height)*18.3*800/1e9
        for i in range(self.front_n):
            h=self.front_x[i+1]-self.front_x[i];q=-frontmass*G/(1991-9)
            own[self.front_ids[[i,i+1],:2].flatten()]+=q*np.array([h/2,h*h/12,h/2,-h*h/12])
        # Reserva1kg de fixacoes fixas, nao massa pesada; distribuida nas estacoes.
        for j in self.box_joints:self.panels[j['panels'][0]].add_point(own,j['point_mm'],[0,0,-G/len(self.box_joints)])
        mm=np.eye(4);mm[2,3]=2132
        doorrows=[dict(side='left',module_matrix=mm.tolist(),hinge_support_inner_x_mm=5408,hinge_origin_y_mm=3346.5,closed_leaf_base=[5392,3290,1],front_local_box=[0,0,0,672,18,306]),
                  dict(side='right',module_matrix=mm.tolist(),hinge_support_inner_x_mm=6722,hinge_origin_y_mm=3346.5,closed_leaf_base=[6738,3290,1],front_local_box=[-672,0,0,0,18,306])]
        for pose,angles in [('fechadas',[0,0]),('esquerda86',[86,0]),('direita86',[0,86]),('ambas86',[86,86])]:
            for packing in ['areas_centrais','areas_frente','duas_areas50_frente','oito_areas50']:
                f=own.copy();doorcenters=[]
                for row,ang,name,x in zip(doorrows,angles,['esquerda','direita'],[18,1332]):
                    xy=motion.polygons(row,[ang])[0].mean(0);cg=np.array([xy[0],xy[1],2286])-ORIGIN
                    ref=np.array([x,57,154]);force=np.array([0,0,-4*G]);moment=np.cross(cg-ref,force)
                    self.panels[name].add_point(f,ref,force,moment);doorcenters.append(cg.tolist())
                base=self.panels['base']
                for x in [115.,685.]:
                    x-=18 # coordenada local da base; global relativo ao apto e x+18
                    if packing.startswith('areas_'):
                        y=120-20 if packing=='areas_centrais' else 0
                        base.add_pressure_rectangle(f,[x,y],[x+550,y+350],[0,0,-10*G])
                    elif packing=='duas_areas50_frente':
                        base.add_pressure_rectangle(f,[x+250,0],[x+300,50],[0,0,-10*G])
                    else:
                        for dx in [25,475]:
                            for y in [125,375]:
                                base.add_pressure_rectangle(f,[x+dx,y],[x+dx+50,y+50],[0,0,-2.5*G])
                fs.append(f);cases.append(dict(pose=pose,packing=packing,content_kg=20,door_centers_relative_mm=doorcenters))
        return np.array(fs).T,cases,dict(panel_mass_kg=mass,door_mass_kg=8.,fixed_accessory_reserve_kg=1.,P01_front_mass_kg=frontmass)
    def solve(self,stress=False):
        F,cases,masses=self.loads();start=time.time()
        # Uma fatoracao por configuracao, todas as cargas e flexibilidades dos
        # contatos. DowndateWoodbury resolve o conjunto sem reacoes de tracao.
        allsol=solve_spd(self.K,np.column_stack([F,self.C.T]),self.s.fixed)
        U=allsol[:,:F.shape[1]];V=allsol[:,F.shape[1]:];M=self.C@V;g0=self.C@U
        outputs=[]
        for k,case in enumerate(cases):
            off=[];last=None
            for iteration in range(250):
                u=U[:,k].copy();g=g0[:,k].copy()
                if off:
                    B=np.diag(1/self.ks[off])-M[np.ix_(off,off)]
                    z=np.linalg.solve(B,g0[off,k]);u+=V[:,off]@z;g+=M[:,off]@z
                active=[i for i in range(len(self.ks)) if i not in off]
                reaction=-self.ks*g;reaction[off]=0
                neg=[i for i in active if reaction[i]<-1e-6]
                if neg:off.append(min(neg,key=lambda i:reaction[i]));continue
                penetration=[i for i in off if g[i]<-1e-7]
                if penetration:off.remove(min(penetration,key=lambda i:g[i]));continue
                break
            else:raise AssertionError('Contatos sem convergencia')
            roots={};groundR=np.zeros(self.s.ndof)
            for name,r in self.roots.items():
                vals=-r['k']*u[r['ids']];groundR[r['ids']]+=vals
                roots[name]=dict(vertical_reaction_N=float(vals[0]),moment_X_Nmm=float(vals[1]),moment_Y_Nmm=float(vals[2]),
                    vertical_settlement_mm=float(-u[r['ids'][0]]),rotation_X_rad=float(u[r['ids'][1]]),rotation_Y_rad=float(u[r['ids'][2]]))
            # Equilibrio global: deriva virtual rigidaZ/Rx/Ry dos elementos.
            # Os graus de liberdade de parede representam a secao no corteZ0.
            checks=[]
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
                for name,r in self.roots.items():
                    x,y,z=r['point']
                    if axis=='z':v[r['ids'][0]]=1
                    if axis=='rx':v[r['ids'][0]]=y;v[r['ids'][1]]=1
                    if axis=='ry':v[r['ids'][0]]=-x;v[r['ids'][2]]=1
                # Reacoes horizontais dos tres graus fixos devem ser incluidas.
                residual=self.K@u-F[:,k]
                for i in off:residual-=self.ks[i]*self.C[i]*(self.C[i]@u)
                # K contem fundacoes: apoio sobre estrutura = -Kground*u.
                reaction_fixed=np.zeros(self.s.ndof)
                for i in self.s.fixed:reaction_fixed[i]=residual[i]
                check=float(v@(F[:,k]+groundR+reaction_fixed));checks.append(check)
            assert abs(checks[0])<1e-3 and max(abs(x) for x in checks[1:])<.1,checks
            by_receiver={}
            for label in sorted({c['receiver'] for c in self.contacts}):
                ix=[i for i,c in enumerate(self.contacts) if c['receiver']==label]
                by_receiver[label]=dict(force_N=float(sum(reaction[ix])),active=sum(i not in off for i in ix),points=len(ix))
            joints=[]
            for j in self.box_joints:
                delta=np.array([dense(row,self.s.ndof)@u for row in j['rows']]);force=-self.joint_k*delta
                joints.append(dict(name=j['name'],panels=j['panels'],point_relative_mm=j['point_mm'],
                    force_on_first_panel_N=force.tolist(),resultant_N=float(np.linalg.norm(force)),relative_displacement_mm=delta.tolist(),
                    moment_about_seam_Nmm=float(-self.box_rotation_k*dense(j['rotation_row'],self.s.ndof)@u),rotation_axis=j['rotation_axis']))
            vertical={p.name:float(-np.min(u[p.ids[:,2]])) for p in self.panels.values()}
            base=self.panels['base'];defl=u[base.ids[:,2]];frontsett=[]
            for x in [18,1000,1332]:frontsett.append(float(dense(base.displacement_row([x,20,self.base_z],[0,0,1]),self.s.ndof)@u))
            fr=[]
            for j in self.front_joints:
                fr.append(dict(receiver=j['receiver'],vertical_on_front_N=float(-self.joint_k*dense(j['vertical_row'],self.s.ndof)@u),
                               torsion_on_front_Nmm=float(-self.front_rotation_k*dense(j['rotation_row'],self.s.ndof)@u)))
            case=dict(case,base_max_down_mm=vertical['base'],panel_max_down_mm=vertical,
                      base_max_down_location_relative_mm=base.coords[int(np.argmin(defl))].tolist(),
                      front_base_w_at_x18_1000_1332_mm=frontsett,root_reactions=roots,contact_reactions=by_receiver,
                      box_joints=joints,front_P01_joints=fr,removed_contacts=len(off),iterations=iteration+1,
                      equilibrium_residual_N_Nmm_Nmm=checks,
                      max_inactive_penetration_mm=max([max(0,-g[i]) for i in off]+[0]),
                      contact_min_active_reaction_N=float(min(reaction[active])),
                      maximum_box_joint_N=max(j['resultant_N'] for j in joints),
                      small_displacement_screen_ok=bool(vertical['base']<T/2 and max(abs(u[self.front_ids[:,2]]))<.1))
            if stress:case['nominal_stress']={p.name:p.stress(u) for p in self.panels.values()}
            outputs.append(case)
        return dict(closed_back=self.closed_back,rear_support=self.rear_support,front_rail_height_mm=self.front_rail_height,base_thickness_mm=self.base_thickness,nx=self.nx,ny=self.ny,unknowns=self.s.ndof,E_MPa=self.E,
                    joint_translation_k_per_station_N_mm=self.joint_k,divider_root_k_N_mm=self.root_k,
                    joint_rotation_k_per_station_Nmm_rad=self.box_rotation_k,
                    front_joint_rotation_k_Nmm_rad=self.front_rotation_k,contact_penalty_N_mm3=self.penalty,
                    mass_hypotheses=masses,cases=outputs,seconds=time.time()-start)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--quick',action='store_true');a=ap.parse_args()
    out=[];configs=[]
    if a.quick:configs=[dict(closed_back=False,nx=8,ny=4),dict(closed_back=True,nx=8,ny=4),dict(closed_back=True,rear_support=True,nx=8,ny=4)]
    else:
        configs=[dict(closed_back=False,nx=12,ny=6),dict(closed_back=True,nx=12,ny=6),
                 dict(closed_back=True,rear_support=True,nx=12,ny=6)]
        for h in [60.,80.,100.]:configs.append(dict(closed_back=True,nx=12,ny=6,front_rail_height=h))
        preferred=dict(closed_back=True,nx=12,ny=6,front_rail_height=80.)
        for n,y in [(8,4),(16,8)]:configs.append(dict(preferred,nx=n,ny=y))
        for k in [20.,100.,2000.]:configs.append(dict(preferred,joint_k=k))
        for root in [2.,100.,500.,2000.]:configs.append(dict(preferred,root_k=root))
        configs+=[dict(preferred,E=2200.),dict(preferred,E=700.),dict(preferred,front_rotation_k=1e4),
                  dict(preferred,penalty=1000.),dict(preferred,rear_support=True),dict(preferred,box_rotation_k=1e5)]
        # Alternativa sem a longarina que interfere nas reservas da porta P01.
        base25=dict(closed_back=True,nx=12,ny=6,base_thickness=25.)
        configs += [base25,dict(base25,rear_support=True),
                    dict(base25,rear_support=True,box_rotation_k=1e5),
                    dict(base25,rear_support=True,box_rotation_k=1e6),
                    dict(base25,nx=16,ny=8),dict(base25,penalty=1000.),
                    dict(base25,joint_k=100.),dict(base25,root_k=100.)]
    for cfg in configs:
        r=Model(**cfg).solve(stress=not a.quick);out.append(r)
        print(json.dumps(dict(config=cfg,seconds=r['seconds'],max_base_mm=max(c['base_max_down_mm'] for c in r['cases']),max_joint_N=max(c['maximum_box_joint_N'] for c in r['cases'])),ensure_ascii=True),flush=True)
    # Uma envoltoria por estacao em cada configuracao; manter a carga por caso
    # da proposta principal emCSV para conferencia independente sem JSONenorme.
    export=[]
    for idx,r in enumerate(out):
        groups={}
        for ic,c in enumerate(r['cases']):
            joints=c['box_joints']
            for j in joints:
                g=groups.setdefault(j['name'],dict(name=j['name'],panels=j['panels'],point_relative_mm=j['point_relative_mm'],
                    force_min_N=[1e99]*3,force_max_N=[-1e99]*3,max_resultant_N=0,max_absolute_seam_moment_Nm=0,max_relative_translation_mm=0,critical_case=None))
                for axis in range(3):
                    g['force_min_N'][axis]=min(g['force_min_N'][axis],j['force_on_first_panel_N'][axis]);g['force_max_N'][axis]=max(g['force_max_N'][axis],j['force_on_first_panel_N'][axis])
                if j['resultant_N']>g['max_resultant_N']:g['max_resultant_N']=j['resultant_N'];g['critical_case']=[c['pose'],c['packing']]
                g['max_absolute_seam_moment_Nm']=max(g['max_absolute_seam_moment_Nm'],abs(j['moment_about_seam_Nmm'])/1000)
                g['max_relative_translation_mm']=max(g['max_relative_translation_mm'],float(np.linalg.norm(j['relative_displacement_mm'])))
                if idx in [1,21,22,24]:
                    export.append(dict(case=ic,pose=c['pose'],packing=c['packing'],joint=j['name'],
                        configuration=idx,
                        x_mm=ORIGIN[0]+j['point_relative_mm'][0],y_mm=ORIGIN[1]+j['point_relative_mm'][1],z_mm=ORIGIN[2]+j['point_relative_mm'][2],
                        Fx_N=j['force_on_first_panel_N'][0],Fy_N=j['force_on_first_panel_N'][1],Fz_N=j['force_on_first_panel_N'][2],
                        resultant_N=j['resultant_N'],seam_moment_Nm=j['moment_about_seam_Nmm']/1000))
            c['critical_joint']=max(joints,key=lambda j:j['resultant_N'])
            if not a.quick:del c['box_joints']
        r['joint_envelopes']=list(groups.values())
    result=dict(source_sha256=motion.D['source_sha256'],source_unchanged=motion.sha(ROOT/motion.D['source'])==motion.D['source_sha256'],
                quick=a.quick,numerical_validation=validate(),configurations=out,
                proposed_closed_geometry=dict(side_mm=[630,308,18],base_top_mm=[1314,630,18],current_A_base_top_mm=[1314,612,18],
                    added_depth_at_back_mm=18,external_envelope_mm=[1350,650,308],internal_clear_mm=[1314,612,272],
                    added_mass_hypothesis_800_t18_3_kg=2*1314*18*18.3*800/1e9),
                alternative_base25=dict(base_mm=[1314,630,25],back_mm=[1314,265,18],internal_clear_mm=[1314,612,265],
                    suitcase250_nominal_vertical_remainder_mm=15,selection='ESTUDO, nao adotada',
                    lower_plate_screw_nominal_above_base_mm=12),
                limitations=['Casca isotropica linear;17.7 resistente,18.3massa,rho800,nu0.30.E1100 diferido e hipotese,E2200 imediato referencia.',
                    'Molas20/100/500/2000 por estacao sao parametros,nao curvasConfirmat+cavilha. Rotacoes das juntasP03 livres no caso principal;semcola/atrito presumidos.',
                    'Fundo so recebejuntasbase/topo no cenario fechado;encontro dearesta atualnao virou apoio ficticio.',
                    'P01 reduzido a secoes axiais/rotacionais e viga frontal comtorcao;nao e modelo completo da caixaP01, piso,soco ouretencao.',
                    'Rigidez da raiz da divisoria e sensibilidade;nao credita automaticamente socoR01. Rigidezesrotacionais da raizP01 ainda referencia ideal.',
                    'Ligacoes da travessa/extensoesP01 sao positivas e hipoteticas,nao gabarito nem capacidade;descrever demandasantesdefechar caminhoaopiso.',
                    'LongarinaP01 e sensibilidade de EI/GJ independente adicionado a travessa,sem termo de secao composta. Compatibilidade vertical/torcional entre pecas e ligacoes ainda deve ser demonstrada;modelo equivalente naoreproduz todos os offsets da montagem.',
                    'Reserva1kg de acessoriosfixos nao e pesagem. Malas20kg em areas/patches deestudo,nao rodas reais.',
                    'SemP02 acoplado ou conteudo do restoP01;nao envelope global simultaneo doL.',
                    'Tensoes porGauss sao nominais de casca,nao esmagamento,arrancamento ou concentrações nosfuros.',
                    'Grandes deslocamentos/rotacoes invalidam hipotese linear;nessescasos os valores nao preveem o movel real.',
                    'Longarina frontal na posicaoY3354..3372,Z2034..2114 interfere nas reservas de guia/retencaoP01;nao e solucao montavel validada.',
                    'Base25 usa24.7 resistente/25.3massa e E=2100/2200 vezes o E dos demais paineis;altura interna265,sem validar acesso ou ferragens.',
                    'Sem capacidadehomologada de junta,prototipo ou fabricaçao/carga liberados. CAD nao aberto nemalterado.'],
                gate='NAO_LIBERADO: estudo de solicitacoes/rigidezes e proposta geometrica separada;validar produto,juntas,apoios eP02.')
    if not a.quick:
        (OUT/'Caixa_20kg.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
        with (OUT/'Caixa_20kg_juntas.csv').open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(export[0]),delimiter=';');w.writeheader();w.writerows(export)
    else:
        for r in out:
            print(json.dumps(dict(closed=r['closed_back'],rear=r['rear_support'],selected=[{k:c[k] for k in ['pose','packing','base_max_down_mm','maximum_box_joint_N','removed_contacts']} for c in r['cases'] if c['pose'] in ['fechadas','ambas86']]),ensure_ascii=True))

if __name__=='__main__':main()
