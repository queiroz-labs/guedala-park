"""Barra afirmacoes perigosas escritas sem fonte (IA tende a inventar aprovacao do Elias).

python ferramentas/verificar_afirmacoes.py                 # linhas adicionadas no commit (staged)
python ferramentas/verificar_afirmacoes.py --desde REF     # linhas adicionadas desde REF (CI)

So olha linhas NOVAS de arquivos .md; o historico existente nao e julgado.

1) "Elias aprovou/confirmou/escolheu/..." precisa de fonte na MESMA linha:
   uma data (25/10, 25/10/2026), um codigo F123, uma citacao entre aspas, ou link para o Registro de decisoes.
2) Afirmar que algo esta "liberado para fabricacao", "capacidade aprovada", "carga liberada",
   "homologado" ... sem ressalva (nao, sem, pendente, condicionado, ainda, depende...) e erro:
   o projeto ainda nao liberou nada para fabricar.
"""
import re, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

ATRIBUICAO = re.compile(r'(?i)\b(elias|usu[aá]rio)\b[^.\n]{0,25}\b(aprov(?:ou|a|ada|ado)|confirm(?:ou|a)|escolh(?:eu|e)|aceit(?:ou|a)|decidiu|autoriz(?:ou|a)|defini(?:u|ndo)|pediu)\b'
                        r'|\b(aprovad[oa]s?|escolhid[oa]s?|confirmad[oa]s?|autorizad[oa]s?)\s+(?:por|pelo)\s+(?:elias|usu[aá]rio)\b')
FONTE = re.compile(r'\b\d{1,2}/\d{1,2}(/\d{2,4})?\b|\b\d{4}-\d{2}-\d{2}\b|\bF\d{2,3}\b|[“"][^”"\n]{3,}[”"]|Registro_de_decisoes|\bfonte:', re.I)
LIBERACAO = re.compile(r'(?i)\b(liberad[oa]s?\s+para\s+(?:fabric|corte|compra|execu)|fabrica[cç][aã]o\s+liberada|pode\s+(?:fabricar|cortar|comprar)\b|aprovad[oa]s?\s+para\s+(?:fabric|corte|execu)'
                       r'|pronto[as]?\s+para\s+(?:fabricar|cortar|executar)|capacidade\s+(?:aprovada|comprovada|liberada)|carga\s+(?:aprovada|liberada)|homologad[oa]s?)', re.I)
RESSALVA = re.compile(r'(?i)\b(n[aã]o|nada|sem|nenhum[a]?|nunca|ainda|pendente|condicionad[oa]s?|depende[mr]?|exige|exigem|antes\s+de|at[eé]\s+que|para\s+liberar|quando|se\b|enquanto|falta|faltam|nem)\b')


def linhas_novas(base):
    cmd = ['git', '-c', 'core.quotepath=off', 'diff', '-U0', '--no-color', '--diff-filter=AM']
    cmd += [base] if base else ['--cached']
    cmd += ['--', '*.md']
    out = subprocess.run(cmd, cwd=RAIZ, capture_output=True, text=True, encoding='utf-8', errors='ignore').stdout
    arq, n, res = None, 0, []
    for l in out.split('\n'):
        if l.startswith('+++ b/'):
            arq = l[6:]
        elif l.startswith('@@'):
            m = re.search(r'\+(\d+)', l)
            n = int(m.group(1)) - 1 if m else 0
        elif l.startswith('+') and not l.startswith('+++'):
            n += 1
            res.append((arq, n, l[1:]))
    return res


def main():
    base = None
    if '--desde' in sys.argv:
        base = sys.argv[sys.argv.index('--desde') + 1]
    erros = []
    for arq, n, linha in linhas_novas(base):
        if arq in ('AGENTS.md',) or (arq or '').startswith(('02_Modelo_3D/Componentes/', '08_Contratos_e_atraso/Pesquisa/', 'ferramentas/')) or '/Fontes/' in (arq or ''):
            continue
        if ATRIBUICAO.search(linha) and not FONTE.search(linha):
            erros.append('%s:%d atribui decisao a Elias sem fonte (data, F-codigo, aspas ou Registro): %s' % (arq, n, linha.strip()[:110]))
        if LIBERACAO.search(linha) and not RESSALVA.search(linha):
            erros.append('%s:%d afirma liberacao/aprovacao tecnica sem ressalva: %s' % (arq, n, linha.strip()[:110]))
    for e in erros:
        print('ERRO:', e)
    print('Afirmacoes: %s' % ('OK' if not erros else '%d erro(s)' % len(erros)))
    return 1 if erros else 0


sys.exit(main())
