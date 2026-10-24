"""Estudo nominal de uniões internas P19; não é programa CNC nem cálculo estrutural."""
from pathlib import Path
import FreeCAD as App, Part, json, csv, hashlib

ROOT=Path(r'C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park')
OUT=Path(__file__).resolve().parent
SOURCE=ROOT/'01_Projeto/Cozinha/Rodizios_gaveta_2026-10-24/Guedala_Park_R45_Rodizios_P08.FCStd'
source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
doc=App.openDocument(str(SOURCE));group=doc.getObject('Modulo018')
study=App.newDocument('Espelheiro_Unioes_P19')
boards={name:doc.getObject(name).Shape.copy() for name in ['Peca400','Peca401','Peca402','Peca403','Peca404']}
result={};tools=[];positions=[];operations=[]

def addtool(host,kind,diameter,depth,point,axis,number):
    shape=Part.makeCylinder(diameter/2,depth,App.Vector(*point),App.Vector(*axis))
    assert shape.common(boards[host]).Volume>1e-6,(host,kind)
    tools.append((host,shape))
    o=study.addObject('Part::Feature','FerramentaP19')
    o.Label=f'{number:02} {kind} {host} — nominal';o.Shape=shape
    if o.ViewObject:o.ViewObject.Visibility=False
    operations.append(dict(joint=number,part=host,operation=kind,diameter_mm=diameter,depth_mm=depth,x=point[0],y=point[1],z=point[2],axis_x=axis[0],axis_y=axis[1],axis_z=axis[2],status='Nominal para prova em oficina; não CNC'))

# Base e tampo: dois Minifix em cada extremidade, acesso pelo interior.
for board,zentry,zaxis,zpin in [('Peca403',18,-1,9),('Peca404',732,1,741)]:
    for side,edge,sign,camx in [('Peca401',-582,1,-548),('Peca400',-18,-1,-52)]:
        for y in [50,106]:
            n=len(positions)+1
            addtool(board,'Caixa Minifix',15,14,(camx,y,zentry),(0,0,zaxis),n)
            addtool(board,'Passagem cabeça S100',7,34,(edge,y,zpin),(sign,0,0),n)
            addtool(side,'Piloto S100 proposto',5,8.5,(edge,y,zpin),(-sign,0,0),n)
            positions.append(dict(joint=n,board=board,side=side,cam=[camx,y,zentry],cam_axis=[0,0,zaxis],edge=[edge,y,zpin],pin_axis=[-sign,0,0]))
# Fundo 18 mm entre laterais: acesso à caixa pela face interna, sem cabeças externas.
for side,edge,sign,camx in [('Peca401',-582,1,-548),('Peca400',-18,-1,-52)]:
    for z in [120,630]:
        n=len(positions)+1
        addtool('Peca402','Caixa Minifix',15,14,(camx,132,z),(0,1,0),n)
        addtool('Peca402','Passagem cabeça S100',7,34,(edge,141,z),(sign,0,0),n)
        addtool(side,'Piloto S100 proposto',5,8.5,(edge,141,z),(-sign,0,0),n)
        positions.append(dict(joint=n,board='Peca402',side=side,cam=[camx,132,z],cam_axis=[0,1,0],edge=[edge,141,z],pin_axis=[-sign,0,0]))
assert len(positions)==12 and len(operations)==36

def bbox(s):
    b=s.copy().cleaned().BoundBox
    return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]

for name,shape in boards.items():
    cut=shape
    for host,tool in tools:
        if host==name:cut=cut.cut(tool)
    assert cut.isValid(),name
    assert all(abs(a-b)<1e-7 for a,b in zip(bbox(shape),bbox(cut))),name
    o=study.addObject('Part::Feature',name);o.Label=doc.getObject(name).Label+' — uniões Minifix propostas';o.Shape=cut
    if o.ViewObject:o.ViewObject.ShapeColor=(0.84,0.74,0.58) if name in ['Peca400','Peca401'] else (0.92,0.92,0.89)
    result[name]=dict(valid=True,bbox=bbox(cut),removed_volume_mm3=shape.Volume-cut.Volume)

# Conferência dos volumes de usinagem contra prateleiras, portas e ferragens existentes.
def descendants(o):
    for c in getattr(o,'Group',[]):
        yield c
        yield from descendants(c)
context=[];inv=group.getGlobalPlacement().inverse()
for o in descendants(group):
    if o.Name in boards or not o.isDerivedFrom('Part::Feature') or o.Shape.isNull():continue
    # Furos são ferramentas históricas, não peças instaladas.
    if o.Name.startswith(('Furos','Caneco')):continue
    s=o.Shape.copy();s.Placement=inv.multiply(o.getGlobalPlacement())
    context.append((o.Name,s))
collisions=[]
for host,t in tools:
    a=t.BoundBox
    for name,s in context:
        b=s.BoundBox
        if any([a.XMax<=b.XMin,a.XMin>=b.XMax,a.YMax<=b.YMin,a.YMin>=b.YMax,a.ZMax<=b.ZMin,a.ZMin>=b.ZMax]):continue
        v=t.common(s).Volume
        if v>1e-6:collisions.append(dict(host=host,context=name,volume=v))
assert not collisions,collisions
study.recompute()
target=OUT/'Espelheiro_P19_Unioes_NOMINAIS.FCStd';study.saveAs(str(target))
App.closeDocument(study.Name);check=App.openDocument(str(target))
assert all(check.getObject(name).Shape.isValid() for name in boards)
with (OUT/'P19_Unioes_nominais.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(operations[0]));writer.writeheader();writer.writerows(operations)
report=dict(date='2026-10-24',source=str(SOURCE),sourceSHA256=source_hash,study=str(target),studySHA256=hashlib.sha256(target.read_bytes()).hexdigest(),coordinate_system='Local do Modulo018 da R45/P08; X=-600..0, Y=24..150, Z=0..750. Não são coordenadas do apartamento.',minifix_sets=12,operations=36,mapped_interfaces=6,boards=result,positions=positions,context_objects=len(context),collisions=collisions,reopened=True,source_unchanged=hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash,assembly='Montar fundo/base/topo entre as laterais; travar Minifix pelo interior antes de instalar prateleiras e portas. Ferragem real e ferramenta devem ser provadas.',limits=['Alojamentos e passagem são gabaritos, não sólidos dos conectores.','Acesso de chave, montagem, torque, retenção e resistência exigem prova de oficina.','Piloto 8,5 e furo máximo 14 são propostas de usinagem; medir chapa/ponta da broca.','Suspensão/ancoragem e adesivo dos espelhos não foram dimensionados por este mapa.'],sources=['01_Projeto/Consolidacao_R45_2026-10-23/Inventario/Minifix_C.md','https://hafelethailand.com/wp-content/uploads/2025/12/02-connector-technology-shelf-supports.pdf'])
assert report['source_unchanged']
(OUT/'Verificacao_unioes_P19.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('P19: 12 uniões Minifix, 36 operações, 6 interfaces mapeadas; estudo salvo/reaberto; principal preservado.')
