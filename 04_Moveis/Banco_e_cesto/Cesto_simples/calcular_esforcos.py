"""Estática nominal para informar a operação manual; não dimensiona ferragens."""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'Consolidacao_R45_2026-10-23'
objects = json.loads((SOURCE / 'Inventario/Folhas_ativas_globais_R44.json').read_text(encoding='utf-8'))
by_name = {obj['name']: obj for obj in objects}
g = 9.80665

bench = []
for name in ('BancoR43_Painel1', 'BancoR43_Painel2'):
    box = by_name[name]['bbox']
    volume = math.prod(box[i + 3] - box[i] for i in range(3)) / 1e9
    # Eixo abstrato junto à borda traseira, NÃO eixo de produto selecionado.
    arm_cg = ((box[0] + box[3]) / 2 - 102) / 1000
    arm_hand = (box[3] - 102) / 1000
    for density in (650, 900):
        mass = volume * density
        bench.append(dict(tampa=name, densidade_kg_m3=density, massa_kg=mass,
                          torque_horizontal_Nm=mass * g * arm_cg,
                          forca_vertical_borda_horizontal_N=mass * g * arm_cg / arm_hand,
                          equivalente_kgf=mass * arm_cg / arm_hand))

front = by_name['PecaCestoR003']
frame = [by_name[f'PecaCestoR{i:03d}'] for i in range(4, 17)]
box = front['bbox']
# Pega ideal no centro superior da frente; não é uma posição real medida.
hand_y = (box[1] + box[4]) / 2
hand_z = box[5]
hand_radius = math.hypot(hand_y - 6440, hand_z - 120) / 1000

def moment(obj, density, angle):
    b = obj['bbox']
    dy = ((b[1] + b[4]) / 2 - 6440) / 1000
    dz = ((b[2] + b[5]) / 2 - 120) / 1000
    return obj['volume'] / 1e9 * density * g * (-dy * math.cos(angle) + dz * math.sin(angle))

hamper = []
for density in (650, 900):
    for degree in (0, 15, 30, 45, 55):
        angle = math.radians(degree)
        empty = sum(moment(obj, density, angle) for obj in [front, *frame])
        center = 8 * g * (-.125 * math.cos(angle) + .225 * math.sin(angle))
        envelope = [8 * g * (-dy * math.cos(angle) + dz * math.sin(angle))
                    for dy in (.025, .225) for dz in (.025, .425)]
        bounds = [empty + min(envelope), empty + max(envelope)]
        maximum = max(abs(x) for x in bounds) / hand_radius
        hamper.append(dict(densidade_kg_m3=density, angulo_graus=degree,
                           torque_vazio_Nm=empty, torque_cheio_central_Nm=empty + center,
                           torque_cheio_envelope_Nm=bounds,
                           maior_forca_tangencial_ideal_no_envelope_N=maximum,
                           equivalente_kgf=maximum / g))

result = dict(
    alcance='Estática nominal para comparar operação manual. Não valida produto, resistência, colisões ou ergonomia.',
    banco_premissas='Painéis retangulares homogêneos, almofadas retiradas, eixo abstrato X102. Exclui ferragens, atrito, mãos, choque e deformação.',
    cesto_premissas='Eixo ideal Y6440/Z120; frente + 13 peças de armação hipotéticas + 8 kg roupa. Exclui saco, ferragens e choques. Força tangencial ideal no topo; direção real da mão e pega alteram esforço.',
    cesto_raio_pega_ideal_m=hand_radius,
    banco=bench, cesto=hamper,
)
(HERE / 'Esforcos_nominais.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(banco=bench, cesto_55=[row for row in hamper if row['angulo_graus'] == 55]), ensure_ascii=False, indent=2))
