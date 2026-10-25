"""Study only: lowering the existing shelf/appliance200mm, never adopted in R52."""
from pathlib import Path
import json,hashlib,traceback,os,sys,runpy,math
import FreeCAD as App,Part
HERE=Path(__file__).resolve().parent;PROJ=HERE.parents[1];ROOT=PROJ.parent.parent
SOURCE=PROJ/'Correcao_integral_R52_2026-10-25/Guedala_Park_R52_Corrigido.FCStd'
TARGET=HERE/'ME23P_folga300_ESTUDO_NAO_ADOTADO.FCStd'

def write(n,d):
    (HERE/n).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def world(o):
    s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def bbox(s):
    b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def overlap(a,b):return all(min(a[i+3],b[i+3])-max(a[i],b[i])>1e-6 for i in range(3))

try:
    assert not TARGET.exists(),'Preserve the existing study.'
    sha=hashlib.sha256(SOURCE.read_bytes()).hexdigest();assert sha=='941da02d367c5f6ce2992f72985f86c3aceba23f899a4c394cf3569f19d7b4da'
    d=App.openDocument(str(SOURCE));moving=['Peca350','Peca351'];old={n:world(d.getObject(n)) for n in moving}
    proposed={n:s.copy() for n,s in old.items()}
    for s in proposed.values():s.translate(App.Vector(0,0,-200))
    cabinet_bottom=world(d.getObject('Peca337')).BoundBox.ZMin
    assert abs(cabinet_bottom-old['Peca351'].BoundBox.ZMax-100)<1e-6
    assert abs(cabinet_bottom-proposed['Peca351'].BoundBox.ZMax-300)<1e-6
    inv=json.loads((ROOT/'outputs/correcao-r52-2026-10-25/validacao_final/geometria_cad.json').read_text(encoding='utf-8'))
    active=[r for r in inv if r['active'] and r['solids'] and r['volume']>0.01 and r['name'] not in moving]
    hits=[];tested=0;context=[]
    region=[1400,6200,900,2600,7100,2600]
    for r in active:
        if overlap(region,r['bbox']) and not r['name'].startswith(('Ferragem','Calco','Caneco','Minifix')):context.append(r['name'])
        for n,s in proposed.items():
            if not overlap(bbox(s),r['bbox']):continue
            tested+=1;vol=s.common(world(d.getObject(r['name']))).Volume
            if vol>0.1:hits.append({'moving':n,'fixed':r['name'],'label':r['label'],'common_mm3':vol})
    assert not hits,hits
    study=App.newDocument('ME23P_Folga300_ESTUDO')
    study.Label='ME23P - folga300 - ESTUDO NAO ADOTADO'
    current=study.addObject('App::DocumentObjectGroup','LayoutF104Preservado');current.Label='Historico de comparacao - F104 permanece na R52'
    alt=study.addObject('App::DocumentObjectGroup','Hipotese300');alt.Label='Hipotese de projeto - prateleira e aparelho200mm abaixo'
    ctx=study.addObject('App::DocumentObjectGroup','ContextoR52');ctx.Label='Contexto nominal R52 - sem alteracoes'
    def add(n,s,label,group,visible=True):
        o=study.addObject('Part::Feature',n);o.Shape=s;o.Label=label;group.addObject(o)
        if 'Visibility' not in o.PropertiesList:o.addProperty('App::PropertyBool','Visibility')
        o.Visibility=visible;return o
    for n,s in old.items():add('Original_'+n,s,'F104 original - '+d.getObject(n).Label,current,False)
    for n,s in proposed.items():add('Proposta_'+n,s,'ESTUDO - '+d.getObject(n).Label,alt)
    for n in context:add('Contexto_'+n,world(d.getObject(n)),d.getObject(n).Label,ctx)
    current.Visibility=False
    info=study.addObject('App::FeaturePython','Limites')
    info.addProperty('App::PropertyString','Estado');info.Estado='NAO ADOTADO. R52/F104 com100mm superiores intacta. Hipotese nominal sem nova prateleira, sem perda do armario B; requer aceitar outra altura e definir apoio/fixacao. Nao certifica ventilacao/uso/ergonomia.'
    info.addProperty('App::PropertyString','Fonte');info.Fonte=str(SOURCE)+' SHA256 '+sha
    study.recompute()
    assert all(o.Shape.isValid() for o in study.Objects if o.isDerivedFrom('Part::Feature'))
    save=runpy.run_path(str(PROJ/'Otimizacao_FreeCAD_R50_2026-10-24/serializacao_binaria.py'))['salvar_documento'](study,TARGET)
    App.closeDocument(study.Name);reopened=App.openDocument(str(TARGET))
    assert reopened.getObject('Proposta_Peca351').Shape.BoundBox.ZMax==1640
    count=len(reopened.Objects);App.closeDocument(reopened.Name);App.closeDocument(d.Name)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==sha
    write('Micro_estudo.json',{'source_sha256':sha,'source_unchanged':True,'F104_preserved':True,'adopted':False,'study':save,
        'old_boxes':{n:bbox(s) for n,s in old.items()},'proposed_boxes':{n:bbox(s) for n,s in proposed.items()},
        'cabinet_bottom_mm':cabinet_bottom,'current_upper_gap_mm':100,'proposed_upper_gap_mm':300,'extra_margin_over_minimum_mm':0,
        'source_active_solids_considered':len(active),'bbox_candidate_booleans':tested,'positive_intersections':hits,'reopened_objects':count,
        'limits':['Nominal geometry only; no real-apartment dimensions','No adoption or reversal of F104','No load/anchor/thermal/ergonomic approval','Actual shelf/appliance mounting, access and tolerance still needed']})
except BaseException:write('Erro_micro.json',traceback.format_exc())
sys.stdout.flush();sys.stderr.flush();os._exit(0)
