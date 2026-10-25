"""Confere os documentos vigentes contra os fatos do projeto em ferramentas/fatos.json.

python ferramentas/verificar_fatos.py             # tudo (CI)
python ferramentas/verificar_fatos.py --staged    # proibicoes so nos arquivos do commit (hook)

Cada fato pode ter:
  exigir:  o arquivo precisa conter o texto (regex); evita o fato sumir ou ser trocado por outro valor
  proibir: nos arquivos do escopo, nenhuma linha pode casar a regex (valor contraditorio);
           linhas que falam de historico/substituicao (ver IGNORAR) nao contam
  release: campo de ferramentas/site/current_release.json cujo valor tem de aparecer nos arquivos listados
So os documentos VIGENTES entram no escopo; Registro_de_decisoes e fontes brutas ficam de fora.
Para mudar um fato (ex.: verba) so com decisao de Elias: edite fatos.json e os documentos no mesmo commit.
"""
import fnmatch, json, re, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FATOS = RAIZ / 'ferramentas/fatos.json'
RELEASE = RAIZ / 'ferramentas/site/current_release.json'
IGNORAR = re.compile(r'(?i)hist[oó]ric|anterior|antig[oa]|supera|substitu|deixa de|n[aã]o vale|referência superada|cenário|alternativa|candidat|comparaç|descart|cancelad|rejeitad|retirad|em vez de|ao invés|não (?:é|era|foi)|\bera\b|\bvenax\b.*(?:superad|histór)')


def git(*a):
    return subprocess.run(['git', '-c', 'core.quotepath=off', *a], cwd=RAIZ, capture_output=True,
                          text=True, encoding='utf-8').stdout.splitlines()


def arquivos_do_escopo(globs, staged):
    todos = git('diff', '--cached', '--name-only', '--diff-filter=AM') if staged else git('ls-files', '-co', '--exclude-standard')
    return sorted(f for f in todos if f.endswith('.md') and any(fnmatch.fnmatch(f, g) for g in globs))


def main():
    staged = '--staged' in sys.argv
    dados = json.loads(FATOS.read_text(encoding='utf-8'))
    release = json.loads(RELEASE.read_text(encoding='utf-8'))
    erros = []
    for fato in dados['fatos']:
        fid = fato['id']
        for ex in fato.get('exigir', []):
            p = RAIZ / ex['arquivo']
            texto = p.read_text(encoding='utf-8', errors='ignore') if p.exists() else ''
            if not re.search(ex['regex'], texto):
                erros.append('[%s] %s deveria conter %r (%s)' % (fid, ex['arquivo'], ex['regex'], fato['descricao']))
        for pr in fato.get('proibir', []):
            rx = re.compile(pr['regex'])
            for f in arquivos_do_escopo(pr['escopo'], staged):
                for n, linha in enumerate((RAIZ / f).read_text(encoding='utf-8', errors='ignore').splitlines(), 1):
                    if rx.search(linha) and not IGNORAR.search(linha):
                        erros.append('[%s] %s:%d contradiz o fato (%s): %s' % (fid, f, n, fato['descricao'], linha.strip()[:100]))
        rel = fato.get('release')
        if rel:
            valor = str(release[rel['campo']])
            for arq in rel['arquivos']:
                texto = (RAIZ / arq).read_text(encoding='utf-8', errors='ignore') if (RAIZ / arq).exists() else ''
                if valor not in texto:
                    erros.append('[%s] %s nao menciona %s=%s do current_release.json' % (fid, arq, rel['campo'], valor))
    for e in erros:
        print('ERRO:', e)
    print('Fatos: %s (%d fatos)' % ('OK' if not erros else '%d erro(s)' % len(erros), len(dados['fatos'])))
    return 1 if erros else 0


sys.exit(main())
