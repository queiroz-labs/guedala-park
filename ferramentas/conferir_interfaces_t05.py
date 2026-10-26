"""Percursos nominais P08/varal a partir da base salva; nao abre FreeCAD."""
from pathlib import Path
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def overlap(a, b):
    return all(min(a[i+3], b[i+3])-max(a[i], b[i]) > 1e-6 for i in range(3))


def swept(box, axis, delta):
    result = box.copy()
    result[axis] += min(0, delta)
    result[axis+3] += max(0, delta)
    return result


def save(path, data):
    (ROOT/path).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def main():
    path = ROOT/'02_Modelo_3D/Base_verificacao.json.gz'
    base = json.loads(gzip.decompress(path.read_bytes()))
    objects = base['objetos']
    release = json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((ROOT/release['cadPath']).read_bytes()).hexdigest() == base['sha256']

    def ancestors(name):
        seen = []
        while name in objects and name not in seen:
            seen.append(name)
            name = objects[name].get('pai')
        return seen

    parts = {n:o for n,o in objects.items()
             if o.get('forma', {}).get('solidos', 0) > 0
             and o.get('tipo', '').startswith(('Part::', 'PartDesign::'))
             and all(objects[a].get('visivel', True) for a in ancestors(n))}
    common = dict(cad_sha256=base['sha256'],base_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        cad_opened=False,cad_changed=False,physical_tests_executed=0,
        obstacle_policy='Part::/PartDesign:: com solidos e visibilidade na cadeia pai salva; App::Part/grupos agregados excluidos, filhos mantidos.',
        scope='Caixas alinhadas globais, translação retilinea. Sobreposicao e candidato, nao colisao BREP. Separacao exclui intersecao apenas no conjunto testado.',
        absent=['pessoas/maos','tolerancias/deformacao','posicoes abertas simultaneas de outros controles','corpos comerciais ausentes'])
    # Controle negativo: obstaculo no meio do percurso, fora das duas pontas.
    test = [0.,0.,0.,1.,1.,1.]
    end = [0.,-10.,0.,1.,-9.,1.]
    middle = [0.,-5.,0.,1.,-4.,1.]
    assert not overlap(test,middle) and not overlap(end,middle)
    assert overlap(swept(test,1,-10),middle)
    assert not overlap(test,[1.,0.,0.,2.,1.,1.])  # contato sem volume

    movements_path = ROOT/'ferramentas/verificar_modelo/movimentos.json'
    movements = json.loads(movements_path.read_text(encoding='utf-8'))
    def find_case(x):
        if isinstance(x,dict):
            if x.get('id')=='m086':return x
            for v in x.values():
                result=find_case(v)
                if result:return result
        if isinstance(x,list):
            for v in x:
                result=find_case(v)
                if result:return result
        return None
    case=find_case(movements)
    assert ['Gaveta007','Extensao',400.] in case['input']
    assert 'LocalY=0 mm - Extensao' in objects['Gaveta007']['expressoes']
    moving={n:o for n,o in parts.items() if 'Gaveta007' in ancestors(n)}
    fixed={n:o for n,o in parts.items() if n not in moving}
    pairs=[]
    for n,o in moving.items():
        envelope=swept(o['caixa_global'],1,-400.)
        for k,p in fixed.items():
            if overlap(envelope,p['caixa_global']):pairs.append([n,k])
    assert not pairs, 'Novo candidato P08: revisar antes de relatar separacao'
    b=objects['Gaveta007']['caixa_global']
    p08=dict(common,movement_case=case,travel_mm=400.,direction='-Y global',
        moving_parts=list(moving),fixed_parts=len(fixed),pair_checks=len(moving)*len(fixed),
        candidates=pairs,closed_box_mm=b,open_box_mm=swept(b,1,0),
        remaining_behind_closed_front_plane_mm=b[4]-400-b[1],
        limits=['400 mm vem do cenario salvo, nao define batente comercial.',
                'Piso com contato tangente nao e colisao volumetrica nem prova de nivelamento.',
                'Nao inclui guia/batente ainda sem geometria, giro, inclinacao ou retirada vertical.',
                'Reacoes das rodas e resistencia permanecem no estudo Apoios.json.'])
    p08['open_box_mm'][1]-=400;p08['open_box_mm'][4]-=400
    save('04_Moveis/P08/Conferencia_percurso.json',p08)

    b=objects['Peca157']['caixa_global']
    assert b == [3705.,5650.,2310.,4705.,6150.,2340.]
    assert any('min(860 mm;' in e for e in objects['Peca157']['expressoes'])
    fixed={n:o for n,o in parts.items() if n!='Peca157'}
    rows=[]
    for descent in [310.,410.,860.]:
        for length in [0.,500.,800.,1200.]:
            # Roupa hipotetica pendurada a partir da face inferior do gabarito.
            for spread in ([0.] if length==0 else [0.,50.,100.]):
                envelope=swept(b,2,-descent)
                envelope[2]-=length
                for i in [0,1]:
                    envelope[i]-=spread;envelope[i+3]+=spread
                hits=[dict(name=n,label=o['rotulo'],box_mm=o['caixa_global'])
                      for n,o in fixed.items() if overlap(envelope,o['caixa_global'])]
                rows.append(dict(descent_mm=descent,frame_bottom_mm=b[2]-descent,
                    assumed_hanging_length_mm=length,assumed_plan_spread_each_side_mm=spread,
                    swept_box_mm=envelope,candidates=hits,
                    floor_clearance_mm=envelope[2]))
    varal=dict(common,frame_box_mm=b,controller_max_descent_mm=860.,cases=rows,
        pairs_checked=len(rows)*len(fixed),fixed_parts=len(fixed),
        rows_with_candidates=sum(bool(r['candidates']) for r in rows),
        limits=['30 mm de altura e volume de reserva, nao quadro comercial.',
                'Comprimentos 500/800/1200 e acrescimos 0/50/100 mm sao hipoteses de roupa, nao limites de uso.',
                'A base CAD mantem alturas antigas; pe-direito de teste 2600 nao foi aplicado a ela.',
                'Nao avalia gases/calor, afastamentos do E21/duto, cordas/roldanas/comando ou ancoragem.',
                'Ausencia de candidato nao comprova acesso, alcance ou secagem.'])
    save('03_Ambientes/Lavanderia/Varal_percurso.json',varal)
    print(json.dumps(dict(P08_pairs=p08['pair_checks'],P08_candidates=len(pairs),
        varal_cases=len(rows),varal_candidates=varal['rows_with_candidates'])))
    for row in rows:
        if row['candidates']:print(json.dumps(row,ensure_ascii=False))


if __name__=='__main__':main()
