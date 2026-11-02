"""Extrai envelopes globais da R53 sem recalcular ou salvar o FCStd."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '06_Entregas/Caderno_pranchas/Geometria.json'


def complementar(payload):
    """Campos derivados da própria exportação; referência nominal congelada, não entrada editável."""
    sys.path.insert(0, str(Path(__file__).parent))
    from medidas import carregar, numero
    rows = carregar(ROOT)
    config = json.loads((ROOT/'06_Entregas/Planta_cotada/Cotas.json').read_text(encoding='utf-8'))['pranchas']
    ceilings = {room: numero(rows[code]['valor_nominal_atual'], nominal=True) for room,code in config['ceiling'].items()}
    payload['ceilings_at_export'] = ceilings
    payload['modules'] = {}
    for name in sorted({o['module'] for o in payload['objects'] if o['module']}):
        objs = [o for o in payload['objects'] if o['module']==name]
        b = [min(o['box'][i] for o in objs) if i<3 else max(o['box'][i] for o in objs) for i in range(6)]
        payload['modules'][name] = dict(box=b, position=b[:3], size=[b[i+3]-b[i] for i in range(3)],
                                       ceiling_ref=config['ceiling'][objs[0]['room']],
                                       clearance_at_export=ceilings[objs[0]['room']]-b[5])
    if len(payload['modules']) != 20:
        raise ValueError('Exportação incompleta: esperados P01-P20')
    return payload


def exportar():
    import FreeCAD as App
    release=json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    path=ROOT/release['cadPath']; before=hashlib.sha256(path.read_bytes()).hexdigest()
    if before!=release['cadSHA256']:raise ValueError('SHA do modelo diverge do manifesto')
    doc=App.openDocument(str(path),True)
    try:
        result=exportar_documento_gui(doc,OUT,oficial=True)
    finally:
        App.closeDocument(doc.Name)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==before
    print(result)


def atualizar_selecao(ids_atualizar):
    """Relê os objetos selecionados para R02, sem reinterpretar a árvore R55."""
    import FreeCAD as App
    release = json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    path = ROOT/release['cadPath']
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    assert before == release['cadSHA256']
    doc = App.ActiveDocument
    assert doc and Path(doc.FileName).resolve() == path.resolve()
    payload = json.loads(OUT.read_text(encoding='utf-8'))
    anteriores = {o['id']:list(o['box']) for o in payload['objects']}
    if set(ids_atualizar)-set(anteriores):
        raise ValueError('Objeto fora da seleção histórica')
    for record in payload['objects']:
        obj = doc.getObject(record['id'])
        if obj is None or not hasattr(obj, 'Shape') or obj.Shape.isNull():
            raise ValueError('Objeto da seleção anterior ausente: '+record['id'])
        box = obj.Shape.BoundBox
        parent = obj.getParentGeoFeatureGroup()
        matrix = parent.getGlobalPlacement().toMatrix() if parent else App.Matrix()
        pts = [matrix.multVec(App.Vector(x,y,z)) for x in (box.XMin,box.XMax)
               for y in (box.YMin,box.YMax) for z in (box.ZMin,box.ZMax)]
        record['box'] = [round(fn(getattr(p,a) for p in pts),3)
                         for fn in (min,max) for a in ('x','y','z')]
    payload.update(cad_path=release['cadPath'],cad_sha256=before,
                   method='Seleção histórica R02; 24 alvos conferidos no CAD vigente. Envelopes atualizados explicitamente: '+', '.join(ids_atualizar)+'. Demais envelopes históricos preservados; arquitetura R55 não reexportada.')
    payload = complementar(payload)
    # As fórmulas dimensionais só são preservadas se seus 24 alvos continuarem iguais.
    rules_path = ROOT/'04_Moveis/Dependencias/regras.json'
    rules = json.loads(rules_path.read_text(encoding='utf-8'))
    objects = {o['id']:o for o in payload['objects']}
    for name,target in rules['alvos'].items():
        actual = payload['modules'][name] if target['tipo']=='modulo' else objects[name]
        if actual['box'] != target['box']:
            raise ValueError('Alvo dimensional mudou; revisar fórmulas: '+name)
    for record in payload['objects']:
        if record['id'] not in ids_atualizar:
            record['box'] = anteriores[record['id']]
    payload = complementar(payload)
    rules['cad_sha256'] = before
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rules_path.write_text(json.dumps(rules,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def exportar_documento_gui(doc, destino, oficial=False):
    """Candidato externo: seleção do site relida no CAD + corte arquitetônico real.

    Não salva/recalcula o documento nem atualiza release, regras ou base.
    """
    import FreeCAD as App
    path = Path(doc.FileName).resolve()
    destino = Path(destino).resolve()
    if destino.is_relative_to(ROOT) and not oficial:
        raise ValueError('Conferência deve ficar fora do repositório')
    raw = (ROOT/'ferramentas/site/src/cad-data.js').read_text(encoding='utf-8')
    data = json.loads(raw[raw.index('{'):raw.rindex('}')+1])
    records = []
    historical=json.loads((ROOT/'06_Entregas/Caderno_pranchas/Geometria.json').read_text(encoding='utf-8'))
    selected={p['id']:p for p in historical['objects']}
    selected.update({p['source']:p for p in data['parts']})
    for obj in doc.Objects:
        if obj.Name.startswith('PE11X_') and hasattr(obj,'Shape'):
            selected[obj.Name] = dict(room='cozinha',module=None)
    for name, record in selected.items():
        obj = doc.getObject(name)
        if obj is None or not hasattr(obj,'Shape') or obj.Shape.isNull() or not obj.Visibility:
            continue
        parent = obj.getParentGeoFeatureGroup()
        if parent and not parent.Visibility:
            continue
        shape = obj.Shape.copy()
        if parent:shape.Placement = parent.getGlobalPlacement().multiply(shape.Placement)
        b = shape.BoundBox
        records.append(dict(id=name,label=obj.Label,room=record['room'],module=record.get('module'),
                            box=[round(v,3) for v in (b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax)]))
    for prefix,group,room in [('IB6S_','IB6S_Visual','cozinha'),('LGVC4_','LGVC4_Visual','lavanderia'),('ME23P_','ME23P_Visual','cozinha'),('PE12G_','PE12G_Visual','cozinha')]:
        members=[r for r in records if r['id'].startswith(prefix)]
        if not members:raise ValueError('Aparelho sem geometria: '+group)
        bounds=[fn(r['box'][i] for r in members) for fn,indices in [(min,range(3)),(max,range(3,6))] for i in indices]
        records.append(dict(id=group,label=doc.getObject(group).Label,room=room,module=None,box=bounds,aggregate=True))
    wall = doc.getObject('VaosCorte_PI')
    if wall is None:raise ValueError('Parede arquitetônica vigente ausente')
    wires = [[[round(p.x,3),round(p.y,3)] for p in wire.discretize(Deflection=0.5)]
             for wire in wall.Shape.slice(App.Vector(0,0,1),1000)]
    if not wires:raise ValueError('Corte arquitetônico vazio')
    payload = complementar(dict(schema=2,units='mm',cad_path=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path),
        cad_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        method='Seleção ativa do visualizador relida no candidato GUI; paredes em corte Z1000 mm',
        objects=records,architecture=dict(source=wall.Name,height=1000,wires=wires)))
    payload['openings']={}
    for i,name,axis in [(1,'Batente_Escritorio_Compatibilizado','x'),(2,'Batente_Quarto','y'),(3,'Batente_Banheiro_Compatibilizado','x'),(4,'Batente_Entrada','y')]:
        obj=doc.getObject(name);b=obj.Shape.BoundBox
        lo=[b.XMin,b.YMin];hi=[b.XMax,b.YMax];k=0 if axis=='x' else 1
        lo[k]+=20;hi[k]-=20
        payload['openings']['porta-'+str(i)]=dict(source=name,values=[7400-hi[0],lo[1],hi[0]-lo[0],hi[1]-lo[1],0,2100])
    destino.parent.mkdir(parents=True,exist_ok=True)
    destino.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return dict(objects=len(records),wires=len(wires),sha=payload['cad_sha256'])


if os.environ.get('GP_PRANCHAS_FREECAD') == '1':
    exportar()
elif __name__ == '__main__':
    previous_mtime = OUT.stat().st_mtime_ns if OUT.exists() else None
    binary = Path(os.environ['LOCALAPPDATA']) / 'Programs/FreeCAD-1.1.4/bin/freecadcmd.exe'
    if not binary.exists():
        binary = Path.home() / 'AppData/Local/Programs/FreeCAD-1.1.4/bin/freecadcmd.exe'
    subprocess.run([str(binary), str(Path(__file__).resolve())],
                   env=dict(os.environ, GP_PRANCHAS_FREECAD='1', PYTHONDONTWRITEBYTECODE='1'), check=True)
    if not OUT.exists() or OUT.stat().st_mtime_ns == previous_mtime:
        raise SystemExit('FreeCAD não produziu a exportação')

