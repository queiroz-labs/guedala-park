from pathlib import Path
from collections import defaultdict, Counter
import json, math, re, zipfile, xml.etree.ElementTree as ET

HERE=(Path(__file__).resolve().parent / '.').resolve()
BASE=(Path(__file__).resolve().parent / '../..').resolve()
FILE=(Path(__file__).resolve().parent / '../Rotulos_R23_2026-10-14/Guedala_Park_R23_Rotulos_Consistentes.FCStd').resolve()
with zipfile.ZipFile(FILE) as z:
    doc=ET.fromstring(z.read('Document.xml'))
    gui=ET.fromstring(z.read('GuiDocument.xml'))
TYPES={o.get('name'):o.get('type') for o in doc.find('Objects') if o.tag=='Object'}
DATA={o.get('name'):{p.get('name'):p for p in o.find('Properties') if p.tag=='Property'} for o in doc.find('ObjectData')}
VIEWS={o.get('name'):{p.get('name'):p for p in o.find('Properties')} for o in gui.find('ViewProviderData')}
def child(name,prop):
    p=DATA.get(name,{}).get(prop)
    return p[0] if p is not None and len(p) else None
def val(name,prop,default=None):
    e=child(name,prop)
    if e is None:
        cells=child(name,'cells')
        if cells is not None:
            matches=[c for c in cells if c.tag=='Cell' and (c.get('address')==prop or c.get('alias')==prop)]
            if matches:
                content=matches[0].get('content','')
                m=re.fullmatch(r'=\s*([-+]?\d+(?:\.\d+)?)\s*(?:deg|mm)?',content)
                return float(m[1]) if m else content
        return default
    if e.tag in ('Float','Integer'):return float(e.get('value'))
    if e.tag=='Bool':return e.get('value')=='true'
    if e.tag=='String':return e.get('value','')
    if e.tag=='Link':return e.get('value')
    if e.tag=='XLink':return e.get('name')
    if e.tag=='LinkList':return [x.get('value') for x in e]
    return e.attrib
def visible(n):return val(n,'Visibility',True)
def label(n):return val(n,'Label','')
GROUPS={n:val(n,'Group',[]) for n in DATA if 'Group' in DATA[n]}
PARENTS=defaultdict(list)
for p,children in GROUPS.items():
    for c in children:PARENTS[c].append(p)
GEOPARENTS={c:[p for p in parents if TYPES[p]=='App::Part'] for c,parents in PARENTS.items()}
def chain(n):
    out=[n]; seen={n}
    while GEOPARENTS.get(n):
        ps=GEOPARENTS[n]
        if len(ps)!=1:return out+['MULTIPLE_GEOPARENTS:'+','.join(ps)]
        n=ps[0]
        if n in seen:return out+['CYCLE:'+n]
        seen.add(n);out.append(n)
    return out
def ident():return [[float(i==j) for j in range(4)] for i in range(4)]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
def placement(n,prop='Placement'):
    e=child(n,prop)
    if e is None:return ident()
    q=[float(e.get('Q'+str(i),'0' if i<3 else '1')) for i in range(4)]
    x,y,z,w=q
    a=ident();a[:3]=[[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w),float(e.get('Px','0'))],
                     [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w),float(e.get('Py','0'))],
                     [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y),float(e.get('Pz','0'))]]
    return a
def world(n):
    a=ident()
    for p in reversed(chain(n)):a=mul(a,placement(p))
    return a
REFLECT=ident();REFLECT[0][0]=-1;REFLECT[0][3]=7400
def point(a,p):return [sum(a[i][j]*p[j] for j in range(3))+a[i][3] for i in range(3)]
def bounds(a,dims):
    pts=[point(a,[x,y,z]) for x in (0,dims[0]) for y in (0,dims[1]) for z in (0,dims[2])]
    return [min(p[i] for p in pts) for i in range(3)]+[max(p[i] for p in pts) for i in range(3)]
def inherited_hidden(n,stop=None):
    q=n;out=[];seen=set()
    while q!=stop:
        if not visible(q):out.append(q)
        if q in seen:break
        seen.add(q)
        ps=GEOPARENTS.get(q,[])
        if not ps:break
        q=ps[0]
    return out
