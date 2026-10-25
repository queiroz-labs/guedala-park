"""Verifica o modelo FreeCAD vigente e acusa erro se algo foi alterado sem querer.

Uso (python comum, na raiz do repo):
  python ferramentas/verificar_modelo/verificar_modelo.py              # rapido, sem abrir o FreeCAD (segundos)
  python ferramentas/verificar_modelo/verificar_modelo.py --completo   # abre no FreeCADCmd (sem salvar) e compara com a base (minutos)
  python ferramentas/verificar_modelo/verificar_modelo.py --completo --relatorio
      alem de verificar, escreve 02_Modelo_3D/Relatorio_mudanca.md (o que mudou, legivel, com aprovacao PENDENTE)
  python ferramentas/verificar_modelo/verificar_modelo.py --completo --atualizar-base --aprovado-por "Elias, 25/10/2026: o que foi aprovado"
      grava a base nova. Se houver diferencas em relacao a base, SO grava com --aprovado-por
      (texto com a data e o que Elias aprovou). Escreve o relatorio com essa aprovacao.

Saida: 0 = ok, 1 = erro. Avisos nao reprovam.
Base: 02_Modelo_3D/Base_verificacao.json. Relatorio: 02_Modelo_3D/Relatorio_mudanca.md.
No commit, se a base mudou, o relatorio aprovado precisa ir junto (o hook confere).
"""
import datetime, hashlib, json, math, os, re, subprocess, sys, tempfile, zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
RELEASE = RAIZ / 'ferramentas/site/current_release.json'
BASE = RAIZ / '02_Modelo_3D/Base_verificacao.json'
RELATORIO = RAIZ / '02_Modelo_3D/Relatorio_mudanca.md'
INSPETOR = Path(__file__).with_name('inspecionar_freecad.py')
FREECADCMD = Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs/FreeCAD-1.1.4/bin/freecadcmd.exe'
LINHA_APROVACAO = '**Aprovação de Elias:**'
MAX_LISTA = 40

erros, avisos = [], []


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for bloco in iter(lambda: f.read(1 << 20), b''):
            h.update(bloco)
    return h.hexdigest()


def git(*a):
    return subprocess.run(['git', '-c', 'core.quotepath=off', *a], cwd=RAIZ, capture_output=True,
                          text=True, encoding='utf-8').stdout


def guarda_do_commit():
    """Se a base entrou no commit, o relatorio aprovado precisa entrar junto."""
    staged = git('diff', '--cached', '--name-only').splitlines()
    rel_base = str(BASE.relative_to(RAIZ)).replace(os.sep, '/')
    rel_relatorio = str(RELATORIO.relative_to(RAIZ)).replace(os.sep, '/')
    if rel_base not in staged:
        return
    if rel_relatorio not in staged:
        erros.append('Base_verificacao.json mudou no commit sem Relatorio_mudanca.md no mesmo commit. '
                     'Gere com --completo --atualizar-base --aprovado-por "Elias, dd/mm/aaaa: ..."')
        return
    texto = git('show', ':' + rel_relatorio)
    linha = next((l for l in texto.splitlines() if l.startswith(LINHA_APROVACAO)), '')
    if not linha or 'PENDENTE' in linha or not re.search(r'\d{1,2}/\d{1,2}', linha):
        erros.append('Relatorio_mudanca.md sem aprovacao de Elias (linha "%s" com data). Nao basta gerar: precisa da decisao dele.' % LINHA_APROVACAO)


