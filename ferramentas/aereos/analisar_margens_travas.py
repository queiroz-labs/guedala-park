"""Sensibilidade geometrica P14/P20; fontes salvas, sem CAD ou produto inventado."""
from pathlib import Path
import csv
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '04_Moveis/Banco_e_cesto/Cesto_simples/Conferencia'
SOURCE = OUT / 'Resultados.json'


def distance(s, angle):
    t = math.radians(angle)
    x, y = [p-a for p, a in zip(s['mobile'], s['axis'])]
    p = [s['axis'][0]+x*math.cos(t)-y*math.sin(t),
         s['axis'][1]+x*math.sin(t)+y*math.cos(t)]
    return math.dist(p, s['fixed'])


def inverse(s, length, stop):
    """Ramo crescente da distancia; nao extrapola alem da parada estudada."""
    v = [p-a for p, a in zip(s['mobile'], s['axis'])]
    w = [p-a for p, a in zip(s['fixed'], s['axis'])]
    r, q = math.hypot(*v), math.hypot(*w)
    phi = math.atan2(v[0]*w[1]-v[1]*w[0], sum(a*b for a, b in zip(v, w)))
    c = (r*r+q*q-length*length)/(2*r*q)
    if not -1 <= c <= 1:
        return None
    angle = math.degrees(phi+math.acos(c))
    if angle < 0 or angle > stop+1e-8:
        return None
    return min(angle, stop)


def main():
    sources = json.loads(SOURCE.read_text(encoding='utf-8'))['articuladores']
    rows, checks = [], 0
    for name, stop in [('banco_tampa1', 90), ('banco_tampa2', 90),
                       ('cesto_direito', 55), ('cesto_esquerdo', 55)]:
        s = next(x for x in sources if x['id'] == name)
        end = distance(s, stop)
        assert abs(end-291) < 1e-6
        assert inverse(s, 300, stop) is None
        for lock in [288., 290., 291.]:
            nominal = inverse(s, lock, stop)
            assert nominal is not None
            # Conferencia independente: rotacao cartesiana + bissecao.
            lo, hi = 45., stop
            assert distance(s, lo) < lock
            for _ in range(60):
                mid = (lo+hi)/2
                if distance(s, mid) < lock:
                    lo = mid
                else:
                    hi = mid
            assert abs((lo+hi)/2-nominal) < 1e-8
            checks += 1
            for error in [.5, 1., 2.]:
                # Discos independentes de raio error para cada centro de terminal.
                # Rotacao preserva norma: erro da distancia limitado por 2*error.
                early = inverse(s, lock-2*error, stop)
                late = inverse(s, lock+2*error, stop)
                assert early is not None and early <= nominal
                if late is not None:
                    assert late >= nominal
                    assert abs(distance(s, late)-(lock+2*error)) < 1e-6
                reserve = end-lock-2*error
                rows.append(dict(mechanism=name,stop_deg=stop,
                    assumed_lock_distance_mm=lock,terminal_radial_error_mm=error,
                    distance_error_bound_mm=2*error,nominal_lock_angle_deg=nominal,
                    earliest_bound_deg=early,latest_bound_deg=late,
                    reserve_at_stop_mm=reserve,
                    guaranteed_geometric_reach_in_error_model=reserve >= -1e-8,
                    physical_result=None))
    result = dict(scope='Sensibilidade, nao tolerancia de fabricacao ou validacao de trava',
        source=SOURCE.relative_to(ROOT).as_posix(),
        source_sha256=hashlib.sha256(SOURCE.read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
        hash_rule='UTF8 LF para a fonte JSON',physical_tests_executed=0,
        cad_opened=False,cad_changed=False,independent_inverse_checks=checks,
        model='Eixo fixo; erro de posicao de cada terminal limitado por disco de raio e. Limite de distancia 2e por desigualdade triangular.',
        limits=['e=0.5/1/2 mm e engates 288/290/291 mm sao hipoteses, nao dados do fabricante.',
                'Campo latest_bound_deg nulo: limite superior fora da parada; nao permite extrapolar o movimento.',
                'Nao inclui erro do eixo, deformacao, largura, corpos, ferramentas, folga de pinos ou tolerancia da propria trava.',
                'Reserva de distancia nao e curso de liberacao; mecanismo dobrado/retencao e resistencia nao demonstrados.',
                'Nenhum furo, batente, numero de articuladores ou produto selecionado por este estudo.'],
        cases=rows)
    (OUT/'Margens_travas.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (OUT/'Margens_travas.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter=';')
        writer.writeheader();writer.writerows(rows)
    print(json.dumps(dict(cases=len(rows),inverse_checks=checks,
        geometric_reach_cases=sum(x['guaranteed_geometric_reach_in_error_model'] for x in rows))))
    for row in rows:
        if row['assumed_lock_distance_mm']==290 and row['terminal_radial_error_mm']==1:
            print(row)


if __name__ == '__main__':
    main()
