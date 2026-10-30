"""Quantidades nominais do desenho vigente; não altera CAD, orçamento ou site."""
import ast
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '03_Ambientes/Acabamentos'


def union_area(rects):
    """União exata de retângulos ortogonais (unidades do chamador)."""
    rects = [r for r in rects if r[2] > r[0] and r[3] > r[1]]
    xs = sorted({v for r in rects for v in (r[0], r[2])})
    total = 0.0
    for a, b in zip(xs, xs[1:]):
        intervals = sorted((r[1], r[3]) for r in rects if r[0] < b and r[2] > a)
        end = None
        length = 0.0
        for c, d in intervals:
            length += max(0, d - max(c, end if end is not None else c))
            end = max(d, end) if end is not None else d
        total += (b - a) * length
    return total


def clip(a, b):
    return (max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3]))


def inside(x, z, rects):
    return any(a <= x <= c and b <= z <= d for a, b, c, d in rects)


def js_json(path, name):
    s = path.read_text(encoding='utf-8')
    return json.JSONDecoder().raw_decode(s[s.index('=', s.index('const ' + name)) + 1:].lstrip())[0]


def array(s, name):
    return ast.literal_eval(re.search(r'const ' + name + r'=(\[.*?\]);', s).group(1))


def write_csv(name, rows):
    with (OUT / name).open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def liters_finished(area, yield_m2_l, allowance=0):
    """Rendimento acabado já inclui demãos; acréscimo é hipótese de reserva."""
    if yield_m2_l <= 0 or area < 0 or allowance < 0:
        raise ValueError('Área, rendimento ou reserva inválidos')
    return area * (1 + allowance) / yield_m2_l


