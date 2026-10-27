"""Geometria candidata da fixacao das frentes, sem CAD nem produto homologado."""
from pathlib import Path
import gzip,hashlib,json,math
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/Inventario_dimensional/Gavetas'
def overlap(a,b):return all(min(a[i+3],b[i+3])-max(a[i],b[i])>1e-6 for i in range(3))
def main():
 b=json.loads(gzip.decompress((ROOT/'02_Modelo_3D/Base_verificacao.json.gz').read_bytes()));obs=b['objetos']
 p=json.loads((OUT/'Proposta_FGVTN_500.json').read_text(encoding='utf-8'))
 rel=json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
 assert hashlib.sha256((ROOT/rel['cadPath']).read_bytes()).hexdigest()==b['sha256']==p['cad_sha256']
 def ancestors(n):
  a=[]
  while n in obs and n not in a:a.append(n);n=obs[n].get('pai')
  return a
 parts={n:o for n,o in obs.items() if o.get('tipo','').startswith(('Part::','PartDesign::')) and o.get('forma',{}).get('solidos',0)>0 and all(obs[a].get('visivel',True) for a in ancestors(n))}
 proposed={x['object']:x['proposed_box_mm'] for x in p['parts']};rows=[]
 for dr in p['rows']:
  name=dr['drawer'];front=next(x for x in p['parts'] if x['drawer']==name and x['role']=='frente_interna');decor=next(x for x in p['parts'] if x['drawer']==name and x['role']=='frente_decorativa')
  f=front['proposed_box_mm'];d=decor['proposed_box_mm'];H=f[5]-f[2]
  assert f[4]-f[1]==16 and d[4]-d[1]==18 and f[1]==d[4]
  for col,x in [('xmin',f[0]+40),('xmax',f[3]-40)]:
   for level,h in [('baixo',15),('alto',H-15)]:
    z=f[2]+h;recess=5 if name=='Gaveta005' and level=='baixo' else 0
    length=25 if recess else 30
    def envelope(depth):
     # Relative to moving box: fixed screw/washer centre z ranges z-1.5 .. z+1.5.
     return [x-8.4,f[4]-depth,z-9.4,x+8.4,f[4]-depth+4.3,z+9.4]
    installed=envelope(recess);normal=envelope(0)
    tool=[x-6.5,f[4]-recess+4.3,z-7.5,x+6.5,f[4]-recess+104.3,z+7.5]
    fixed={n:proposed.get(n,o['caixa_global']) for n,o in parts.items() if name in ancestors(n) and n not in [front['object'],decor['object']] and 'T51.7601' not in o.get('rotulo','')}
    normalhits=[n for n,box in fixed.items() if overlap(normal,box)]
    hits=[n for n,box in fixed.items() if overlap(installed,box)]
    toolhits=[n for n,box in fixed.items() if overlap(tool,box)]
    r=10 if recess else 4
    edge=min(x-f[0]-r,f[3]-x-r,z-f[2]-r,f[5]-z-r)
    assert edge>0
    penetration=length-(16-recess)-1.2
    assert abs(penetration-12.8)<1e-6
    rows.append(dict(drawer=name,module=dr['module'],point=col+'_'+level,internal_front=front['object'],decorative_front=decor['object'],
      x_global_mm=x,passage_z_at_adjustment_zero_mm=z,fixed_screw_z_mm=z+1.5,
      x_from_internal_front_xmin_mm=x-f[0],z_from_internal_front_bottom_mm=h,
      passage_axis='-Y global, from inside toward decorative front',passage_diameter_mm=8,
      recess_diameter_mm=20 if recess else 0,recess_depth_mm=recess,remaining_internal_thickness_mm=16-recess,
      screw_nominal_length_mm=length,front_penetration_including_tip_mm=penetration,front_outer_skin_mm=18-penetration,
      nominal_board_edge_ligament_mm=edge,hardware_swept_box_relative_to_box_mm=installed,
      normal_surface_head_candidates=normalhits,proposed_installed_candidates=hits,
      hypothetical_tool_d12_l100_candidates=toolhits,
      tool_candidates_after_contents_removed=[n for n in toolhits if n.startswith(('GavetaComum','MontagemG2'))]))
 assert len(rows)==28 and sum(r['recess_depth_mm']>0 for r in rows)==2
 assert not any(r['proposed_installed_candidates'] for r in rows)
 assert not any(r['tool_candidates_after_contents_removed'] for r in rows)
 offset=math.hypot(1.5,.5)
 margins=dict(shaft_radial_clearance_mm=4-4.3/2-offset,washer_radial_cover_mm=14.4/2-4-offset-.4,
  head_overlap_washer_hole_mm=(7.5-4.8)/2-.4,recess_radial_clearance_mm=10-7.5-offset-.4,
  recess_depth_reserve_mm=5-1.4-2.9)
 assert min(margins.values())>0
 result=dict(status='PROPOSTA_GEOMETRICA_NAO_APLICADA',cad_sha256=b['sha256'],cad_opened=False,cad_changed=False,
  physical_tests_executed=0,assumptions=dict(passage_diameter_mm=8,shaft_max_mm=4.3,washer_nominal_outer_mm=15,
  washer_min_outer_mm=14.4,washer_min_bore_mm=4.4,washer_max_bore_mm=4.8,washer_eccentricity_mm=.4,washer_nominal_thickness_mm=1.2,washer_max_thickness_mm=1.4,
  head_min_diameter_mm=7.5,head_max_height_mm=2.9,head_max_diameter_within_envelope_mm=15,
  horizontal_offset_envelope_mm=.5,vertical_offset_envelope_mm=1.5,tool_diameter_mm=12,tool_length_mm=100),
  analytical_margins=margins,points=rows,limits=['Dimensions are study envelopes, not a selected commercial product or manufacturer tolerances.',
  'Only own visible drawer wood/contents tested, hardware T51 excluded; FGVTN envelope unknown.',
  'Current board machining/holes not represented by bounding boxes; especially imported G2 front.',
  'Friction, pullout, fatigue, torque, actual pilot, wood quality and 11 mm recessed section strength unverified.',
  'Tool is shaft envelope only, not hand/driver body or external access. Contents removed condition required.'])
 (OUT/'Fixacao_frentes.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(points=len(rows),margins=margins,recess_points=[r for r in rows if r['recess_depth_mm']]),ensure_ascii=True))
if __name__=='__main__':main()
