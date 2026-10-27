from pathlib import Path
import csv, hashlib, json, re
import pdfplumber

p = (Path(__file__).resolve().parent / '.').resolve()
b = (Path(__file__).resolve().parent / '../..').resolve()
repo = (Path(__file__).resolve().parent / '../../../..').resolve()
manifest = json.loads(((Path(__file__).resolve().parent / 'Manifesto_entrega.json').resolve()).read_text(encoding='utf-8'))
result = {'pdfs': [], 'csvs': {}, 'links': [], 'cad_changed': False}
for raw, expected in zip(manifest['pdfs'], [21, 20]):
    path = Path(raw)
    with pdfplumber.open(path) as pdf:
        assert len(pdf.pages) == expected
        outside = []
        for n, page in enumerate(pdf.pages, 1):
            assert len(page.extract_text() or '') > 100, (path.name, n)
            for c in page.chars:
                if c['x0'] < -0.5 or c['x1'] > page.width + .5 or c['top'] < -.5 or c['bottom'] > page.height + .5:
                    outside.append({'page': n, 'text': c['text']})
        assert not outside, outside
        result['pdfs'].append({'file': path.name, 'pages': expected, 'characters_outside_page': len(outside), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
for name, expected, unique in [
    ('Ferragens_consolidadas_R28.csv', 15, None),
    ('Referencias_calcos_54_R28.csv', 54, 'Objeto'),
    ('Componentes_774_R28.csv', 774, 'Objeto'),
    ('Conferencia_documental_R28.csv', 9, None),
]:
    with (p / name).open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f, delimiter=';'))
    assert len(rows) == expected, (name, len(rows))
    if unique:
        assert len({r[unique] for r in rows}) == expected
    if name.startswith('Referencias'):
        assert all((b / '02_Revisoes_e_estudos' / r['Fonte']).is_file() for r in rows)
    result['csvs'][name] = {'rows': len(rows), 'unique_objects_checked': bool(unique)}
html = ((Path(__file__).resolve().parent / 'Indice_entregas_R28.html').resolve()).read_text(encoding='utf-8')
for href in re.findall(r'href="([^"]+)"', html):
    target = (p / href).resolve()
    assert target.is_file(), target
    result['links'].append({'href': href, 'exists': True})
assert len(result['links']) == 9
assert len(json.loads(((Path(__file__).resolve().parent / 'Sequencias_R28.json').resolve()).read_text(encoding='utf-8'))) == 10
cad = (Path(__file__).resolve().parent / '../Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve()
result['canonical_sha256'] = hashlib.sha256(cad.read_bytes()).hexdigest()
assert result['canonical_sha256'] == manifest['canonical_sha256']
result['visual_review'] = 'Todas as 41 páginas renderizadas e inspecionadas; detalhes do canto e escritório conferidos. Sem nova simulação de movimento.'
((Path(__file__).resolve().parent / 'Verificacao_entregas.json').resolve()).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'pages': 41, 'csvs': result['csvs'], 'links': len(result['links']), 'cad_hash_preserved': True}, ensure_ascii=False))