def rapido():
    rel = json.loads(RELEASE.read_text(encoding='utf-8'))
    cad = RAIZ / rel['cadPath']
    if not cad.exists():
        erros.append('Modelo vigente nao encontrado: %s (current_release.json -> cadPath)' % rel['cadPath'])
        return rel, cad
    # um so modelo vigente na pasta do modelo
    extras = [p.name for p in (RAIZ / '02_Modelo_3D').glob('*.FCStd') if p != cad]
    if extras:
        erros.append('Mais de um .FCStd em 02_Modelo_3D (so o vigente pode ficar): %s' % ', '.join(extras))
    lixo = [str(p.relative_to(RAIZ)) for pat in ('*.FCBak', '*.FCStd1', '*.FCStd.*') for p in RAIZ.rglob(pat)
            if '.git' not in p.parts and 'node_modules' not in p.parts]
    if lixo:
        erros.append('Backups/temporarios do FreeCAD na pasta do projeto: %s' % ', '.join(lixo[:10]))
    try:
        with zipfile.ZipFile(cad) as z:
            nomes = set(z.namelist())
            if z.testzip() is not None:
                erros.append('Arquivo .FCStd corrompido (CRC do ZIP falhou)')
            if 'Document.xml' not in nomes:
                erros.append('Document.xml ausente no .FCStd')
            if 'GuiDocument.xml' not in nomes:
                erros.append('GuiDocument.xml ausente: cores e visibilidade foram perdidas (salvo pelo FreeCADCmd?)')
    except zipfile.BadZipFile:
        erros.append('Modelo vigente nao e um .FCStd valido')
        return rel, cad
    atual = sha(cad)
    if atual != rel['cadSHA256']:
        erros.append('O modelo mudou e o current_release.json nao foi atualizado (SHA %s... esperado %s...). '
                     'Se a mudanca foi aprovada, rode --completo --atualizar-base --aprovado-por "..." e atualize o release.' % (atual[:12], rel['cadSHA256'][:12]))
    if BASE.exists():
        base = json.loads(BASE.read_text(encoding='utf-8'))
        if base.get('sha256') != rel['cadSHA256']:
            avisos.append('A base de verificacao e de outro arquivo (%s...); rode --completo --atualizar-base' % base.get('sha256', '')[:12])
    else:
        avisos.append('Sem base de verificacao; rode --completo --atualizar-base')
    guarda_do_commit()
    return rel, cad


def inspecionar(cad, refinar=None):
    if not FREECADCMD.exists():
        erros.append('FreeCADCmd nao encontrado em %s' % FREECADCMD)
        return None
    saida = Path(tempfile.gettempdir()) / 'gp_retrato_modelo.json'
    env = dict(os.environ, GP_MODELO=str(cad), GP_SAIDA=str(saida))
    arq_ref = Path(tempfile.gettempdir()) / 'gp_refinar.json'
    if refinar:
        arq_ref.write_text(json.dumps(refinar), encoding='utf-8')
        env['GP_REFINAR'] = str(arq_ref)
    else:
        env.pop('GP_REFINAR', None)
    antes = sha(cad)
    proc = subprocess.run([str(FREECADCMD), str(INSPETOR)], env=env, capture_output=True, text=True, errors='replace')
    if sha(cad) != antes:
        erros.append('A inspecao alterou o arquivo do modelo; isso nunca deveria acontecer')
    if not saida.exists():
        erros.append('FreeCADCmd nao gerou o retrato: %s' % (proc.stdout + proc.stderr)[-800:])
        return None
    retrato = json.loads(saida.read_text(encoding='utf-8'))
    saida.unlink()
    return retrato


def comparar(base, atual):
    """Compara retratos. Registra erros/avisos e devolve o detalhe das diferencas (para o relatorio)."""
    bo, ao = base['objetos'], atual['objetos']
    dif = {'removidos': sorted(set(bo) - set(ao)), 'novos': sorted(set(ao) - set(bo)),
           'geometria': [], 'posicao': [], 'visibilidade': [], 'expressoes': [], 'suspeitos': [], 'invalidos_novos': []}
    for n in sorted(set(bo) & set(ao)):
        b, a = bo[n], ao[n]
        if b.get('forma') != a.get('forma'):
            dif['geometria'].append((n, b.get('forma'), a.get('forma')))
        if b.get('posicao') != a.get('posicao'):
            dif['posicao'].append((n, b.get('posicao'), a.get('posicao')))
        if b.get('visivel') != a.get('visivel'):
            dif['visibilidade'].append((n, b.get('visivel'), a.get('visivel')))
        if b.get('expressoes') != a.get('expressoes'):
            dif['expressoes'].append((n, len(b.get('expressoes') or []), len(a.get('expressoes') or [])))
    if dif['removidos']:
        erros.append('%d objetos removidos: %s' % (len(dif['removidos']), ', '.join(dif['removidos'][:15])))
    if dif['novos']:
        avisos.append('%d objetos novos: %s' % (len(dif['novos']), ', '.join(dif['novos'][:15])))
    for rotulo, chave in (('geometria alterada', 'geometria'), ('posicao alterada', 'posicao'),
                          ('visibilidade alterada', 'visibilidade'), ('expressoes alteradas', 'expressoes')):
        if dif[chave]:
            avisos.append('%d com %s: %s' % (len(dif[chave]), rotulo, ', '.join(x[0] for x in dif[chave][:15])))
    if atual['total_expressoes'] < base['total_expressoes']:
        erros.append('Expressoes perdidas: %d -> %d' % (base['total_expressoes'], atual['total_expressoes']))
    inval_base = {i['nome'] for i in base['invalidos']}
    dif['invalidos_novos'] = [i for i in atual['invalidos'] if i['nome'] not in inval_base]
    if dif['invalidos_novos']:
        erros.append('%d objetos invalidos novos: %s' % (len(dif['invalidos_novos']), ', '.join('%s %s' % (i['nome'], i['estado']) for i in dif['invalidos_novos'][:15])))
    if 'caixas_sobrepostas' in atual and 'caixas_sobrepostas' in base:
        cb = {(p[0], p[1]): p[2] for p in base['caixas_sobrepostas']}
        ca = {(p[0], p[1]): p[2] for p in atual['caixas_sobrepostas']}
        dif['suspeitos'] = sorted(k for k in ca if k not in cb or ca[k] > cb[k] * 1.05 + 1)
    return dif


