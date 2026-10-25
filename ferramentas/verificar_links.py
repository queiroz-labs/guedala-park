"""Lista links locais quebrados nos .md do projeto (fontes brutas e geradas ficam de fora).

python ferramentas/verificar_links.py [--todos]
Sem --todos, so os .md versionados ou novos; sai com 1 se houver link quebrado.
"""
import os, re, subprocess, sys
from pathlib import Path
from urllib.parse import unquote

RAIZ = Path(__file__).resolve().parents[1]
LINK = re.compile(r'\]\(([^)\s]+)\)')
IGNORAR = ('/Fontes/', '/fontes/', '08_Contratos_e_atraso/Pesquisa/', '02_Modelo_3D/Componentes/')


def arquivos():
    # --staged: so os .md do commit (trabalho de outra sessao ainda nao commitado nao entra)
    cmd = (['diff', '--cached', '--name-only', '--diff-filter=AM', '--', '*.md'] if '--staged' in sys.argv
           else ['ls-files', '-co', '--exclude-standard', '*.md'])
    out = subprocess.run(['git', '-c', 'core.quotepath=off', *cmd],
                         cwd=RAIZ, capture_output=True, text=True, encoding='utf-8').stdout.split('\n')
    return [f for f in out if f and not any(i in '/' + f for i in IGNORAR)]


def ignorado_pelo_git(alvo):
    """Arquivos locais ignorados pelo git (zips, videos) existem so no PC; link para eles e intencional."""
    try:
        rel = str(alvo.relative_to(RAIZ)).replace(os.sep, '/')
    except ValueError:
        return False
    return subprocess.run(['git', 'check-ignore', '-q', rel], cwd=RAIZ).returncode == 0


def quebrados():
    achados = []
    for f in arquivos():
        p = RAIZ / f
        if not p.exists():
            continue
        texto = p.read_text(encoding='utf-8', errors='ignore')
        for m in LINK.finditer(texto):
            u = m.group(1).split('#')[0].split('?')[0]
            if not u or re.match(r'^[a-z]+:', u) or u.startswith(('/', '{', '$')):
                continue
            alvo = (p.parent / unquote(u)).resolve()
            if not alvo.exists() and not (str(alvo).endswith('.md.html') and Path(str(alvo)[:-5]).exists()) and not ignorado_pelo_git(alvo):
                linha = texto.count('\n', 0, m.start()) + 1
                achados.append('%s:%d -> %s' % (f, linha, m.group(1)))
    return achados


if __name__ == '__main__':
    q = quebrados()
    for x in q:
        print('LINK QUEBRADO:', x)
    print('Links: %s' % ('OK' if not q else '%d quebrado(s)' % len(q)))
    sys.exit(1 if q else 0)
