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
    release = json.loads((ROOT / 'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    path = ROOT / release['cadPath']
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    if before != release['cadSHA256']:
        raise ValueError('SHA do modelo diverge do manifesto')
    doc = App.openDocument(str(path), True)
    records = []
    modules = {('Modulo' + (f'{i:03}' if i else '')): f'P{i+1:02}' for i in range(20)}
    parents = {child.Name: p for p in doc.Objects for child in getattr(p, 'Group', [])}
    try:
        for obj in doc.Objects:
            shape = getattr(obj, 'Shape', None)
            if shape is None or shape.isNull() or hasattr(obj, 'Group'):
                continue
            chain, parent = [obj], obj
            while parent.Name in parents:
                parent = parents[parent.Name]
                chain.append(parent)
            rooms = [p.Name.removeprefix('Ambiente_') for p in chain if p.Name.startswith('Ambiente_')]
            bathroom = any(p.Name == 'BanheiroCorrerR43' for p in chain)
            if bathroom:
                rooms = ['banho']
            if not rooms or any(hasattr(p, 'Visibility') and not p.Visibility for p in chain):
                continue
            # Shape inclui Placement próprio; aplica somente a transformação dos pais.
            box = shape.BoundBox
            parent = obj.getParentGeoFeatureGroup()
            matrix = parent.getGlobalPlacement().toMatrix() if parent else App.Matrix()
            pts = [matrix.multVec(App.Vector(x,y,z)) for x in (box.XMin,box.XMax)
                   for y in (box.YMin,box.YMax) for z in (box.ZMin,box.ZMax)]
            bounds = [min(getattr(p,a) for p in pts) for a in ('x','y','z')]
            bounds += [max(getattr(p,a) for p in pts) for a in ('x','y','z')]
            records.append(dict(id=obj.Name, label=obj.Label, room=rooms[0],
                                module='P18' if bathroom else next((modules[p.Name] for p in chain if p.Name in modules), None),
                                box=[round(v,3) for v in bounds]))
        payload = dict(schema=1, units='mm', cad_path=release['cadPath'], cad_sha256=before,
                       method='FreeCAD: envelopes globais de objetos visíveis; sem recálculo/gravação', objects=records)
        OUT.write_text(json.dumps(complementar(payload), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    finally:
        App.closeDocument(doc.Name)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before, 'FCStd alterado'
    print(f'Exportados {len(records)} envelopes; SHA preservado: {before}')


if os.environ.get('GP_PRANCHAS_FREECAD') == '1':
    exportar()
elif __name__ == '__main__':
    binary = Path(os.environ['LOCALAPPDATA']) / 'Programs/FreeCAD-1.1.4/bin/freecadcmd.exe'
    if not binary.exists():
        binary = Path.home() / 'AppData/Local/Programs/FreeCAD-1.1.4/bin/freecadcmd.exe'
    subprocess.run([str(binary), str(Path(__file__).resolve())],
                   env=dict(os.environ, GP_PRANCHAS_FREECAD='1', PYTHONDONTWRITEBYTECODE='1'), check=True)
    if not OUT.exists():
        raise SystemExit('FreeCAD não produziu a exportação')
