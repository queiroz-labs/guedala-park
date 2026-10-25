# Roda dentro do FreeCADCmd. Abre o modelo SEM salvar e grava um retrato em JSON (schema 2).
# Entradas (variaveis de ambiente):
#   GP_MODELO     caminho do .FCStd            GP_SAIDA      JSON de saida
#   GP_COLISOES   '1' (padrao) triagem por caixas globais; '0' pula
#   GP_REFINAR    JSON [[a,b],...]: intersecao exata so desses pares
#   GP_PROPS      JSON {objeto: [propriedades]}: valores gravados em retrato['props']
#   GP_MOVIMENTOS JSON [{"id":..,"input":[[objeto,propriedade,valor],..]},..]: roda cada cenario em memoria
# Nunca chama doc.save(); fecha o documento no fim. Alteracoes dos cenarios vivem so na memoria.
import os, json, time, itertools
import FreeCAD

SCHEMA = 2
modelo = os.environ['GP_MODELO']
saida = os.environ['GP_SAIDA']
colisoes = os.environ.get('GP_COLISOES', '1') == '1'
TOL_VOL = 0.01  # mm3: comum abaixo disso e ruido numerico
TOL_POS = 1e-6


def r(x, n=4):
    return round(float(x), n)


def carregar(var):
    p = os.environ.get(var)
    return json.load(open(p, encoding='utf-8')) if p and os.path.exists(p) else None


def matriz_do_pai(o):
    """Matriz global do contêiner (App::Part/Group com placement). None se o objeto e de topo."""
    try:
        p = o.getParentGeoFeatureGroup()
    except Exception:
        return None
    return p.getGlobalPlacement().toMatrix() if p is not None else None


def caixa_global(sh, m):
    bb = sh.BoundBox
    if m is None:
        return bb
    pts = [m.multVec(FreeCAD.Vector(x, y, z)) for x in (bb.XMin, bb.XMax) for y in (bb.YMin, bb.YMax) for z in (bb.ZMin, bb.ZMax)]
    return FreeCAD.BoundBox(min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts),
                            max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts))


def lista_caixa(bb):
    return [r(bb.XMin, 3), r(bb.YMin, 3), r(bb.ZMin, 3), r(bb.XMax, 3), r(bb.YMax, 3), r(bb.ZMax, 3)]


def sobrepoe(a, b):
    dx = min(a.XMax, b.XMax) - max(a.XMin, b.XMin)
    dy = min(a.YMax, b.YMax) - max(a.YMin, b.YMin)
    dz = min(a.ZMax, b.ZMax) - max(a.ZMin, b.ZMin)
    return (dx * dy * dz) if (dx > 0 and dy > 0 and dz > 0) else 0.0


t0 = time.time()
doc = FreeCAD.openDocument(modelo, True)  # True = oculto
objs = list(doc.Objects)
retrato = {'schema': SCHEMA, 'arquivo': modelo, 'objetos': {}, 'invalidos': [],
           'total_objetos': len(objs), 'total_expressoes': 0}

