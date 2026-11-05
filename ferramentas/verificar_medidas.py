"""Portao de medidas: barra script de calculo novo sem fonte de medida declarada (IA tende a inventar numero).

python ferramentas/verificar_medidas.py                 # arquivos adicionados no commit (staged)
python ferramentas/verificar_medidas.py --desde REF     # arquivos adicionados desde REF (CI)

Todo .py NOVO (fora de ferramentas/site, verificar_* e test_*) precisa, nas primeiras 15 linhas, de
    # MEDIDAS: <fonte>
com uma destas fontes:
  oficial  -> planta/memorial em 09_Referencias (cite o arquivo)
  fatos    -> ferramentas/fatos.json
  manual   -> manual ou catalogo de fabricante (cite)
  campo    -> medida real registrada em 07_Imovel (depois das chaves)
  Elias dd/mm[/aaaa] -> valor dado por Elias no chat, com data
  nao se aplica - <motivo com pelo menos 15 caracteres>  (ex.: so le dados existentes)
"hipotese", "assumido" ou "nominal" sem fonte de Elias com data reprova: sem medida, nao se calcula.
So olha arquivos NOVOS; scripts antigos nao sao julgados.

Em .md novo, linhas com simulacao/cenarios/sensibilidade/varredura sem fonte geram AVISO (nao bloqueia).
"""
import re, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

FONTE = re.compile(
    r'(?i)\b(oficial|fatos(?:\.json)?|manual|cat[aá]logo|campo)\b'
    r'|\belias\b[^\n]{0,20}\d{1,2}/\d{1,2}(?:/\d{2,4})?'
    r'|\bn[aã]o se aplica\b\s*[-–—:]\s*\S[^\n]{14,}')
HIPOTESE = re.compile(r'(?i)\b(hip[oó]tese|assumid[oa]s?|nominal|supost[oa]s?|estimad[oa]s?)\b')
ELIAS_DATA = re.compile(r'(?i)\belias\b[^\n]{0,20}\d{1,2}/\d{1,2}(?:/\d{2,4})?')
ESTUDO_MD = re.compile(r'(?i)\b(simula[cç][aã]o|simulac[oõ]es|cen[aá]rios?|sensibilidades?|monte carlo|varredura|otimiza[cç][aã]o)\b')
FONTE_MD = re.compile(r'(?i)\belias\b[^\n]{0,40}\d{1,2}/\d{1,2}|\boficial\b|\bmanual\b|\bcat[aá]logo\b|\bfatos\b|\bremovid[oa]\b|\bn[aã]o h[aá]\b|\bsem\b')


def git(*a):
    return subprocess.run(['git', '-c', 'core.quotepath=off', *a], cwd=RAIZ, capture_output=True,
                          text=True, encoding='utf-8').stdout


def escopo(caminho):
    p = Path(caminho)
    return (p.suffix == '.py' and not caminho.startswith('ferramentas/site/')
            and not p.name.startswith(('verificar_', 'test_')))


def cabecalho(texto):
    """Devolve a linha 'MEDIDAS:' das 15 primeiras linhas, ou None."""
    for linha in texto.splitlines()[:15]:
        m = re.search(r'MEDIDAS:\s*(.*)', linha)
        if m:
            return m.group(1).strip()
    return None


def julgar(caminho, texto):
    """Lista de erros de um script novo."""
    declarado = cabecalho(texto)
    if declarado is None:
        return [f'{caminho}: falta "# MEDIDAS: <fonte>" nas primeiras 15 linhas (veja ferramentas/verificar_medidas.py)']
    if not FONTE.search(declarado):
        return [f'{caminho}: MEDIDAS "{declarado[:60]}" nao cita fonte (oficial, fatos, manual, campo, Elias dd/mm ou nao se aplica - motivo)']
    if HIPOTESE.search(declarado) and not ELIAS_DATA.search(declarado):
        return [f'{caminho}: MEDIDAS usa hipotese/nominal sem fonte de Elias com data: sem medida, nao se calcula']
    return []


def adicionados(base):
    cmd = ['diff', '--name-only', '--diff-filter=A', base, 'HEAD'] if base else ['diff', '--cached', '--name-only', '--diff-filter=A']
    return [f for f in git(*cmd).split('\n') if f]


def conteudo(caminho, base):
    if base:
        return git('show', f'HEAD:{caminho}')
    p = RAIZ / caminho
    return p.read_text(encoding='utf-8', errors='replace') if p.exists() else ''


def avisos_md(base):
    cmd = ['diff', '-U0', '--no-color', '--diff-filter=AM']
    cmd += [base, 'HEAD'] if base else ['--cached']
    atual, saida = None, []
    for linha in git(*cmd, '--', '*.md').split('\n'):
        if linha.startswith('+++ b/'):
            atual = linha[6:]
        elif linha.startswith('+') and not linha.startswith('+++') and atual:
            if ESTUDO_MD.search(linha) and not FONTE_MD.search(linha):
                saida.append(f'AVISO: {atual}: estudo/cenario sem fonte de medida na linha: {linha[1:80].strip()}')
    return saida


def main():
    base = sys.argv[sys.argv.index('--desde') + 1] if '--desde' in sys.argv else None
    erros = []
    for f in adicionados(base):
        if escopo(f):
            erros += julgar(f, conteudo(f, base))
    for e in erros:
        print('ERRO:', e)
    for a in avisos_md(base)[:10]:
        print(a)
    print('Medidas: %s' % ('OK' if not erros else '%d script(s) novo(s) sem fonte de medida' % len(erros)))
    sys.exit(1 if erros else 0)


if __name__ == '__main__':
    main()
