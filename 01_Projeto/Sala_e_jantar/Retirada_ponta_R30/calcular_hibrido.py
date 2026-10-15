"""Pre-dimensioning with explicit hypotheses, not a code/compliance certificate."""
from pathlib import Path
import json,math
p=Path(__file__).resolve().parent
g=9.81;live=240*g;dead=60*g;P=2*live+dead
def beam_point(force,span,E,I,Z):return {'force_N':force,'span_mm':span,'stress_MPa':force*span/4/Z,'deflection_mm':force*span**3/(48*E*I)}
wood={'nominal_core_mm':18,'minimum_core_mm':17.1,'finished_lid_envelope_mm':20,'E_required_MPa':8000,'bending_design_resistance_required_MPa':16,'shear_design_resistance_required_MPa':1,'compression_design_resistance_required_MPa':2,'note':'Procurement/performance requirements, not assigned properties of generic MDF or plywood. Verify declared properties, direction, moisture, load duration and applicable material factors. Finishes do not contribute to strength.'}
h=17.1;w=200;I=w*h**3/12;Z=I/(h/2);span=376
lid_uls=beam_point(2*80*g,span,8000,I,Z)
lid_sls=beam_point(80*g,span,8000,I,Z)
lid_uls['shear_MPa']=1.5*(2*80*g/2)/(w*h)
lid_uls['bearing_MPa']=(2*80*g/2)/(18*w)
lid_sls['chosen_deflection_limit_mm']=2
# Entire large lid, 3 occupants + all assumed dead load, not narrow concentrated patch.
large=beam_point(P,span,8000,825*h**3/12,825*h**2/6)
head=beam_point(P,420,200000,40*30**3/12,40*30**2/6)
head['section']='solid steel bar 40x30, 30 vertical; no hollow-section corner approximation'
head['fy_min_MPa']=235;head['chosen_stress_limit_MPa']=235/1.5
A=30**2-24**2;Ip=(30**4-24**4)/12;Zp=Ip/15
post={'section':'SHS30x30x3; effective A and I reduced10% for preliminary tolerance/corner sensitivity','A_effective_mm2':A*.9,'I_effective_mm4':Ip*.9,'length_mm':370,'force_one_post_N':P,'eccentricity_mm':24}
post['combined_stress_MPa']=P/(A*.9)+P*24/(Zp*.9)
post['Euler_N']=math.pi**2*200000*(Ip*.9)/370**2
post['chosen_Euler_margin']=post['Euler_N']/P
panel={'effective_width_mm':200,'thickness_mm':17.1,'height_mm':400,'force_N':P}
panel['compression_MPa']=P/(200*17.1)
panel['Euler_N']=math.pi**2*8000*(200*17.1**3/12)/400**2
# Weld group preliminary full perimeter, 3mm leg (2.1 throat), no credit for seat bearing.
weld={'leg_mm':3,'effective_throat_mm':2.1,'length_mm':120,'assumed_allowable_MPa':90,'force_N':P,'moment_Nmm':P*24}
weld['direct_MPa']=P/(120*2.1)
weld['moment_MPa']=P*24*15/(18000*2.1)
weld['conservative_sum_MPa']=weld['direct_MPa']+weld['moment_MPa']
# Cleat connection demand screening: 4 M6 through-bolts in effective200mm loaded zone.
connection={'case':'one160kg-equivalent local lid load entirely reaching one cleat; four effective M6 through-bolts in200mm zone','effective_bolts':4,'shear_each_N':2*80*g/4,'wood_bearing_required_MPa':4,'edge_distance_min_mm':24,'vertical_row_spacing_mm':30,'pitch_each_row_mm':100,'offset_rows_mm':50}
connection['bearing_demand_MPa']=connection['shear_each_N']/(6*17.1)
connection['projection_moment_Nmm']=2*80*g*18
connection['couple_N']=connection['projection_moment_Nmm']/30
connection['tension_each_top_bolt_N']=connection['couple_N']/2
connection['washer_effective_area_mm2']=math.pi/4*(24**2-6.5**2)
connection['washer_pressure_MPa']=connection['tension_each_top_bolt_N']/connection['washer_effective_area_mm2']
# Tray conservative total mass budget, not usable-load label.
tray={'rail':'Accuride DZ5321-0070','quantity_pairs':1,'closed_length_mm':700,'travel_mm':723,'height_mm':53.1,'thickness_mm':19.1,'side_space_mm':19.5,'supplier_rating_reference_kg':110,'supplier_rating_conditions':'80,000 cycles;450mm drawer width;vertical side mounting;centrally loaded. NOT certification of our shifted load or bench.','tray_length_mm':750,'tray_outer_width_mm':337,'tray_motion_mm':723,'leaf_additional_slide_mm':120,'leaf_supported_length_final_mm':645,'leaf_overhang_final_mm':105,'leaf_final_cg_x_mm':-425,'support_interval_x_mm':[-695,55],'mass_budget_total_kg':25,'leaf_mass_at900_density_kg':.75*.30*.03*900,'source_correction':'7957 actual height70.8mm, not53.1; previous reference superseded.5321-0070 is700mm with723mm travel, not750.'}
assert lid_uls['stress_MPa']<16 and lid_sls['deflection_mm']<2
assert large['stress_MPa']<16 and head['stress_MPa']<235/1.5
assert post['combined_stress_MPa']<235/1.5 and post['Euler_N']>3*P
assert panel['compression_MPa']<2 and panel['Euler_N']>3*P
assert weld['conservative_sum_MPa']<90
assert connection['bearing_demand_MPa']<4 and connection['washer_pressure_MPa']<2
report={'status':'PRELIMINARY CONDITIONAL MEMBER SIZING; not fabrication release or verified240kg rating','loads':{'occupants':3,'kg_each':80,'live_service_N':live,'dead_mass_budget_kg':60,'chosen_live_amplification':2,'global_screening_N':P,'local_load_patch_mm':[200,200],'note':'Factor2, 60kg dead budget and2mm service deflection are project screening assumptions, not claimed furniture-standard test loads. Seat use only; impact, standing/jumping, fatigue and racking not certified.'},'wood_requirements':wood,'lid_local_strength':lid_uls,'lid_local_service':lid_sls,'large_lid_global':large,'portal_header':head,'portal_post':post,'wood_vertical_panel':panel,'portal_weld_group':weld,'cleat_joint_screening':connection,'tray_hardware':tray,'not_closed':['actual wood grade and certificate; costs/availability','final fixing drawing and end zones/splitting/pull-through','lateral stability and floor protection/leveling','hinges and retention revised for actual lid masses','rail eccentric loading approval/test, locking pin receiver and actuation drawing','full physical assembly/prototype and local professional review']}
(p/'Calculo_hibrido_240kg.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['lid_local_strength','lid_local_service','portal_header','portal_post','cleat_joint_screening']},ensure_ascii=False))
