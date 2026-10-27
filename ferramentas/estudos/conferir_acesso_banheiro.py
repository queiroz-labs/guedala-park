"""Faixas geometricas da retirada BC43; nao escolhe ferramentas ou novos percursos."""
from pathlib import Path
import gzip, hashlib, json

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'03_Ambientes/Banheiro/Fechamento_pre_entrega'


def main():
    source=ROOT/'02_Modelo_3D/Base_verificacao.json.gz'
    base=json.loads(gzip.decompress(source.read_bytes()));o=base['objetos']
    release=json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((ROOT/release['cadPath']).read_bytes()).hexdigest()==base['sha256']
    box=lambda n:o[n]['caixa_global']
    left,right,top=box('BC43_LateralE'),box('BC43_LateralD'),box('BC43_Travessa')
    door,wall,stone=box('Peca075'),box('Peca051'),box('Peca399')
    ref=ROOT/'04_Moveis/Avanco_pendencias/Banheiro_solucao/Detalhamento/Obstaculo_manutencao.json'
    toilet=json.loads(ref.read_text(encoding='utf-8'))['bbox']
    toilet_names=[n for n,v in o.items() if v.get('caixa_global')==toilet]
    assert toilet_names, 'Reconciliar volume do vaso com R52'
    dowels=[box(n) for n in o if n.startswith('BC43_CavilhaRemovivel')]
    insertion=max(b[4] for b in dowels)-left[4]
    gap_door=left[1]-door[4]
    shift_min=door[3]-left[0]
    shift_max=toilet[0]-right[3]
    axis_x=(box('BC43_M6E0')[0]+box('BC43_M6E0')[3])/2
    tool_radius_limit=axis_x-wall[3]
    assert (insertion,gap_door,shift_min,shift_max,tool_radius_limit)==(15.,70.,100.,157.5,11.)
    first=[]
    for length in [700.,725.,740.,750.,755.]:
        for margin in [0.,2.,5.,10.]:
            lo=insertion+margin
            hi=gap_door-(length-700)-margin
            feasible=hi>=lo
            if feasible:
                mid=(lo+hi)/2
                assert mid-insertion>=margin-1e-8
                assert gap_door-(length-700)-mid>=margin-1e-8
            first.append(dict(assumed_entry_door_length_mm=length,margin_each_constraint_mm=margin,
                withdrawal_lower_mm=lo,withdrawal_upper_mm=hi,interval_nonempty=feasible,
                positive_interval=hi>lo,original_20mm_within_interval=lo<=20<=hi))
    lateral=[]
    for added in [0.,10.,20.,30.]:
        lo,hi=shift_min+added,shift_max-added
        lateral.append(dict(assumed_added_envelope_each_side_mm=added,
            lateral_shift_lower_mm=lo,lateral_shift_upper_mm=hi,interval_nonempty=lo<=hi,
            original_120mm_residual_door_mm=120-shift_min-added,
            original_120mm_residual_toilet_mm=shift_max-120-added))
    tools=[dict(assumed_tool_diameter_mm=d,wall_clearance_mm=tool_radius_limit-d/2)
           for d in [11.,12.,16.,20.,22.,24.]]
    result=dict(cad_sha256=base['sha256'],base_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        cad_opened=False,cad_changed=False,physical_tests_executed=0,
        source_toilet_objects=toilet_names,frame_outer_box_mm=[left[0],left[1],left[2],right[3],right[4],right[5]],
        door_box_mm=door,toilet_box_mm=toilet,dowel_insertion_mm=insertion,
        stone_vertical_gap_mm=stone[2]-top[5],first_withdrawal_cases=first,
        lateral_cases=lateral,tool_cases=tools,
        maximum_symmetric_lateral_added_envelope_mm=(shift_max-shift_min)/2,
        limits=['Faixas aritmeticas para a sequencia existente: retirar, transladar, retirar. Nao varredura de uma rota nova.',
                'Porta700 e poses do vaso sao gabaritos, nao levantamento; macaneta/maos ausentes.',
                'Margens e diametros sao sensibilidades; nao tolerancias/escolhas de ferramenta.',
                'Intervalo reduzido a um ponto com margem zero implica contato e nao libera operacao.',
                'Raio da ferramenta trata so a parede esquerda e eixo M6, nao acesso completo, torque ou comprimento.',
                'Quadro deve ser apoiado antes de retirar fixacoes; resistencia, massas reais e suspensao nao demonstradas.'])
    (OUT/'Acesso_manutencao_T05.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(first_cases=len(first),lateral=lateral,tool=tools,
        stone_gap=result['stone_vertical_gap_mm'],toilet=toilet_names),ensure_ascii=True))


if __name__=='__main__':main()
