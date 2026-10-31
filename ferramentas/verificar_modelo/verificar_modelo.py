"""Verifica o modelo FreeCAD vigente e acusa erro se algo foi alterado sem querer.

Uso (python comum, na raiz do repo):
  python ferramentas/verificar_modelo/verificar_modelo.py              # rapido, sem abrir o FreeCAD (segundos)
  python ferramentas/verificar_modelo/verificar_modelo.py --completo   # abre no FreeCADCmd (sem salvar) e confere tudo (minutos)
      invariantes (invariantes.json), nada novo fora do apartamento, aparencia por objeto, cenarios de movimento
      (movimentos.json), objetos removidos, formas invalidas, expressoes perdidas, colisoes novas
  ... --completo --relatorio
      alem de verificar, escreve 02_Modelo_3D/Relatorio_mudanca.md (legivel, com aprovacao PENDENTE)
  ... --completo --atualizar-base --aprovado-por "Elias, 25/10/2026: o que foi aprovado"
      grava a base nova. Se houver diferencas em relacao a base, SO grava com --aprovado-por.
  ... --sem-movimentos   pula os cenarios de movimento (mais rapido)
  ... --completo --relatorio --candidato <FCStd externo>
      inspecao somente leitura do candidato; nunca atualiza base/release.

Saida: 0 = ok, 1 = erro. Avisos nao reprovam.
Base: 02_Modelo_3D/Base_verificacao.json.gz. Relatorio: 02_Modelo_3D/Relatorio_mudanca.md.
No commit, se a base mudou, o relatorio aprovado precisa ir junto (o hook confere).
"""
import datetime, gzip, hashlib, json, math, os, re, subprocess, sys, tempfile, zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import aparencia as ap

RAIZ = Path(__file__).resolve().parents[2]
RELEASE = RAIZ / 'ferramentas/site/current_release.json'
BASE = RAIZ / '02_Modelo_3D/Base_verificacao.json.gz'
RELATORIO = RAIZ / '02_Modelo_3D/Relatorio_mudanca.md'
INVARIANTES = Path(__file__).with_name('invariantes.json')
MOVIMENTOS = Path(__file__).with_name('movimentos.json')
INSPETOR = Path(__file__).with_name('inspecionar_freecad.py')
FREECADCMD = Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs/FreeCAD-1.1.4/bin/freecadcmd.exe'
LINHA_APROVACAO = '**Aprovação de Elias:**'
SCHEMA = 2
MAX_LISTA = 40
EIXOS = {'x': (0, 3), 'y': (1, 4), 'z': (2, 5)}

erros, avisos = [], []


def ler_base():
    with gzip.open(BASE, 'rt', encoding='utf-8') as f:
        return json.load(f)