def refinar_colisoes(cad, dif):
    """Segunda passada: intersecao exata so dos pares suspeitos. Devolve lista [a, b, mm3] com colisao real."""
    if not dif['suspeitos']:
        return []
    print('Triagem: %d pares de pecas com caixas novas/maiores; conferindo a intersecao exata...' % len(dif['suspeitos']))
    exato = inspecionar(cad, [list(k) for k in dif['suspeitos']])
    batidas = [e for e in (exato or {}).get('colisoes_exatas', []) if e[2] > 0.01]
    if batidas:
        erros.append('%d colisoes novas (pecas se sobrepondo): %s' % (len(batidas), '; '.join('%s x %s (%.1f mm3)' % tuple(e) for e in batidas[:15])))
    else:
        avisos.append('%d pares tiveram caixa maior, mas sem sobreposicao real' % len(dif['suspeitos']))
    return batidas


def tem_diferencas(dif, batidas):
    return any(dif[k] for k in ('removidos', 'novos', 'geometria', 'posicao', 'visibilidade', 'expressoes', 'invalidos_novos')) or bool(batidas)


def fmt_pos(p):
    return '(%s)' % ', '.join('%g' % v for v in p[:3]) if p else '-'


def delta_pos(a, b):
    if not a or not b:
        return float('nan')
    return math.dist(a[:3], b[:3])


def escrever_relatorio(base, atual, dif, batidas, aprovacao, rel):
    agora = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    L = ['# Relatório de mudança do modelo', '',
         'Gerado por `verificar_modelo.py` em %s. Revisão `%s`. SHA256 `%s` → `%s`.' % (
             agora, rel['cadRevision'], (base or {}).get('sha256', '-')[:12], atual['sha256'][:12]), '',
         '%s %s' % (LINHA_APROVACAO, aprovacao or 'PENDENTE: nada daqui vale sem a decisão de Elias'), '']
    if base is None:
        L += ['Base inicial: não havia retrato anterior para comparar.', '']
    L += ['## Resumo', '', '| | Base anterior | Agora |', '|---|---:|---:|']
    for rot, chave in (('Objetos', 'total_objetos'), ('Expressões', 'total_expressoes'), ('Formas ativas', 'formas_ativas')):
        L.append('| %s | %s | %s |' % (rot, (base or {}).get(chave, '-'), atual.get(chave, '-')))
    L.append('| Formas inválidas | %s | %d |' % (len((base or {}).get('invalidos', [])) if base else '-', len(atual['invalidos'])))
    L.append('')
    if dif:
        def secao(titulo, itens, linha):
            if not itens:
                return
            L.append('## %s (%d)' % (titulo, len(itens)))
            L.append('')
            for it in itens[:MAX_LISTA]:
                L.append(linha(it))
            if len(itens) > MAX_LISTA:
                L.append('- … e mais %d' % (len(itens) - MAX_LISTA))
            L.append('')
        secao('Objetos removidos', dif['removidos'], lambda n: '- `%s`' % n)
        secao('Objetos novos', dif['novos'], lambda n: '- `%s` %s' % (n, atual['objetos'][n].get('rotulo', '')))
        secao('Posição alterada', dif['posicao'], lambda x: '- `%s`: %s → %s (Δ %.1f mm)' % (x[0], fmt_pos(x[1]), fmt_pos(x[2]), delta_pos(x[1], x[2])))
        secao('Geometria alterada', dif['geometria'], lambda x: '- `%s`: volume %s → %s mm³' % (
            x[0], (x[1] or {}).get('volume', '-'), (x[2] or {}).get('volume', '-')))
        secao('Visibilidade alterada', dif['visibilidade'], lambda x: '- `%s`: %s → %s' % (x[0], 'visível' if x[1] else 'oculto', 'visível' if x[2] else 'oculto'))
        secao('Expressões alteradas', dif['expressoes'], lambda x: '- `%s`: %d → %d expressões' % x)
        secao('Formas inválidas novas', dif['invalidos_novos'], lambda i: '- `%s` %s' % (i['nome'], i['estado']))
        secao('Colisões novas confirmadas (interseção exata)', batidas, lambda e: '- `%s` × `%s`: %.1f mm³' % tuple(e))
        if not tem_diferencas(dif, batidas):
            L += ['Nenhuma diferença em relação à base anterior.', '']
    L += ['## Como usar', '',
          '1. Leia as seções acima. Conferiu que cada mudança é a que Elias pediu?',
          '2. Só com a aprovação dele: `python ferramentas/verificar_modelo/verificar_modelo.py --completo --atualizar-base --aprovado-por "Elias, dd/mm/aaaa: o que aprovou"`.',
          '3. Commite a base, este relatório, `current_release.json` (SHA) e o `ESTADO_ATUAL.md` juntos.', '']
    RELATORIO.write_text('\n'.join(L), encoding='utf-8')


