"""Sensibilidades analíticas da envoltória; não estima Rw/DnT,w da unidade."""
import csv
import hashlib
import math
from pathlib import Path

from acustica_cenarios import base_homogenea, somar_niveis

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '03_Ambientes/Acustica/Envoltoria'
FREQUENCIAS = (100, 125, 160, 200, 250, 315, 400, 500, 630, 800,
               1000, 1250, 1600, 2000, 2500, 3150)


def massa_normal(massa, frequencia, rho=1.2, c=343):
    """Folha flácida infinita, incidência normal; impedância i*omega*m.

    H-ar: rho=1.2 kg/m³ e c=343 m/s. Sem rigidez, vazios ou coincidência.
    Não é lei difusa, Rw, curva Sharp ou modelo validado de bloco vazado.
    """
    if min(massa, frequencia, rho, c) <= 0:
        raise ValueError('Parâmetros devem ser positivos')
    return 10 * math.log10(1 + (math.pi * frequencia * massa / (rho*c))**2)


def composto(componentes):
    """Pares (área, R por banda). Não ponderar índices Rw desta maneira."""
    if not componentes or any(s <= 0 or r < 0 for s, r in componentes):
        raise ValueError('Áreas positivas e reduções não negativas necessárias')
    area = sum(s for s, _ in componentes)
    return -10*math.log10(sum(s*10**(-r/10) for s, r in componentes)/area)


def perda_flancos(q):
    """q = energia marginal/direta H; NÃO é previsão ISO 12354."""
    if q < 0:
        raise ValueError('Energia negativa')
    return somar_niveis([0, 10*math.log10(q)]) if q else 0.0


def ressonancia(m1, m2, d):
    """Duas massas e mola de ar por unidade de área, sem pontes rígidas."""
    if min(m1, m2, d) <= 0:
        raise ValueError('Massas e cavidade positivas necessárias')
    return math.sqrt(1.2*343**2/d*(1/m1+1/m2))/(2*math.pi)


def corrigir_fundo(total, fundo):
    """Subtração energética; protocolo indicativo exige margem >=10 dB."""
    if total-fundo < 10:
        raise ValueError('Margem insuficiente para o protocolo indicativo')
    return 10*math.log10(10**(total/10)-10**(fundo/10))


def fronteiras():
    """Inventário de faces do modelo; não atribui vizinho por suposição.

    Segmentos disjuntos existentes são agregados só na mesma face/cômodo.
    Duas faces de uma parede interna pertencem a recintos diferentes.
    """
    fonte = ROOT / '03_Ambientes/Acabamentos/Faces_e_vaos.csv'
    groups = {}
    for n, row in enumerate(csv.DictReader(fonte.read_text(encoding='utf-8-sig').splitlines()), 2):
        key = row['ambiente'], row['eixo'], row['coordenada_cm']
        g = groups.setdefault(key, {'comprimento_m': 0, 'area_bruta_m2': 0,
                                   'vaos_m2': 0, 'area_liquida_m2': 0, 'linhas': []})
        g['comprimento_m'] += (float(row['fim_cm'])-float(row['inicio_cm']))/100
        for dest, src in [('area_bruta_m2','parede_bruta_m2'), ('vaos_m2','vaos_m2'),
                          ('area_liquida_m2','parede_liquida_m2')]:
            g[dest] += float(row[src])
        g['linhas'].append(str(n))
    result = []
    for (room, axis, coord), g in sorted(groups.items()):
        # As faces com janela são observáveis na planta da unidade. A vizinhança
        # dos demais segmentos não pode ser inferida de área, espessura ou cor.
        janela = (room, axis, coord) in {('quarto','z','100'), ('escritorio','z','0'),
                   ('sala','z','185'), ('banho','x','255'), ('lavanderia','x','255')}
        porta = (room,axis,coord) == ('cozinha','x','740')
        result.append(dict(id=f'{room}_{axis}{coord}', ambiente=room, eixo=axis,
            coordenada_cm=coord, comprimento_m=round(g['comprimento_m'],5),
            area_bruta_m2=round(g['area_bruta_m2'],6), vaos_m2=round(g['vaos_m2'],6),
            area_liquida_m2=round(g['area_liquida_m2'],6),
            outro_lado=('exterior na janela; restante a confirmar' if janela else
                        'acesso comum na porta; restante a confirmar' if porta else
                        'a confirmar: interno/unidade/hall/escada/elevador/shaft/exterior'),
            fonte='Acabamentos/Faces_e_vaos.csv linhas '+','.join(g['linhas']),
            limite='faces e vaos nominais; nao paredes medidas nem mapa seguro de vizinhos'))
    return result