for o in objs:
    item = {'tipo': o.TypeId, 'rotulo': o.Label}
    estado = [s for s in o.State if s in ('Invalid', 'Error', 'Touched', 'Restore')]
    if 'Invalid' in estado or 'Error' in estado:
        retrato['invalidos'].append({'nome': o.Name, 'estado': estado})
    expr = getattr(o, 'ExpressionEngine', []) or []
    retrato['total_expressoes'] += len(expr)
    if expr:
        item['expressoes'] = sorted('%s=%s' % (p, e) for p, e in expr)
    if hasattr(o, 'Visibility'):
        item['visivel'] = bool(o.Visibility)
    pl = getattr(o, 'Placement', None)
    if pl is not None and hasattr(pl, 'Base'):
        b = pl.Base; q = pl.Rotation.Q
        item['posicao'] = [r(b.x), r(b.y), r(b.z)] + [r(v, 6) for v in q]
    sh = getattr(o, 'Shape', None)
    if sh is not None and hasattr(sh, 'isNull') and not sh.isNull():
        try:
            bb = sh.BoundBox
            item['forma'] = {'volume': r(sh.Volume, 3), 'area': r(sh.Area, 3),
                             'faces': len(sh.Faces), 'solidos': len(sh.Solids),
                             'caixa': lista_caixa(bb), 'valida': bool(sh.isValid())}
            m = matriz_do_pai(o)
            item['caixa_global'] = lista_caixa(caixa_global(sh, m))
            pai = o.getParentGeoFeatureGroup()
            if pai is not None:
                item['pai'] = pai.Name
            if not sh.isValid():
                if o.isDerivedFrom('Part::Feature'):  # geometria PROPRIA gravada no arquivo: invalida de verdade
                    retrato['invalidos'].append({'nome': o.Name, 'estado': ['ShapeInvalida']})
                else:
                    # Contêiner (App::Part/grupo): o FreeCAD MONTA a forma juntando os filhos transformados; nao ha forma
                    # gravada. Ferragens B-spline de fabricante ficam invalidas ao serem transformadas, mesmo com
                    # determinante 1. Registro informativo, nao e defeito de peca.
                    retrato.setdefault('agregados_invalidos', []).append(o.Name)
        except Exception as e:  # forma ilegivel conta como invalida
            retrato['invalidos'].append({'nome': o.Name, 'estado': ['Excecao: %s' % e]})
    retrato['objetos'][o.Name] = item

# Propriedades pedidas pelas invariantes (valores escalares)
pedidas = carregar('GP_PROPS') or {}
retrato['props'] = {}
for nome, props in pedidas.items():
    o = doc.getObject(nome)
    if o is None:
        continue
    vals = {}
    for p in props:
        try:
            v = getattr(o, p)
            v = getattr(v, 'Value', v)  # Quantity (com unidade) -> numero em mm/graus
            vals[p] = r(v, 6) if isinstance(v, (int, float)) and not isinstance(v, bool) else str(v)
        except Exception:
            vals[p] = None
    retrato['props'][nome] = vals

# Formas "ativas" (visiveis, com solido), em coordenadas GLOBAIS.
ativos = {}
if colisoes or os.environ.get('GP_MOVIMENTOS'):
    for o in objs:
        if not getattr(o, 'Visibility', False) or o.TypeId.startswith('App::'):
            continue
        sh = getattr(o, 'Shape', None)
        if sh is None or sh.isNull() or not sh.Solids or sh.Volume <= TOL_VOL:
            continue
        if any(p.TypeId.startswith('Part::') and p.Visibility for p in o.InList if hasattr(p, 'Visibility')):
            continue  # filho de outra forma visivel: a mae ja representa
        ativos[o.Name] = o


def forma_global(o):
    m = matriz_do_pai(o)
    sh = o.Shape
    return sh.transformed(m) if m is not None else sh


# Colisoes em duas etapas, para ser rapido:
# 1) triagem por caixas globais de TODAS as formas ativas (segundos);
# 2) intersecao exata (common) so para os pares de GP_REFINAR (novos ou que cresceram vs a base).
globais = {}
if colisoes:
    caixas = {n: caixa_global(o.Shape, matriz_do_pai(o)) for n, o in ativos.items()}
    nomes = sorted(ativos)
    pares = []
    for i, na in enumerate(nomes):
        ba = caixas[na]
        for nb in nomes[i + 1:]:
            v = sobrepoe(ba, caixas[nb])
            if v > 0:
                pares.append([na, nb, r(v, 1)])
    retrato['formas_ativas'] = len(ativos)
    retrato['caixas_sobrepostas'] = pares
    refinar = carregar('GP_REFINAR')
    if refinar:
        exatas = []
        for na, nb in refinar:
            if na in ativos and nb in ativos:
                for n in (na, nb):
                    if n not in globais:
                        globais[n] = forma_global(ativos[n])
                try:
                    v = globais[na].common(globais[nb]).Volume
                except Exception:
                    v = -1
                exatas.append([na, nb, r(v, 2)])
        retrato['colisoes_exatas'] = exatas

