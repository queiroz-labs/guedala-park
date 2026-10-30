"""Repete localmente os testes e o build do site que o CI roda antes de publicar.

python ferramentas/verificar_site.py

Usado pelo hook de pre-push: assim uma falha aparece antes de publicar, nao depois.
Gera tudo numa pasta temporaria; nao altera arquivos versionados.
Se o Node nao estiver instalado, avisa e nao reprova (o CI continua cobrindo).
"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SITE = RAIZ / 'ferramentas/site'
PY = sys.executable
NODE = shutil.which('node')

TESTES_NODE = ['test_orientation.cjs', 'test_scene_revision.cjs', 'test_lighting.cjs',
               'test_part_groups_ui.cjs', 'test_storage.cjs', 'test_document_library.cjs',
               'test_navigation.cjs', 'test_field.cjs', 'test_field_datum.cjs', 'test_field_guides.cjs', 'test_work.cjs']


def passo(nome, cmd, env=None):
    p = subprocess.run(cmd, cwd=RAIZ, capture_output=True, text=True, errors='replace', env=env)
    ok = p.returncode == 0
    print('%s %s' % ('OK  ' if ok else 'ERRO', nome))
    if not ok:
        print('\n'.join((p.stdout + p.stderr).strip().splitlines()[-12:]))
    return ok


def git(*a):
    return subprocess.run(['git', '-c', 'core.quotepath=off', *a], cwd=RAIZ, capture_output=True,
                          text=True, encoding='utf-8').stdout


def pacote_local_ignorado():
    """Artefatos do pacote selado que o git ignora: o CI nunca os tem, entao saem do caminho durante o teste."""
    pasta = RAIZ / '06_Entregas/Publicacao'
    if not pasta.exists():
        return []
    return [f for f in pasta.iterdir() if f.is_file() and git('check-ignore', str(f.relative_to(RAIZ))).strip()]


def main():
    if not NODE or not (SITE / 'node_modules').exists():
        print('AVISO: Node ou ferramentas/site/node_modules ausentes; testes do site pulados (o CI roda).')
        return 0
    ok = True
    for t in TESTES_NODE:
        ok &= passo(t, [NODE, str(SITE / t)])
    ok &= passo('test_part_groups.py', [PY, '-B', str(SITE / 'test_part_groups.py')])
    ok &= passo('test_document_library.py', [PY, '-B', str(SITE / 'test_document_library.py')])
    ok &= passo('test_work_data.py', [PY, '-B', str(SITE / 'test_work_data.py')])
    ok &= passo('test_importar_medidas_site.py', [PY, '-B', str(RAIZ / 'ferramentas/estudos/test_importar_medidas_site.py')])
    tmp = Path(tempfile.mkdtemp(prefix='gp_site_'))
    antes = git('status', '--porcelain')
    guardados = []
    for f in pacote_local_ignorado():
        destino = tmp / 'pacote_local' / f.name
        destino.parent.mkdir(exist_ok=True)
        shutil.move(str(f), str(destino))
        guardados.append((destino, f))
    try:
        env = dict(os.environ, GUEDALA_TEST_ROOT=str(tmp / 'testes'))
        cmd = [PY, '-B', str(SITE / 'preparar_pages.py'), '--output-dir', str(tmp / 'site'),
               '--package-mode', 'auto']
        # Validar artefato local nao concede autorizacao de publicacao.
        import json
        release=json.loads((SITE/'current_release.json').read_text(encoding='utf-8'))
        if release['publicationStatus'] in ('publication_authorized','published'):
            cmd.append('--publication-ready')
        else:
            print('INFO: verificando pacote local; publicacao continua bloqueada')
        if not passo('preparar_pages (build do site e pacote)', cmd, env):
            for f in (RAIZ / '06_Entregas/Publicacao').glob('*'):  # tentativa limpa (gravacao concorrente no Windows)
                if f.is_file() and git('check-ignore', str(f.relative_to(RAIZ))).strip():
                    f.unlink()
            ok &= passo('preparar_pages, segunda tentativa', cmd, env)
        ok &= passo('test_current_release.py (selagem do pacote)', [PY, '-B', str(SITE / 'test_current_release.py')], env)
    finally:
        for f in pacote_local_ignorado():  # o pacote gerado agora sai; o guardado volta
            f.unlink()
        for origem, destino in guardados:
            shutil.move(str(origem), str(destino))
        shutil.rmtree(tmp, ignore_errors=True)
    depois = git('status', '--porcelain')
    if depois != antes:
        novos = sorted(set(depois.splitlines()) - set(antes.splitlines()))
        print('AVISO: o build alterou %d arquivos versionados (gerados). Confira com git status antes de commitar: %s' % (
            len(novos), ', '.join(n.strip() for n in novos[:5])))
    print('Site: %s' % ('OK' if ok else 'REPROVADO'))
    return 0 if ok else 1


sys.exit(main())