def gravar_base(dados):
    with gzip.open(BASE, 'wt', encoding='utf-8', compresslevel=9) as f:
        json.dump(dados, f, ensure_ascii=False, separators=(',', ':'))


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
        erros.append('Base_verificacao.json.gz mudou no commit sem Relatorio_mudanca.md no mesmo commit. '
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
        base = ler_base()
        if base.get('sha256') != rel['cadSHA256']:
            avisos.append('A base de verificacao e de outro arquivo (%s...); rode --completo --atualizar-base' % base.get('sha256', '')[:12])
    else:
        avisos.append('Sem base de verificacao; rode --completo --atualizar-base')
    guarda_do_commit()
    return rel, cad


def inspecionar(cad, refinar=None, props=None, movimentos=None, colisoes=True):
    if not FREECADCMD.exists():
        erros.append('FreeCADCmd nao encontrado em %s' % FREECADCMD)
        return None
    tmp = Path(tempfile.gettempdir())
    saida = tmp / 'gp_retrato_modelo.json'
    env = dict(os.environ, GP_MODELO=str(cad), GP_SAIDA=str(saida), GP_COLISOES='1' if colisoes else '0')
    for var, nome, dados in (('GP_REFINAR', 'gp_refinar.json', refinar), ('GP_PROPS', 'gp_props.json', props),
                             ('GP_MOVIMENTOS', 'gp_movimentos.json', movimentos)):
        if dados:
            (tmp / nome).write_text(json.dumps(dados), encoding='utf-8')
            env[var] = str(tmp / nome)
        else:
            env.pop(var, None)
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


# ---------------------------------------------------------------- invariantes

def propriedades_pedidas(inv):
    pedidas = {}
    for r in inv['regras']:
        if r['tipo'] == 'propriedade':
            pedidas.setdefault(r['objeto'], []).append(r['propriedade'])
    return pedidas


def avaliar_invariantes(retrato, inv):
    objs = retrato['objetos']
    falhas = []
    for r in inv['regras']:
        t = r['tipo']
        if t == 'existe':
            ausentes = [n for n in r['objetos'] if n not in objs]
            if ausentes:
                falhas.append('[%s] objetos ausentes: %s' % (r['id'], ', '.join(ausentes)))
        elif t == 'oculto':
            visiveis = [n for n in r['objetos'] if n in objs and objs[n].get('visivel')]
            ausentes = [n for n in r['objetos'] if n not in objs]
            if visiveis:
                falhas.append('[%s] deveriam estar ocultos: %s' % (r['id'], ', '.join(visiveis)))
            if ausentes:
                falhas.append('[%s] objetos ausentes: %s' % (r['id'], ', '.join(ausentes)))
        elif t == 'caixa_global':
            o = objs.get(r['objeto'], {})
            cg = o.get('caixa_global')
            if not cg:
                falhas.append('[%s] %s sem caixa global (objeto ausente ou sem forma): %s' % (r['id'], r['objeto'], r['descricao']))
            elif any(abs(a - b) > r['tolerancia_mm'] for a, b in zip(cg, r['caixa'])):
                falhas.append('[%s] %s fora da caixa documentada: esperado %s, atual %s (%s)' % (r['id'], r['objeto'], r['caixa'], cg, r['descricao']))
        elif t == 'folga_minima':
            a, b = objs.get(r['a'], {}).get('caixa_global'), objs.get(r['b'], {}).get('caixa_global')
            if not a or not b:
                falhas.append('[%s] objeto sem caixa global (%s ou %s)' % (r['id'], r['a'], r['b']))
                continue
            lo, hi = EIXOS[r['eixo']]
            folga = max(b[lo] - a[hi], a[lo] - b[hi])
            if folga < r['minimo_mm'] - 1e-6:
                falhas.append('[%s] folga de %.1f mm entre %s e %s no eixo %s; minimo %.1f mm (%s)' % (
                    r['id'], folga, r['a'], r['b'], r['eixo'], r['minimo_mm'], r['descricao']))
        elif t == 'propriedade':
            v = (retrato.get('props', {}).get(r['objeto']) or {}).get(r['propriedade'])
            if not isinstance(v, (int, float)) or abs(v - r['valor']) > r['tolerancia']:
                falhas.append('[%s] %s.%s = %s; esperado %s (%s)' % (r['id'], r['objeto'], r['propriedade'], v, r['valor'], r['descricao']))
    return falhas


def fora_do_envelope(retrato, env):
    c, tol = env['caixa'], env['tolerancia_mm']
    fora = []
    for n, o in retrato['objetos'].items():
        f, cg = o.get('forma'), o.get('caixa_global')
        if not o.get('visivel') or not f or not f.get('solidos') or f['volume'] <= 0.01 or o['tipo'].startswith('App::') or not cg:
            continue
        if any(cg[i] < c[i] - tol for i in range(3)) or any(cg[i] > c[i] + tol for i in range(3, 6)):
            fora.append(n)
    return sorted(fora)


# ---------------------------------------------------------------- comparacao

def comparar(base, atual, inv):
    """Compara retratos. Registra erros/avisos e devolve o detalhe das diferencas (para o relatorio)."""
    bo, ao = base['objetos'], atual['objetos']
    dif = {'removidos': sorted(set(bo) - set(ao)), 'novos': sorted(set(ao) - set(bo)),
           'geometria': [], 'posicao': [], 'visibilidade': [], 'expressoes': [], 'aparencia': [],
           'suspeitos': [], 'invalidos_novos': [], 'fora_envelope': [], 'movimentos': []}
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
    ba, aa = base.get('aparencia'), atual.get('aparencia')
    if ba and aa:
        for n in sorted(set(ba) & set(aa)):
            if ba[n]['h'] != aa[n]['h']:
                dif['aparencia'].append((n, ba[n], aa[n]))
    if dif['removidos']:
        erros.append('%d objetos removidos: %s' % (len(dif['removidos']), ', '.join(dif['removidos'][:15])))
    if dif['novos']:
        avisos.append('%d objetos novos: %s' % (len(dif['novos']), ', '.join(dif['novos'][:15])))
    for rotulo, chave in (('geometria alterada', 'geometria'), ('posicao alterada', 'posicao'), ('visibilidade alterada', 'visibilidade'),
                          ('expressoes alteradas', 'expressoes'), ('aparencia (cor/transparencia) alterada', 'aparencia')):
        if dif[chave]:
            avisos.append('%d com %s: %s' % (len(dif[chave]), rotulo, ', '.join(x[0] for x in dif[chave][:15])))
    if atual['total_expressoes'] < base['total_expressoes']:
        erros.append('Expressoes perdidas: %d -> %d' % (base['total_expressoes'], atual['total_expressoes']))
    inval_base = {i['nome'] for i in base['invalidos']}
    dif['invalidos_novos'] = [i for i in atual['invalidos'] if i['nome'] not in inval_base]
    if dif['invalidos_novos']:
        erros.append('%d objetos invalidos novos: %s' % (len(dif['invalidos_novos']), ', '.join('%s %s' % (i['nome'], i['estado']) for i in dif['invalidos_novos'][:15])))
    if base.get('schema') == SCHEMA and 'caixas_sobrepostas' in atual and 'caixas_sobrepostas' in base:
        cb = {(p[0], p[1]): p[2] for p in base['caixas_sobrepostas']}
        ca = {(p[0], p[1]): p[2] for p in atual['caixas_sobrepostas']}
        dif['suspeitos'] = sorted(k for k in ca if k not in cb or ca[k] > cb[k] * 1.05 + 1)
        antes_fora = set(fora_do_envelope(base, inv['envelope']))
        dif['fora_envelope'] = [n for n in fora_do_envelope(atual, inv['envelope']) if n not in antes_fora]
        if dif['fora_envelope']:
            erros.append('%d objetos visiveis novos fora do apartamento: %s' % (len(dif['fora_envelope']), ', '.join(dif['fora_envelope'][:15])))
        dif['movimentos'] = comparar_movimentos(base.get('movimentos') or {}, atual.get('movimentos') or {})
    return dif


def comparar_movimentos(mb, ma):
    """Cenarios de movimento: nenhum par novo de pecas pode passar a se tocar; o modelo precisa voltar ao estado inicial."""
    achados = []
    for cid, res in sorted(ma.items()):
        entrada = ', '.join('%s.%s=%g' % (o, p, v) for o, p, v in res['entrada'])
        if not res.get('restaurou', True):
            erros.append('Movimento %s (%s): o modelo nao voltou ao estado inicial depois do teste' % (cid, entrada))
        b = mb.get(cid)
        if b is None:
            avisos.append('Movimento %s (%s) e novo; sem base para comparar' % (cid, entrada))
            continue
        pares_b = {(x[0], x[1]): x[2] for x in b['novas_intersecoes']}
        novos = [x for x in res['novas_intersecoes'] if (x[0], x[1]) not in pares_b or x[2] > pares_b[(x[0], x[1])] * 1.05 + 1]
        if novos:
            achados.append((cid, entrada, novos))
            erros.append('Movimento %s (%s): %d contatos novos entre pecas, ex.: %s' % (
                cid, entrada, len(novos), '; '.join('%s x %s (%.0f mm3)' % tuple(x) for x in novos[:3])))
        err_novos = [e for e in res['erros'] if e not in b['erros']]
        if err_novos:
            erros.append('Movimento %s (%s): %s' % (cid, entrada, '; '.join(err_novos)[:200]))
    sumidos = sorted(set(mb) - set(ma))
    if sumidos and ma:
        avisos.append('%d cenarios de movimento da base nao foram rodados: %s' % (len(sumidos), ', '.join(sumidos[:8])))
    return achados


def refinar_colisoes(cad, dif):
    """Segunda passada: intersecao exata so dos pares suspeitos. Devolve lista [a, b, mm3] com colisao real."""
    if not dif['suspeitos']:
        return []
    print('Triagem: %d pares de pecas com caixas novas/maiores; conferindo a intersecao exata...' % len(dif['suspeitos']))
    exato = inspecionar(cad, refinar=[list(k) for k in dif['suspeitos']])
    batidas = [e for e in (exato or {}).get('colisoes_exatas', []) if e[2] > 0.01]
    if batidas:
        erros.append('%d colisoes novas (pecas se sobrepondo): %s' % (len(batidas), '; '.join('%s x %s (%.1f mm3)' % tuple(e) for e in batidas[:15])))
    else:
        avisos.append('%d pares tiveram caixa maior, mas sem sobreposicao real' % len(dif['suspeitos']))
    return batidas


def tem_diferencas(dif, batidas):
    chaves = ('removidos', 'novos', 'geometria', 'posicao', 'visibilidade', 'expressoes', 'aparencia', 'invalidos_novos', 'fora_envelope', 'movimentos')
    return any(dif[k] for k in chaves) or bool(batidas)


# ---------------------------------------------------------------- relatorio

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
    elif dif is None:
        L += ['Base anterior de outro formato (schema %s): sem comparação detalhada.' % base.get('schema', 1), '']
    L += ['## Resumo', '', '| | Base anterior | Agora |', '|---|---:|---:|']
    for rot, chave in (('Objetos', 'total_objetos'), ('Expressões', 'total_expressoes'), ('Formas ativas', 'formas_ativas')):
        L.append('| %s | %s | %s |' % (rot, (base or {}).get(chave, '-'), atual.get(chave, '-')))
    L.append('| Peças com geometria própria inválida | %s | %d |' % (len((base or {}).get('invalidos', [])) if base else '-', len(atual['invalidos'])))
    L.append('| Contêineres com forma montada inválida (informativo) | %s | %d |' % (
        len((base or {}).get('agregados_invalidos', [])) if base else '-', len(atual.get('agregados_invalidos', []))))
    L.append('| Cenários de movimento | %s | %d |' % (len((base or {}).get('movimentos') or {}) if base else '-', len(atual.get('movimentos') or {})))
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
        secao('Aparência alterada', dif['aparencia'], lambda x: '- `%s`: cor %s → %s, transparência %s → %s%%' % (
            x[0], x[1]['c'] or '-', x[2]['c'] or '-', x[1]['t'], x[2]['t']))
        secao('Visibilidade alterada', dif['visibilidade'], lambda x: '- `%s`: %s → %s' % (x[0], 'visível' if x[1] else 'oculto', 'visível' if x[2] else 'oculto'))
        secao('Expressões alteradas', dif['expressoes'], lambda x: '- `%s`: %d → %d expressões' % x)
        secao('Formas inválidas novas', dif['invalidos_novos'], lambda i: '- `%s` %s' % (i['nome'], i['estado']))
        secao('Objetos visíveis novos fora do apartamento', dif['fora_envelope'], lambda n: '- `%s`' % n)
        secao('Colisões novas confirmadas (interseção exata)', batidas, lambda e: '- `%s` × `%s`: %.1f mm³' % tuple(e))
        secao('Cenários de movimento com contatos novos', dif['movimentos'], lambda x: '- %s (%s): %s' % (
            x[0], x[1], '; '.join('`%s` × `%s` %.0f mm³' % tuple(p) for p in x[2][:3])))
        if not tem_diferencas(dif, batidas):
            L += ['Nenhuma diferença em relação à base anterior.', '']
    L += ['## Como usar', '',
          '1. Leia as seções acima. Cada mudança listada foi pedida e é a esperada?',
          '2. Só com a aprovação dele: `python ferramentas/verificar_modelo/verificar_modelo.py --completo --atualizar-base --aprovado-por "Elias, dd/mm/aaaa: o que aprovou"`.',
          '3. Commite a base, este relatório, `current_release.json` (SHA) e o `ESTADO_ATUAL.md` juntos.', '']
    RELATORIO.write_text('\n'.join(L), encoding='utf-8')


def valor_arg(nome):
    return sys.argv[sys.argv.index(nome) + 1] if nome in sys.argv and sys.argv.index(nome) + 1 < len(sys.argv) else None


def validar_candidato(caminho, completo, atualizar):
    if not completo or atualizar:
        raise ValueError('--candidato exige --completo e proibe --atualizar-base')
    if not caminho:raise ValueError('--candidato precisa de um arquivo externo')
    cad=Path(caminho).resolve()
    if RAIZ==cad or RAIZ in cad.parents or cad.suffix.lower()!='.fcstd':
        raise ValueError('Candidato precisa ser um FCStd fora do repositorio')
    with zipfile.ZipFile(cad) as archive:
        if archive.testzip() or not {'Document.xml','GuiDocument.xml'}<=set(archive.namelist()):
            raise ValueError('Candidato sem documento/cores GUI ou ZIP corrompido')
    return cad


def main():
    completo = '--completo' in sys.argv
    atualizar = '--atualizar-base' in sys.argv
    aprovacao = valor_arg('--aprovado-por')
    rel, cad = rapido()
    protegidos={}
    if '--candidato' in sys.argv:
        try:
            candidato=validar_candidato(valor_arg('--candidato'),completo,atualizar)
        except (ValueError,OSError,zipfile.BadZipFile) as exc:
            print('ERRO:',exc);sys.exit(1)
        if erros:
            for erro in erros:print('ERRO:',erro)
            sys.exit(1)
        protegidos={p:sha(p) for p in (cad,BASE,RELEASE) if p.exists()}
        cad=candidato
        rel=dict(rel,cadRevision='Candidato externo: '+cad.stem)
    if completo and cad.exists():
        inv = json.loads(INVARIANTES.read_text(encoding='utf-8'))
        casos = None if '--sem-movimentos' in sys.argv else json.loads(MOVIMENTOS.read_text(encoding='utf-8'))
        cache = Path(tempfile.gettempdir()) / 'gp_retrato_ultimo.json'
        retrato = None
        if '--reusar-retrato' in sys.argv and cache.exists():  # so para desenvolvimento destas ferramentas
            c = json.loads(cache.read_text(encoding='utf-8'))
            if c.get('sha256') == sha(cad):
                retrato = c
                print('Usando o retrato em cache (%s)' % cache)
        if retrato is None:
            retrato = inspecionar(cad, props=propriedades_pedidas(inv), movimentos=casos)
            if retrato:
                retrato['sha256'] = sha(cad)
                retrato['revisao'] = rel['cadRevision']
                retrato['aparencia'] = ap.ler_aparencia(cad)
                cache.write_text(json.dumps(retrato, ensure_ascii=False), encoding='utf-8')
        if retrato:
            for f in avaliar_invariantes(retrato, inv):
                erros.append('Invariante ' + f)
            base = ler_base() if BASE.exists() else None
            mudou_metodo = bool(base) and base.get('schema') != SCHEMA
            dif, batidas = None, []
            if base and not mudou_metodo:
                dif = comparar(base, retrato, inv)
                batidas = refinar_colisoes(cad, dif)
            elif mudou_metodo:
                avisos.append('A base e de um formato antigo (schema %s); sem comparacao detalhada. Rode --atualizar-base para migrar.' % base.get('schema', 1))
            if atualizar:
                erros[:] = [e for e in erros if 'current_release.json nao foi atualizado' not in e]
                mesmo_modelo = bool(base) and base.get('sha256') == retrato['sha256']
                mudou = bool(dif) and tem_diferencas(dif, batidas)
                if mudou_metodo and not mesmo_modelo:
                    mudou = True  # modelo diferente E metodo diferente: precisa de aprovacao
                hoje = datetime.date.today().strftime('%d/%m/%Y')
                automatica = None  # casos em que gravar a base nao depende de decisao de Elias
                if base is None:
                    automatica = 'Não se aplica: base inicial, sem retrato anterior (%s)' % hoje
                elif mudou_metodo and mesmo_modelo:
                    automatica = 'Não se aplica: migração do formato da base, mesmo modelo e mesmo SHA (%s)' % hoje
                elif not mudou:
                    automatica = 'Não se aplica: modelo inalterado (mesmo SHA); sem diferença de geometria, posição, aparência ou movimento (%s)' % hoje
                escrever_relatorio(base, retrato, dif, batidas, aprovacao or automatica, rel)
                if aprovacao is not None and not re.search(r'\d{1,2}/\d{1,2}', aprovacao):
                    erros.append('--aprovado-por precisa citar a data da aprovacao de Elias (dd/mm) e o que ele aprovou')
                elif mudou and not aprovacao:
                    erros.append('Ha diferencas em relacao a base e nenhuma aprovacao: base NAO gravada. Leia %s, e so com a decisao de Elias rode de novo com --aprovado-por "Elias, dd/mm/aaaa: ..."' % RELATORIO.relative_to(RAIZ))
                elif any(e.startswith('Invariante') for e in erros):
                    erros.append('Base NAO gravada: ha invariantes quebradas (corrija o modelo ou, com decisao de Elias, a regra em invariantes.json)')
                else:
                    if retrato['invalidos']:
                        avisos.append('Base gravada com %d objetos invalidos registrados' % len(retrato['invalidos']))
                    retrato['aprovacao'] = aprovacao or ('base inicial' if base is None else
                                                         'migracao de formato, mesmo modelo' if mudou_metodo else 'sem diferencas')
                    gravar_base(retrato)
                    print('Base gravada: %s (%d objetos, %d pares de caixas, %d cenarios de movimento)' % (
                        BASE.relative_to(RAIZ), retrato['total_objetos'], len(retrato.get('caixas_sobrepostas', [])), len(retrato.get('movimentos') or {})))
                    print('Relatorio: %s' % RELATORIO.relative_to(RAIZ))
            else:
                if '--relatorio' in sys.argv:
                    escrever_relatorio(base, retrato, dif, batidas, None, rel)
                    print('Relatorio (aprovacao PENDENTE): %s' % RELATORIO.relative_to(RAIZ))
                if base is None:
                    avisos.append('Sem base para comparar')
            print('Inspecao em %.0f s: %d objetos, %d formas ativas, %d pares de caixas, %d cenarios de movimento' % (
                retrato['segundos'], retrato['total_objetos'], retrato.get('formas_ativas', 0),
                len(retrato.get('caixas_sobrepostas', [])), len(retrato.get('movimentos') or {})))
    for path,digest in protegidos.items():
        if sha(path)!=digest:erros.append('Arquivo protegido mudou durante a inspecao: '+path.name)
    for a in avisos:
        print('AVISO:', a)
    for e in erros:
        print('ERRO:', e)
    print('Modelo: %s' % ('OK' if not erros else '%d erro(s)' % len(erros)))
    sys.exit(1 if erros else 0)


main()