def valor_arg(nome):
    return sys.argv[sys.argv.index(nome) + 1] if nome in sys.argv and sys.argv.index(nome) + 1 < len(sys.argv) else None


def main():
    completo = '--completo' in sys.argv
    atualizar = '--atualizar-base' in sys.argv
    aprovacao = valor_arg('--aprovado-por')
    rel, cad = rapido()
    if completo and cad.exists():
        retrato = inspecionar(cad)
        if retrato:
            retrato['sha256'] = sha(cad)
            retrato['revisao'] = rel['cadRevision']
            base = json.loads(BASE.read_text(encoding='utf-8')) if BASE.exists() else None
            dif, batidas = None, []
            if base:
                dif = comparar(base, retrato)
                batidas = refinar_colisoes(cad, dif)
            if atualizar:
                erros[:] = [e for e in erros if 'current_release.json nao foi atualizado' not in e]
                mudou = bool(dif) and tem_diferencas(dif, batidas)
                escrever_relatorio(base, retrato, dif, batidas, aprovacao, rel)
                if aprovacao is not None and not re.search(r'\d{1,2}/\d{1,2}', aprovacao):
                    erros.append('--aprovado-por precisa citar a data da aprovacao de Elias (dd/mm) e o que ele aprovou')
                elif mudou and not aprovacao:
                    erros.append('Ha diferencas em relacao a base e nenhuma aprovacao: base NAO gravada. Leia %s, e so com a decisao de Elias rode de novo com --aprovado-por "Elias, dd/mm/aaaa: ..."' % RELATORIO.relative_to(RAIZ))
                else:
                    if retrato['invalidos']:
                        avisos.append('Base gravada com %d objetos invalidos registrados' % len(retrato['invalidos']))
                    retrato['aprovacao'] = aprovacao or ('base inicial' if base is None else 'sem diferencas')
                    BASE.write_text(json.dumps(retrato, ensure_ascii=False, indent=0), encoding='utf-8')
                    print('Base gravada: %s (%d objetos, %d pares de caixas sobrepostas registrados como esperados)' % (
                        BASE.relative_to(RAIZ), retrato['total_objetos'], len(retrato.get('caixas_sobrepostas', []))))
                    print('Relatorio: %s' % RELATORIO.relative_to(RAIZ))
            else:
                if '--relatorio' in sys.argv:
                    escrever_relatorio(base, retrato, dif, batidas, None, rel)
                    print('Relatorio (aprovacao PENDENTE): %s' % RELATORIO.relative_to(RAIZ))
                if base is None:
                    avisos.append('Sem base para comparar')
            print('Inspecao em %.0f s: %d objetos, %d formas ativas, %d pares de caixas sobrepostas' % (
                retrato['segundos'], retrato['total_objetos'], retrato.get('formas_ativas', 0), len(retrato.get('caixas_sobrepostas', []))))
    for a in avisos:
        print('AVISO:', a)
    for e in erros:
        print('ERRO:', e)
    print('Modelo: %s' % ('OK' if not erros else '%d erro(s)' % len(erros)))
    sys.exit(1 if erros else 0)


main()
