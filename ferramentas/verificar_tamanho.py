"""Limites de tamanho para manter o projeto barato de ler (por IA e por gente).

python ferramentas/verificar_tamanho.py                 # confere
python ferramentas/verificar_tamanho.py --gerar-base    # grava os excessos atuais como teto (so com aprovacao de Elias)
python ferramentas/verificar_tamanho.py --apertar       # baixa o teto dos que encolheram

Regra: arquivo novo precisa caber nos limites. Quem ja passava do limite entra em
ferramentas/limites_base.json com o tamanho atual como teto: pode encolher, nao crescer.
Gerados e dados brutos estao no .ignore, mas os limites valem para eles do mesmo jeito.
"""
import json, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
BASE = RAIZ / 'ferramentas/limites_base.json'
KB = 1024
LIMITES = [  # (descricao, teste de nome, bytes)
    ('README.md', lambda n: n.endswith('README.md'), 16 * KB),
    ('.md', lambda n: n.endswith('.md'), 60 * KB),
    ('.html', lambda n: n.endswith(('.html', '.htm')), 1024 * KB),
    ('texto/dados', lambda n: n.endswith(('.json', '.csv', '.txt', '.js', '.cjs', '.py', '.svg', '.xml')), 3 * 1024 * KB),
    ('qualquer arquivo', lambda n: True, 30 * 1024 * KB),
]
IGNORAR = ('.git/', 'node_modules/')


def arquivos():
    out = subprocess.run(['git', '-c', 'core.quotepath=off', 'ls-files', '-co', '--exclude-standard'],
                         cwd=RAIZ, capture_output=True, text=True, encoding='utf-8').stdout.split('\n')
    return [f for f in out if f and not any(i in f for i in IGNORAR) and (RAIZ / f).is_file()]


def limite_de(nome):
    for desc, teste, b in LIMITES:
        if teste(nome):
            return desc, b


def excessos():
    ex = {}
    for f in arquivos():
        tam = (RAIZ / f).stat().st_size
        desc, lim = limite_de(f)
        # o limite mais restritivo que o arquivo viola
        for d, t, b in LIMITES:
            if t(f) and tam > b:
                ex[f] = (tam, d, b)
                break
    return ex


def main():
    ex = excessos()
    base = json.loads(BASE.read_text(encoding='utf-8')) if BASE.exists() else {}
    if '--gerar-base' in sys.argv:
        BASE.write_text(json.dumps({f: v[0] for f, v in sorted(ex.items())}, indent=0, ensure_ascii=False), encoding='utf-8')
        print('Base gravada: %d arquivos acima do limite, congelados no tamanho atual' % len(ex))
        return 0
    if '--apertar' in sys.argv:
        nova = {f: min(t, base[f]) for f, (t, *_ ) in ex.items() if f in base}
        BASE.write_text(json.dumps(dict(sorted(nova.items())), indent=0, ensure_ascii=False), encoding='utf-8')
        print('Base apertada: %d entradas (de %d)' % (len(nova), len(base)))
        return 0
    erros, avisos = [], []
    for f, (tam, d, lim) in sorted(ex.items()):
        if f not in base:
            erros.append('%s tem %d KB; limite de %s e %d KB. Divida, resuma ou mova o bruto para fora do projeto.' % (f, tam // KB, d, lim // KB))
        elif tam > base[f]:
            erros.append('%s cresceu: %d KB, teto %d KB (ja estava acima do limite de %s; so pode encolher).' % (f, tam // KB, base[f] // KB, d))
        elif tam < base[f] * 0.9:
            avisos.append('%s encolheu para %d KB; rode --apertar para travar o ganho.' % (f, tam // KB))
    sumiram = [f for f in base if f not in ex]
    if sumiram:
        avisos.append('%d arquivos da base ja estao dentro do limite (rode --apertar): %s' % (len(sumiram), ', '.join(sumiram[:5])))
    for a in avisos[:6]:
        print('AVISO:', a)
    for e in erros:
        print('ERRO:', e)
    print('Tamanho: %s' % ('OK' if not erros else '%d erro(s)' % len(erros)))
    return 1 if erros else 0


sys.exit(main())
