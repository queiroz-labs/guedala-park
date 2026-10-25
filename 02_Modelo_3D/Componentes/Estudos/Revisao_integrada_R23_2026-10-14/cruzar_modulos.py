"""New static cross-module coverage; source CAD is never saved."""
from pathlib import Path
import hashlib, json, time, traceback
import FreeCAD as App

root = (Path(__file__).resolve().parent / '.').resolve()
manifest_path = (Path(__file__).resolve().parent / '../Auditoria_implantacao_R23_2026-10-14/Manifesto_implantacao_R23.json').resolve()
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
source = Path(manifest['file'])
start = time.monotonic()
budget = 180
report = {'file': str(source), 'manifest': str(manifest_path), 'status': 'running',
          'scope': 'Saved-state solid pairs belonging to different roots, at least one of the twenty cabinetry modules',
          'budget_s': budget, 'criterion_mm3': 0.1, 'bbox_epsilon_mm': 1e-6,
          'sha256_before': hashlib.sha256(source.read_bytes()).hexdigest(),
          'stats': {'cross_root_pairs': 0, 'bbox_rejected': 0, 'candidates': 0, 'booleans': 0},
          'contacts': [], 'errors': [], 'completed_pairs': []}
out = (Path(__file__).resolve().parent / 'Encontros_modulos_R23.json').resolve()

def dump():
    report['elapsed_s'] = time.monotonic() - start
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

def check():
    if time.monotonic() - start > budget:
        raise TimeoutError('180s budget exhausted')

def separated(a, b):
    return any(a[i+3] <= b[i]+1e-6 or b[i+3] <= a[i]+1e-6 for i in range(3))

def bounds(b):
    return [b.XMin, b.YMin, b.ZMin, b.XMax, b.YMax, b.ZMax]

def summary(r):
    return {k: r[k] for k in ['name', 'label', 'source_root', 'source_group', 'bbox_source_mm']}

d = None
try:
    assert not App.GuiUp
    assert report['sha256_before'] == manifest['sha256'], 'Manifest/source mismatch'
    modules = {r['source_root'] for r in manifest['items'] if r['source_root'].startswith('Modulo')}
    assert len(modules) == 20
    rows = manifest['items']
    candidates = []
    for i, a in enumerate(rows):
        for b in rows[i+1:]:
            if a['source_root'] == b['source_root'] or not ({a['source_root'], b['source_root']} & modules):
                continue
            report['stats']['cross_root_pairs'] += 1
            if separated(a['bbox_source_mm'], b['bbox_source_mm']):
                report['stats']['bbox_rejected'] += 1
            else:
                candidates.append((a, b))
        check()
    report['stats']['candidates'] = len(candidates)
    report['candidate_manifest'] = [[summary(a), summary(b)] for a, b in candidates]
    dump()
    d = App.openDocument(str(source))
    cache = {}
    def shape(r):
        if r['name'] not in cache:
            o = d.getObject(r['name'])
            assert o is not None
            s = o.Shape.copy()
            s.Placement = o.getGlobalPlacement()
            assert not s.isNull()
            assert max(abs(x-y) for x,y in zip(bounds(s.BoundBox),r['bbox_source_mm'])) < 1e-5, r['name']
            cache[r['name']] = s
        return cache[r['name']]
    for a, b in candidates:
        check()
        report['stats']['booleans'] += 1
        try:
            common = shape(a).common(shape(b))
            if common.Volume > report['criterion_mm3']:
                report['contacts'].append({'one': summary(a), 'two': summary(b),
                    'volume_mm3': common.Volume, 'common_bbox_source_mm': bounds(common.BoundBox),
                    'fraction_one': common.Volume/a['volume_mm3'], 'fraction_two': common.Volume/b['volume_mm3'],
                    'classification': 'requires_context_review_not_automatic_error'})
        except Exception:
            report['errors'].append({'objects': [a['name'], b['name']], 'error': traceback.format_exc()})
        report['completed_pairs'].append([a['name'], b['name']])
        dump()
    report['status'] = 'complete_static_cross_module_scope'
except TimeoutError as e:
    report.update(status='partial_budget_limit', error=str(e))
except Exception:
    report.update(status='failed', error=traceback.format_exc())
finally:
    if d is not None:
        App.closeDocument(d.Name)
    report['sha256_after'] = hashlib.sha256(source.read_bytes()).hexdigest()
    report['source_unchanged'] = report['sha256_after'] == report['sha256_before']
    report['limits'] = 'Static saved state only. No within-module, standalone-standalone, continuous motion, physical dimensions, structure/load/installation certification. Contacts require contextual classification. No CAD save/GUI.'
    dump()
    print('CROSS_MODULE_RESULT', report['status'], report['stats'], len(report['contacts']), len(report['errors']))