mapping=json.loads(((Path(__file__).resolve().parent / '../Apartamento_espelhado_R20_2026-10-14/Espelhamento_R20.json').resolve()).read_text(encoding='utf-8'))
LINKS=[n for n in DATA if n.startswith('EspelhoPecaR') and TYPES[n]=='App::Link']
by_source=defaultdict(list)
issues=[];link_rows=[]
for n in LINKS:
    source=val(n,'LinkedObject');by_source[source].append(n)
    scale=val(n,'ScaleVector',{})
    sv=[float(scale.get('value'+i,'1')) for i in 'XYZ']
    a=placement(n,'LinkPlacement');a=[row[:] for row in a]
    for i in range(3):
        for j in range(3):a[i][j]*=sv[j]
    err=max(abs(a[i][j]-REFLECT[i][j]) for i in range(4) for j in range(4))
    group_parents=PARENTS.get(n,[])
    nested=[p for p in group_parents if TYPES[p]=='App::Link' or TYPES[p]=='App::Part']
    if source not in DATA or TYPES.get(source)=='App::Link' or err>1e-8 or not val(n,'LinkTransform') or nested:
        issues.append(dict(kind='link_transform_or_target',link=n,source=source,error=err,nested=nested))
    link_rows.append(dict(link=n,source=source,label=label(n),source_type=TYPES.get(source),visible=visible(n),groups=group_parents,scale=sv,matrix=a,max_transform_error=err,LinkTransform=val(n,'LinkTransform')))
for s,ls in by_source.items():
    if len([n for n in ls if visible(n)])>1:issues.append(dict(kind='duplicate_visible_source',source=s,links=ls))
    if label(s).lower().startswith(('histórico','historico')) and any(visible(n) for n in ls):
        issues.append(dict(kind='historical_source_visible_via_mirror',source=s,source_label=label(s),source_visibility=visible(s),links=[n for n in ls if visible(n)]))
expected=set(x for r in mapping['mapping'] for x in r['source_roots'])
if expected!=set(by_source):issues.append(dict(kind='root_coverage',missing=sorted(expected-set(by_source)),extra=sorted(set(by_source)-expected)))
def coverage(n):
    ch=chain(n);root=ch[-1];links=by_source.get(root,[])
    return dict(object=n,label=label(n),exists=n in DATA,geo_chain=ch,source_root=root,mirror_links=links,root_link_visible=[l for l in links if visible(l)],hidden_below_link_root=inherited_hidden(n,root),base_world_matrix=world(n),mirrored_world_matrix=mul(REFLECT,world(n)) if links else None)
inventory=json.loads(((Path(__file__).resolve().parent / '../Rotulos_R23_2026-10-14/Inventario_modulos_R23.json').resolve()).read_text(encoding='utf-8'))
modules=[]
for row in inventory['modules']:
    n=row['object'];c=coverage(n);c['inventory_dimensions']=row['cad_body_dimensions_mm'];c['native_dimensions']={p:val(n,p) for p in row['cad_body_dimensions_mm']}
    dims=[val(n,p) for p in ['Comprimento','Profundidade','Altura']]
    c['body_property_envelope_mirrored']=bounds(c['mirrored_world_matrix'],dims) if c['mirrored_world_matrix'] else None
    c['closed_envelope_warning']='Envelope somente das propriedades de corpo; não conjunto acabado, conteúdo ou superfícies BREP'
    if c['native_dimensions']!=c['inventory_dimensions'] or len(c['root_link_visible'])!=1:issues.append(dict(kind='module_inventory_or_link',object=n))
    modules.append(c)
equipment_names=['Peca133','Peca134','Peca138','Peca139','Peca140','Peca147','Peca148','Peca149','Peca152','Peca154','Peca155','Peca156','Peca351']
equipment=[]
for n in equipment_names:
    c=coverage(n);dims=[val(n,p) for p in ['Length','Width','Height']];c['box_dimensions']=dims
    if c['mirrored_world_matrix'] and all(isinstance(x,(int,float)) for x in dims):c['box_envelope_mirrored']=bounds(c['mirrored_world_matrix'],dims)
    if len(c['root_link_visible'])!=1:issues.append(dict(kind='equipment_link_coverage',object=n))
    equipment.append(c)
program_sets={
 'Banco_R16':json.loads(((Path(__file__).resolve().parent / '../Banco_R16_2026-10-14/Montagem_R16.json').resolve()).read_text(encoding='utf-8'))['content'],
 'Limpeza_R13':json.loads(((Path(__file__).resolve().parent / '../Gaveta_rodas_R13_2026-10-14/Montagem_R13.json').resolve()).read_text(encoding='utf-8'))['program_names']
}
g2=json.loads(((Path(__file__).resolve().parent / '../G2_R06_2026-10-13/Bandejas_G2_R06.json').resolve()).read_text(encoding='utf-8'))
((Path(__file__).resolve().parent / 'Schema_G2.json').resolve()).write_text(json.dumps({'keys':list(g2),'items':g2},ensure_ascii=False,indent=2),encoding='utf-8')
program_sets['G2_nove_gabaritos']=[]
for item in g2['items']:
    matches=[n for n in DATA if n.startswith('OrganizadorG2') and label(n)==item['item']]
    if len(matches)!=1:issues.append(dict(kind='g2_program_item_match',item=item['item'],matches=matches))
    program_sets['G2_nove_gabaritos']+=matches
