from pathlib import Path
import csv
import hashlib
import json
import re
import zipfile

root = (Path(__file__).resolve().parent / '.').resolve()
targets = {
    'CLIP_top_BLUMOTION': ['71B3550', '71B3650', '71B3750', '173H7100', '173H7130'],
    'CLIP_top': ['71T7550', '79T8500', '70T7553.09', '173H7100', '173H7130'],
    'MOVENTO': ['760H4000S', '760H5000S', 'T51.7600', 'T51.7601'],
    'TANDEM': ['560H4000B', '560H5000B', 'T51.1901'],
}
report = {'date_local': '2026-10-13', 'timezone': 'America/Sao_Paulo',
    'source': 'https://e-services.blum.com/',
    'service': 'CAD/CAM > Pacotes > Produto unico (3D) > STEP MEDIUM; todos os produtos individualmente',
    'scope': 'Biblioteca de familias candidatas, nao selecao executiva de ferragens ou compra.',
    'packages': []}
rows = []
references = []
for family, codes in targets.items():
    archive = (Path(__file__).resolve().parent / 'Pacotes').resolve()/(family+'_STEP.zip')
    summary = {'family': family, 'archive': str(archive.relative_to(root)).replace('\\','/'),
        'bytes_zip': archive.stat().st_size, 'sha256_zip': hashlib.file_digest(archive.open('rb'), 'sha256').hexdigest(),
        'references': []}
    with zipfile.ZipFile(archive) as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError('ZIP com CRC invalido: '+bad)
        entries = [i for i in z.infolist() if not i.is_dir() and i.filename.lower().endswith(('.step','.stp'))]
        summary.update({'crc_all_entries_ok': True, 'step_entries': len(entries),
                        'bytes_steps_expanded': sum(i.file_size for i in entries)})
        ids = set()
        for entry in entries:
            clean = Path(entry.filename).name.strip()
            match = re.match(r'(.+)_([0-9]+)\.(?:step|stp)$', clean, re.I)
            code, cadid = match.groups() if match else (clean, '')
            ids.add(cadid)
            data = None
            # Reading and validating the STEP wrapper verifies every downloaded entry.
            with z.open(entry) as stream:
                header = stream.read(256)
            if b'ISO-10303-21;' not in header:
                raise RuntimeError('STEP sem cabecalho ISO: '+entry.filename)
            selected = code in codes
            row = {'familia': family, 'codigo_no_arquivo': code, 'id_cad': cadid,
                'arquivo_no_zip': entry.filename, 'bytes': entry.file_size,
                'crc32': f'{entry.CRC:08x}', 'arquivo_zip': summary['archive'],
                'referencia_extraida': ''}
            if selected:
                data = z.read(entry)
                destination = (Path(__file__).resolve().parent / 'Referencias').resolve()/family/clean
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
                relative = str(destination.relative_to(root)).replace('\\','/')
                row['referencia_extraida'] = relative
                reference = {'family': family, 'code': code, 'cad_id': cadid,
                             'path': relative, 'sha256': hashlib.sha256(data).hexdigest()}
                summary['references'].append(reference)
                references.append(reference)
            rows.append(row)
        summary['distinct_cad_ids'] = len(ids)
    report['packages'].append(summary)
report['total_step_entries'] = len(rows)
report['total_zip_bytes'] = sum(p['bytes_zip'] for p in report['packages'])
report['extracted_reference_entries'] = len(references)
((Path(__file__).resolve().parent / 'Inventario_downloads.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
with ((Path(__file__).resolve().parent / 'Indice_STEP.csv').resolve()).open('w',newline='',encoding='utf-8-sig') as stream:
    writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
    writer.writeheader();writer.writerows(rows)
print(json.dumps({'steps': report['total_step_entries'], 'zip_bytes': report['total_zip_bytes'],
    'reference_entries': len(references), 'crc_all_ok': True,
    'packages': [{'family': p['family'], 'steps': p['step_entries'], 'cad_ids':p['distinct_cad_ids']} for p in report['packages']]},indent=2))
