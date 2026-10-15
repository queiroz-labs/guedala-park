from pathlib import Path
import math,json
import numpy as np

HERE=Path(__file__).parent
# cm. Fixed virtual pivots, not Blum's multi-link kinematics.
a,b=np.meshgrid(np.arange(0,92.0001,.25),np.arange(0,60.0001,.25),indexing='ij')
alpha,beta=np.radians(a.ravel()),np.radians(b.ravel())
P=np.broadcast_to([65.,65.],(len(alpha),2))
Q=P+40*np.stack([-np.cos(alpha),np.sin(alpha)],axis=1)
R=Q+40*np.stack([np.sin(alpha+beta),np.cos(alpha+beta)],axis=1)
na=1.8*np.stack([-np.sin(alpha),-np.cos(alpha)],axis=1)
nb=1.8*np.stack([-np.cos(alpha+beta),np.sin(alpha+beta)],axis=1)
A=np.stack([P,Q,Q+na,P+na],axis=1)
B=np.stack([Q,R,R+nb,Q+nb],axis=1)

def to_point_distance(poly,point):
    u=poly;v=np.roll(poly,-1,axis=1);d=v-u;w=np.array(point)-u
    t=np.clip(np.sum(w*d,axis=2)/np.sum(d*d,axis=2),0,1)
    return np.sqrt(np.sum((u+t[:,:,None]*d-point)**2,axis=2)).min(axis=1)

results=[]
for filler in [0,8,10,12,15]:
    width=(180-filler)/4
    pivot=[25,105+filler+width]
    dist=np.minimum(to_point_distance(A,pivot),to_point_distance(B,pivot))
    idx=int(np.argmin(dist))
    # The neighbouring 18-mm panel's full disk is enclosed by r=hypot(width,t).
    # A full disk is conservative for that leaf's 0..90 degree quarter-sweep.
    rad=math.hypot(width,1.8)
    results.append({'fixed_front_cm':filler,'neighbour_width_cm':width,'neighbour_pivot':pivot,
      'min_distance_corner_to_neighbour_pivot_cm':round(float(dist[idx]),4),
      'neighbour_enclosing_radius_cm':round(rad,4),'separation_from_enclosing_disk_cm':round(float(dist[idx])-rad,4),
      'alpha_deg':float(a.ravel()[idx]),'beta_deg':float(b.ravel()[idx])})

# Explicit center-line intersection witness in original R01 (all within allowable angles).
def point(alpha,beta):
    aa=math.radians(alpha);bb=math.radians(beta)
    q=(65-40*math.cos(aa),65+40*math.sin(aa))
    return q,(q[0]+40*math.sin(aa+bb),q[1]+40*math.cos(aa+bb))
q,r=point(10,0)
delta=math.degrees(math.atan2(r[0]-25,150-r[1]))
dist=math.hypot(r[0]-25,r[1]-150)
assert 0<delta<90 and dist<45
angles=[]
for angle in [92,110,130,155,170]:
    qq,rr=point(angle,60)
    angles.append({'alpha_deg':angle,'beta_deg':60,'tip':list(rr),'tip_y_minus_maleiro_face_cm':round(rr[1]-65,4)})

# Bound change between grid samples in this model: at most length * angular increment
# for alpha and beta; nearest grid point is <=0.125 deg along each axis.
grid_error_bound=(math.hypot(80,3.6)+math.hypot(40,1.8))*math.radians(.125)
result={'status':'triagem geométrica, não validação executiva das ferragens',
 'model':'painéis 18 mm; duas frentes nominais 400 mm; eixos virtuais fixos nos vértices externos; sem braços/traslados reais, puxadores ou tolerâncias',
 'angle_domain_deg':{'alpha':[0,92],'beta':[0,60],'grid_step':.25},'sample_count':len(alpha),
 'sampling_distance_bound_cm':round(grid_error_bound,4),
 'r01_simultaneous_collision_witness':{'alpha':10,'beta':0,'neighbour_angle_deg':round(delta,4),'intersection_point':list(r),'distance_from_neighbour_pivot_cm':round(dist,4),'neighbour_length_cm':45},
 'main_angle_comparison':angles,'transition_front_sensitivity':results,
 'hinge_candidates':{'main':'Blum CLIP top 71T7550, 155 graus, referência a compatibilizar','corner':'Blum CLIP top 79T8500, articulação 60 graus','stop':'Blum 70T7553.09, limita a principal a 92 graus'},
 'pending':['eixos e curso multilink reais em CAD ou gabarito com peças','calços, recobrimentos, folgas e furação','quantidade e carga das dobradiças no conjunto baixo','puxadores sem projeção e portas de correr contidas atrás do plano y65','ensaio simultâneo e confirmação da faixa fixa antes de fabricar'],
 'note':'Folgas positivas desta triagem não são folgas garantidas no móvel; o catálogo mostra deslocamentos além de rotação simples.'}
(HERE/'Conferencia_giro_canto_R02.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