def calculate(root=ROOT):
    source = root / 'ferramentas/site/src/app.js'
    s = source.read_text(encoding='utf-8')
    project = js_json(root / 'ferramentas/site/src/data.js', 'PROJECT')
    cad = js_json(root / 'ferramentas/site/src/cad-data.js', 'CAD_DATA')
    if cad['current_revision'] != 'R54':
        raise ValueError('Revisão diferente de R54: conferir premissas antes de regenerar')
    floors = array(s, 'floors')
    rooms = list(dict.fromkeys(r[0] for r in floors))
    fr = {r: [(x, z, x+w, z+d) for room, x, z, w, d, _ in floors if room == r] for r in rooms}
    # H01: prioridade apenas contábil à cozinha na sobreposição gráfica, não limite físico.
    priority = ['cozinha'] + [r for r in rooms if r != 'cozinha']
    xs = sorted({v for rects in fr.values() for r in rects for v in (r[0], r[2])})
    zs = sorted({v for rects in fr.values() for r in rects for v in (r[1], r[3])})
    exclusive = {r: 0 for r in rooms}
    for x, xx in zip(xs, xs[1:]):
        for z, zz in zip(zs, zs[1:]):
            owner = next((r for r in priority if inside((x+xx)/2, (z+zz)/2, fr[r])), None)
            if owner:
                exclusive[owner] += (xx-x)*(zz-z)/10000
    wall_rects = [(r[1], r[2], r[1]+r[3], r[2]+r[4]) for r in array(s, 'walls')]
    # H02: preencher graficamente os vãos para descontar área, sem medir obra.
    windows = [(60,90,180,100),(315,-10,430,0),(533,175,672,185),(245,569,255,675),(245,435,255,475)]
    doors = [(400,295,475,305),(365,315,375,390),(385,395,455,405),(740,615,750,690)]
    openings = [(r,95,205,'janela') for r in windows]+[(r,0,205,'porta') for r in doors]
    walls = wall_rects + windows + doors
    cutsx = sorted({v for r in walls for v in (r[0],r[2])}|set(xs))
    cutsz = sorted({v for r in walls for v in (r[1],r[3])}|set(zs))
    faces = []
    seen = set()
    for a,b,c,d in walls:
        for axis, fixed, lo, hi, sign in [('x',a,b,d,-1),('x',c,b,d,1),('z',b,a,c,-1),('z',d,a,c,1)]:
            cuts = sorted({lo,hi}|{v for v in (cutsz if axis=='x' else cutsx) if lo<v<hi})
            for u,v in zip(cuts,cuts[1:]):
                key=(axis,fixed,u,v,sign)
                if key in seen: continue
                seen.add(key)
                px,pz=(fixed+sign*.01,(u+v)/2) if axis=='x' else ((u+v)/2,fixed+sign*.01)
                if inside(px,pz,walls): continue
                room=next((r for r in priority if inside(px,pz,fr[r])),None)
                if room is None: continue
                h=project['ceilingByRoom'][room]
                holes=[]
                base_holes=[]
                for rect, bottom, top, kind in openings:
                    normal=(rect[0],rect[2]) if axis=='x' else (rect[1],rect[3])
                    span=(rect[1],rect[3]) if axis=='x' else (rect[0],rect[2])
                    if fixed in normal:
                        holes.append(clip((u,0,v,h),(span[0],bottom,span[1],top)))
                        if kind=='porta': base_holes.append((max(u,span[0]),0,min(v,span[1]),1))
                gross=(v-u)*h/10000
                opening=union_area(holes)/10000
                faces.append(dict(ambiente=room,eixo=axis,coordenada_cm=fixed,inicio_cm=u,fim_cm=v,
                                  altura_cm=h,parede_bruta_m2=round(gross,6),vaos_m2=round(opening,6),
                                  parede_liquida_m2=round(gross-opening,6),
                                  rodape_antes_moveis_m=round(((v-u)-union_area(base_holes))/100,6)))
    totals=[]
    for room in rooms:
        ff=[f for f in faces if f['ambiente']==room]
        totals.append(dict(ambiente=room,piso_bruto_uniao_m2=round(union_area(fr[room])/10000,6),
                           piso_sem_sobreposicao_H01_m2=round(exclusive[room],6),teto_projecao_H01_m2=round(exclusive[room],6),
                           parede_bruta_m2=round(sum(f['parede_bruta_m2'] for f in ff),6),
                           vaos_m2=round(sum(f['vaos_m2'] for f in ff),6),
                           parede_liquida_antes_revestimentos_moveis_m2=round(sum(f['parede_liquida_m2'] for f in ff),6),
                           rodape_antes_moveis_m=round(sum(f['rodape_antes_moveis_m'] for f in ff),6)))
    # Envelopes verticais de módulos altos: informativos, SEM descontar pintura automaticamente.
    cabinets=[]
    for module in cad['modules']:
        code=module.get('code',module.get('id'))
        parts=[p for p in cad['parts'] if p.get('module')==code]
        if not parts: continue
        x,z,y=min(p['x'] for p in parts),min(p['z'] for p in parts),min(p['y'] for p in parts)
        xx,zz,yy=max(p['x']+p['w'] for p in parts),max(p['z']+p['d'] for p in parts),max(p['y']+p['h'] for p in parts)
        if yy <150: continue
        cabinets.append(dict(modulo=code,ambiente=module['room'],x_cm=round(x,3),z_cm=round(z,3),base_cm=round(y,3),
                             largura_cm=round(xx-x,3),profundidade_cm=round(zz-z,3),altura_cm=round(yy-y,3),
                             projecao_largura_altura_m2=round((xx-x)*(yy-y)/10000,4),
                             desconto_adotado_m2=0,motivo='Envelope não comprova face encostada; pintura antes da montagem mantida'))
    # H03: envelope a até 5 cm de uma face; limite de ocultação, não área a deixar sem tinta.
    for face in faces:
        projected=[]
        axis=face['eixo']; fixed=face['coordenada_cm']
        for cab in cabinets:
            if cab['ambiente'] != face['ambiente']: continue
            normal=(cab['x_cm'],cab['x_cm']+cab['largura_cm']) if axis=='x' else (cab['z_cm'],cab['z_cm']+cab['profundidade_cm'])
            span=(cab['z_cm'],cab['z_cm']+cab['profundidade_cm']) if axis=='x' else (cab['x_cm'],cab['x_cm']+cab['largura_cm'])
            if min(abs(fixed-n) for n in normal)>5: continue
            projected.append(clip((face['inicio_cm'],0,face['fim_cm'],face['altura_cm']),
                                  (span[0],cab['base_cm'],span[1],cab['base_cm']+cab['altura_cm'])))
        holeclips=[]
        for rect,bottom,top,_ in openings:
            normal=(rect[0],rect[2]) if axis=='x' else (rect[1],rect[3])
            span=(rect[1],rect[3]) if axis=='x' else (rect[0],rect[2])
            if fixed in normal:
                holeclips.extend(clip(p,(span[0],bottom,span[1],top)) for p in projected)
        face['ocultacao_envelopes_H03_m2']=round((union_area(projected)-union_area(holeclips))/10000,6)
    for row in totals:
        row['ocultacao_envelopes_H03_m2']=round(sum(f['ocultacao_envelopes_H03_m2'] for f in faces if f['ambiente']==row['ambiente']),6)
        row['parede_aparente_H03_antes_revestimentos_m2']=round(row['parede_liquida_antes_revestimentos_moveis_m2']-row['ocultacao_envelopes_H03_m2'],6)
    return totals, faces, cabinets


