"""Triagem nominal: parcelas conhecidas, opções elétricas e clima TMY; não dimensiona AC."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '03_Ambientes/Equipamentos'
BTU_PER_WH = 3.412141633
OPTIONS = [('LG S3-Q09AA31C', 9000, 780, 150, 220),
           ('LG S3-Q12JA33K', 12000, 1130, 200, 220),
           ('LG S3-W18KL31C', 18000, 1600, 210, 220),
           ('Ventisol Mistral DC controle', 0, 30, None, 127),
           ('Sem equipamento adicional', 0, 0, 0, 127)]


def energy(watts, hours, days=30):
    if min(watts, hours, days) < 0:
        raise ValueError('Valores negativos')
    return watts * hours * days / 1000


def union_area(rects):
    xs = sorted({x for r in rects for x in (r[0], r[0]+r[2])})
    ys = sorted({y for r in rects for y in (r[1], r[1]+r[3])})
    return sum((b-a)*(d-c) for a,b in zip(xs,xs[1:]) for c,d in zip(ys,ys[1:])
               if any(x <= (a+b)/2 < x+w and y <= (c+d)/2 < y+h for x,y,w,h in rects))


def write_csv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def equipment_audit(inputs):
    """Rastreia todas as entradas; somente ASUS tem parcela condicional nesta zona."""
    rows=[]
    for r in inputs:
        known=r['potencia_W']!=''
        included=r['id']=='EQ28A' and known
        if included:
            reason='H06: ASUS ligado, referencia publicada; dissipacao sensivel integral condicional, nao maximo'
        elif not known:
            reason='Potencia de entrada ausente; nao equivale a zero'
        else:
            reason='Cozinha/lavanderia: entrada eletrica conhecida; fracao para ar, extracao/agua e transferencia de zona ausentes'
        rows.append(dict(id=r['id'],ambiente=r['ambiente'],item=r['item'],
            entrada_referencia_W=r['potencia_W'],qualidade=r['qualidade'],
            parcela_sensivel_H06_W=float(r['potencia_W']) if included else '',
            tratamento=reason,fonte=r['fonte']))
    return rows


def partial_gain(people, light, fraction, equipment):
    sensible=72*people+light*fraction+equipment
    latent=45*people
    return sensible,latent


def generate():
    sys.path.insert(0, str(ROOT/'ferramentas/pranchas'))
    from gerar import Projeto
    p=Projeto()  # exportação existente; não abre nem salva FreeCAD
    floors={}
    for r in p.data['floors']:
        floors.setdefault(r['room'], []).append([p.m(k).mm/1000 for k in r['refs']])
    light={}
    with (ROOT/'03_Ambientes/Iluminacao/Correntes_luz.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f, delimiter=';'):
            light[r['ambiente']]=light.get(r['ambiente'],0)+float(r['W_entrada_cenario'])
    inputs=ROOT/'03_Ambientes/Planta_pontos/Cargas_entradas.csv'
    with inputs.open(encoding='utf-8-sig') as f:
        audit=equipment_audit(list(csv.DictReader(f,delimiter=';')))
    write_csv(OUT/'Climatizacao_equipamentos.csv',audit)
    rows=[]
    for room in ('quarto','sala','escritorio'):
        for scenario,n,frac in [('otimista_parcial',1,.25),('central_parcial',2,.5),('conservador_parcial',3,1)]:
            equipment=sum(r['parcela_sensivel_H06_W'] for r in audit
                          if r['ambiente']==room and r['parcela_sensivel_H06_W']!='')
            missing=sum(r['entrada_referencia_W']=='' for r in audit if r['ambiente']==room)
            sensible,latent=partial_gain(n,light[room],frac,equipment)
            rows.append(dict(ambiente=room,cenario=scenario,area_modelada_m2=round(union_area(floors[room]),4),
                altura_hipotese_m=2.6,volume_nominal_m3=round(union_area(floors[room])*2.6,4),
                pessoas_H02=n,luz_instalada_W=round(light[room],2),fracao_luz_H03=frac,
                ganho_sensivel_parcial_W=round(sensible,2),ganho_latente_parcial_W=latent,
                ganho_interno_parcial_W=round(sensible+latent,2),ganho_interno_parcial_BTU_h=round((sensible+latent)*BTU_PER_WH,1),
                equipamentos_referencia_H06_W=equipment,equipamentos_sem_potencia=missing,
                envoltoria_solar_infiltracao_W='dado ausente',
                carga_total_W='',carga_total_BTU_h='',situacao='pessoas+luz+referencia condicional; não é faixa de dimensionamento'))
    write_csv(OUT/'Climatizacao_parcelas.csv',rows)
    rows=[]
    for sku,btu,power,pmin,voltage in OPTIONS:
        for hours in (2,4,8):
            rows.append(dict(opcao=sku,capacidade_nominal_BTU_h=btu,entrada_nominal_W=power,
                entrada_min_catalogo_W='' if pmin is None else pmin,tensao_catalogo_V=voltage,
                corrente_P_V_equivalente_A=round(power/voltage,3),FP='ausente',
                horas_dia_H04=hours,kWh_mes_nominal_constante=energy(power,hours),
                kWh_mes_min_constante='' if pmin is None else energy(pmin,hours),
                situacao='opção; consumo real e corrente dimensionante não determinados'))
    write_csv(OUT/'Climatizacao_opcoes.csv',rows)


def climate(epw, output):
    raw=epw.read_bytes(); lines=raw.decode('utf-8-sig').splitlines()
    lines=[s for s in lines if s.strip()]
    header=next(csv.reader([lines[0]]))
    if header[0]!='LOCATION' or header[5]!='837800':
        raise ValueError('Esperado Congonhas 837800')
    rows=[]
    for r in csv.reader(lines[8:]):
        if len(r)<22: raise ValueError('Linha EPW incompleta')
        t,ur,ghi,dni,dhi=map(float,(r[6],r[8],r[13],r[14],r[15]))
        if t>=99 or ur>100 or max(ghi,dni,dhi)>=9999: raise ValueError('EPW contém dado ausente')
        rows.append(dict(mes=int(r[1]),dia=int(r[2]),hora_final=int(r[3]),temperatura_C=t,
                         UR_pct=ur,global_horizontal_Wh_m2=ghi,direta_normal_Wh_m2=dni,difusa_horizontal_Wh_m2=dhi))
    if len(rows)!=8760: raise ValueError('TMY deve conter 8760 horas')
    output.parent.mkdir(parents=True,exist_ok=True); write_csv(output,rows)
    summary=dict(estacao=header[1],periodo='TMYx 2011-2025',horas=len(rows),epw_sha256=hashlib.sha256(raw).hexdigest(),
                 csv_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),min_C=min(r['temperatura_C'] for r in rows),
                 max_C=max(r['temperatura_C'] for r in rows),media_C=round(sum(r['temperatura_C'] for r in rows)/len(rows),2),
                 horas_acima_24_C=sum(r['temperatura_C']>24 for r in rows),
                 limite='clima de estação, não temperatura interior nem carga horária')
    (OUT/'Climatizacao_clima_resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return summary


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--epw',type=Path);ap.add_argument('--clima-csv',type=Path)
    args=ap.parse_args();generate()
    if args.epw:
        if not args.clima_csv: ap.error('--clima-csv obrigatório fora do repositório')
        if args.clima_csv.resolve().is_relative_to(ROOT): ap.error('Série horária volumosa deve ficar fora do git')
        print(json.dumps(climate(args.epw,args.clima_csv),ensure_ascii=False))