# Cenarios de movimento: aplica o controle em memoria, recalcula, mede o que passou a se tocar, restaura.
casos = carregar('GP_MOVIMENTOS')
if casos:
    def estado_global():
        return {n: caixa_global(o.Shape, matriz_do_pai(o)) for n, o in ativos.items()}

    def igual(a, b):
        return all(abs(x - y) <= TOL_POS for x, y in zip((a.XMin, a.YMin, a.ZMin, a.XMax, a.YMax, a.ZMax),
                                                            (b.XMin, b.YMin, b.ZMin, b.XMax, b.YMax, b.ZMax)))

    inicial = estado_global()
    # Formas iniciais capturadas ANTES de qualquer cenario mexer no modelo (calcular depois daria o estado ja movido).
    formas_ini = {n: forma_global(o) for n, o in ativos.items()}
    invalidos_ini = {o.Name for o in doc.Objects if 'Invalid' in o.State}
    cache_ini = {}

    def tocava_no_inicio(na, nb):
        k = (na, nb)
        if k not in cache_ini:
            try:
                cache_ini[k] = formas_ini[na].common(formas_ini[nb]).Volume > TOL_VOL
            except Exception:
                cache_ini[k] = True
        return cache_ini[k]

    retrato['movimentos'] = {}
    for caso in casos:
        t1 = time.time()
        originais = []
        resultado = {'entrada': caso['input'], 'erros': [], 'novas_intersecoes': []}
        try:
            for nome, prop, valor in caso['input']:
                o = doc.getObject(nome)
                if o is None:
                    resultado['erros'].append('objeto ausente: %s' % nome)
                    continue
                atual_valor = getattr(o, prop)
                originais.append((o, prop, atual_valor))
                if isinstance(atual_valor, bool):  # bool antes de int: bool e subclasse de int
                    setattr(o, prop, bool(valor))
                elif isinstance(atual_valor, int):
                    setattr(o, prop, int(valor))
                else:
                    setattr(o, prop, float(valor))
            doc.recompute()
            agora = estado_global()
            # o proprio cenario pode ocultar pecas (ex.: almofada do banco): oculta nao conta
            visiveis_agora = {n for n, o in ativos.items() if getattr(o, 'Visibility', True)}
            movidos = [n for n in ativos if n in visiveis_agora and not igual(inicial[n], agora[n])]
            resultado['movidos'] = len(movidos)
            atuais = {}
            vistos = set()
            for c in movidos:
                for n in ativos:
                    if n == c or n not in visiveis_agora:
                        continue
                    chave = tuple(sorted((c, n)))
                    if chave in vistos or not sobrepoe(agora[c], agora[n]) > 0:
                        continue
                    vistos.add(chave)
                    for x in chave:
                        if x not in atuais:
                            atuais[x] = forma_global(ativos[x])
                    try:
                        v = atuais[chave[0]].common(atuais[chave[1]]).Volume
                    except Exception:
                        v = -1
                    if v > TOL_VOL and not tocava_no_inicio(*chave):
                        resultado['novas_intersecoes'].append([chave[0], chave[1], r(v, 1)])
            novos_inv = sorted({o.Name for o in doc.Objects if 'Invalid' in o.State} - invalidos_ini)
            if novos_inv:
                resultado['erros'].append('objetos invalidos apos recalcular: %s' % ', '.join(novos_inv[:10]))
        except Exception as e:
            resultado['erros'].append('excecao: %s' % e)
        for o, prop, orig in originais:  # restaura sempre
            try:
                setattr(o, prop, orig)
            except Exception as e:
                resultado['erros'].append('nao restaurou %s.%s: %s' % (o.Name, prop, e))
        doc.recompute()
        volta = estado_global()
        resultado['restaurou'] = all(igual(inicial[n], volta[n]) for n in ativos)
        resultado['novas_intersecoes'].sort()
        resultado['segundos'] = r(time.time() - t1, 1)
        retrato['movimentos'][caso['id']] = resultado

FreeCAD.closeDocument(doc.Name)
retrato['segundos'] = r(time.time() - t0, 1)
with open(saida, 'w', encoding='utf-8') as f:
    json.dump(retrato, f, ensure_ascii=False, indent=0)
