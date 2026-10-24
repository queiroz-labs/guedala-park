import FreeCAD as A, Part, pathlib,json,hashlib,csv
from xml.sax.saxutils import escape
root=pathlib.Path(__file__).resolve().parent;base=root.parents[1]
src=base/'Modelo_FreeCAD/01_Atual/Consolidacao_R42_2026-10-22/Guedala_Park_R42_Consolidado.FCStd';hash0=hashlib.sha256(src.read_bytes()).hexdigest()
d=A.openDocument(str(src));cache={}
def shape(o):
 if o.Name not in cache:
  s=o.Shape.copy()
  if hasattr(o,'getGlobalPlacement'):s.Placement=o.getGlobalPlacement()
  cache[o.Name]=s
 return cache[o.Name]
def bb(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def box(b):return Part.makeBox(b[3]-b[0],b[4]-b[1],b[5]-b[2],A.Vector(*b[:3]))
def leaves(o):
 children=[c for c in getattr(o,'Group',[]) if hasattr(c,'Shape') or hasattr(c,'Group')]
 if children:
  result=[]
  for c in children:result+=leaves(c)
  return result
 return [o] if hasattr(o,'Shape') and not o.Shape.isNull() else []
groups=[('Modulo',['Gaveta','Gaveta001','Gaveta002','Gaveta003'],3372,1,520,['Peca206','Peca207','Peca208','Peca209','Peca210','Peca211','Peca212','Peca213','Peca226','Peca227','Peca228','Peca241','Peca242','Peca243','Peca244','Peca245','Peca246']),('Modulo005',['Gaveta004','Gaveta005','Gaveta006'],6410,1,520,['Peca283','Peca284','Peca285','Peca286']),('Modulo015',['Gaveta008','Gaveta009'],680,-1,420,['Peca367','Peca368','Peca369','Peca370','Peca371'])]
results=[];envs={}
for mod,names,front,sign,minimum,carcase in groups:
 obs=[d.getObject(n) for n in carcase]
 for name in names:
  o=d.getObject(name)
  wood=[c for c in o.OutList if hasattr(c,'Shape') and not c.Shape.isNull() and ('lateral comum' in c.Label.lower() or 'lateral_da_gaveta' in c.Label.lower())]
  assert len(wood)==2,(name,[c.Label for c in wood])
  bounds=[bb(shape(c)) for c in wood];xlo=min(b[0] for b in bounds);xhi=max(b[3] for b in bounds);ylo=min(b[1] for b in bounds);yhi=max(b[4] for b in bounds);zlo=min(b[2] for b in bounds);zhi=max(b[5] for b in bounds)
  env=[xlo-.5,ylo if sign>0 else ylo-10,zlo,xhi+.5,yhi+10 if sign>0 else yhi,zhi]
  envs[name]=box(env)
  # Ray sections inspect both runner lanes and central box lane at three elevations.
  hits=[]
  for x in [xlo-3,(xlo+xhi)/2,xhi+3]:
   for z in [zlo-10,zlo+10,zhi-1]:
    line=Part.makeLine(A.Vector(x,front+sign*.01,z),A.Vector(x,front+sign*1000,z))
    candidates=[]
    for ob in obs:
     common=line.common(shape(ob))
     if not common.isNull() and common.Vertexes:
      dist=min(sign*(v.Point.y-front) for v in common.Vertexes)
      if dist>=0:candidates.append((dist,ob.Name,ob.Label))
    if candidates:
     hit=min(candidates);hits.append({'x':x,'z':z,'depth_mm':round(hit[0],4),'obstacle':hit[1],'label':hit[2]})
  assert len(hits)==9,(name,hits)
  free=min(h['depth_mm'] for h in hits)
  candidatecollisions=[]
  for ob in obs:
   vol=envs[name].common(shape(ob)).Volume
   if vol>0.001:candidatecollisions.append({'object':ob.Name,'volume_mm3':vol})
  back=currentrear=yhi if sign>0 else ylo
  backplane=front+sign*free;newrear=back+sign*10
  # Clear width measured from actual carcass/divider inner faces at the box's mid height.
  zmid=(zlo+zhi)/2;ymid=(ylo+yhi)/2
  left=[];right=[]
  for ob in obs:
   b=bb(shape(ob))
   if b[1]<=ymid<=b[4] and b[2]<=zmid<=b[5]:
    if b[3]<=xlo+.001:left.append((b[3],ob.Name))
    if b[0]>=xhi-.001:right.append((b[0],ob.Name))
  wallL=max(left);wallR=min(right);width=wallR[0]-wallL[0]
  row={'gaveta':name,'rotulo':o.Label,'modulo':mod,'frente_carcaca_y_mm':front,'direcao_fundo_y':sign,'fundo_interno_y_mm':backplane,'profundidade_livre_mm':free,'minimo_FGVTN_mm':minimum,'margem_minimo_mm':free-minimum,'largura_livre_mm':width,'limites_laterais':{'esquerda':wallL,'direita':wallR},'caixa_externa_atual_largura_mm':xhi-xlo,'caixa_externa_candidata_largura_mm':xhi-xlo+1,'folga_lateral_por_lado_candidata_mm':(width-(xhi-xlo+1))/2,'caixa_externa_atual_profundidade_mm':yhi-ylo,'caixa_externa_candidata_profundidade_mm':yhi-ylo+10,'traseira_caixa_atual_y_mm':back,'traseira_caixa_candidata_y_mm':newrear,'folga_caixa_atual_fundo_mm':sign*(backplane-back),'folga_caixa_candidata_fundo_mm':sign*(backplane-newrear),'envelope_caixa_candidata_mm':env,'colisoes_envelope_com_carcaca':candidatecollisions,'raios':hits,'resultado':'Atende profundidade P1 no modelo' if free>=minimum else 'NAO atende P1 no modelo: faltam '+str(minimum-free)+' mm'}
  results.append(row)
print('MEASURED',[(r['gaveta'],r['profundidade_livre_mm'],r['margem_minimo_mm']) for r in results],flush=True)
# Office solution: extend the rear of the carcass by20 mm, keeping visible front, width, height and18 mm panels.
office_names=['Peca367','Peca368','Peca369','Peca370','Peca371'];proposed={};original={}
for n in office_names:
 s=shape(d.getObject(n));original[n]=s;b=bb(s)
 if n in ['Peca367','Peca368']:b[1]-=20
 elif n=='Peca369':b[1]-=20;b[4]-=20
 else:b[1]-=20
 proposed[n]=box(b)
# Check only added/repositioned volume against every other leaf shape in the full apartment.
# Original drawer rails are retained reference, so report any overlap rather than excluding arbitrary neighbors.
checks=[];nearby=set()
for n,s in proposed.items():
 delta=s.cut(original[n]);b=delta.BoundBox
 for ob in d.Objects:
  if ob.Name in office_names or hasattr(ob,'Group') or not hasattr(ob,'Shape') or ob.Shape.isNull():continue
  os=shape(ob);q=os.BoundBox
  if min(b.XMax,q.XMax)-max(b.XMin,q.XMin)<=1e-6 or min(b.YMax,q.YMax)-max(b.YMin,q.YMin)<=1e-6 or min(b.ZMax,q.ZMax)-max(b.ZMin,q.ZMin)<=1e-6:continue
  nearby.add(ob.Name);v=delta.common(os).Volume
  if v>0.001:checks.append({'proposed':n,'other':ob.Name,'label':ob.Label,'volume_mm3':round(v,5),'visible':str(getattr(ob,'Visibility','unknown'))})
study=A.newDocument('Escritorio_FGVTN_estudo')
for groupname,items in [('Carcaca_atual',original),('Carcaca_proposta_mais20mm',proposed),('Caixas_candidatas_envelopes',{n:envs[n] for n in ['Gaveta008','Gaveta009']})]:
 g=study.addObject('App::DocumentObjectGroup',groupname)
 for n,s in items.items():
  o=study.addObject('PartDesign::Feature',groupname+'_'+n);o.Shape=s;o.Label=groupname+' - '+n;g.addObject(o)
meta=study.addObject('App::DocumentObjectGroup','LEIA_ME');meta.addProperty('App::PropertyString','Premissas');meta.Premissas='ESTUDO SEPARADO. Dois cenarios sobrepostos: exibir apenas carcaca atual ou proposta. Alongamento traseiro20mm: profundidadeexterna450para470, frente/largura/altura intactas. Vao livre432mm, margem12sobreminimo420. Caixas sao ENVELOPES400x353, nao desenho executivo; nenhum furo/engate homologado. Nao alteradoR42.'
study.recompute();study.saveAs(str(root/'Escritorio_FGVTN_mais20mm_ESTUDO.FCStd'));A.closeDocument(study.Name)
re=A.openDocument(str(root/'Escritorio_FGVTN_mais20mm_ESTUDO.FCStd'));invalid=[o.Name for o in re.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]
assert not invalid and hashlib.sha256(src.read_bytes()).hexdigest()==hash0
report={'source':str(src),'sha256_source_before_after':hash0,'source_unchanged':True,'method':'World-coordinate shape sections; front carcass plane from actual side panels;9 rays per drawer at runner lanes and center,3elevations; candidate bounding envelope +1mmwidth/+10mmrear tested against carcass solids. Not manufacturer hole compatibility or physical measurement.','drawers':results,'office_proposal':{'rear_extension_mm':20,'external_depth_before_after_mm':[450,470],'front_carcass_y_unchanged_mm':680,'inside_back_y_before_after_mm':[268,248],'free_depth_before_after_mm':[412,432],'margin_over_minimum_mm':12,'candidate_box_to_back_mm':34,'new_geometry_collisions':checks,'overlapping_bboxes_examined':sorted(nearby),'study_invalid_shapes':invalid,'front_width_height_storage':'preserved','limit':'No full mechanical installation or fixing validation. Modelled room objects only; no physical measurements.'}}
(root/'Medicoes_nove_gavetas.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
cols=['gaveta','rotulo','modulo','frente_carcaca_y_mm','fundo_interno_y_mm','profundidade_livre_mm','minimo_FGVTN_mm','margem_minimo_mm','largura_livre_mm','caixa_externa_candidata_largura_mm','folga_lateral_por_lado_candidata_mm','caixa_externa_candidata_profundidade_mm','folga_caixa_candidata_fundo_mm','resultado']
with (root/'Medicoes_nove_gavetas.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(results)
print(json.dumps(report['office_proposal'],ensure_ascii=True),flush=True)
