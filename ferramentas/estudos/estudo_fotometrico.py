"""Estudo de luz reproduzível; lê exportações R54, nunca abre/salva FreeCAD.

Fontes comerciais são as da lista curta. Hipóteses não são dados de fabricante.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '03_Ambientes/Iluminacao'
DATE = '29/10/2026'
SOURCES = {
    'N1': ('ABNT NBR ISO/CIE 8995-1:2013, §§4.2–4.4, 4.8, 4.10 e tabela 5/22; texto primário em cópia pública; edição aplicável a confirmar', 'https://drb-assessoria.com.br/drbr/nbrisocie8995.pdf'),
    'N2': ('ABNT NBR 5413:1992, §5.3.65; referência histórica secundária, não declaração de vigência', 'http://ftp.demec.ufpr.br/disciplinas/TM802/NBR5413.pdf'),
    'N3': ('ABNT NBR 5410:2004 corrigida 2008, §§5.1.3.2.2 e 9.1; edição aplicável pelo RT', 'https://universidadeniltonlins.com.br/wp-content/uploads/2019/04/NBR-5410.pdf'),
    'S1': ('Stella: anexos IES /30 e fator de utilização; consulta 29/10', 'https://conhecimento.stella.com.br/hc/pt-br/articles/11888873996311-PLAFON-DE-SOBREPOR-EVO-30W-STH21967-XX'),
    'S2': ('Galaxy, loja oficial: 9608, 2000 lm/25 W/110°/IRC80/IP44; consulta técnica 29/10', 'https://galaxyshop.com.br/plafon-firefly-com-led-integrado-quadrado-ip44-25w-3000k-branco.html'),
    'S3': ('Galaxy, loja oficial: 9605, 2000 lm/25 W/110°/IRC80/IP44; consulta técnica 29/10, preço não transportado', 'https://galaxyshop.com.br/plafon-firefly-com-led-integrado-redondo-ip44-25w-3000k-branco.html'),
    'S4': ('WiZ oficial 929002424712: 800 lm/8,8 W/127 V; não identifica automaticamente a oferta 806 lm/bivolt', 'https://www.wizconnected.com/pt-br/p/lampada-moderna-lampada-60w-a60-e27/8718699787370'),
    'S5': ('Elgin 48D18WSRWIFI: referência comercial 1440 lm/18 W; curva e fluxo por branco ausentes', 'https://www.avantistore.com.br/luminaria-de-sobrepor-redonda-inteligente-18w-3000-6500k-wifi-48d18wsrwifi-elgin'),
    'S6': ('Nordecor EVY2054: 270 lm/3 W/30°/IP20; consulta fabricante 29/10', 'https://nordecor.com.br/produto/arandela-led-pix/'),
    'S7': ('Brilia 314450: 320 lm/3,5 W/3000 K/127 V na tabela, IRC>80; cabeçalho 12 V/0,015 A inconsistente, não usado', 'https://brilia.com/produtos/residencial-e-comercial/mini-g9-35w'),
    'S8': ('Cristallux 221506: 1200 lm/m,12 W/m,12 V,IRC>90; campo0,1 A/m inconsistente, cálculo usa1 A/m', 'https://www.cristallux.com.br/produto/fita-led-cristall-pro-dry-cob-5mt-12v-12w-m-3000k-1200lm-m-ip65-480led-m-irc-90'),
    'S9': ('3R, COB4000K:1200 lm/m,12 W/m,IRC>90; dado comercial, confirmar CLX-FT331240/lote', 'https://www.3reletrica.com.br/fita-de-led-cob-480led/m-ip65-4000k-12v-5-metros-dimerizavel-cristallux'),
    'S10': ('Brilia318939:530 lm/m,4,8 W/m,12 V,3000K,IRC80,IP65; valor comercial já registrado', 'https://www.belluce.com.br/bll604418-fita-de-led-4-8wm-3000k-irc-80-530lmm-12v-angulo-120-brilia-318939'),
    'S11': ('WiZ Pro Kit-C929002681171:1600 lm/20 W/2 m,IRC80,IP20; E05, E06 adiada', 'https://assets.wizconnected.com/datasheets/WiZ_Pro_LED_Strip_RGBTW_2M_Kit-C_929002681171_DS1022.pdf'),
    'S12': ('Shelly Plus RGBW PM:12/24 V CC,<1,2 W,4 A/canal,10 A total,PWM833 Hz/22 kHz; consulta29/10', 'https://kb.shelly.cloud/knowledge-base/shelly-plus-rgbw-pm'),
    'P1': ('Seleção e preços27/10 prevalecem; sem recotação, frete ou instalação', 'Lista_curta_luminarias_e_madeira.md'),
    'P2': ('Alturas nominais2,60/2,50 m; rebaixos e vigas sem cotas verticais confirmadas', '../../01_Programa_e_decisoes/Pesquisa_pe_direito.md'),
    'P3': ('Planta oficial, 1 folha, conferida visualmente29/10; não localiza luminárias', '../../09_Referencias/Plantas_e_manuais/Planta_oficial.pdf'),
    'P4': ('PR-PONTO e contornos nominais, não levantamento da unidade', '../../07_Imovel/Medidas_e_impactos.csv'),
    'P5': ('Comandos funcionais não identificam circuitos/disjuntores/condutores', '../Planta_pontos/README.md'),
    'P6': ('Perfis e fontes; comprimentos existentes C2=1,1 m,S3=1 m,Q06=2 m, não cortes executivos', 'Fechamento_custo_beneficio/Revisao_quarto_CB02.md'),
    'V1': ('Outra unidade espelhada: quatro saídas de teto; foto07:26 conferida29/10', '../../07_Imovel/Complemento/Fotos/AD-0446.jpg'),
    'V2': ('Outra unidade: duas teclas junto ao interfone; função não testada', '../../07_Imovel/Complemento/Fotos/AD-0334.jpg'),
    'V3': ('Outra unidade: três teclas junto à circulação, mão encobre parte', '../../07_Imovel/Complemento/Fotos/AD-0430.jpg'),
    'V4': ('Outra unidade: tomada e interruptor junto ao lavatório/porta', '../../07_Imovel/Complemento/Fotos/AD-0486.jpg'),
    'V5': ('Correspondência corrigida: quartoA→escritório; B→quarto principal; provável', '../../07_Imovel/Complemento/Complemento_da_visita_R02.md'),
}

# Alvos adotados, não uma tabela normativa aplicada a toda residência.
# ambiente, tarefa, altura m, lux mantidos, U0, classificação, fonte
TARGETS = [
    ('sala', 'geral', .75, 150, .4, 'conforto residencial adotado', 'N2 §5.3.65'),
    ('sala', 'mesa/leitura', .75, 500, .7, 'meta residencial para leitura/jogos', 'N2 §5.3.65; N1 analogia tarefa'),
    ('cozinha', 'geral', .75, 150, .4, 'conforto residencial adotado', 'N2 §5.3.65'),
    ('cozinha', 'preparo', .85, 500, .7, 'meta residencial exigente', 'N2 faixa local200–500; N1 analogia tarefa'),
    ('cozinha', 'pia', .85, 300, .7, 'meta residencial adotada', 'N2 §5.3.65'),
    ('lavanderia', 'geral', .75, 150, .4, 'hipótese de conforto', 'H1; N2 analogia'),
    ('lavanderia', 'tanque', .85, 300, .7, 'meta residencial adotada', 'H1; N2 analogia tarefa'),
    ('banho', 'geral', .75, 150, .4, 'hipótese de conforto', 'H1; N2 analogia'),
    ('banho', 'rosto vertical', 1.60, 300, .7, 'meta residencial; faixa de teste150–500', 'H1; não é piso normativo para maquiagem'),
    ('quarto', 'geral', .75, 150, .4, 'conforto residencial adotado', 'N2 §5.3.65'),
    ('quarto', 'leitura cama', .45, 300, .7, 'meta residencial adotada', 'N2 §5.3.65'),
    ('escritorio', 'geral', .75, 150, .4, 'conforto residencial adotado', 'H1; N2 analogia'),
    ('escritorio', 'mesa/monitores', .75, 500, .7, 'referência normativa de tarefa laboral', 'N1 tabela5/22 e§4.3.4; UGR≤19,Ra≥80'),
    ('circulacao', 'piso', 0, 100, .4, 'meta residencial adotada', 'N2 §5.3.65; não iluminação de emergência'),
    ('sala', 'TV', .75, 30, 0, 'faixa de conforto10–50, sem fonte visível/reflexo', 'H1; não requisito normativo'),
]
REFLECTANCES = [
    ('teto branco', .70, .85, 'pintura branca; não medido'),
    ('Algodão Egípcio/off-white', .50, .75, 'paredes claras foscas; não medido'),
    ('Arenza/Beige Matt', .35, .60, 'acabamento areia/fendi; não medido'),
    ('Azul Petróleo/Sauge', .10, .30, 'cores escuras/verde; não medido'),
    ('Itaúnas', .45, .70, 'pedra clara; componente especular não modelado'),
    ('Olmo/greige', .15, .35, 'piso; não medido'),
    ('suede cinza/areia', .20, .50, 'tecido; não medido'),
    ('metal preto/tela apagada', .02, .10, 'difusa apenas; reflexo especular não modelado'),
]
# Fluxos da fonte nua; perdas de vidro/perfil são hipóteses separadas.
PRODUCTS = {
    'C13': dict(room='cozinha', lm=2300, w=30, cct='3000', cri='>90', source='S1', mode='IES', drop=.038),
    'L11': dict(room='lavanderia', lm=2000, w=25, cct='3000', cri='80', source='S2', mode='cos110', drop=.05),
    'B11': dict(room='banho', lm=2000, w=25, cct='3000', cri='80', source='S3', mode='cos110', drop=.05),
    'S03': dict(room='sala', lm=1600, w=17.6, cct='3000 branco de teste; RGB fora da fotometria', cri='80', source='S4', mode='diffuse', drop=.10),
    'E04': dict(room='escritorio', lm=1600, w=17.6, cct='3000 branco de teste; RGB fora da fotometria', cri='80', source='S4', mode='diffuse', drop=.10),
    'Q05': dict(room='quarto', lm=1440, w=18, cct='3000 de teste; ajustável3000–6500', cri='dado ausente', source='S5', mode='diffuse', drop=.05),
    'S04': dict(room='sala', lm=960, w=10.5, cct='3000', cri='>80', source='S7', mode='isotropic', drop=None),
    'Q01': dict(room='quarto', lm=270, w=3, cct='3000', cri='dado ausente', source='S6', mode='cos30', drop=None),
    'Q02': dict(room='quarto', lm=270, w=3, cct='3000', cri='dado ausente', source='S6', mode='cos30', drop=None),
    'C14': dict(room='cozinha', lm=1320, w=13.2, cct='3000', cri='>90', source='S8/P6', mode='strip', length=1.1),
    'S05': dict(room='sala', lm=1200, w=12, cct='3000', cri='>90', source='S8/P6', mode='indirect', length=1),
    'Q06': dict(room='quarto', lm=2400, w=24, cct='3000', cri='>90', source='S8/P6', mode='indirect', length=2),
    'B09': dict(room='banho', lm=1320, w=13.2, cct='4000', cri='>90 comercial', source='S9/P5', mode='mirror', length=1.1),
    'B10': dict(room='banho', lm=1060, w=9.6, cct='3000', cri='80 comercial', source='S10/P5', mode='indirect', length=2),
    'E05': dict(room='escritorio', lm=1600, w=20, cct='3000 de teste; ajustável/RGB', cri='80', source='S11', mode='indirect', length=2),
}


def read_ies(text):
    """LM-63 type C, TILT=NONE, quarter symmetry only; reject unsupported input."""
    if 'TILT=NONE' not in text:
        raise ValueError('Somente TILT=NONE')
    a = [float(x) for x in text.split('TILT=NONE', 1)[1].replace(',', ' ').split()]
    lamps, lm, mult, nv, nh, kind, units, width, length, height = a[:10]
    nv, nh = int(nv), int(nh)
    if kind != 1 or units != 2 or lamps != 1 or len(a) != 13+nv+nh+nv*nh:
        raise ValueError('Cabeçalho IES não suportado ou truncado')
    va, ha = a[13:13+nv], a[13+nv:13+nv+nh]
    if ha[0] != 0 or ha[-1] != 90 or va[0] != 0 or va[-1] != 90:
        raise ValueError('Simetria IES não suportada')
    return dict(lumens=lm, watts=a[12], vertical=va, horizontal=ha,
                cd=[[v*mult for v in a[13+nv+nh+i*nv:13+nv+nh+(i+1)*nv]] for i in range(nh)])


def interpolate(xs, ys, x):
    if x <= xs[0]: return ys[0]
    if x >= xs[-1]: return ys[-1]
    for i in range(1, len(xs)):
        if xs[i] >= x:
            f=(x-xs[i-1])/(xs[i]-xs[i-1])
            return ys[i-1]*(1-f)+ys[i]*f
    raise ValueError(x)


def ies_cd(ies, theta, phi):
    if theta > 90: return 0
    phi=abs(phi)%180
    if phi > 90: phi=180-phi
    rows=[interpolate(ies['vertical'], r, theta) for r in ies['cd']]
    return interpolate(ies['horizontal'], rows, phi)


def cosine_cd(lm, cosine, n=1):
    return lm*(n+1)/(2*math.pi)*max(0,cosine)**n


def illuminance(cd, distance, incidence):
    if distance <= 0: raise ValueError('Distância não positiva')
    return cd*max(0,incidence)/distance**2


def segment_box(a,b,box):
    """Open segment versus axis aligned box; excludes endpoint contact."""
    lo,hi=0.,1.
    for i in range(3):
        d=b[i]-a[i]
        if abs(d)<1e-12:
            if not box[i] < a[i] < box[i+3]: return False
        else:
            u,v=sorted(((box[i]-a[i])/d,(box[i+3]-a[i])/d))
            lo,hi=max(lo,u),min(hi,v)
            if hi <= lo: return False
    return hi>1e-6 and lo<1-1e-6


def write_csv(path, rows):
    rows=list(rows)
    if not rows: return
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';')
        w.writeheader(); w.writerows(rows)


def premises():
    lines=['# Estudo fotométrico do apartamento', '',
        f'Estudo de {DATE}; hipóteses explícitas, sem seleção de produto ou alteração de orçamento/CAD. Gerado por `ferramentas/estudos/estudo_fotometrico.py`.', '',
        '## Enquadramento e níveis-alvo', '',
        'N1 trata de trabalho interior. Seus 500 lx mantidos, U0≥0,70, UGR≤19 e Ra≥80 são referência da tarefa de escritório; não uma exigência geral para todos os cômodos domésticos. N2 é referência histórica secundária residencial. Edição aplicável precisa ser confirmada pelo RT; a edição internacional ISO/CIE2025 não atualiza automaticamente a adoção ABNT. Os demais valores são metas de conforto deste estudo, não texto de norma.', '',
        '| Ambiente | Tarefa | Plano m | Meta lx | U0 | Natureza e fonte |',
        '|---|---|---:|---:|---:|---|']
    for room,task,z,lx,u,nature,source in TARGETS:
        lines.append(f'| {room} | {task} | {z:g} | {lx} | {u:g} | {nature}; {source} |')
    lines += ['', 'Limpeza usa a geral+tarefas a100%, sem criar piso normativo próprio. Noite adota5–20 lx no percurso como hipótese de conforto, sem equivaler a iluminação de emergência. A meta TV refere-se ao ambiente, não iluminância da tela. Para maquiagem,300 lx verticais é meta de comparação residencial; não diagnóstico de cores ou suficiência para qualquer tarefa fina.', '',
        '## Refletâncias e perdas', '',
        'Acabamentos identificados no `data.js` e na decisão de chapas vigente; cor de imagem/RGB não é refletância fotópica medida. Faixas abaixo são hipóteses H2 de sensibilidade, não fichas dos materiais nem conversão automática de sRGB. Espelho e tela não podem ser tratados como difusores.', '',
        '| Superfície vigente | ρ mínimo | ρ máximo | Premissa |', '|---|---:|---:|---|']
    for label,lo,hi,note in REFLECTANCES: lines.append(f'| {label} | {lo:.2f} | {hi:.2f} | H2: {note} |')
    lines += ['', 'H3: fatores de manutenção0,70/0,80/0,90 (baixo/central/alto); N1§4.8 exige justificar manutenção real, não usar estes fatores como garantia. H4: FU zonal0,30/0,45/0,60 para comparação; não são tabela do fabricante, nem derivados das refletâncias. O FU concentra distribuição e reflexões de forma agregada. A análise direta ponto a ponto não usa FU e não soma reflexão inventada.', '',
        'H5: transmissão Jurerê0,50/0,65/0,85; âmbar0,40/0,55/0,75; perfil/difusor0,60/0,75/0,90. Faixas de ensaio escolhidas pelo estudo, não limites garantidos do produto. H6: distribuidores analíticos sem IES usam cosⁿ; n=1 como difuso e n=ln(0,5)/ln(cos(facho/2)) quando há facho. Um ângulo publicado não determina toda a curva; a aproximação precisa ser substituída pela fotometria do conjunto.', '',
        '## Produtos e rastreabilidade', '',
        '| Grupo | Fluxo nu lm | Potência W | Cor K | IRC | Fonte / limite |', '|---|---:|---:|---|---|---|']
    for code,p in PRODUCTS.items():
        lines.append(f"| {code} | {p['lm']:g} | {p['w']:g} | {p['cct']} | {p['cri']} | {p['source']}; {p['mode']} |")
    lines += ['', 'Fluxos de fitas resultam de comprimento nominal×lm/m. C2/S3/Q06 mantêm os comprimentos já usados em P6; não são comprimentos de compra. B09=2×0,55 m e B10≤2 m em P5; E05=kit2 m. Não há dado de fluxo por branco/RGB ou intensidade regulada; os cálculos funcionais consideram branco a100%. Faltam transmissão/curva dos conjuntos; IRC das EVY e do Elgin não está comprovado nas fontes usadas. Não confundir lista comercial e SKU conciliado.', '',
        'IES EVO obtido diretamente do anexo oficial S1 em29/10: teste31/08/2021,2329 lm/35,65 W; catálogo2300 lm/30 W. A curva original é cenário histórico, não fotometria certificada do lote30 W. Serão mostrados separadamente curva original e comparação normalizada2300/2329; normalizar fluxo não resolve diferença construtiva. Curva numérica pequena preservada em `Fotometria_fontes.json`, com SHA do IES original.', '',
        '## Geometria e evidências do vídeo', '',
        'Planta oficial P3 conferida com a skill PDF; projeções PR-FLOORS e PR-PONTO de P4 fixam o sistema global da prancha em mm. Exportação R54 e modelo são vinculados por SHA. O FreeCAD não é aberto. Os `bounds` do site incluem margens de câmera e não são áreas dos cômodos. Usar união dos retângulos PR-FLOORS sem duplicar sobreposições; excluir footprints de caixas que atravessam o plano apenas na malha útil, mantendo a área bruta separada.', '',
        'Elias,29/10/2026, nesta conversa: “tem imagens de um video de um apartamento semelhante ao meu (só q espelhado)”. V1–V5 foram conferidos: quatro saídas no conjunto social/cozinha/serviço; duas teclas junto ao interfone; três junto à circulação; tomada+interruptor junto ao lavatório. A→Dormitório02/escritório e B→Dormitório01/quarto é a correspondência provável corrigida pela R02. Orientação transferida pelas paredes e vãos da planta, não por inverter coordenadas de pixels. O vídeo sustenta quantidade e região, não centímetros, retorno, neutro ou circuito.', '',
        'Para o cálculo: centros nominais dos pontos existentes; altura do teto2,60 m (banho2,50) menos corpo/hipótese do emissor. Não deduzir novamente forro de uma altura já acabada. Jurerê10 cm de corpo; EVO3,8 cm; Elgin/Firefly5 cm como hipótese, sem dimensão exata comprovada. Rebaixos/vigas sem cotas ficam como perguntas, sem inventar seção. Deslocamento de±25 cm será ensaio de sensibilidade, não precisão atribuída ao vídeo.', '',
        'Planos pedidos0,75/0,85/0,45 m são comparadores; bancadas atuais chegam a0,92 m na cozinha e0,765 no banho; cama atual tem0,64 m. Registrar as duas referências, sem alterar móveis. Plano vertical do rosto separado da horizontal. Portas/varal e armários serão apenas envelopes de oclusão, não simulação contínua de interferências.', '',
        '## Método a executar', '',
        'Fluxo zonal: Emed=ΣΦ×transmissão×FU×FM/área bruta. Direta: E=ΣI(θ,φ)×cos(incidência)/r²×FM, com visibilidade por segmento×caixa; todas as coordenadas convertidas para metros. Não multiplicar a direta por FU novamente. Emed ponderada pela área das células; Emin por amostra e U0=Emin/Emed. Refinar malha só para testar erro numérico, sem redimensionar instalação condicionada.', '',
        'UGR real requer luminância direcional, área luminosa aparente, luminância de fundo e índice de posição. Curva só da lâmpada/alegaçãoUGR<19 não comprova o ambiente. Sem esses dados, registrar indeterminado e risco/reflexo geométrico, sem fabricar um UGR numérico. Luz natural, Ambilight, telas acesas e iluminação do depurador não entram como fluxo conhecido.', '',
        'Resultados espaciais, cenas/consumo e alternativas serão gerados nas próximas etapas deste mesmo arquivo.', '', '## Fontes', '']
    for k,(label,url) in SOURCES.items(): lines.append(f'- **{k}:** [{label}]({url}).')
    return '\n'.join(lines)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--importar-ies',type=Path)
    parser.add_argument('--saida',type=Path,default=OUT)
    args=parser.parse_args(); args.saida.mkdir(parents=True,exist_ok=True)
    if args.importar_ies:
        raw=args.importar_ies.read_bytes(); ies=read_ies(raw.decode('utf-8-sig'))
        ies.update(sha256=hashlib.sha256(raw).hexdigest(),url='https://conhecimento.stella.com.br/hc/pt-br/article_attachments/35841818392983',test_date='31/08/2021')
        (args.saida/'Fotometria_fontes.json').write_text(json.dumps({'EVO_2021':ies},ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    (args.saida/'Estudo_fotometrico.md').write_text(premises(),encoding='utf-8')
    write_csv(args.saida/'Premissas_luz.csv',(dict(zip(('ambiente','tarefa','plano_m','meta_lx','uniformidade','natureza','fonte'),r)) for r in TARGETS))
    print('Premissas:15 tarefas; fonte IES pequena e hipóteses identificadas. Sem alteração de CAD/site/orçamento.')


if __name__=='__main__': main()
