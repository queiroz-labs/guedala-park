"""Roda todas as verificacoes rapidas do projeto. Usado pelo hook de pre-commit e pelo CI (--ci).

python ferramentas/verificar_tudo.py
Sai com 1 se alguma reprovar. A verificacao completa do FreeCAD (minutos) e separada:
python ferramentas/verificar_modelo/verificar_modelo.py --completo
"""
import re, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PY = sys.executable
DATA = re.compile(r'(_\d{4}-\d{2}-\d{2}|_\d{2}_\d{2}_\d{4}|_R\d{2,3})$')
# Pastas historicas que ja existiam com data/revisao no nome (nao crescer esta lista)
LEGADO = ('02_Modelo_3D/Componentes/', '06_Entregas/', 'ferramentas/site/', '04_Moveis/Inventario_dimensional/',
          '04_Moveis/Avanco_pendencias/', '04_Moveis/Proximas_decisoes/', '03_Ambientes/Cozinha/Fechamento/',
          '09_Referencias/', '07_Imovel/', '08_Contratos_e_atraso/')


def git(*a):
    return subprocess.run(['git', '-c', 'core.quotepath=off', *a], cwd=RAIZ, capture_output=True,
                          text=True, encoding='utf-8').stdout.split('\n')


def estrutura():
    erros = []
    # No commit, so o indice (arquivos versionados + staged): trabalho de outra sessao ainda nao commitado nao entra.
    no_commit = '--ci' not in sys.argv and any(git('diff', '--cached', '--name-only'))
    arquivos = [f for f in (git('ls-files') if no_commit else git('ls-files', '-co', '--exclude-standard')) if f]
    pastas = {'/'.join(f.split('/')[:i]) for f in arquivos for i in range(1, f.count('/') + 1)}
    datadas = sorted(p for p in pastas if DATA.search(p.split('/')[-1]) and not p.startswith(LEGADO))
    if datadas:
        erros.append('Pasta com data/revisao no nome (regra 2 do AGENTS.md): ' + ', '.join(datadas[:10]))
    proibidos = sorted(f for f in arquivos if re.search(r'(^|/)(__pycache__|node_modules|\.venv|venv)/|\.pyc$|\.FCBak$', f))
    if proibidos:
        erros.append('Arquivos que nao podem ficar no projeto (regra 5): ' + ', '.join(proibidos[:10]))
    copias = sorted(f for f in arquivos if re.search(r'_(novo|final|v\d|copia|backup|antes)\.[a-z]+$', f, re.I)
                    and not f.startswith(LEGADO))
    if copias:
        erros.append('Copias lado a lado em vez de versao unica (regra 3): ' + ', '.join(copias[:10]))
    sem_readme = sorted(p for p in pastas if p.count('/') == 0 and p[:2].isdigit() and not (RAIZ / p / 'README.md').exists())
    if sem_readme:
        erros.append('Pasta de topo sem README.md: ' + ', '.join(sem_readme))
    return erros


def rodar(rotulo, cmd, linhas_max=12):
    p = subprocess.run([PY, '-B', *cmd], cwd=RAIZ, capture_output=True, text=True, errors='replace')
    linhas = [l for l in p.stdout.splitlines() if l.startswith(('ERRO', 'AVISO', 'LINK'))]
    ultima = p.stdout.splitlines()[-1] if p.stdout.splitlines() else '(sem saida) ' + p.stderr[-300:]
    print('\n'.join(linhas[-linhas_max:] + [ultima]))
    return p.returncode == 0


def main():
    ci = '--ci' in sys.argv
    falhou = False
    for e in estrutura():
        print('ERRO:', e); falhou = True
    print('Estrutura: %s' % ('OK' if not falhou else 'com erro'))
    tem_staged = any(git('diff', '--cached', '--name-only'))
    so_commit = ['--staged'] if (tem_staged and not ci) else []
    passos = [('modelo', ['ferramentas/verificar_modelo/verificar_modelo.py']),
              ('links', ['ferramentas/verificar_links.py'] + so_commit),
              ('tamanho', ['ferramentas/verificar_tamanho.py'] + so_commit),
              ('privacidade', ['ferramentas/verificar_privacidade.py'] + so_commit),
              ('fatos', ['ferramentas/verificar_fatos.py'] + so_commit)]
    if not ci:  # a consistencia usa datas de arquivo, que o checkout limpo do CI nao preserva
        passos.append(('consistencia', ['ferramentas/verificar_consistencia.py']))
        if tem_staged:
            passos.append(('afirmacoes', ['ferramentas/verificar_afirmacoes.py']))
    for rotulo, cmd in passos:
        if not rodar(rotulo, cmd):
            falhou = True
    print('\nRESULTADO: %s' % ('REPROVADO - corrija antes de commitar' if falhou else 'OK'))
    sys.exit(1 if falhou else 0)


main()
