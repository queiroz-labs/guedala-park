from pathlib import Path
from datetime import datetime
import shutil,json
import FreeCAD as App, Part, Import

root=(Path(__file__).resolve().parent / '.').resolve()
base=(Path(__file__).resolve().parent / '../G2_R06_2026-10-13').resolve()
sourcefile=(Path(__file__).resolve().parent / '../G2_R06_2026-10-13/Blum_configurado/G2_MOVENTO_500_40kg_Recobrimento3_5.STEP').resolve()
source=App.newDocument('BlumG2ReferenciaCorrigida')
Import.insert(str(sourcefile),source.Name);source.recompute()
source.saveAs(str((Path(__file__).resolve().parent / 'Fonte_G2_BlUM.FCStd').resolve()))
oldpath=(Path(__file__).resolve().parent / '../G2_R06_2026-10-13/Guedala_Park_R06_G2_Simples.FCStd').resolve()
old=next((d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==oldpath),None)
if old is None:old=App.openDocument(str(oldpath))
old.save()
dest=(Path(__file__).resolve().parent / 'Guedala_Park_R07_Montagem_G2.FCStd').resolve()
if dest.exists():dest=dest.with_stem(dest.stem+'_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
shutil.copy2(oldpath,dest)
doc=App.openDocument(str(dest));App.setActiveDocument(doc.Name)
doc.Label='Guedala Park - R07 - montagem comum de G2 proposta'
g=next(o for o in doc.Objects if o.Label=='G2 · utensílios' and hasattr(o,'Extensao'))
module=next(o for o in g.InList if o.TypeId=='App::Part')
trays=[o for o in g.Group if o.Label.startswith('Bandeja removivel')]
oldwood=[o for o in g.Group if hasattr(o,'Shape') and o.TypeId!='App::Part' and len(o.Shape.Solids)]
legacy=doc.addObject('App::Part','HistoricoG2R06');g.addObject(legacy)
legacy.Label='Caixa G2 R06 - referência histórica oculta'
for o in oldwood:g.removeObject(o);legacy.addObject(o);o.Visibility=False
legacy.Visibility=False
fixed=doc.addObject('App::Part','GuiasG2R07');module.addObject(fixed)
fixed.Label='Guias G2 - montagem fechada estática oficial'
fixed.Placement=App.Placement(App.Vector(g.Placement.Base.x,0,g.Placement.Base.z),App.Rotation())
fixed.addProperty('App::PropertyString','Status');fixed.Status='Perfil principal STEP é sólido único; não é telescópio animável. Não transladar inteiro como mecanismo real.'
mapplace=App.Placement(App.Vector(600,18,3.5),App.Rotation(App.Vector(1,0,0),90))
wood=[];locks=[];profiles=[];screws=[];rows=[]
for o in source.Objects:
    if o.TypeId!='Part::Feature' or len(o.Shape.Solids)!=1:continue
    s=o.Shape.copy();s.Placement=o.getGlobalPlacement()
    s=s.transformGeometry(s.Placement.toMatrix());s.Placement=App.Placement()
    s=s.transformGeometry(mapplace.toMatrix());s.Placement=App.Placement()
    label=o.Label
    iswood='gaveta' in label.lower() or '[3B03-' in label
    islock=label.startswith('46166126') or label.startswith('43107713')
    parent=g if iswood or islock else fixed
    obj=doc.addObject('Part::Feature','MontagemG2R07');parent.addObject(obj);obj.Shape=s
    obj.Label=label+' - proposta R07'
    obj.addProperty('App::PropertyString','Fonte');obj.Fonte=sourcefile.name+' / '+o.Name
    obj.addProperty('App::PropertyString','Status');obj.Status='Montagem oficial configurada aplicada como proposta; não libera corte, furação ou compra.'
    if iswood:wood.append(obj);obj.ViewObject.ShapeColor=(.76,.71,.60)
    elif islock:locks.append(obj);obj.ViewObject.ShapeColor=(.95,.42,.08)
    elif 'translator' in label:screws.append(obj);obj.ViewObject.ShapeColor=(.55,.55,.55)
    else:profiles.append(obj);obj.ViewObject.ShapeColor=(.70,.72,.74)
    b=s.BoundBox
    rows.append({'name':obj.Name,'source':o.Name,'label':label,'category':'wood' if iswood else 'locking' if islock else 'screw' if 'translator' in label else 'profile','bboxLocal':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],'valid':s.isValid()})
for t in trays:t.Placement.Base.y=36
g.addProperty('App::PropertyString','MontagemR07');g.MontagemR07='MOVENTO500/40kg+T51.7600 candidatos; fundo com rasgos comuns, dianteira16; vão interno541x459; controle é translação rígida, não animação das etapas da guia.'
doc.recompute()
def shape(o):
    s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def volume(a,b):
    x,y=a.BoundBox,b.BoundBox
    if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
    return a.common(b).Volume
hits=[]
for i,o in enumerate(wood):
    for q in wood[i+1:]:
        v=volume(shape(o),shape(q))
        if v>.1:hits.append({'pair':[o.Label,q.Label],'mm3':v})
contents=[c for t in trays for c in t.Group if hasattr(c,'Status') and 'Gabarito' in c.Status]
traywood=[c for t in trays for c in t.Group if c not in contents]
hardware=[]
for o in profiles+locks:
    for q in wood:
        v=volume(shape(o),shape(q))
        if v>.1:hardware.append({'hardware':o.Label,'wood':q.Label,'mm3':v})
for o in contents+traywood:
    for q in wood:
        v=volume(shape(o),shape(q))
        if v>.1:hits.append({'pair':[o.Label,q.Label],'mm3':v})
front=next(o for o in wood if 'Frente_da_gaveta' in o.Label)
b=front.Shape.BoundBox
report={'file':str(dest),'source':str(sourcefile),'parts':rows,'wood_internal_hits':hits,'hardware_wood_hits':hardware,'front_bbox':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],
 'visible_internal_floor_mm':[541,459],'tray_depth_mm':455,'front_rear_gap_mm':[2,2],'contents_count':len(contents),
 'proposed_changes':'Dianteira16, rasgos laterais5, fundo551x490 incluindo encaixes; corpo avançado7mm para apoiar diretamente na frente. Frentes e conteúdo preservados.',
 'scope':'Montagem fechada oficial e sólidos estáticos. Carga40kg inclui caixa/frente/conteúdo; peso total ainda não medido. Parafusos EURO entram nos apoios por definição; não classificados como colisão livre. Não certifica tolerâncias ou movimento telescópico.'}
g.Extensao=0;doc.recompute();doc.save()
((Path(__file__).resolve().parent / 'Montagem_G2_R07.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({k:v for k,v in report.items() if k!='parts'},ensure_ascii=False)
