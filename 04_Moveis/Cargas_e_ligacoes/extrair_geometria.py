"""Leitura da R50 aberta: caixas, grupos e contatos BREP. Nao altera/salva CAD."""
from pathlib import Path
import hashlib
import json
import re
import time
import FreeCAD as App
import FreeCADGui as Gui

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CAD=ROOT/'01_Projeto/Otimizacao_FreeCAD_R50_2026-10-24/Guedala_Park_R50_Completo_Otimizado.FCStd'
EXPECTED='1eda9a56e7346f5e08d5b4a391a57b4407132f14a142efdef1e2e5699c4dfd69'
TOL=1e-5

def write(name,data):
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def bbox(shape):
    b=shape.BoundBox
    return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]

def center(shape):
    # Compounds de ferragens/referencias nem sempre expoem CenterOfMass.
    solids=shape.Solids
    volume=sum(s.Volume for s in solids)
    if volume<=TOL:return None
    return [sum(s.CenterOfMass[k]*s.Volume for s in solids)/volume for k in range(3)]

doc=next(d for d in App.listDocuments().values() if Path(d.FileName).resolve()==CAD.resolve())
assert hashlib.sha256(CAD.read_bytes()).hexdigest()==EXPECTED
assert not Gui.getDocument(doc.Name).Modified, 'Documento tem mudancas nao salvas; reconciliar antes da leitura'
started=time.perf_counter()
joinery=json.loads((ROOT/'ferramentas/site/fabrication/r14/joinery.json').read_text(encoding='utf-8'))
parents={o.Name:[p.Name for p in o.InList if 'Group' in p.PropertiesList and o in p.Group] for o in doc.Objects}

def effective_visible(o,seen=frozenset()):
    if o.Name in seen:return False
    return bool(o.ViewObject.Visibility) and all(effective_visible(doc.getObject(n),seen|{o.Name}) for n in parents[o.Name])

def descendants(obj,seen=None):
    seen=set() if seen is None else seen
    if obj.Name in seen:return
    seen.add(obj.Name)
    yield obj
    if 'Group' in obj.PropertiesList:
        for child in obj.Group:yield from descendants(child,seen)

shapes={}
def world(name):
    if name not in shapes:
        obj=doc.getObject(name);sh=obj.Shape.copy()
        parent=obj.getGlobalPlacement().multiply(obj.Placement.inverse())
        sh.Placement=parent.multiply(sh.Placement)
        shapes[name]=sh
    return shapes[name]

records={}
modules={}
supplemental={f'P{i:02d}':[] for i in range(1,21)}
for part in doc.Objects:
    code=str(getattr(part,'ModuloR14',''))
    if code in supplemental and part.isDerivedFrom('Part::Feature') and not part.Shape.isNull():
        supplemental[code].append(part)
for number in range(20):
    code=f'P{number+1:02d}'
    obj=doc.getObject('Modulo' if number==0 else f'Modulo{number:03d}')
    pieces=[]
    candidates=list(descendants(obj))+supplemental[code]
    visited=set()
    for part in candidates:
        if part.Name in visited:continue
        visited.add(part.Name)
        if not part.isDerivedFrom('Part::Feature') or part.Shape.isNull():continue
        local=part.Shape
        record={'id':part.Name,'label':part.Label,'type':part.TypeId,'module':code,
                'visible_local':bool(part.ViewObject.Visibility),'visible_effective':effective_visible(part),
                'parents':parents[part.Name],'bbox_local_mm':bbox(local),'bbox_global_mm':bbox(world(part.Name)),
                'volume_mm3':local.Volume,'placement_matrix':list(part.Placement.toMatrix().A)}
        record['center_of_mass_local_mm']=center(local)
        record['center_of_mass_global_mm']=center(world(part.Name))
        if all(p in part.PropertiesList for p in ['Length','Width','Height']):
            record['box_mm']=[part.Length.Value,part.Width.Value,part.Height.Value]
        if part.TypeId=='Part::Cylinder':record['cylinder_mm']={'radius':part.Radius.Value,'length':part.Height.Value}
        for prop in ['MaterialReferencia','EspecificacaoR14','Natureza','ModuloR14']:
            if prop in part.PropertiesList:record[prop]=str(getattr(part,prop))
        records[part.Name]=record;pieces.append(part.Name)
    modules[code]={'object':obj.Name,'label':obj.Label,'pieces':pieces,
                   'unmapped_contacts_in_source':len(joinery['modules'][code].get('unmappedInterfaces',[])),
                   'nominal_positions_in_source':len(joinery['modules'][code].get('nominalPositions',[]))}