program={}
for title,names in program_sets.items():
    program[title]=[coverage(n) for n in names]
    for c in program[title]:
        if not c['exists'] or not c['root_link_visible']:issues.append(dict(kind='program_missing_root',set=title,object=c['object']))
catalog=json.loads(((Path(__file__).resolve().parent / '../Rotulos_R23_2026-10-14/Controles_R23.json').resolve()).read_text(encoding='utf-8'))
controls=[]
for row in catalog['catalog']:
    n=row['control'];fields={p:val(n,p,'MISSING') for p in row['fields']};shortcut=row.get('shortcut');original=val(shortcut,'LinkedObject') if shortcut else None
    direct_bindings=[]
    for target,ps in DATA.items():
        e=child(target,'ExpressionEngine')
        if e is None:continue
        for x in e:
            expression=x.get('expression','')
            if n+'.' in expression:
                direct_bindings.append(dict(object=target,path=x.get('path'),expression=expression,saved_value=val(target,x.get('path'))))
    direct_equal=[]
    for b in direct_bindings:
        if b['expression'].startswith(n+'.') and b['expression'].count('.')==1:
            p=b['expression'].split('.')[1];v=val(n,p);tv=val(b['object'],b['path'])
            if isinstance(v,(int,float)) and isinstance(tv,(int,float)):
                direct_equal.append(dict(target=b['object'],property=b['path'],control_field=p,control_value=v,target_value=tv,equal=abs(v-tv)<1e-7))
                if abs(v-tv)>=1e-7:issues.append(dict(kind='direct_control_value_mismatch',control=n,target=b['object'],field=p,control_value=v,target_value=tv))
    if n not in DATA or label(n)!=row['label'] or 'MISSING' in fields.values() or (shortcut and (original!=n or visible(shortcut))):issues.append(dict(kind='control_catalog',control=n,shortcut=shortcut))
    controls.append(dict(control=n,label=label(n),fields=fields,shortcut=shortcut,shortcut_target=original,shortcut_visible=visible(shortcut) if shortcut else None,geo_chain=chain(n),direct_bindings=direct_bindings,direct_equal_checks=direct_equal))
historical=[dict(object=n,label=label(n),visibility=visible(n),geo_chain=chain(n)) for n in DATA if n.startswith('Historico')]
if any(x['visibility'] for x in historical):issues.append(dict(kind='visible_historical_group',objects=[x['object'] for x in historical if x['visibility']]))
def effective_original(n,seen=None):
    seen=set() if seen is None else seen
    if n in seen:return False
    seen.add(n)
    if not visible(n):return False
    return all(effective_original(p,seen.copy()) for p in PARENTS.get(n,[]))
unmirrored_visible=[]
for n,t in TYPES.items():
    if (t=='App::Part' or 'Shape' in DATA[n]) and not GEOPARENTS.get(n) and t!='App::Link' and effective_original(n):
        unmirrored_visible.append(dict(object=n,label=label(n),parents=PARENTS.get(n,[])))
if unmirrored_visible:issues.append(dict(kind='unmirrored_visible_root',objects=unmirrored_visible))
georoots=[n for n,t in TYPES.items() if (t=='App::Part' or 'Shape' in DATA[n]) and not GEOPARENTS.get(n) and t!='App::Link']
unmapped_roots=[dict(object=n,label=label(n),visibility=visible(n),effective_original_visibility=effective_original(n),parents=PARENTS.get(n,[])) for n in georoots if n not in by_source]
report=dict(file=str(FILE),method='Somente ZIP/XML/JSON, sem runtime CAD, GUI, checksum em massa, save ou teste de movimento',links=link_rows,modules=modules,equipment=equipment,program=program,controls=controls,historical_groups=historical,unmapped_geometric_roots=unmapped_roots,unmirrored_visible_roots=unmirrored_visible,issues=issues,summary=dict(objects=len(DATA),mirror_links=len(LINKS),visible_mirror_links=sum(visible(n) for n in LINKS),mapped_sources=len(by_source),modules=len(modules),controls=len(controls),program_items=sum(len(v) for v in program.values()),direct_control_value_checks=sum(len(c['direct_equal_checks']) for c in controls),issues=len(issues)),limits=['BREP não recalculado e nenhuma colisão auditada','Matrices registradas derivadas de placements/quaternions XML; não homologam superfícies de fabricante','Envelope de corpo não é envelope acabado/corte','Programa verificado somente nos conjuntos documentados selecionados; não prova catálogo completo de objetos pessoais reais'])
((Path(__file__).resolve().parent / 'Auditoria_XML.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report['summary'],ensure_ascii=False));print(json.dumps(issues,ensure_ascii=False))
