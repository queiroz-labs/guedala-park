import FreeCAD as A, FreeCADGui as G, Part, pathlib, json, math, hashlib, shutil
ROOT=pathlib.Path('C:/Users/Elias/Documents/PROJETOS/Guedala park')
P=ROOT/'guedala-park/01_Projeto'
OUT=P/'Estudo_dimensional_R45_2026-10-23'
OUT.mkdir(exist_ok=True)
main=A.getDocument('Guedala_Park_R44_Consolidado')
src=pathlib.Path(main.FileName)
sha=hashlib.sha256(src.read_bytes()).hexdigest()
office=next(d for d in A.listDocuments().values() if d.FileName.endswith('Escritorio_fixacao_simples_R04_ESTUDO.FCStd'))
rail=next(d for d in A.listDocuments().values() if d.FileName.endswith('FECHADA_400_GUI_INSPECAO.FCStd'))
def world(o):
 q=o.Shape.copy();q.Placement=o.getGlobalPlacement();return q
def bb(q):
 b=q.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def box(v):return Part.makeBox(v[3]-v[0],v[4]-v[1],v[5]-v[2],A.Vector(*v[:3]))
def hit(a,b):
 if not a.BoundBox.intersect(b.BoundBox):return 0
 return a.common(b).Volume
d=A.newDocument('Estudo_Dimensional_R45')
d.Label='R45 ESTUDO — gavetas e banco; R44 preservada'
def group(n,label):
 g=d.addObject('App::DocumentObjectGroup',n);g.Label=label;return g
def add(g,n,label,q,color=(.72,.67,.56),trans=0):
 o=d.addObject('PartDesign::Feature',n);o.Label=label;o.Shape=q;g.addObject(o)
 o.ViewObject.ShapeColor=color;o.ViewObject.Transparency=trans;return o
meta=d.addObject('App::FeaturePython','LeiaMe');meta.Label='LEIA-ME — estudo dimensional, não executivo'
for name,value in {'Escopo':'Cotas nominais de R44, caixa R04 e documentos FGVTN; nenhuma medida de campo presumida.', 'Fonte':str(src),'SHA256Fonte':sha,'Relatorio':str(OUT/'Relatorio.html'),'Limites':'Sem engates/pares inventados. Marcadores do banco não são ferragens nem furos aprovados. Massas são cenários, não pesagens.'}.items():
 meta.addProperty('App::PropertyString',name,'Estudo');setattr(meta,name,value)
car=group('Escritorio_Carcaca','Gavetas — carcaça proposta R04, não incorporada')
drawer_groups=[]
for o in office.getObject('Carcaca_470x248').Group:add(car,'R45_'+o.Name,o.Label,world(o),trans=60)
drawers=[]
for n in ['Gaveta008','Gaveta009']:
 g=group('R45_'+n,n+' — caixa R04 / fixação direta');drawer_groups.append(g)
 parts={o.Name:world(o) for o in office.getObject('Caixa_'+n).Group}
 drawers.append(parts)
 for name,q in parts.items():add(g,'R45_'+name,name,q)
 storage=add(g,'R45_Util_'+n,'Volume útil R04 — '+n,world(office.getObject('Util_'+n)),(.1,.7,.5),80);storage.Visibility=False
# Repeat the R44 hypothesis and bracket transverse orientation; alternatives are not approved datums.
railparts={o.Name:world(o) for o in rail.Objects if o.TypeId=='Part::Feature'}
carparts={o.Name:world(o) for o in office.getObject('Carcaca_470x248').Group}
rot=A.Rotation(A.Vector(1,1,1),-120)
cases=[]
for idx,(n,floor) in enumerate([('Gaveta008',521),('Gaveta009',629)]):
 for shiftz in [0,-1,-2,-5,-10,-12]:
  for travel in [0,374.3]:
   hits=[]
   for name,q0 in railparts.items():
    q=q0.copy();q.Placement=A.Placement(A.Vector(4318,527.5,floor-30.6+shiftz),rot).multiply(q0.Placement)
    if name in ['Part__Feature001','Part__Feature002','Part__Feature005']:q.translate(A.Vector(0,travel,0))
    if name=='Part__Feature004':q.translate(A.Vector(0,travel*256.35/374.3,0))
    for wn,w0 in dict(carparts,**drawers[idx]).items():
     w=w0.copy()
     if wn in drawers[idx]:w.translate(A.Vector(0,travel,0))
     v=hit(q,w)
     if v>.01:hits.append({'rail':name,'wood':wn,'mm3':round(v,3)})
   cases.append({'drawer':n,'lower_rail_mm':-shiftz,'travel_mm':travel,'hits':hits})
   if shiftz==0 and travel==0:
    g=group('Hipotese_'+n,'HIPÓTESE R44 REJEITADA — '+n)
    for name,q0 in railparts.items():
     q=q0.copy();q.Placement=A.Placement(A.Vector(4318,527.5,floor-30.6),rot).multiply(q0.Placement)
     add(g,'H_'+n+'_'+name,rail.getObject(name).Label,q,(.85,.22,.15))
    g.Visibility=False
