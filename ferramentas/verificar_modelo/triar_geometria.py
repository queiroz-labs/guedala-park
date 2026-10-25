"""Triagem somente de leitura, executada pelo FreeCADCmd (sem recompute/save).

Consulta o CAD de current_release.json e os agregados_invalidos da base, sem muda-la.
GP_TRIAGEM_SAIDA permite escolher outro JSON; GP_TRIAGEM_BOP=1 habilita
Shape.check(True) nas fontes afetadas e nas pecas das fichas P06/P07.
Os grandes agregados recebem apenas Shape.check(), evitando BOP entre todos
os solidos do apartamento. Os resultados nao liberam corte ou carga.
"""
import collections
import gzip
import hashlib
import json
import math
import os
import re
from pathlib import Path

import FreeCAD

RAIZ = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(shape, bop=False):
    try:
        shape.check(bop)
        return {'ok': True, 'bop': bop, 'erros': {}}
    except Exception as exc:
        # O OCC pode acrescentar linhas "No error" junto de erros reais.
        mensagens = [s.strip() for s in str(exc).splitlines()
                     if s.strip() and s.strip() != 'No error']
        return {'ok': False, 'bop': bop, 'excecao': type(exc).__name__,
                'erros': dict(collections.Counter(mensagens))}


def resumo(shape):
    solids = shape.Solids
    return {'tipo': shape.ShapeType, 'valida': bool(shape.isValid()),
            'volume_mm3': float(shape.Volume), 'area_mm2': float(shape.Area),
            'faces': len(shape.Faces), 'solidos': len(solids),
            'solidos_invalidos': [i for i, s in enumerate(solids, 1) if not s.isValid()],
            'delta_volume_soma_solidos_mm3': float(shape.Volume - sum(s.Volume for s in solids))}


def com_forma(obj):
    shape = getattr(obj, 'Shape', None)
    return shape is not None and not shape.isNull()


def mesma_assinatura(a, b):
    return (len(a.Solids) == len(b.Solids) and len(a.Faces) == len(b.Faces)
            and math.isclose(a.Volume, b.Volume, rel_tol=1e-9, abs_tol=1e-5))


def rastrear(obj, fragmento, caminho):
    """Associa a arvore Group aos filhos do agregado, conferindo a assinatura.

    Nao associa por volume sozinho: exige ordem, numero de filhos, faces e
    solidos. Se o mapeamento nao for demonstrado, registra essa limitacao.
    """
    filhos = [c for c in getattr(obj, 'Group', []) if com_forma(c)]
    partes = fragmento.childShapes()
    if len(filhos) != len(partes):
        # O Group pode conter caixas usadas como Base/Tool de um Fuse.
        # O agregado representa o resultado, sem repetir esses operandos.
        nomes = {c.Name for c in filhos}
        filhos = [c for c in filhos if not any(
            p.Name in nomes and p.TypeId.startswith('Part::') and getattr(p, 'Visibility', False)
            for p in c.InList)]
    if (filhos and len(filhos) == len(partes)
            and all(mesma_assinatura(c.Shape, p) for c, p in zip(filhos, partes))):
        achados = []
        for filho, parte in zip(filhos, partes):
            if not parte.isValid():
                achados.extend(rastrear(filho, parte, caminho + [filho.Name]))
        return achados
    return [{'objeto': obj.Name, 'rotulo': obj.Label, 'caminho': caminho,
             'mapeamento_folha': not filhos, 'nativo': resumo(obj.Shape),
             'no_agregado': resumo(fragmento), 'check_agregado': check(fragmento)}]


