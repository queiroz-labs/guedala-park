"""T05: cadeia vertical da alternativa ME23P, sem adotar ou editar o CAD."""
from pathlib import Path
import hashlib
import itertools
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'04_Moveis/Proximas_decisoes/Instalacao_e_P16'
SOURCE = OUT/'Micro_estudo.json'


def main():
    src = json.loads(SOURCE.read_text(encoding='utf-8'))
    shelf = src['old_boxes']['Peca350']
    appliance = src['old_boxes']['Peca351']
    cabinet = src['cabinet_bottom_mm']
    counter = 920.  # Referencia nominal do estudo existente, nao medida no imovel.
    required = 300.  # Requisito transcrito no estudo; nao nova validacao termica.
    height = appliance[5]-appliance[2]
    thickness = shelf[5]-shelf[2]
    gap = cabinet-appliance[5]
    work = shelf[2]-counter
    assert appliance[2] == shelf[5]
    assert (height, thickness, gap, work) == (290., 18., 100., 612.)
    assert src['proposed_upper_gap_mm'] == 300
    assert src['extra_margin_over_minimum_mm'] == 0
    cases, vertices = [], 0
    for e in [0., 2., 5.]:
        # Sensibilidade igual por grandeza; nao especificacao de tolerancias.
        # Aereo, altura do aparelho, topo da prateleira, espessura, bancada.
        for lowering in [200., 206., 215.]:
            nominal_upper = gap+lowering
            nominal_work = work-lowering
            upper_min = nominal_upper-3*e
            work_min = nominal_work-3*e
            measured = []
            for ec, eh, es, et, eb in itertools.product([-e, e], repeat=5):
                s = shelf[5]-lowering+es
                measured.append((cabinet+ec-(s+height+eh),
                                 s-(thickness+et)-(counter+eb)))
            assert abs(min(x[0] for x in measured)-upper_min) < 1e-8
            assert abs(min(x[1] for x in measured)-work_min) < 1e-8
            vertices += len(measured)
            cases.append(dict(assumed_error_per_quantity_mm=e,
                hypothetical_lowering_mm=lowering,
                nominal_upper_gap_mm=nominal_upper,
                minimum_upper_gap_in_error_model_mm=upper_min,
                upper_requirement_met_in_error_model=upper_min >= required,
                nominal_counter_clearance_mm=nominal_work,
                minimum_counter_clearance_in_error_model_mm=work_min,
                adopted=False))
    budgets = [dict(error_per_quantity_mm=e,
        minimum_lowering_for_upper_gap_mm=200+3*e,
        maximum_user_clearance_compatible_mm=412-6*e) for e in [0.,2.,5.]]
    result = dict(scope='Cadeia dimensional da alternativa separada; nao instalacao aprovada',
        source=SOURCE.relative_to(ROOT).as_posix(),
        source_sha256=hashlib.sha256(SOURCE.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        hash_rule='UTF8 LF',cad_opened=False,cad_changed=False,adopted=False,
        physical_tests_executed=0,vertex_checks=vertices,
        datums=dict(cabinet_bottom_mm=cabinet,counter_top_mm=counter,
                    shelf_thickness_mm=thickness,appliance_height_mm=height,
                    upper_requirement_transcribed_from_existing_study_mm=required),
        equations=dict(upper_gap='100 + delta - ec - eh - es (pior caso)',
                       counter_clearance='612 - delta - es - et - eb (pior caso)',
                       feasible_lowering_interval='[200+ec+eh+es, 612-Huso-es-et-eb]',
                       compatibility='Huso <= 412-(ec+eh+es)-(es+et+eb)'),
        cases=cases,budgets=budgets,
        shelf_edge_offsets_mm=dict(left=appliance[0]-shelf[0],
            right=shelf[3]-appliance[3],front=appliance[1]-shelf[1],
            back=shelf[4]-appliance[4]),
        limits=['Erros sao magnitudes independentes hipoteticas, nao tolerancias especificadas.',
                'Huso ainda nao definido. Margem superior e uso da bancada disputam o mesmo espaco.',
                'Os dois minimos de folga podem ocorrer em vertices diferentes: nao sao um unico estado medido.',
                'Apoio do aparelho coincide com seu envelope inferior na fonte; confirmar pes, apoio e altura instalada.',
                'Distancias as bordas da prateleira nao sao distancias a paredes nem prova de ventilacao.',
                'Sem desenho de ancoragem, desempenho termico, ergonomia, porta aberta ou retirada de cabo.',
                'F104 e alternativa de 200 mm preservadas; nao aplicar 206/215 mm ao CAD.'])
    (OUT/'Margens_instalacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(cases),vertex_checks=vertices,budgets=budgets)))


if __name__ == '__main__':
    main()