def finishing(totals):
    """Cenários separados; parâmetros do orçamento conservados, sem alterá-lo."""
    by={r['ambiente']:r for r in totals}
    vinyl=sum(r['piso_sem_sobreposicao_H01_m2'] for r in totals if r['ambiente'] not in ('banho','lavanderia'))
    # H04: box nominal 0,80 x 1,24; não inclui desenvolvimento do enchimento/soleiras.
    wet=[dict(item='Piso EXT box',cenario='H04 planta do desenho',area_liquida_m2=.8*1.24,reserva_percentual=15),
         dict(item='Piso Satin fora box',cenario='H04 piso total menos box',area_liquida_m2=by['banho']['piso_sem_sobreposicao_H01_m2']-.8*1.24,reserva_percentual=15),
         dict(item='Piso lavanderia',cenario='cota oficial 1,29 x 1,54',area_liquida_m2=by['lavanderia']['piso_sem_sobreposicao_H01_m2'],reserva_percentual=15),
         dict(item='Duas paredes verdes',cenario='H05A gráfico: (0,80 + 1,24) x 2,25 menos janela 0,40 x 1,10; hipótese',area_liquida_m2=2.04*2.25-.4*1.1,reserva_percentual=15),
         dict(item='Duas paredes verdes',cenario='H05B gráfico até 2,50 menos janela; hipótese',area_liquida_m2=2.04*2.5-.4*1.1,reserva_percentual=15),
         dict(item='Duas paredes verdes',cenario='H05C orçamento: fundo 1,24 x 2,47 + janela 0,80 x 2,47 sem descontar abertura; hipótese',area_liquida_m2=(1.24+.8)*2.47,reserva_percentual=15),
         dict(item='Parede clara box',cenario='H05A: 0,80 x 2,25; hipótese gráfica',area_liquida_m2=.8*2.25,reserva_percentual=15),
         dict(item='Parede clara box',cenario='H05B: 0,80 x 2,50; hipótese',area_liquida_m2=.8*2.5,reserva_percentual=15),
         dict(item='Parede clara box',cenario='H05C orçamento remanescente: 0,80 x 2,47; hipótese',area_liquida_m2=.8*2.47,reserva_percentual=15)]
    for row in wet:
        row['area_com_reserva_m2']=round(row['area_liquida_m2']*(1+row['reserva_percentual']/100),6)
        row['area_liquida_m2']=round(row['area_liquida_m2'],6)
    paint=[]
    # Pedra de 10 cm explícita no app; extensão lateral e retornos não desenhados: ausentes.
    for row in totals:
        room=row['ambiente']
        deduction={'cozinha':1.869*.10,'lavanderia':1.33*.10,'banho':1.8+4.15}.get(room,0)
        net=row['parede_liquida_antes_revestimentos_moveis_m2']-deduction
        paint.append(dict(ambiente=room,cenario='H05A pintura completa antes dos móveis',
                          parede_pintura_m2=round(net,6),desconto_revestimento_m2=round(deduction,6),
                          parede_L_catalogo_150m2_por18L=round(liters_finished(net,150/18),4),
                          parede_L_reserva10_H06=round(liters_finished(net,150/18,.10),4),
                          parede_L_reserva20_H06=round(liters_finished(net,150/18,.20),4),
                          teto_m2=row['teto_projecao_H01_m2'],
                          teto_L_catalogo_6m2_por09L=round(liters_finished(row['teto_projecao_H01_m2'],6/.9),4),
                          teto_L_reserva20_H06=round(liters_finished(row['teto_projecao_H01_m2'],6/.9,.20),4),
                          rodape_m_antes_moveis=row['rodape_antes_moveis_m']))
    def comparison(item,budget,value,unit,cause):
        return dict(item=item,quantidade_orcamento=budget,quantidade_cenario=value,unidade=unit,
                    diferenca=round(value-budget,6) if isinstance(budget,(float,int)) else '',causa_limite=cause)
    comparisons=[comparison('R01 vinílico compra',35.8,round(vinyl,6),'m2','Compra inclui cortes; área líquida não prova redução de caixas nem repete plano de corte'),
                 comparison('Base R44 sete retângulos',31.4485,round(vinyl,6),'m2','Agora união sem dupla contagem; soleiras gráficas atuais incluídas, não somar novamente 0,48'),
                 comparison('R02/R03 serviço',34,round(vinyl,6),'m2','Área geométrica versus verba de serviço; mínimo/preparação podem persistir'),
                 comparison('R04 rodapé/transições',35,round(sum(r['rodape_antes_moveis_m'] for r in totals if r['ambiente'] not in ('banho','lavanderia')),6),'m','Antes de desconto de armários; transições e perdas não incluídas'),
                 comparison('R06 Satin área histórica',2.4,round(by['banho']['piso_sem_sobreposicao_H01_m2']-.992,6),'m2','Área líquida fora do box; quantidade por caixa do SKU pendente'),
                 comparison('R08 verde compra',3.74,round(5.0388*1.15,6),'m2','H05C: duas paredes, janela adicional 0,80 x 2,47 sem desconto; hipótese, não altera R44/caixas'),
                 comparison('R08B claro compra',5,round(1.976*1.15,6),'m2','H05C: uma parede clara restante, hipótese; não altera R44/caixas'),
                 comparison('R09 lavanderia compra',3.24,round(1.9866*1.15,6),'m2','Duas caixas vigentes de 1,62; reserva15% não implica reduzir a uma caixa'),
                 comparison('R11 base de assentamento',12,round(.992+(by['banho']['piso_sem_sobreposicao_H01_m2']-.992)+1.9866+1.8+4.15,6),'m2','H05A: pisos+paredes sem perdas; enchimento e arremates ausentes; não reduzir verba automaticamente'),
                 comparison('O06 tinta paredes',21.6,round(sum(p['parede_L_reserva20_H06'] for p in paint),4),'L','H05A catálogo acabado +20%; produto/cobertura real pendentes'),
                 comparison('O06 tinta teto',7.2,round(sum(p['teto_L_reserva20_H06'] for p in paint),4),'L','Rendimento normalizado da embalagem0,9L oficial; conferir embalagem exata antes de compra'),
                 comparison('O07 forro escritório',7,by['escritorio']['piso_sem_sobreposicao_H01_m2'],'m2','Projeção horizontal; faixas/cortineiros/minimum de serviço não calculados')]
    return wet,paint,comparisons


def main():
    OUT.mkdir(exist_ok=True)
    totals, faces, cabinets=calculate()
    wet,paint,comparisons=finishing(totals)
    write_csv('Quantidades_por_ambiente.csv',totals)
    write_csv('Faces_e_vaos.csv',faces)
    write_csv('Revestimentos_cenarios.csv',wet)
    write_csv('Pintura_por_ambiente.csv',paint)
    write_csv('Comparacao_orcamento.csv',comparisons)
    if cabinets: write_csv('Moveis_altos_sem_desconto.csv',cabinets)
    sources=['ferramentas/site/src/app.js','ferramentas/site/src/data.js','ferramentas/site/src/cad-data.js',
             '06_Entregas/Planta_cotada/Cotas.json','07_Imovel/Medidas_e_impactos.csv',
             'ferramentas/site/fabrication/Decisao_acabamentos_R13.md',
             '05_Orcamento_e_cronograma/Orcamento/Pisos_e_revestimentos/Revisao_pisos.json',
             '05_Orcamento_e_cronograma/Orcamento/Obra_e_pintura/Revisao_obra.json']
    write_csv('Fontes_locais.csv',[dict(arquivo=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in sources])
    print(json.dumps(totals,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