# Exhaustive conservative translational envelopes for wood and useful contents, no hardware claim.
woodtests=[]
for idx,n in enumerate(['Gaveta008','Gaveta009']):
 util=world(office.getObject('Util_'+n));v=bb(util);v[4]+=378;v[5]+=3;env=box(v)
 hits=[]
 for wn,w in carparts.items():
  vv=hit(env,w)
  if vv>.01:hits.append([wn,vv])
 for wn,w in drawers[1-idx].items():
  v=bb(w);v[4]+=378
  if not ('_Frente' in wn or '_Parafuso' in wn or '_Arruela' in wn):v[5]+=3
  vv=hit(env,box(v))
  if vv>.01:hits.append([wn,vv])
 woodtests.append({'drawer':n,'cargo_envelope':bb(env),'hits':hits,'dimensions_mm':[323,364,[60.4,54][idx]],'volume_l':util.Volume/1e6})
# Fresh R44 nominal depth check using actual world side and back shapes from each prior ray.
old=json.loads((P/'Avanco_pendencias_2026-10-21/Gavetas/Medicoes_nove_gavetas.json').read_text(encoding='utf8'))
nine=[]
for item in old['drawers']:
 sides=[world(main.getObject(item['limites_laterais'][k][1])) for k in ['esquerda','direita']]
 left=bb(sides[0])[3];right=bb(sides[1])[0];width=right-left
 direction=item['direcao_fundo_y'];sideb=bb(sides[0]);front=sideb[1] if direction>0 else sideb[4]
 back=bb(world(main.getObject(item['raios'][0]['obstacle'])));inner=back[1] if direction>0 else back[4]
 depth=(inner-front)*direction
 nine.append({'drawer':item['gaveta'],'width_mm':width,'depth_mm':depth,'min_depth_mm':item['minimo_FGVTN_mm'],'depth_margin_mm':depth-item['minimo_FGVTN_mm'],'nominal_inside_width_mm':width-41,'nominal_outside_width_15mm_sides':width-11,'inside_width_range_mm':[width-41-.5,width-41+1],'side_gap_range_centered_mm':[5,5.75],'note':'Somente relação dimensional; não verifica montagem das guias de 500.'})
# Bank context copied from current visible objects; original document never mutated.
inventory=json.loads((ROOT/'outputs/estudo-dimensional-2026-10-23/banco_visivel.json').read_text(encoding='utf8'))
bank=group('Banco_Contexto','Banco R44 — contexto e armazenamento preservados')
obstacles={}
for item in inventory:
 n=item['name']
 if n.startswith('BancoR43_') or n in ['Peca003','Peca006','Peca035','Peca036']:continue
 q=world(main.getObject(n));obstacles[n]=q
 add(bank,'B_'+n,item['label'],q,trans=65 if 'gabarito' not in item['label'] else 45)
