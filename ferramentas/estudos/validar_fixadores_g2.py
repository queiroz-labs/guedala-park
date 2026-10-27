"""Sensibilidades dimensionais dos alojamentos; nao calcula capacidade de MDF."""
from pathlib import Path
import itertools,json,hashlib,math
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/Inventario_dimensional/Gavetas'
def main():
 src=json.loads((OUT/'Fixacao_frentes.json').read_text(encoding='utf-8'))
 rel=json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
 assert hashlib.sha256((ROOT/rel['cadPath']).read_bytes()).hexdigest()==src['cad_sha256']
 assert sum(p['recess_depth_mm']==5 for p in src['points'])==2
 cases=[]
 for depth,L,label in [(5,25,'base_5_L25'),(3.5,25,'comparacao_3p5_L25'),(3,25,'comparacao_3_L25'),(5,30,'erro_5_L30')]:
  values=[]
  for t,tf,d,l,w,k,g in itertools.product([15.7,16.3],[17.7,18.3],[depth-.2,depth+.2],[L-.3,L+.3],[1,1.4],[2.7,2.9],[1.5,2.5]):
   residual=t-d;embed=l-residual-w;skin=tf-embed;projection=max(0,w+k-d)
   values.append(dict(internal_t=t,decor_t=tf,depth=d,length=l,washer_t=w,head_h=k,tray_gap=g,
     residual_mm=residual,penetration_including_tip_mm=embed,outer_skin_mm=skin,
     skin_after_pilot_plus1_mm=skin-1,tray_clearance_mm=g-projection))
  fields=['residual_mm','penetration_including_tip_mm','outer_skin_mm','skin_after_pilot_plus1_mm','tray_clearance_mm']
  cases.append(dict(case=label,nominal_depth_mm=depth,nominal_length_mm=L,combinations=len(values),
    nominal=dict(residual_mm=16-depth,penetration_including_tip_mm=L-(16-depth)-1.2,outer_skin_mm=18-(L-(16-depth)-1.2),
     tray_clearance_mm=2-max(0,1.2+2.9-depth)),
    ranges={f:[min(v[f] for v in values),max(v[f] for v in values)] for f in fields},
    worst_outer_skin_case=min(values,key=lambda v:v['outer_skin_mm']),
    worst_tray_clearance_case=min(values,key=lambda v:v['tray_clearance_mm']),
    through_front_cases=sum(v['outer_skin_mm']<0 for v in values),zero_or_negative_tray_clearance_cases=sum(v['tray_clearance_mm']<1e-8 for v in values)))
 offset=math.hypot(1.5,.5)
 washers=[]
 for name,odmin,odmax,idmax,centering in [('envelope_anterior',14.4,15,4.8,4),('M4_catalogo_ACC U'.replace(' ',''),11.57,12,4.48,4),('M5_nominal_apenas',15,15,5.3,4),('M5_nominal_pescoco3',15,15,5.3,3)]:
  e=(idmax-centering)/2
  washers.append(dict(case=name,assumed_centering_diameter_mm=centering,eccentricity_mm=e,
   washer_cover_mm=odmin/2-4-offset-e,recess_wall_clearance_mm=10-odmax/2-offset-e,
   note='M5 only nominal catalog sizes, not toleranced acceptance' if name.startswith('M5') else 'Geometry only, no procurement approval'))
 area=math.pi/4*(14.4**2-8**2-4.8**2)
 result=dict(status='VALIDACAO_DIMENSIONAL_PARCIAL_RESISTENCIA_NAO_DEMONSTRADA',cad_sha256=src['cad_sha256'],cad_opened=False,cad_changed=False,
  physical_tests_executed=0,assumptions='All tolerance intervals below are sensitivity hypotheses, not measured values or manufacturer tolerances.',
  sensitivity_intervals_mm=dict(internal_board=[15.7,16.3],decorative_board=[17.7,18.3],depth_error=[-.2,.2],length_error=[-.3,.3],washer=[1,1.4],head=[2.7,2.9],tray_gap=[1.5,2.5]),
  depth_cases=cases,washer_cases=washers,material_load_path=dict(internal='Washer bearing and local pull-through around clearance hole; no screw withdrawal engagement.',decorative='Blind screw thread engagement; nominal penetration includes point.'),
  conservative_flat_bearing_area_lower_bound_mm2=area,
  assumed_preload_pressures=[dict(assumed_preload_per_fastener_N=n,average_pressure_upper_bound_N_per_mm2=n/area) for n in [100,250,500]],
  pressure_limits='No allowable compression, preload or torque assigned; flat bearing area assumes undamaged continuous material and rigid seated washer. No local peak prediction.',
  decision='Do not qualify remaining 11 mm. Compare 3.5 mm recess (12.5 nominal remaining), conditional on actual gap, hardware and thread engagement; baseline proposal unchanged.')
 # Separate catalog candidate: nominal dimensions are not certified limits.
 candidate=[]
 for neck in [3,4]:
  e=(4.3-neck)/2
  candidate.append(dict(assumed_neck_mm=neck,eccentricity_mm=e,
   cover_mm=15/2-4-offset-e,recess_clearance_mm=10-15/2-offset-e,
   head_cover_mm=(8-4.3)/2-e))
 boards=[]
 for t in [15,16,18]:
  for depth in [5,3.5]:
   gap=2+16-t # Keep decorative contact Y6408 and trays Y6426 fixed.
   penetration=25-(t-depth)-1
   boards.append(dict(internal_thickness_mm=t,recess_mm=depth,residual_mm=t-depth,
    penetration_including_tip_mm=penetration,outer_skin_mm=18-penetration,
    tray_gap_mm=gap,tray_clearance_mm=gap-max(0,2.8+1-depth)))
 result['catalog_candidate']=dict(screw='RECA 01814 25',washer='ETTINGER 003.06.941',
  washer_nominal_mm=dict(inner=4.3,outer=15,thickness=1),screw_head_nominal_mm=dict(diameter=8,height=2.8),
  status='Candidate for qualification only; tolerances, screw neck, passage through washer and strength unconfirmed',
  neck_sensitivity=candidate,board_comparisons=boards,
  envelope_condition=dict(assumed_washer_od_max_mm=15.2,assumed_washer_id_max_mm=4.4,
   assumed_neck_min_mm=3,recess_clearance_mm=10-15.2/2-offset-(4.4-3)/2,
   note='Illustrative acceptance budget, NOT catalog tolerances; washer minimum ID must exceed maximum screw diameter along assembly path.'))
 assert candidate[0]['recess_clearance_mm']>0
 assert boards[-1]['tray_clearance_mm']<0
 assert cases[0]['through_front_cases']==0 and cases[3]['through_front_cases']>0
 assert cases[1]['zero_or_negative_tray_clearance_cases']==0 and cases[2]['zero_or_negative_tray_clearance_cases']>0
 (OUT/'Validacao_fixadores_G2.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result,ensure_ascii=True))
if __name__=='__main__':main()
