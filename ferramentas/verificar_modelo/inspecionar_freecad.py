# Roda dentro do FreeCADCmd. Abre o modelo SEM salvar e grava um retrato em JSON.
# Entrada: variaveis de ambiente GP_MODELO (caminho .FCStd) e GP_SAIDA (JSON).
# Nunca chama doc.save(); fecha o documento no fim.
import os, json, math, time, itertools
import FreeCAD

modelo = os.environ['GP_MODELO']
saida = os.environ['GP_SAIDA']
colisoes = os.environ.get('GP_COLISOES', '1') == '1'
TOL_VOL = 0.01  # mm3: comum abaixo disso e ruido numerico


def r(x, n=4):
    return round(float(x), n)


t0 = time.time()
doc = FreeCAD.openDocument(modelo, True)  # True = oculto
objs = list(doc.Objects)
retrato = {'arquivo': modelo, 'objetos': {}, 'invalidos': [], 'expressoes_quebradas': [],
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
                             'caixa': [r(bb.XMin, 3), r(bb.YMin, 3), r(bb.ZMin, 3), r(bb.XMax, 3), r(bb.YMax, 3), r(bb.ZMax, 3)],
                             'valida': bool(sh.isValid())}
            if not sh.isValid():
                retrato['invalidos'].append({'nome': o.Name, 'estado': ['ShapeInvalida']})
        except Exception as e:  # forma ilegivel conta como invalida
            retrato['invalidos'].append({'nome': o.Name, 'estado': ['Excecao: %s' % e]})
    retrato['objetos'][o.Name] = item

# Colisoes em duas etapas, para ser rapido:
# 1) triagem por caixas delimitadoras de TODAS as formas ativas (segundos);
# 2) intersecao exata (common) so para os pares listados em GP_REFINAR (JSON [[a,b],...]),
#    que o verificador preenche com os pares novos ou que cresceram em relacao a base.
if colisoes:
    ativos = {}
    for o in objs:
        if not getattr(o, 'Visibility', False) or o.TypeId.startswith('App::'):
            continue
        sh = getattr(o, 'Shape', None)
        if sh is None or sh.isNull() or not sh.Solids or sh.Volume <= TOL_VOL:
            continue
        if any(p.TypeId.startswith('Part::') and p.Visibility for p in o.InList if hasattr(p, 'Visibility')):
            continue  # filho de outra forma visivel: a mae ja representa
        ativos[o.Name] = (sh, sh.BoundBox)
    nomes = sorted(ativos)
    pares = []
    for i, na in enumerate(nomes):
        ba = ativos[na][1]
        for nb in nomes[i + 1:]:
            bb = ativos[nb][1]
            dx = min(ba.XMax, bb.XMax) - max(ba.XMin, bb.XMin)
            dy = min(ba.YMax, bb.YMax) - max(ba.YMin, bb.YMin)
            dz = min(ba.ZMax, bb.ZMax) - max(ba.ZMin, bb.ZMin)
            if dx > 0 and dy > 0 and dz > 0:
                pares.append([na, nb, r(dx * dy * dz, 1)])
    retrato['formas_ativas'] = len(ativos)
    retrato['caixas_sobrepostas'] = pares
    refinar = os.environ.get('GP_REFINAR')
    if refinar and os.path.exists(refinar):
        exatas = []
        for na, nb in json.load(open(refinar, encoding='utf-8')):
            if na in ativos and nb in ativos:
                try:
                    v = ativos[na][0].common(ativos[nb][0]).Volume
                except Exception:
                    v = -1
                exatas.append([na, nb, r(v, 2)])
        retrato['colisoes_exatas'] = exatas

FreeCAD.closeDocument(doc.Name)
retrato['segundos'] = r(time.time() - t0, 1)
with open(saida, 'w', encoding='utf-8') as f:
    json.dump(retrato, f, ensure_ascii=False, indent=0)