lids=group('Banco_Tampas','Banco — duas tampas, sem almofadas durante abertura')
poses=group('Banco_Pose90','Referência 90 graus — eixo ideal existente');poses.Visibility=False
markers=group('Banco_Referencias_SlowMulti','Slow Multi — referências dimensionais condicionais; NÃO FURAR')
bank_result=[];allhits=[]
for idx,(length,y) in enumerate([(971,3751),(825,4724)],1):
 q0=world(main.getObject('BancoR43_Painel'+str(idx)))
 add(lids,'Tampa'+str(idx),f'Tampa {idx} — {length} x 448 x 20 mm',q0,(.65,.48,.29))
 tests=[]
 other=world(main.getObject('BancoR43_Painel'+str(3-idx)))
 # Absolute copied solids: rotate around the original hinge axis without changing original controls.
 for angle in range(91):
  q=q0.copy();q.rotate(A.Vector(102,y,420),A.Vector(0,1,0),-angle)
  hits=[]
  for n,w in dict(obstacles,other_lid=other).items():
   v=hit(q,w)
   if v>.1:hits.append({'name':n,'mm3':round(v,4)})
  tests.append({'angle':angle,'hits':hits})
  if hits:allhits.append({'lid':idx,'angle':angle,'hits':hits})
  if angle==90:add(poses,'Aberta'+str(idx),'Tampa '+str(idx)+' a 90° — eixo ideal',q,(.4,.6,.85),55)
 volume=q0.Volume/1e9
 masses=[{'density_kg_m3':rho,'panel_kg':volume*rho,'allowance_to_7kg':7-volume*rho} for rho in [650,750,800,900]]
 planes=[3780,4702] if idx==1 else [4744,5520]
 datums=[]
 for j,plane in enumerate(planes):
  # 12mm inward from inner side face; lid rear edge102 used for188/204 marking only.
  for x in [290,306]:
   q=Part.makeSphere(2,A.Vector(x,plane,400));add(markers,f'M_L{idx}_{j}_{x}','Referência tampa — não é furo executivo',q,(.1,.4,.9))
  face=[3768,4714][j] if idx==1 else [4732,5532][j]
  for z in [346,374]:add(markers,f'M_S{idx}_{j}_{z}','Referência lateral — topo400, recuo60 do fundo118',Part.makeSphere(2,A.Vector(178,face,z)),(.1,.4,.9))
  # A 130mm ruler at the lid attachment zone, NOT a solid hardware envelope.
  ruler=Part.makeLine(A.Vector(290,plane,400),A.Vector(290,plane,270))
  add(markers,f'Regua130_{idx}_{j}','130 mm mínimos — linha de conferência, não ferragem',ruler,(.9,.25,.1))
  datums.append({'inner_side_face_y':face,'lid_mount_plane_y':plane,'distance_from_lid_edge_mm':plane-y if j==0 else y+length-plane,'side_fixed_center':[178,face,360],'side_holes_z':[374,346],'lid_reference_points':[[290,plane,400],[306,plane,400]],'conditional':'Datum de tampa referido à borda traseira; dobradiça/recobrimento r ainda indefinidos. Conferir antes de furar.'})
 bank_result.append({'lid':idx,'size_mm':[length,448,20],'volume_m3':volume,'density_limit_panel_only_kg_m3':7/volume,'mass_scenarios':masses,'two_units_required_by_width':True,'reference_datums':datums,'motion':tests,'open90_top_z':868,'clearance_backrest_mm':2,'hinge_model':'ideal original axis, not hinge kinematics'})
markers.Visibility=False
poses.Visibility=False
report={'date':'2026-10-23','source':str(src),'source_sha256_before':sha,'nine_drawers':nine,'office_R04':{'clear_depth':432,'margin_P1':12,'width_inside':323,'width_outside':353,'cargo':woodtests,'rail_cases':cases,'rail_case_method':'Mesma hipótese R44: sourceY0 -> X4318, sourceZ148.5 -> Y676, sourceX30.6 -> fundo inferior. Rebaixamentos são apenas sensibilidade; não indicam montagem válida. Estados abertos reconstruídos pelos deslocamentos oficiais 374.3/256.35mm.','vertical_cargo_nominal_margins_mm':[1.6,1.0],'tolerance_budget_examples':[{'errors_mm':[.5,.5],'remaining_mm':[.6,0]},{'errors_mm':[.5,.5,.5],'remaining_mm':[.1,-.5]}]},'bank':bank_result,'bank_motion_hits':allhits,'bank_shelf':{'shelf_top_mm':310,'shelf_bottom_mm':292,'closed_lid_underside_mm':400,'free_height_mm':90,'manual_minimum_mm':130,'shortfall_mm':40,'lower_shelf_40_new_bottom_mm':252,'stored_objects_top_mm':274,'resulting_overlap_mm':22,'note':'Cota mínima do manual aplicada à região da montagem. Perfil/mecanismo exato ainda necessário. Abaixar toda prateleira40 invade os gabaritos de aspirador/jogos; não aplicado.'},'not_validated':['Engates, orientação/datum, furos traseiros e parafusos da corrediça','Carga, resistência e montagem das gavetas','Dobradiças reais, recobrimento r, corpo/cinemática/retencao do Slow Multi','Massa acabada das tampas, ligações e resistência do banco','Tolerâncias de fabricação e medidas executadas']}
d.recompute()
invalid=[o.Name for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]
report['study_invalid_shapes']=invalid
assert not invalid
assert hashlib.sha256(src.read_bytes()).hexdigest()==sha
report['source_sha256_after']=sha
target=OUT/'Gavetas_Banco_R45_ESTUDO.FCStd'
d.recompute();d.saveAs(str(target))
report['study_file']=str(target);report['study_objects']=len(d.Objects)
(OUT/'Calculos_e_ensaios.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
G.activeDocument().activeView().viewAxonometric();G.activeDocument().activeView().fitAll();G.updateGui()
result={'file':str(target),'objects':len(d.Objects),'bank_hits':len(allhits),'rail_cases':len(cases),'source_unchanged':True}
