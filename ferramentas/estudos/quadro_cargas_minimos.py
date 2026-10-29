"""Mínimos nominais por recinto, sem dimensionamento de execução."""
import ast
import csv
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '03_Ambientes/Planta_pontos'


def union_geometry(rects, excluded=()):
    """União/diferença ortogonal exata por células das bordas; cm -> m²/m."""
    all_rects = list(rects) + list(excluded)
    xs = sorted({v for r in all_rects for v in (r[0], r[2])})
    ys = sorted({v for r in all_rects for v in (r[1], r[3])})
    def inside(x, y, rs):
        return any(a < x < c and b < y < d for a, b, c, d in rs)
    cells = set()
    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            x, y = (xs[i]+xs[i+1])/2, (ys[j]+ys[j+1])/2
            if inside(x, y, rects) and not inside(x, y, excluded):
                cells.add((i,j))
    area = perimeter = 0
    for i,j in cells:
        w,h = xs[i+1]-xs[i], ys[j+1]-ys[j]
        area += w*h
        for dx,dy,length in [(-1,0,h),(1,0,h),(0,-1,w),(0,1,w)]:
            if (i+dx,j+dy) not in cells: perimeter += length
    return area/10000, perimeter/100


def minimum_points(kind, area, perimeter):
    if min(area, perimeter) <= 0: raise ValueError('Geometria não positiva')
    if kind == 'banheiro': return 1
    if kind == 'molhado': return math.ceil(perimeter/3.5-1e-10)
    if kind == 'sala_dormitorio' or area > 6: return math.ceil(perimeter/5-1e-10)
    return 1


def lighting_va(area):
    if area <= 0: raise ValueError('Área não positiva')
    return 100 + 60*max(0, math.floor((area-6)/4+1e-10))


def socket_va(n, wet, reduction=False):
    high = min(n, 2 if reduction else 3) if wet else 0
    return high*600+(n-high)*100


def main():
    source = ROOT/'ferramentas/site/src/app.js'
    floors = ast.literal_eval(re.search(r'const floors=(\[.*?\]);', source.read_text(encoding='utf-8')).group(1))
    rooms = list(dict.fromkeys(r[0] for r in floors))
    rects = {room:[(x,y,x+w,y+h) for r,x,y,w,h,_ in floors if r == room] for room in rooms}
    inputs = [dict(ambiente=r,x_cm=x,y_cm=y,largura_cm=w,profundidade_cm=h) for r,x,y,w,h,_ in floors]
    rows = []
    for room in rooms:
        excluded = rects['cozinha'] if room == 'sala' else []
        area,p = union_geometry(rects[room], excluded)
        bruto,_ = union_geometry(rects[room])
        kind = 'banheiro' if room == 'banho' else ('molhado' if room in ('cozinha','lavanderia') else ('sala_dormitorio' if room in ('sala','quarto') else 'outro'))
        n = minimum_points(kind,area,p)
        rows.append(dict(ambiente=room,cenario='recintos nominais separados',area_bruta_m2=round(bruto,6),area_exclusiva_m2=round(area,6),perimetro_contorno_m=round(p,6),criterio=kind,pontos_TUG_minimos=n,TUG_minimo_VA=socket_va(n,kind in ('banheiro','molhado')),TUG_alternativa_reducao_VA='',iluminacao_minima_VA=lighting_va(area),pontos_luz_referencia=1,geometria='app.js floors; união; cozinha precede sala na sobreposição',limite='contorno inclui linhas virtuais nas conexões abertas; não metros de parede disponível'))
    wet_total = sum(r['pontos_TUG_minimos'] for r in rows if r['criterio'] in ('banheiro','molhado'))
    if wet_total > 6:
        for r in rows: r['TUG_alternativa_reducao_VA'] = socket_va(r['pontos_TUG_minimos'],r['criterio'] in ('banheiro','molhado'),True)
    for name,data in [('Minimos_por_recinto.csv',rows),('Minimos_geometria.csv',inputs)]:
        with (OUT/name).open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]),delimiter=';');w.writeheader();w.writerows(data)
    a,p = union_geometry(rects['sala']+rects['cozinha'])
    result=dict(fonte='ferramentas/site/src/app.js',sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                pontos_TUG=sum(r['pontos_TUG_minimos'] for r in rows),TUG_VA=sum(r['TUG_minimo_VA'] for r in rows),
                pontos_molhados=wet_total,TUG_alternativa_VA=sum(r['TUG_alternativa_reducao_VA'] for r in rows) if wet_total>6 else None,
                iluminacao_VA=sum(r['iluminacao_minima_VA'] for r in rows),
                sala_cozinha_uniao=dict(area_m2=round(a,6),perimetro_m=round(p,6),iluminacao_VA=lighting_va(a),pontos_TUG=None,nota='Diagnóstico geométrico, não somar à tabela; classificação de recinto aberto com usos distintos pendente'),
                norma='ABNT NBR 5410:2004 Versão Corrigida:2008; 9.5.2.1.2 e 9.5.2.2')
    (OUT/'Minimos_resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__': main()