def cenarios():
    rows = []
    def add(tipo, caso, entrada, valor, metrica, limite):
        rows.append(dict(tipo=tipo, caso=caso, entrada=entrada, resultado=round(valor,4),
                         metrica=metrica, limite=limite))
    # Massas de peças comerciais distintas. Junta 10 mm H nos blocos Tatu;
    # não se presume o fornecedor, resistência ou graute do Guedala.
    bases = {'ceramico14_BR12':7.124*12.5, 'ceramico19_BR13':8*12.5,
             'concreto14_BR14':9.53/(.30*.20), 'concreto19_BR15':17.97/(.40*.20)}
    for name, base in bases.items():
        for revest in (20,60):
            for graute in (0,100):
                massa = base+revest+graute
                for f in FREQUENCIAS:
                    add('massa_parede_H',name, f'f={f} Hz; m={massa:.4f}; revest={revest}; graute={graute}',
                        massa_normal(massa,f),'R_normal_H_dB',
                        'massas adicionais arbitrarias kg/m2; nao Rw; sem coincidencia; nao bloco real')
    for t in (.10,.12,.14):
        for rho in (2300,2500):
            m=t*rho
            for f in FREQUENCIAS:
                add('massa_laje_H',f't={t}; rho={rho}',f'f={f} Hz; m={m}',massa_normal(m,f),
                    'R_normal_H_dB','laje macica HIPOTESE; nao Rw ou desempenho de campo')
            add('impacto_base_H',f't={t}; rho={rho}',f'm={m}',base_homogenea(m),
                'Lnw_eq_base_H_dB','base homogenea somente; piso superior desconhecido; NAO Lntw')
    for q in (0,.25,1,3):
        add('flancos_H','razao energetica',f'q={q}',perda_flancos(q),'perda_H_dB',
            'varredura arbitraria; nao ISO 12354 nem conversao Rw para DnTw')
    for frac in (.001,.01,.05):
        for r in (0,10,20):
            add('ponto_fraco_H','parede R=50 por banda',f'fracao={frac}; R_fraco={r}',
                composto([(1-frac,50),(frac,r)]),'R_composto_H_dB',
                'fracao hipotetica; caixa/shaft/visita sem caracterizacao real')
    for r in (20,30,40):
        for gap in (0,.001,.003,.010):
            s=.8*gap
            rd=composto([(1.6-s,r)]+([(s,0)] if s else []))
            add('porta_H',f'folha R={r}',f'porta=0.8x2 m; fresta={gap} m',rd,
                'R_porta_composto_H_dB','R por banda constante H; nao Rw tipico de material')
            add('parede_porta_H',f'parede R=50; folha R={r}',f'area total=10 m2; fresta={gap} m',
                composto([(8.4,50),(1.6,rd)]),'R_composto_H_dB',
                'parede e porta HIPOTETICAS; nao area real de entrada ou DnTw')
    for m1 in (150,350):
        for m2 in (10,20):
            for d in (.03,.05,.10):
                add('ressonancia_H','massa-mola-massa',f'm1={m1}; m2={m2}; d={d}',
                    ressonancia(m1,m2,d),'f0_H_Hz','sem pontes rigidas/amortecimento; nao DeltaRw')
    return rows


def escrever(path, rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';')
        writer.writeheader(); writer.writerows(rows)


def gerar():
    OUT.mkdir(parents=True,exist_ok=True)
    for filename, data in [('Cenarios_envoltoria.csv',cenarios()),('Fronteiras.csv',fronteiras())]:
        p=OUT/filename; escrever(p,data)
        print(filename,len(data),hashlib.sha256(p.read_bytes()).hexdigest())


if __name__ == '__main__':
    gerar()
