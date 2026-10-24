import FreeCAD as A, Part, pathlib,json,hashlib
P=pathlib.Path(__file__).resolve().parent
s=A.getDocument('Banheiro_Detalhamento_R02');d=A.getDocument('Guedala_Park_R42_Consolidado')
def w(o):
 q=o.Shape.copy();q.Placement=o.getGlobalPlacement();return q
def v(a,b):
 return a.common(b).Volume if a.BoundBox.intersect(b.BoundBox) else 0
def box(x,y,z,a,b,c):return Part.makeBox(a,b,c,A.Vector(x,y,z))
r={'combinations':[],'bolt_extraction':[],'stop_contacts':[],'geometry_measurements':{},'hypotheses':[]}
fixed=[o for o in s.Madeira.Group]+list(s.Trilhos.Group)+list(s.Batentes.Group)
for a in [0,134,268]:
 for b in [0,116.5,233]:
  s.Controle.CursoEsquerda=a;s.Controle.CursoDireita=b;s.recompute()
  le=[(o.Name,w(o)) for o in s.FolhaEsquerda.Group];ri=[(o.Name,w(o)) for o in s.FolhaDireita.Group]
  hits=[]
  for n,q in le:
   for m,t in ri:
    vol=v(q,t)
    if vol>.1:hits.append([n,m,round(vol,4)])
  for n,q in le+ri:
   for o in fixed:
    vol=v(q,o.Shape)
    if vol>.1:hits.append([n,o.Name,round(vol,4)])
  r['combinations'].append({'front_mm':a,'rear_mm':b,'hits':hits})
s.Controle.CursoEsquerda=0;s.Controle.CursoDireita=0;s.recompute()
entry=w(d.getObject('Peca075'));wall=w(d.getObject('Peca051'));stone=w(d.getObject('Peca399'));toilet=w(d.getObject('Peca190'))
for x in [2771,3349]:
 for z in [260,680]:
  path=Part.makeCylinder(5.5,106,A.Vector(x,4714,z),A.Vector(0,1,0))
  r['bolt_extraction'].append({'X':x,'Z':z,'hits':[(n,v(path,q)) for n,q in [('entry',entry),('wall',wall),('stone',stone),('toilet',toilet)] if v(path,q)>.1],'wall_clearance_mm':path.distToShape(wall)[0]})
front=w(s.PainelEsquerda);rear=w(s.PainelDireita)
r['geometry_measurements']={'overlap_mm':front.BoundBox.XMax-rear.BoundBox.XMin,'leaf_heights_mm':[front.BoundBox.ZLength,rear.BoundBox.ZLength],'gap_to_stone_mm':stone.BoundBox.ZMin-s.Travessa.Shape.BoundBox.ZMax,'module_height_mm':s.LateralE.Shape.BoundBox.ZLength,'hardware_depth_gap_mm':rear.BoundBox.YMin-(front.BoundBox.YMax+9),'normal_entry_clearance_mm':4820-entry.BoundBox.YMax,'maintenance_entry_clearance_after20_mm':4800-entry.BoundBox.YMax,'module_clearance_to_toilet_after_shift_mm':toilet.BoundBox.XMin-3480,'dowels_clear_box_after20_mm':4890-4885,'rear_cavity_exposed_clearance_mm':(2815+272-9)-(2780+292)}
r['tolerance_scenarios']={'note':'Independent arithmetic stress cases, not measured production tolerances. Do not add these to claim an overall tolerance guarantee.','overlap_nominal24_minus4_plus4_mm':[20,28],'depth_gap3_minus1_per_component_mm':1,'stone_gap2_minus1_mm':1,'moving_envelope_expand_1_mm':[],'door_leaf_length_vs_service_gap_mm':[[700,50],[725,25],[740,10],[750,0],[800,-50]],'rail_slot3_15_vs_test_pin2_5_radial_mm':(3.15-2.5)/2}
for x,y,width in [(2780,4822,560),(2815,4852,525)]:
 sh=box(x-1,y-1,220.5,width+2,29,502)
 # Expanded panel/hardware body envelope only; designed stop contacts excluded.
 hits=[(o.Name,round(v(sh,o.Shape),4)) for o in s.Madeira.Group if v(sh,o.Shape)>.1]
 r['tolerance_scenarios']['moving_envelope_expand_1_mm'].append(hits)
r['hypotheses']=['Carros/guias são envelopes; folga radial0,325 só descreve esses envelopes. Não é medida do kit.','A extração de parafusos foi testada com cilindroØ11; não demonstra ergonomia da mão/chave junto à parede.','Passagem do quadro tem folga nominal2 sob pedra; definir tolerâncias reais e junta removível, sem colagem à pedra.','Suspensão existente e resistência das chapas não estão especificadas.']
r['invalid_shapes']=[o.Name for o in s.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]
r['source_sha256']=hashlib.sha256(pathlib.Path(d.FileName).read_bytes()).hexdigest()
(P/'Auditoria_independente.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
s.save()
