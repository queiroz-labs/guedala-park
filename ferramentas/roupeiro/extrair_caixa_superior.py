"""Ler R52 sem recomputar/salvar; individualizar P02 e encontros da caixa superior.

Executar com FreeCADCmd. Saidas sao estudos; nenhuma furacao ou CAD e alterado.
"""
from pathlib import Path
import hashlib
import itertools
import json
import FreeCAD as App
import Part

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '04_Moveis/Proximas_decisoes/P01_P03'
RELEASE = json.loads((ROOT / 'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
SOURCE = ROOT / RELEASE['cadPath']
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
before = sha(SOURCE)
assert before == RELEASE['cadSHA256']

P01 = ['Peca206', 'Peca207', 'Peca208', 'Peca209', 'Peca210',
       'ReferenciaCorrerR14', 'ReferenciaCorrerR001', 'ReferenciaCorrerR002', 'ReferenciaCorrerR003']
P03 = ['Peca259', 'Peca260', 'Peca261', 'Peca262', 'Peca263']
P02 = ['PlacaL', 'PlacaL001', 'Peca255', 'Peca256', 'LateralApoioPrincipal',
       'ApoioPortaBR04', 'FaixaQuinaAR04', 'FaixaQuinaBR04']
DOORS = ['Peca264', 'Peca265', 'FrenteSimplesR04', 'FrenteSimplesR001']
doc = App.openDocument(str(SOURCE))


def world(obj):
    s = obj.Shape.copy()
    s.Placement = obj.getGlobalPlacement().multiply(obj.Placement.inverse()).multiply(s.Placement)
    return s


def bounds(s):
    b = s.BoundBox
    return [b.XMin, b.YMin, b.ZMin, b.XMax, b.YMax, b.ZMax]


def point(v):
    return [v.x, v.y, v.z]


def record(s):
    vol = sum(t.Volume for t in s.Solids)
    cg = sum((t.CenterOfMass * t.Volume for t in s.Solids), App.Vector()) / vol
    return dict(volume_mm3=vol, com_mm=point(cg), bbox_mm=bounds(s), valid=s.isValid())


def face_record(f):
    return dict(area_mm2=f.Area, center_mm=point(f.CenterOfMass), bbox_mm=bounds(f),
                vertices_mm=[point(v.Point) for v in f.Vertexes],
                edges_mm=[[point(v.Point) for v in e.Vertexes] for e in f.Edges])


shapes = {n: world(doc.getObject(n)) for n in P01 + P03 + P02 + DOORS}
metadata = {n: dict(name=n, label=doc.getObject(n).Label,
                   module='P01' if n in P01 else 'P03' if n in P03 + DOORS[:2] else 'P02',
                   door=n in DOORS, **record(s)) for n, s in shapes.items()}
assert all(r['valid'] for r in metadata.values())
legacy = json.loads((ROOT / '04_Moveis/P01/Massas_equilibrio/Geometria_R51.json').read_text(encoding='utf-8'))
old = {r['name']: r for rows in legacy['wood'].values() for r in rows}
for n, r in metadata.items():
    a = old[n]
    assert abs(r['volume_mm3'] - a['volume_mm3']) < .02, n
    assert max(abs(x - y) for x, y in zip(r['com_mm'], a['com_global_mm'])) < 1e-6, n
    assert max(abs(x - y) for x, y in zip(r['bbox_mm'], a['bbox_global_mm'])) < 1e-6, n

variants = {}
for label, extend in [('atual_R52', False), ('traseiro_ESTUDO', True), ('caixa_fechada_ESTUDO', True)]:
    ss = {n: s.copy() for n, s in shapes.items() if n not in DOORS}
    if extend:
        ss['Peca208'] = Part.makeBox(1964, 18, 2114, App.Vector(5408, 3922, 18))
        ss['Peca262'] = Part.makeBox(1314, 650, 18, App.Vector(5408, 3290, 2132))
    if label == 'caixa_fechada_ESTUDO':
        # Trocar a chapa inteira do topo: nao e colagem de uma tira18.
        ss['Peca263'] = Part.makeBox(1314, 650, 18, App.Vector(5408, 3290, 2422))
    contacts, lines, overlaps = [], [], []
    for a, b in itertools.combinations(ss, 2):
        ba, bb = bounds(ss[a]), bounds(ss[b])
        if any(min(ba[i+3], bb[i+3]) < max(ba[i], bb[i]) - 1e-6 for i in range(3)):
            continue
        common = ss[a].common(ss[b])
        if common.Volume > .01:
            overlaps.append(dict(a=a, b=b, volume_mm3=common.Volume))
        pair_faces, pair_edges = [], {}
        for fa in ss[a].Faces:
            for fb in ss[b].Faces:
                intersection = fa.common(fb)
                for e in intersection.Edges:
                    vv = sorted(tuple(round(c, 6) for c in point(v.Point)) for v in e.Vertexes)
                    if len(vv) == 2 and e.Length > .01:
                        pair_edges[tuple(vv)] = e.Length
                for f in intersection.Faces:
                    if f.Area > .01:
                        r = face_record(f)
                        flat = [i for i in range(3) if abs(r['bbox_mm'][i+3] - r['bbox_mm'][i]) < 1e-6]
                        assert len(flat) == 1, (a, b, r)
                        pair_faces.append(dict(a=a, b=b, axis=flat[0], **r))
        contacts.extend(pair_faces)
        if not pair_faces:
            # Common de solidos/duas faces pode omitir uma aresta tangente.
            # Reconhecer a mesma aresta reta completa nos dois BREP.
            def straight_edges(s):
                result = {}
                for e in s.Edges:
                    vv = sorted(tuple(round(c, 6) for c in point(v.Point)) for v in e.Vertexes)
                    if len(vv) == 2 and abs(sum((vv[0][i]-vv[1][i])**2 for i in range(3))**.5-e.Length) < 1e-6:
                        result[tuple(vv)] = e.Length
                return result
            ea, eb = straight_edges(ss[a]), straight_edges(ss[b])
            for key in ea.keys() & eb.keys():
                pair_edges[key] = ea[key]
            length = sum(pair_edges.values())
            if length > .01:
                lines.append(dict(a=a, b=b, length_mm=length,
                                  edges_mm=[list(k) for k in pair_edges]))
    variants[label] = dict(bodies={n: dict(metadata[n], **record(s)) for n, s in ss.items()},
                           contacts=contacts, edge_only=lines, positive_intersections=overlaps)

# Corte geometrico na linha mais avancada do apoio P01, y=3290.
# Tambem guarda y=3372, onde comecam as laterais originais (nao e outro apoio independente).
cuts = {}
for y in (3290., 3372.):
    box = Part.makeBox(3000, y-2000, 1000, App.Vector(5000, 2000, 2000))
    rows = []
    for n in P02 + DOORS[2:]:
        s = shapes[n].common(box)
        if s.Volume > .01:
            rows.append(dict(name=n, **record(s)))
    cuts[str(int(y))] = rows

footprints = {}
for n in ['PlacaL', 'PlacaL001']:
    z = metadata[n]['bbox_mm'][2]
    footprints[n] = [face_record(f) for f in shapes[n].Faces
                     if abs(f.BoundBox.ZMin-z) < 1e-6 and abs(f.BoundBox.ZMax-z) < 1e-6]
gaps = []
for a, candidates in [('FaixaQuinaAR04', ['PlacaL', 'PlacaL001', 'LateralApoioPrincipal']),
                       ('FaixaQuinaBR04', ['PlacaL', 'PlacaL001', 'Peca256'])]:
    for b in candidates:
        dist, pairs, info = shapes[a].distToShape(shapes[b])
        gaps.append(dict(a=a, b=b, distance_mm=dist,
                         closest_points_mm=[[point(u), point(v)] for u,v in pairs]))
App.closeDocument(doc.Name)
assert sha(SOURCE) == before
out = dict(source=str(SOURCE.relative_to(ROOT)), source_sha256=before, source_unchanged=True,
           units=dict(length='mm', volume='mm3', area='mm2'), panels=metadata,
           variants=variants, footprints=footprints, P02_front_cut_parts=cuts, trim_gaps=gaps,
           limitations=['Geometria nominal nao e capacidade ou ligacao resistente.',
                        'Portas so entram em massas, nao como contraventamento.',
                        'Proposta traseira nao incorporada a R52.',
                        'Sem recalculo, alteracao ou salvamento do CAD.'])
(OUT / 'Geometria_P02_individual.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(panels=len(metadata), variants={k: dict(contacts=len(v['contacts']),
      edge_only=len(v['edge_only']), overlaps=len(v['positive_intersections'])) for k,v in variants.items()},
      source_unchanged=True)))
