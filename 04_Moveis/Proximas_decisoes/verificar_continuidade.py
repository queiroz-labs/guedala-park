"""Verifica evidências, preservação, pacote e navegação desta etapa local."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[2]
OUT = WORKSPACE / 'outputs/continuidade-pos-r52-2026-10-25'
REPORT = ROOT / 'Verificacao_continuidade.json'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8'))

def main():
    cad = WORKSPACE / 'guedala-park/02_Modelo_3D/Guedala_Park_R52_Corrigido.FCStd'
    previous = WORKSPACE / 'guedala-park/01_Projeto/Revisao_sem_tubos_R51_2026-10-25/Guedala_Park_R51_Sem_estudo_tubular.FCStd'
    expected = '941da02d367c5f6ce2992f72985f86c3aceba23f899a4c394cf3569f19d7b4da'
    assert sha(cad) == expected
    assert sha(previous) == 'ab5323bb12f8eca40b25bdfe4eadc8a3221c82b0646f354cd1f2832acfb27c16'
    with zipfile.ZipFile(cad) as archive:
        assert archive.testzip() is None
    manifests = []
    unique_backups = set()
    for name in ['manifesto-fabricacao-sha256.json', 'manifesto-originais.json',
                 'manifesto-entradas-principal.json', 'manifesto-reconstrucao-local.json']:
        rows = json.loads((OUT / name).read_text(encoding='utf-8'))
        for row in rows:
            backup = WORKSPACE / row['backup']
            assert sha(backup) == row['sha256'], str(backup)
            unique_backups.add(str(backup.resolve()))
        manifests.append({'file': str((OUT / name).relative_to(WORKSPACE)), 'records': len(rows), 'passed': True})
    protected = json.loads((OUT / 'estado-protegido-antes.json').read_text(encoding='utf-8'))
    for row in protected:
        assert sha(WORKSPACE / row['path']) == row['sha256'], row['path']

    offline = read('Cinematica/Verificacao_offline_R52.json')
    native = read('Cinematica/Verificacao_nativa_R52.json')
    equilibrium = read('P01_P03/Verificacao_caixa.json')
    cutting = read('Corte_e_formatos/Verificacao.json')
    micro = read('Instalacao_e_P16/Micro_estudo.json')
    package = read('Pacote_local/verificacao-pacote.json')
    assert offline['passed'] and native['passed']
    assert offline['source_unchanged'] and native['source_unchanged'] and equilibrium['source_unchanged'] and micro['source_unchanged']
    assert cutting['source_hashes_unchanged'] and cutting['no_overlap_or_kerf_violation'] and cutting['inside_usable_sheets']
    assert len(equilibrium['checks']) == equilibrium['body_equilibrium_cases'] == 12
    assert max(c['max_body_force_residual_N'] for c in equilibrium['checks']) < 1e-7
    assert max(c['max_body_moment_residual_Nmm'] for c in equilibrium['checks']) < 1e-4
    assert not equilibrium['finite_joint_design_envelope']
    assert micro['F104_preserved'] and not micro['adopted'] and not micro['positive_intersections']
    assert sha(Path(micro['study']['file'])) == micro['study']['sha256']
    package_path = WORKSPACE / package['zip']
    assert sha(package_path) == package['sha256']
    assert package_path.stat().st_size == package['bytes']
    with zipfile.ZipFile(package_path) as archive:
        assert archive.testzip() is None
        assert sum(not item.is_dir() for item in archive.infolist()) == package['files']
        cad_entries = [item for item in archive.namelist() if item.endswith('/Guedala_Park_R52_Corrigido.FCStd')]
        assert len(cad_entries) == 1
        assert hashlib.sha256(archive.read(cad_entries[0])).hexdigest() == expected
    assert not package['missingLocalLinks']
    browser = read('Pacote_local/qa-browser-pacote.json')
    web = read('Pacote_local/qa-web-isolada.json')
    assert not browser['network'] and not browser['errors']
    assert all(case['offlineModelAndP20'] for case in browser['cases'])
    assert not web['errors'] and not web['external'] and web['workerGeometryReady'] and web['lazyP20Ready']
    consistency = (WORKSPACE / 'guedala-park/ferramentas/Verificacao_consistencia.md').read_text(encoding='utf-8')
    assert '| ATENÇÃO |' not in consistency
    consistency_checks = consistency.count('| OK |')
    assert consistency_checks == 19

    link_count = 0
    broken = []
    for doc in ROOT.rglob('*.md'):
        for raw in re.findall(r'\[[^\]]*\]\(([^\n]+?)\)', doc.read_text(encoding='utf-8')):
            target = raw.strip().strip('<>')
            parts = urlsplit(target)
            if parts.scheme or target.startswith('#'):
                continue
            local = unquote(parts.path)
            if not local:
                continue
            link_count += 1
            candidate = (doc.parent / local).resolve()
            if candidate != REPORT.resolve() and not candidate.exists():
                broken.append({'document': str(doc.relative_to(ROOT)), 'target': target})
    assert not broken, broken
    evidence = []
    for path in sorted(ROOT.rglob('*')):
        if path.is_file() and path != REPORT:
            evidence.append({'file': str(path.relative_to(ROOT)), 'bytes': path.stat().st_size, 'sha256': sha(path)})
    result = {
        'date': '2026-10-25', 'passed': True,
        'scope': 'Continuidade local sem medidas reais; estudos separados e correções documentais. Não libera fabricação.',
        'cad': {'revision': 'R52', 'sha256': expected, 'unchanged': True, 'crcPassed': True, 'R51Preserved': True},
        'kinematics': {'native_R52_poses': native['poses'], 'reference_poses': offline['reference_poses'],
                       'rotation_matrices': offline['rotation_poses'], 'max_error_mm': native['max_error_mm'], 'passed': True},
        'equilibrium': {'body_cases_verified': 12, 'scenarios': 54, 'finite_joint_capacity_demonstrated': False, 'passed': True},
        'cutting': {'base_panels': cutting['base_panels'], 'separate_proposals': cutting['proposals'],
                    'included_panels': 210, 'excluded_panels': 39, 'nominal_pair_checks': cutting['nominal_pair_checks'],
                    'no_overlap_or_kerf_violation': True, 'purchase_release': False},
        'micro_study': {'sha256': micro['study']['sha256'], 'objects_reopened': micro['reopened_objects'],
                        'upper_gap_mm': micro['proposed_upper_gap_mm'], 'adopted': False, 'F104_preserved': True},
        'package': package,
        'offline_browser_and_isolated_web_passed': True,
        'general_consistency_checks_passed': consistency_checks,
        'continuity_markdown_local_links_checked': link_count, 'broken_links': broken,
        'protected_files_rechecked': len(protected), 'protected_bytes': sum(row['bytes'] for row in protected),
        'backup_manifests': manifests, 'unique_backup_files_verified': len(unique_backups),
        'published': False, 'physical_tests_performed': 0, 'evidence': evidence,
    }
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in ['passed', 'general_consistency_checks_passed',
        'continuity_markdown_local_links_checked', 'broken_links', 'protected_files_rechecked',
        'unique_backup_files_verified']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