contacts=[]
for code,module in joinery['modules'].items():
    for index,text in enumerate(module.get('unmappedInterfaces',[]),1):
        match=re.match(r'([^ ]+)\s*↔\s*([^ ]+)',text)
        assert match,text
        a,b=match.groups();sa,sb=world(a),world(b);ba,bb=bbox(sa),bbox(sb)
        overlap=[min(ba[k+3],bb[k+3])-max(ba[k],bb[k]) for k in range(3)]
        planes=[k for k,v in enumerate(overlap) if abs(v)<TOL and all(overlap[j]>TOL for j in range(3) if j!=k)]
        area=0.
        for axis in planes:
            coordinate=(max(ba[axis],bb[axis])+min(ba[axis+3],bb[axis+3]))/2
            fa=[f for f in sa.Faces if bbox(f)[axis+3]-bbox(f)[axis]<TOL and abs(bbox(f)[axis]-coordinate)<TOL]
            fb=[f for f in sb.Faces if bbox(f)[axis+3]-bbox(f)[axis]<TOL and abs(bbox(f)[axis]-coordinate)<TOL]
            for facea in fa:
                for faceb in fb:area+=facea.common(faceb).Area
        distance=sa.distToShape(sb)[0]
        interference=sa.common(sb).Volume if all(v>TOL for v in overlap) else 0.
        state='contato de faces' if area>TOL else 'interferencia volumetrica' if interference>TOL else 'aresta/ponto' if distance<TOL else 'separados'
        contacts.append({'id':f'{code}-R50-{index:03d}','module':code,'a':a,'b':b,'source_text':text,
                         'bbox_overlap_mm':overlap,'global_normal_axis':['XYZ'[k] for k in planes],
                         'common_face_area_mm2':area,'distance_mm':distance,'interference_mm3':interference,
                         'state':state,'a_visible':effective_visible(doc.getObject(a)),
                         'b_visible':effective_visible(doc.getObject(b)),
                         'status':'Geometria nominal conferida; nao comprova ligacao resistente'})
        if index%10==0:write('Progresso_extracao.json',{'module':code,'contacts':len(contacts)})

# Interfaces que nao estavam na amostra antiga, criticas para caminho de carga.
special=[]
for a,b in [('Peca362','Peca361'),('Peca363','Peca361'),('Peca269','Peca268'),('Peca270','Peca268')]:
    sa,sb=world(a),world(b);ba,bb=bbox(sa),bbox(sb)
    special.append({'a':a,'b':b,'bbox_a':ba,'bbox_b':bb,'overlap_mm':[min(ba[i+3],bb[i+3])-max(ba[i],bb[i]) for i in range(3)],
                    'distance_mm':sa.distToShape(sb)[0],'method':'BREP distance and global bbox; area audited in contact classification'})
write('Geometria_R50.json',{'date':'2026-10-25','cad':str(CAD.relative_to(ROOT)),'sha256':EXPECTED,
                           'method':'FreeCAD GUI, BREP e parametros atuais; leitura sem recomputar/salvar a R50',
                           'modules':modules,'parts':records,'special_interfaces':special})
write('Contatos_reconciliados.json',{'source':joinery['revision'],'cad_sha256':EXPECTED,'contacts':contacts,
                                    'count':len(contacts),'module_count':len(modules),'additional_interfaces':special})
assert hashlib.sha256(CAD.read_bytes()).hexdigest()==EXPECTED
write('Progresso_extracao.json',{'complete':True,'modules':len(modules),'parts':len(records),
                               'contacts':len(contacts),'seconds':time.perf_counter()-started,'CAD_unchanged':True})
print(json.dumps({'modules':len(modules),'parts':len(records),'contacts':len(contacts),'seconds':time.perf_counter()-started}))
