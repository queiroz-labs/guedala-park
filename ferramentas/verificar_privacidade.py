"""Procura dado pessoal ou segredo em arquivos do projeto (o repositorio e o site sao PUBLICOS).

python ferramentas/verificar_privacidade.py             # arquivos versionados e novos
python ferramentas/verificar_privacidade.py --staged    # so o que esta no commit (usado pelo hook)
python ferramentas/verificar_privacidade.py --gerar-base  # aceita os achados atuais (so com aprovacao de Elias)

ERRO: CPF, numero de cartao valido (Luhn), chave/token, chave privada, arquivo de segredo,
      qualquer arquivo dentro de guedala-pessoal/.
AVISO: e-mail pessoal (gmail, hotmail...) e telefone: pode ser contato publico de loja, confira.
Achados antigos ja revisados ficam em ferramentas/privacidade_base.json (por arquivo e tipo).
"""
import json, re, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
BASE = RAIZ / 'ferramentas/privacidade_base.json'
MAX_BYTES = 8 * 1024 * 1024
SEM_VARREDURA = {'ferramentas/verificar_privacidade.py', 'ferramentas/privacidade_base.json', '02_Modelo_3D/Base_verificacao.json.gz'}
EXT = {'.md', '.html', '.htm', '.json', '.csv', '.txt', '.js', '.cjs', '.py', '.svg', '.xml', '.yml', '.yaml', '.ps1', '.tsv'}
PROIBIDO = re.compile(r'(^|/)(guedala-pessoal/|\.env(\.|$)|id_rsa|.*\.(pem|pfx|p12|key|kdbx)$|.*credentials.*\.json$)', re.I)

CPF = re.compile(r'(?<![\d.])\d{3}\.\d{3}\.\d{3}-\d{2}(?![\d-])')
# cartao: so grupos de 4 digitos separados (ou 16 digitos colados perto de "cartao/cvv"), e passa no Luhn
CARTAO = re.compile(r'(?<![\d.-])\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{1,7}(?![\d.-])|(?i:cart[aã]o|card|cvv)[^\n]{0,40}?(?<!\d)(\d{16})(?!\d)')
CHAVE = re.compile(r'(?<![A-Za-z0-9+/_-])(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{24,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|xox[baprs]-[A-Za-z0-9-]{20,})(?![A-Za-z0-9+/=_-])')
PRIVADA = re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----')
SENHA = re.compile(r'(?i)\b(senha|password|passwd)\b\s*[:=]\s*["\']?(?!R\$)[^\s"\'<>|,;]{6,}')
EMAIL_PESSOAL = re.compile(r'[\w.+-]+@(?:gmail|hotmail|outlook|live|yahoo|icloud|proton(?:mail)?|bol|uol|terra)\.[\w.]+', re.I)
# telefone: so formatado ((11) 98888-7777, 11 98888-7777, +55 ...); numero solto e timestamp/codigo
TELEFONE = re.compile(r'(?<![\d.])(?:\+55\s?)?(?:\(\d{2}\)\s?|\b\d{2}\s)9?\d{4}-\d{4}(?![\d])')


def luhn(num):
    d = [int(c) for c in num][::-1]
    return (sum(d[0::2]) + sum(sum(divmod(2 * x, 10)) for x in d[1::2])) % 10 == 0


def git(*a):
    return subprocess.run(['git', '-c', 'core.quotepath=off', *a], cwd=RAIZ, capture_output=True,
                          text=True, encoding='utf-8').stdout.split('\n')


def lista(staged):
    if staged:
        return [f for f in git('diff', '--cached', '--name-only', '--diff-filter=AM') if f]
    return [f for f in git('ls-files', '-co', '--exclude-standard') if f]


def achados_do_texto(t):
    ach = {}
    for m in CPF.finditer(t):
        ach.setdefault('cpf', []).append(m.group(0))
    for m in CARTAO.finditer(t):
        n = re.sub(r'\D', '', m.group(0) if m.group(1) is None else m.group(1))
        if 13 <= len(n) <= 19 and luhn(n) and len(set(n)) > 3:
            ach.setdefault('cartao', []).append(n[:4] + '...' + n[-4:])
    for rx, nome in ((CHAVE, 'chave'), (PRIVADA, 'chave_privada'), (SENHA, 'senha')):
        for m in rx.finditer(t):
            ach.setdefault(nome, []).append(m.group(0)[:30])
    for m in EMAIL_PESSOAL.finditer(t):
        ach.setdefault('email_pessoal', []).append(m.group(0))
    for m in TELEFONE.finditer(t):
        ach.setdefault('telefone', []).append(m.group(0))
    return ach


def varrer(staged):
    res = {}
    for f in lista(staged):
        p = RAIZ / f
        if f in SEM_VARREDURA:
            continue
        if PROIBIDO.search(f):
            res.setdefault(f, {})['arquivo_proibido'] = [f]
            continue
        if p.suffix.lower() not in EXT or not p.is_file() or p.stat().st_size > MAX_BYTES:
            continue
        try:
            t = p.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            continue
        a = achados_do_texto(t)
        if a:
            res[f] = a
    return res


GRAVES = {'cpf', 'cartao', 'chave', 'chave_privada', 'senha', 'arquivo_proibido'}


def main():
    staged = '--staged' in sys.argv
    res = varrer(staged)
    if '--gerar-base' in sys.argv:
        base = {f: sorted(a) for f, a in res.items()}
        BASE.write_text(json.dumps(base, indent=0, ensure_ascii=False, sort_keys=True), encoding='utf-8')
        print('Base gravada: %d arquivos com achados aceitos' % len(base))
        return 0
    base = json.loads(BASE.read_text(encoding='utf-8')) if BASE.exists() else {}
    erros, avisos = [], []
    for f, a in sorted(res.items()):
        for tipo, itens in a.items():
            if tipo in base.get(f, []):
                continue
            msg = '%s: %s (%d), ex.: %s' % (f, tipo, len(itens), itens[0])
            (erros if tipo in GRAVES else avisos).append(msg)
    for a in avisos[:15]:
        print('AVISO:', a)
    if len(avisos) > 15:
        print('AVISO: ... e mais %d avisos' % (len(avisos) - 15))
    for e in erros:
        print('ERRO:', e)
    print('Privacidade: %s' % ('OK' if not erros else '%d erro(s)' % len(erros)))
    return 1 if erros else 0


sys.exit(main())
