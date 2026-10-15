"""Estudo separado de apoios; R30 somente leitura. Rodar uma vez no FreeCAD."""
import FreeCAD as App, FreeCADGui as Gui, Part
from pathlib import Path
import json,math,hashlib
here=Path(__file__).resolve().parent
source=App.ActiveDocument
assert source.Name=='Guedala_Park_R30_Juntas_Rotulos'
base=here.parent/'Modelo_FreeCAD/02_Revisoes_e_estudos'
bank=json.loads((base/'Banco_R16_2026-10-14/Montagem_R16.json').read_text(encoding='utf-8'))
basket=json.loads((base/'Cesto_R15_2026-10-14/Montagem_R15.json').read_text(encoding='utf-8'))
for c in [x['control'] for x in bank['lids']]+['ControleCestoR15']:
    assert abs(float(source.getObject(c).Abertura))<1e-7, 'Estudo exige controles fechados; não alterar automaticamente'
hash_before=hashlib.sha256(Path(source.FileName).read_bytes()).hexdigest()
def local_shape(name,module):
    o=source.getObject(name)
    if not o or not hasattr(o,'Shape') or o.Shape.isNull():return None
    s=o.Shape.copy();s.Placement=source.getObject(module).getGlobalPlacement().inverse().multiply(o.getGlobalPlacement())
    return s
bank_names=list(dict.fromkeys(bank['structure']+bank['new']))
cesto_names=list(dict.fromkeys(basket['fixed']+basket['moving']+basket['hydraulic']+[basket['bag'],'Peca352','Peca353','FundoTanqueR29']))
collections={
 'banco':{n:local_shape(n,'Modulo019') for n in bank_names},
 'cesto':{n:local_shape(n,'Modulo013') for n in cesto_names}}
collections={k:{n:s for n,s in v.items() if s is not None} for k,v in collections.items()}
supports=[
 ('B01','banco','Apoio sob divisória dos potes',(1402,20,0),(18,390,80)),
 ('B02','banco','Apoio sob base e divisória das bebidas',(1034,20,0),(18,390,82)),
 ('B03','banco','Apoio sob base e divisória da folha',(818,20,0),(18,390,82)),
 ('B04','banco','Fechamento de apoio sob posterior',(18,432,0),(1764,18,18)),
 ('C01','cesto','Apoio inferior lateral 1 recuado',(0,50,0),(18,580,98)),
 ('C02','cesto','Apoio inferior lateral 2 recuado',(572,50,0),(18,580,98)),
 ('C03','cesto','Apoio traseiro sob base',(18,594,0),(554,18,80)),
]
new={code:Part.makeBox(*dim,App.Vector(*pos)) for code,group,label,pos,dim in supports}
checks=[];hits=[]
for code,group,label,pos,dim in supports:
    s=new[code]
    for name,t in collections[group].items():
        a=s.BoundBox;b=t.BoundBox
        if all(min(getattr(a,k+'Max'),getattr(b,k+'Max'))-max(getattr(a,k+'Min'),getattr(b,k+'Min'))>1e-6 for k in ['X','Y','Z']):
            volume=s.common(t).Volume
            checks.append({'support':code,'part':name,'intersection_mm3':volume})
            if volume>0.1:hits.append(checks[-1])
assert not hits,hits
# Continuous bounds of the existing moving boxes for 0..55 deg about local (Y70,Z120).
# Evaluate endpoints and derivative roots of y=a cos(t)+b sin(t)+70.
theta=math.radians(55);max_y=-1e100;min_x=1e100;max_x=-1e100
for name in basket['moving']+[basket['bag']]:
    s=collections['cesto'].get(name)
    if s is None:continue
    b=s.BoundBox;min_x=min(min_x,b.XMin);max_x=max(max_x,b.XMax)
    for y in [b.YMin,b.YMax]:
        for z in [b.ZMin,b.ZMax]:
            a=y-70;c=-(z-120);angles=[0,theta]
            critical=math.atan2(c,a)
            for k in range(-2,3):
                t=critical+k*math.pi
                if 0<t<theta:angles.append(t)
            max_y=max(max_y,max(70+a*math.cos(t)+c*math.sin(t) for t in angles))
arc={'method':'Limites contínuos das caixas locais durante rotação rígida ideal +0..55 graus, eixo X em Y70/Z120. Somente contra os três novos apoios; exclui saco deformável, mãos e ferragem real.',
 'min_x':min_x,'max_x':max_x,'max_y':max_y,'left_support_gap':min_x-18,'right_support_gap':572-max_x,'rear_support_gap':594-max_y}
assert arc['left_support_gap']>0 and arc['right_support_gap']>0 and arc['rear_support_gap']>0,arc
name='Estudo_Apoios_Banco_Cesto_R30'
assert name not in App.listDocuments(),'Estudo já aberto; não sobrescrever'
target=here/(name+'.FCStd');assert not target.exists(),'Não sobrescrever estudo existente'
detail=App.newDocument(name)
for group,items in collections.items():
    g=detail.addObject('App::DocumentObjectGroup',group.title());g.Label=group.title()+' · cópias de referência R30'
    offset=App.Vector(0 if group=='banco' else 2050,0,0)
    for n,s in items.items():
        o=detail.addObject('Part::Feature',group+'_'+n);o.Label=source.getObject(n).Label
        clone=s.copy();clone.translate(offset);o.Shape=clone
        o.ViewObject.ShapeColor=(0.75,0.77,0.72);o.ViewObject.Transparency=75
        g.addObject(o)
    ng=detail.addObject('App::DocumentObjectGroup',group+'Apoios');ng.Label=group.title()+' · NOVOS APOIOS PROPOSTOS'
    for code,kind,label,pos,dim in supports:
        if kind!=group:continue
        o=detail.addObject('Part::Feature',code);o.Label=code+' · '+label+' · envelope proposto'
        clone=new[code].copy();clone.translate(offset);o.Shape=clone;o.ViewObject.ShapeColor=(0.86,0.43,0.16);ng.addObject(o)
        o.addProperty('App::PropertyString','Condicao','Estudo');o.Condicao='Envelope total incluindo eventual proteção/nivelamento. Material, ligação, piso real e capacidade por dimensionar. Não é lista de corte.'
detail.recompute();assert all(o.Shape.isValid() for o in detail.Objects if hasattr(o,'Shape'))
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
detail.saveAs(str(target))
Gui.activeDocument().activeView().saveImage(str(here/'Apoios_propostos.png'),1500,950,'White')
report={'source':source.FileName,'source_sha256_before':hash_before,'source_sha256_after':hashlib.sha256(Path(source.FileName).read_bytes()).hexdigest(),
 'study':str(target),'supports':[{'id':c,'group':g,'label':l,'origin_mm':p,'envelope_mm':s} for c,g,l,p,s in supports],
 'reference_shape_counts':{k:len(v) for k,v in collections.items()},'overlap_candidates':checks,'overlaps':hits,'basket_arc':arc,
 'limits':'Estudo de contatos e envelopes. Não dimensiona resistência, união, material, retenção, ferragens ou fixação à obra. Estado fechado; movimentos antigos não repetidos.'}
assert report['source_sha256_before']==report['source_sha256_after']
(here/'Verificacao_apoios.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result={'study':str(target),'support_count':len(supports),'overlaps':hits,'basket_arc':arc,'source_unchanged':True}