def main():
    release = json.loads((RAIZ / 'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    modelo = RAIZ / release['cadPath']
    base_path = RAIZ / '02_Modelo_3D/Base_verificacao.json.gz'
    with gzip.open(base_path, 'rt', encoding='utf-8') as stream:
        base = json.load(stream)
    antes, base_antes = sha(modelo), sha(base_path)
    if antes != release['cadSHA256'] or antes != base['sha256']:
        raise RuntimeError('SHA do modelo, release e base precisam coincidir antes da triagem')
    bop = os.environ.get('GP_TRIAGEM_BOP') == '1'
    saida = Path(os.environ.get('GP_TRIAGEM_SAIDA', str(RAIZ / '02_Modelo_3D/Triagem_geometria.json')))
    alvos = list(dict.fromkeys(base.get('agregados_invalidos', [])))
    invalidos_base = {i['nome'] for i in base['invalidos']}
    # Comecar pelos conjuntos que alimentam a marcenaria.
    ordem = sorted(alvos, key=lambda n: (n not in ('Modulo005', 'Modulo006'), n))
    resultado = {'schema': 2, 'modelo': release['cadPath'], 'sha256': antes,
                 'freecad': FreeCAD.Version(), 'bop_fontes': bop,
                 'metodo': 'Sem recompute ou save; validade propria separada dos agregados informativos; Shape.check nos agregados; rastreio por Group e assinatura.',
                 'objetos': [], 'fontes_afetadas': {}, 'fichas': {}}
    doc = FreeCAD.openDocument(str(modelo), True)
    try:
        proprias = [o for o in doc.Objects if o.isDerivedFrom('Part::Feature') and com_forma(o)]
        invalidos = sorted(o.Name for o in proprias if not o.Shape.isValid())
        agregados = sorted(o.Name for o in doc.Objects if not o.isDerivedFrom('Part::Feature')
                           and com_forma(o) and not o.Shape.isValid())
        resultado['geometria_propria'] = {'criterio': 'Part::Feature e tipos derivados, com forma nao nula',
                                         'total': len(proprias), 'invalidas': len(invalidos)}
        resultado['agregados_invalidos'] = agregados
        resultado['agregados_invalidos_novos'] = sorted(set(agregados) - set(alvos))
        resultado['agregados_base_nao_reproduzidos'] = sorted(set(alvos) - set(agregados))
        resultado['invalidos_atuais'] = invalidos
        resultado['invalidos_novos'] = sorted(set(invalidos) - invalidos_base)
        resultado['invalidos_base_nao_reproduzidos'] = sorted(invalidos_base - set(invalidos))
        for nome in ordem:
            obj = doc.getObject(nome)
            shape = obj.Shape
            item = {'nome': nome, 'rotulo': obj.Label, 'tipo': obj.TypeId,
                    'geometria_propria': False, 'classificacao': 'agregado_informativo',
                    'forma': resumo(shape), 'check': check(shape),
                    'rastreio': rastrear(obj, shape, [nome])}
            resultado['objetos'].append(item)
            print('Triagem:', nome, 'solidos invalidos:', len(item['forma']['solidos_invalidos']), flush=True)
            for fonte in item['rastreio']:
                chave = fonte['objeto']
                if chave in resultado['fontes_afetadas']:
                    continue
                original = doc.getObject(chave)
                nativa = original.Shape
                pai = original.getParentGeoFeatureGroup()
                globalizada = nativa.transformed(pai.getGlobalPlacement().toMatrix()) if pai else nativa.copy()
                checar_bop = bop and fonte['mapeamento_folha']
                resultado['fontes_afetadas'][chave] = {
                    'rotulo': original.Label, 'mapeamento_folha': fonte['mapeamento_folha'],
                    'nativo': resumo(nativa), 'check_nativo': check(nativa, checar_bop),
                    'transformacao_global': resumo(globalizada),
                    'check_global': check(globalizada, checar_bop)}
        texto = (RAIZ / 'ferramentas/site/src/fabrication-data.js').read_text(encoding='utf-8')
        fichas = json.loads(re.search(r'const FABRICATION_DATA\s*=\s*(\{.*\});', texto, re.S)[1])['modules']
        for codigo in ('P01', 'P02', 'P06', 'P07'):
            pecas = []
            for painel in fichas[codigo]['panels']:
                ids = painel.get('ids') or [painel['id']]
                for nome in ids:
                    obj = doc.getObject(nome)
                    if obj is None or not com_forma(obj):
                        pecas.append({'id': nome, 'presente_no_cad': False})
                        continue
                    item = {'id': nome, 'rotulo': obj.Label, 'presente_no_cad': True,
                            'dimensoes_ficha_mm': painel['dimensions'],
                            'forma_nativa': resumo(obj.Shape),
                            'check': check(obj.Shape, bop and codigo in ('P06', 'P07'))}
                    if codigo in ('P06', 'P07'):
                        local = obj.Shape.copy()
                        local.Placement = FreeCAD.Placement()
                        bb = local.BoundBox
                        dims = sorted([bb.XLength, bb.YLength, bb.ZLength], reverse=True)
                        item['dimensoes_cad_mm'] = dims
                        item['tolerancia_dimensoes_mm'] = 0.02
                        item['dimensoes_conferem'] = all(abs(a - b) <= 0.02 for a, b in
                                                       zip(dims, painel['dimensions']))
                    pecas.append(item)
            resultado['fichas'][codigo] = pecas
    finally:
        FreeCAD.closeDocument(doc.Name)
    resultado['sha256_depois'] = sha(modelo)
    resultado['modelo_inalterado'] = resultado['sha256_depois'] == antes
    resultado['base_inalterada'] = sha(base_path) == base_antes
    if not resultado['modelo_inalterado'] or not resultado['base_inalterada']:
        raise RuntimeError('Modelo ou base mudaram durante a leitura')
    saida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Triagem concluida:', len(resultado['objetos']), 'objetos;', len(resultado['fontes_afetadas']), 'fontes afetadas', flush=True)


# FreeCADCmd importa scripts .py como modulos, sem __name__ == '__main__'.
main()
