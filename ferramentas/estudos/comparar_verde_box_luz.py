"""Isola a troca clara→Sauge na janela, com malha, raios e luminárias idênticos."""
from pathlib import Path
import json
import numpy as np
import estudo_fotometrico as f


def compare(out=f.OUT):
    g=f.load_geometry();ies=json.loads((f.OUT/'Fotometria_fontes.json').read_text(encoding='utf-8'))['EVO_2021']
    engine=f.Radiosity(f.scene_faces(g));engine.transport()
    selected=np.array([p['label']=='Sauge_janela_H13' for p in engine.patches])
    area=float(engine.area[selected].sum());rows=[]
    case=next(c for c in f.calculation_cases(g) if c['id']=='banho_geral')
    lights=f.case_lights(case,f.emitters(g));q,emitted=engine.deposit(lights,f.SCENARIOS['central'],ies)
    grids={'box_plano075':f.cells([[2.55,4.05,3.35,5.29]],.75,.10),'banho_geral':case['grid']}
    for name,grid in grids.items():
        direct=np.array([f.direct(c,lights,f.SCENARIOS['central'],ies,f.obstacles_for(g,case)) for c in grid])
        for band,label in enumerate(('baixo','central','alto')):
            values={}
            for variant,rho in (('uma_parede',(.5,.625,.75)),('duas_paredes',(.1,.2,.3))):
                engine.rho[selected]=rho
                B,balance=engine.solve(q,emitted,band)
                assert abs(balance['erro_lm'])<1e-6
                values[variant]=f.statistics(grid,direct+engine.reflected_lux(grid,B))
            a,b=values.values()
            rows.append(dict(caso=name,faixa_rho=label,plano_m=.75,area_sensor_m2=round(b['area'],6),
                area_janela_clara_para_verde_m2=round(area,6),rho_antes=(.5,.625,.75)[band],rho_depois=(.1,.2,.3)[band],
                media_uma_lx=round(a['mean'],3),media_duas_lx=round(b['mean'],3),
                delta_lx=round(b['mean']-a['mean'],3),delta_percentual=round(100*(b['mean']/a['mean']-1),3),
                minimo_uma_lx=round(a['min'],3),minimo_duas_lx=round(b['min'],3),
                u0_uma=round(a['u0'],6),u0_duas=round(b['u0'],6)))
    f.write_csv(out/'Comparacao_verde_box_luz.csv',rows)
    lines=['# Verde nas duas paredes do box','',
           'Fonte da mudança: Elias, 30/10/2026, nesta conversa: “quero que esteja na parede da janela tbm”. Aprovação técnica: PENDENTE.',
           '', 'Comparação H13, sem luz natural: somente a refletância difusa da face interna da janela muda. Mesma malha, semente, raios, fontes e geometria nas duas soluções; abertura preservada. Não é medida real nem fotometria do produto.',
           '', f'Face exposta convertida no modelo de luz: {area:.4f} m², após abertura/ocultações; não serve para compra. Faixas claras 0,50/0,625/0,75 → Sauge 0,10/0,20/0,30, hipóteses sem ensaio de refletância.',
           '', 'Um Firefly B11, posição/fluxo/manutenção centrais existentes; espelho e indireta desligados, como no cenário geral anterior. Sensor no box a 0,75 m, malha 0,10 m. O outro sensor mantém a malha geral do estudo.',
           '', '| Sensor | Faixa | Uma parede (lx) | Duas (lx) | Diferença |','|---|---|---:|---:|---:|']
    lines += [f"| {r['caso']} | {r['faixa_rho']} | {r['media_uma_lx']} | {r['media_duas_lx']} | {r['delta_percentual']}% |" for r in rows]
    lines += ['', 'O verde devolve menos luz difusa: o box tende a ficar mais escuro com a mesma luminária. A ordem de grandeza depende das refletâncias e curvas ainda ausentes; faixas não são intervalos estatísticos. Conferir no local antes de decidir reforço. Nenhuma luminária, compra, potência ou circuito foi alterado.',
              '', '[Valores, mínimos e uniformidade](Comparacao_verde_box_luz.csv). Reproduzir: `python -B ferramentas/estudos/comparar_verde_box_luz.py`.']
    (out/'Verde_box_luz.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    return rows


if __name__=='__main__':
    for row in compare():print(row)
