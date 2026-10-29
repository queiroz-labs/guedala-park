"""Compara rotas nominais, lendo caixas da base vinculada por SHA à R54.

Não abre FreeCAD nem altera o modelo. Gera a comparação única MD e HTML.
As posições hidráulicas desconhecidas são hipóteses explícitas, não medições.
"""
from pathlib import Path
import gzip
import hashlib
import html
import json
import math

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '03_Ambientes/Banheiro'
DIAMETERS = {'PEX 20 × 1,9': 16.2, 'CPVC 22 × 2,0': 18.0}


def volume(length_m, diameter_mm):
    return length_m * math.pi * diameter_mm ** 2 / 4000


def length(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:])) / 1000


def turns(points):
    directions = [tuple(b[i]-a[i] for i in range(3)) for a, b in zip(points, points[1:])]
    return sum(abs(sum(a[i]*b[i] for i in range(3))) < 1e-8
               for a, b in zip(directions, directions[1:]))


def unique_length(paths):
    """Une segmentos ortogonais colineares, inclusive partilhas parciais."""
    groups = {}
    for points in paths:
        for a, b in zip(points, points[1:]):
            axes = [i for i in range(3) if a[i] != b[i]]
            if not axes:
                continue
            if len(axes) != 1:
                raise ValueError('Trecho não ortogonal')
            axis = axes[0]
            key = (axis, tuple(a[i] for i in range(3) if i != axis))
            groups.setdefault(key, []).append(sorted((a[axis], b[axis])))
    total = 0
    for intervals in groups.values():
        start, end = sorted(intervals)[0]
        for a, b in sorted(intervals)[1:]:
            if a <= end:
                end = max(end, b)
            else:
                total += end-start
                start, end = a, b
        total += end-start
    return total / 1000


def geometry(root=ROOT):
    release = json.loads((root/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    base = json.loads(gzip.decompress((root/'02_Modelo_3D/Base_verificacao.json.gz').read_bytes()))
    digest = hashlib.sha256((root/release['cadPath']).read_bytes()).hexdigest()
    if release['cadRevision'] != 'R54' or digest != release['cadSHA256'] or digest != base['sha256']:
        raise ValueError('Base/release/modelo divergentes: reextrair, nunca atualizar a base para passar')
    objects = base['objetos']
    names = ['Peca045', 'Peca049', 'Peca051', 'Peca053', 'Peca159', 'Peca190',
             'Peca399', 'Peca400', 'Peca401', 'Peca403', 'Peca404', 'Peca185',
             'BC43_CaixaE', 'BC43_CaixaD', 'BC43_CaixaBase', 'BC43_Fundo',
             'BC43_Travessa', 'BC43_Sifao', 'BC43_Maos', 'BC43_Desmontagem',
             'BC43_PainelEsquerda', 'BC43_PainelDireita', 'Peca075']
    boxes = {n: objects[n]['caixa_global'] for n in names}
    left, right = boxes['BC43_CaixaE'], boxes['BC43_CaixaD']
    interior = [left[3], left[1], boxes['BC43_CaixaBase'][5], right[0],
                boxes['BC43_Fundo'][1], boxes['BC43_Fundo'][5]]
    return {'sha': digest, 'boxes': boxes, 'interior': interior,
            'width': boxes['Peca045'][0]-boxes['Peca051'][3],
            'depth': boxes['Peca049'][1]-boxes['Peca053'][4]}


def routes(g, source_z=1200):
    b = g['boxes']; xmax = b['Peca045'][0]
    sx = xmax-b['Peca159'][0]  # borda do enchimento, NÃO posição da derivação
    hx = (sx+xmax-b['Peca190'][3])/2  # centro nominal da faixa à esquerda do vaso
    px = xmax-(b['Peca399'][0]+b['Peca399'][3])/2
    S, H, P = (sx, 30, source_z), (hx, 30, 600), (px, 30, 550)
    result = {}
    for ident, z in [('A1',2550), ('A2',2450), ('A3',1000), ('A4',100),
                     ('A6',100), ('B1',100), ('B2',100), ('B3',100)]:
        result[ident] = {'pia':[S,(sx,30,z),(px,30,z),P],
                         'ducha':[S,(sx,30,z),(hx,30,z),H]}
    result['A5'] = {'pia':[S,(sx,30,2550),(2060,30,2550),(2060,30,550),P],
                    'ducha':result['A1']['ducha']}
    result['B4'] = {'ducha':[S,(hx,30,source_z),H]}
    E = (1950,120,400)  # conexão representativa do aparelho, não envelope de produto
    local = {'pia':[E,(1950,30,400),(px,30,400),P],
             'ducha':[E,(1950,30,400),(1950,30,100),(hx,30,100),H]}
    result['C1'] = local
    result['C2'] = local
    result['C3'] = {}  # resistência na própria bica: sem ramal quente exterior
    return result


# D/F são julgamentos de projeto com critérios publicados, não dados de fabricante.
OPTIONS = [
 dict(id='A1', name='Forro existente + descida no canto', d=5, f=2, cost='médio',
      trades='encanador, gesseiro, pintor', steps='inspecionar acesso; instalar/suportar; testar; recompor forro e descida; pintar',
      detail='Travessia no próprio banheiro; descida fechada junto ao lavatório e pequeno ramal vertical até a ducha. O trecho entre espelho e pedra continua precisando de cobertura. Altura do eixo 2,55 m é hipótese acima do teto de 2,50 m, não espaço livre demonstrado.',
      access='Conexões em portinholas; tubo contínuo onde possível. Vazamento pode aparecer tarde no gesso; limpeza externa simples.',
      impact='Preserva piso e tampo; compatibilizar plafon, luz indireta, portas do P19 e a cobertura da descida. Não apoiar tubo na placa de forro.',
      rt='Confirmar vazio acima do próprio forro, suportes, passagem na borda do box e derivação privativa; sem usar vizinho.'),
 dict(id='A2', name='Faixa fechada de gesso no encontro teto/parede', d=4, f=2, cost='médio/alto',
      trades='encanador, gesseiro, pintor', steps='locar faixa; instalar tubos; testar; montar fechamento; pintar',
      detail='Faixa localizada com eixo a 2,45 m, sem rebaixar todo o teto. A seção real depende de tubos, conexões, suporte e isolamento; a linha do desenho não é seção de fabricação.',
      access='Tampas acessíveis nos tês e transições; risco oculto no fechamento. Ressalto alto acumula pó.',
      impact='Volume perceptível no teto; não esconder nem encostar nas fontes e perfis L02. Descida e ramal da ducha permanecem.',
      rt='Verificar fixação sem atingir estrutura/redes, altura útil e travessia do box; mesma consulta hidráulica de A1.'),
 dict(id='A3', name='Prateleira elevada de Itaúnas sobre a caixa', d=4, f=2, cost='médio/alto',
      trades='encanador, marmorista, instalador de acabamento', steps='gabaritar caixa/tampa; instalar; testar; fixar pedra e tampa de acesso; vedar',
      detail='Eixo de cálculo a 1,00 m, apenas hipótese. Prateleira e saia precisam de nível próprio: tampo 76,5 cm < VIP 80 cm. Não elevar a pia. Botão e retirada completa da tampa ainda precisam de gabarito.',
      access='Fechamento inferior removível e juntas acessíveis; risco de vazamento escondido sob pedra. Nova superfície para limpar.',
      impact='Faixa atrás do vaso e entre os pontos; não confundir com prateleira do box. Não bloquear ducha à esquerda nem papeleira no lado do gabinete.',
      rt='Compatibilizar apoios permitidos, manutenção da descarga, passagem pelo fechamento do box e tubulação fria/quente.'),
 dict(id='A4', name='Travessia baixa atrás do vaso', d=5, f=3, cost='baixo/médio',
      trades='encanador, instalador de cobertura', steps='conferir percurso traseiro; montar; testar; fechar partes acessíveis',
      detail='Eixo a 10 cm. A caixa envolvente do VIP chega à parede na R54: a linha cruza esse envelope, portanto NÃO demonstra espaço atrás da louça. Somente se a geometria real permitir sem avançar o vaso.',
      access='Se depender de remover a louça, manutenção piora e a nota de facilidade cai. Cobrir apenas com peças removíveis; juntas ocultas de inspeção difícil.',
      impact='Não consumir passagem frontal nem o vão de cerca de 15 cm. Mantém teto/pedra/P19, mas limpeza traseira é crítica.',
      rt='Conferir forma traseira e fixações do VIP; rejeitar se exigir deslocar louça, abrir piso ou alterar impermeabilização.'),
 dict(id='A5', name='Coluna técnica na lateral do espelheiro', d=4, f=2, cost='alto',
      trades='encanador, marceneiro, gesseiro/pintor', steps='compatibilizar coluna e luz; instalar; testar; montar coluna com tampa; recompor origem',
      detail='Combina alimentação pelo forro com descida na extremidade direita do lavatório (u=2,06 m), até B02. Não é caminho independente da travessia horizontal. Os 12–15 cm do P19 não são espaço vazio disponível.',
      access='Tampa frontal/lateral independente; conexões segregadas de cosméticos e eletricidade. Vazamento dentro de madeira precisa ser visível e drenável.',
      impact='Ocupa faixa do móvel ou exige aumento: nenhuma das duas alterações está adotada. A faixa de 30 mm ao canto no desenho não acomoda automaticamente tubo isolado/curvas. Preservar giro do P19 e retirada BC43.',
      rt='Conferir largura/profundidade da coluna, segregação hidráulica/elétrica e acesso; consultar marcenaria antes de encomendar.'),
 dict(id='A6', name='Rodapé técnico de duas peças e tampa', d=4, f=3, cost='médio',
      trades='encanador, instalador de alumínio ou marceneiro/pintor', steps='gabaritar; instalar tubos; testar; montar base e tampa removível',
      detail='Mesmo traçado baixo de A4, com cobertura contínua projetada para tubos. Alumínio é preferível ao MDF pintado na região de lavagem; MDF e suas bordas exigem proteção compatível e não devem tocar água.',
      access='Tampa contínua removível favorece inspeção; juntas, extremidades e encontros acumulam sujeira. Vazamento pode ficar retido no rodapé se não houver saída visível.',
      impact='Reduz profundidade junto à parede e pode conflitar com VIP e pé/limpeza. Não corrige a falta de folga traseira por escondê-la. Não prende o quadro removível do gabinete.',
      rt='Dimensionar seção útil com isolamento, temperatura e fixação, e comprovar passagem atrás da louça sem avanço.'),
 dict(id='B1', name='PEX ou CPVC aparente na cor da parede', d=2, f=4, cost='baixo',
      trades='encanador, pintor', steps='locar/fixar; conectar; testar; aplicar acabamento compatível',
      detail='Traçado baixo comparável a A4. PEX flexível pede raio de curva e suportes, CPVC usa conexões e dilatação próprias. Pintura não é isolante; compatibilidade da tinta com cada tubo precisa de declaração do fabricante.',
      access='Conexões visíveis facilitam achar vazamento, mas tubo e abraçadeiras dificultam limpeza; superfície quente pode ser tocada.',
      impact='Linha e fixadores visíveis, inclusive subidas. Alternativa alta usa a geometria A2 se o VIP impedir a baixa; não passar na frente da louça como atalho.',
      rt='Material, tinta, suportes, dilatação, proteção ao toque e pressão; mesma avaliação de reforma para o novo ramal.'),
 dict(id='B2', name='Calha/canaleta com tampa pintada', d=3, f=4, cost='baixo/médio',
      trades='encanador, instalador/pintor de acabamento', steps='fixar suporte; instalar/testar tubos; montar e pintar tampa',
      detail='Desenhada no rodapé; alternativa no encontro teto/parede usa os comprimentos de A2. Calha projetada para tubulação, sem compartilhar fiação. Canaleta elétrica comercial é só referência de preço, não produto especificado para água quente.',
      access='Tampa facilita manutenção e reduz pó diretamente nos tubos; conexões continuam acessíveis. Conferir resistência térmica, dilatação e saída de vazamento.',
      impact='Faixa retangular fica visível; se baixa, mesma restrição do VIP; se alta, soma descidas e compatibilização da luz. Preserva Arion e tampo.',
      rt='Conferir seção útil, reação ao calor, suportes independentes e passagem real. Seção 50×50 não comprova dois tubos isolados.'),
 dict(id='B3', name='Cobre ou inox aparente preto fosco', d=1, f=3, cost='médio/alto',
      trades='encanador habilitado no sistema, aplicador de acabamento', steps='cortar/conformar; unir e fixar; testar; aplicar acabamento compatível',
      detail='Linha preta intencional, em diálogo com ducha e papeleira. Cobre para água potável quente tem referência Eluma; inox precisa de linha e conexões próprias, não tubo decorativo. Acabamento e sistema exatos ainda não selecionados.',
      access='Vazamento fácil de localizar; limpar abraçadeiras e evitar abrasivos. Metal exposto esquenta: tinta preta não substitui isolamento; uma capa isolante muda o desenho desejado.',
      impact='Maior contraste visual e possível conflito com metais da ducha/papeleira no vão estreito. Mesmo limite geométrico da passagem baixa.',
      rt='Selecionar liga/sistema, uniões e transições, proteção ao toque e eventual equipotencialização; diâmetro interno real ainda desconhecido.'),
 dict(id='B4', name='Só ducha quente; pia permanece fria', d=3, f=4, cost='menor escopo',
      trades='encanador, acabador da origem', steps='derivar ducha; testar; recompor acesso',
      detail='Referência de economia da extensão até a pia, não custo total zero: B06 é novo, logo derivação, mistura, fria e acabamento continuam custando. Só o incremento da pia é zero. A Arion fica sem função quente, com alimentação a resolver pelo instalador, sem ligação improvisada.',
      access='Percurso curto e acessível, sem travessia atrás da caixa; mantém exigência de fechamento próprio da ducha e teste de temperatura.',
      impact='Não atende o objetivo de pia quente; ganho é reduzir obra. Não muda vaso, P19, luz ou bancada.',
      rt='Mesmo acesso/derivação da família A/B, estabilidade do E21 na ducha e tratamento correto das entradas da Arion.'),
 dict(id='C1', name='Miniacumulador 5–15 L dentro do BC43', d=4, f=1, cost='alto/a cotar',
      trades='encanador, eletricista, marceneiro', steps='selecionar SKU 127 V; validar envelope e serviço; projetar elétrica/dreno; instalar/testar',
      detail='Sem ramal novo desde o enchimento, mas com ligações locais e extensão até a ducha. Nenhum produto 5–15 L ficou demonstrado como adequado ao BC43 e à rede 127 V. O exemplo 10 L Rheem foi verificado e não atende: ver análise dimensional e divergência de tensão abaixo.',
      access='Acesso a válvula, dreno, resistência/ânodo, tomada quando permitida e remoção total; vazamento dentro da caixa de madeira. Não basta abrir meia porta de correr.',
      impact='Perde armazenamento; tanque cheio acrescenta massa não qualificada. Não apoiar na frente removível nem bloquear sifão, trilhos ou acesso hidráulico. A ducha ainda exige passagem pela faixa do vaso.',
      rt='SKU brasileiro adequado, 127 V confirmado, IP/classe, circuito/DR, suporte, alívio com descarga segura, mistura e manutenção. Produto de saída aberta não serve automaticamente para monocomando pressurizado.'),
 dict(id='C2', name='Aquecedor elétrico de passagem sob bancada', d=4, f=2, cost='médio/alto',
      trades='encanador, eletricista; marceneiro se houver adaptação', steps='verificar pressão/vazão; projetar circuito; compatibilizar aparelho; instalar/testar',
      detail='Lorenzetti Versátil 127 V/5500 W aceita monocomandos segundo manual. E21 não participa. A curva da Arion e a pressão real ainda condicionam o funcionamento. Uma unidade alimentando pia e ducha não está demonstrada pelo esquema do fabricante; exigir confirmação, não presumir serviço simultâneo.',
      access='Acesso ao seletor, resistência, engate e conexão elétrica; permitir escoamento de vazamento. Encaixe do corpo não comprova espaço de serviço.',
      impact='Aparelho menor que tanque; mantém Arion. Circuito novo pode exigir calha elétrica separada e interferir no acabamento. A extensão quente até a ducha continua necessária.',
      rt='Circuito exclusivo e ligação direta sem tomada, aterramento, DR, IP24, pressão 2–20 mca e alimentação por reservatório conforme manual; validar produto para os dois destinos.'),
 dict(id='C3', name='Torneira elétrica — registro de incompatibilidade', d=1, f=2, cost='médio/alto',
      trades='eletricista, encanador', steps='avaliar produto/circuito; adaptar hidráulica; instalar/testar (fora da proposta atual)',
      detail='Resistência integrada à própria torneira: não é acessório da Addra Arion. Exigiria substituir o monocomando e sua estética, alcance e comando. Apenas registrada como alternativa descartada no escopo atual; não se propõe a troca.',
      access='Manutenção na bancada; conjunto e alimentação elétrica visíveis. A ducha não ganha água quente com essa solução.',
      impact='Perderia a Arion preta atrás da cuba e a mistura atual; compatibilidade com cuba de apoio e giro do P19 teria de ser refeita.',
      rt='Produto, circuito, IP e volumes precisariam de análise; não usar a saída da torneira como alimentação da ducha. Sem SKU selecionado, potência e IP a confirmar.')]


def f(value, digits=3):
    return f'{value:.{digits}f}'.replace('.', ',')


def metrics(paths):
    return {dest: {'length':length(p), 'turns':turns(p),
                   'volumes':{name:volume(length(p), d) for name,d in DIAMETERS.items()}}
            for dest,p in paths.items()}


CRITERIA = '''## Critérios antes das notas

Notas de julgamento do estudo, contestáveis por Elias; 5 é melhor. Não são prova de viabilidade. Facilidade conta **ofícios e operações**, não dias: não há prazo instalado com fonte. Teste/reforma/RT são necessários em todas as opções e não geram vantagem artificial.

| Nota | Discrição: olho, toque e limpeza | Facilidade: coordenação e sequência |
|---|---|---|
| 5 | Tubos ocultos; apenas acesso discreto, superfície contínua | Um ofício, até três operações, sem acabamento novo |
| 4 | Pequena peça integrada ou aparelho dentro do móvel; tampa perceptível ao toque | Até dois ofícios, até quatro operações, acesso direto |
| 3 | Calha/descida visível, juntas e ressaltos para limpar | Dois ofícios especializados ou montagem/desmontagem condicionada |
| 2 | Tubo/abraçadeiras visíveis mesmo pintados | Três ofícios, recomposição ou circuito novo integrado |
| 1 | Linha contrastante ou equipamento que altera a composição | Produto/encaixe não demonstrado ou extensa adaptação |

Custos relativos comparam escopo adicional, sem cotação instalada: baixo = tubos/fixação/acabamento leve; médio = fechamento removível ou serviço adicional; alto = pedra/marcenaria especial, instalação elétrica importante ou produto sem oferta local validada. Nota alta não remove condição impeditiva.
'''

PREMISES = '''## Base medida e hipóteses de traçado

Pedido de Elias, 29/10/2026, nesta conversa: comparar famílias discretas, simples e com geração local, sem escolher nem alterar CAD. A origem de estudo é o ramal quente privativo no enchimento de gesso, **antes dos controles do chuveiro**, conforme informação de Elias; não a mangueira da ducha. Não se reabre essa premissa. O ponto preciso da derivação continua desconhecido.

Caixas globais da base de verificação vinculada por SHA ao arquivo R54, mesma técnica de `conferir_acesso_banheiro.py`. **FreeCAD não foi aberto, recalculado nem salvo.** A base não foi modificada. São envelopes nominais, não levantamento nem prova de passagem entre superfícies.

Sistema local em mm: **u = 4850 − X**, v = 5290 − Y (para a entrada), z = Z. Assim, visto da entrada: box u=0–800; vaso 800–1490; bancada 1490–2090. Origem gráfica S=(800,30,1200) usa a borda do enchimento como referência e **zS=1200 é hipótese**, baseada somente na altura de referência B07, não cota de derivação. O envelope Peca159 termina a z=200; ele NÃO localiza o ramal. Dentro do enchimento e do E21 até S, comprimento e volume são desconhecidos e adicionais.

Pia P=(1790,30,550), em B02; ducha H=(878,75;30;600), em B06, no centro nominal da faixa entre vidro e lado esquerdo do vaso. B01 fria também tem altura 550; B05 fria, 600. Coordenadas horizontais de projeto, não pontos existentes medidos. L09 (saída E21 a 1400) não define o caminho até o banho. A altura de teto de **2500** prevalece por orientação documental; paredes na R54 ainda chegam a 2470: não alteradas.

Eixos de comparação: forro 2550; faixa 2450; prateleira 1000; baixo 100. São hipóteses de comprimento, não alturas executivas. O desenho em planta projeta a mesma rota sobre móveis para mostrar conflito, sem provar passagem. Em A4/A6/B1/B2/B3 e no retorno C até a ducha, o percurso baixo **intercepta o envelope do VIP**: só permanece candidato se a forma traseira real admitir passagem sem avançar louça. Não há proposta de abrir piso, rasgar estrutura, furar vidro, usar vizinho ou retirar enchimento sem avaliação.

Para qualquer zS, o trecho inicial tem comprimento |zR−zS|/1000; os demais vêm das cotas tabuladas. Se a origem ficar 30 cm mais alta, os caminhos altos encurtam 30 cm e os baixos alongam 30 cm (enquanto não cruzar o nível da rota). uS/vS também precisam ser compatibilizados. Não acrescentar comprimento imaginado para obstáculos: o valor abaixo é cenário ortogonal mínimo, acrescido no projeto de curvas reais, offsets, conexões, engates e acessos.

## Água parada, espera e isolamento

PEX Amanco 20×1,9: diâmetro interno calculado **16,2 mm**, com dimensões da ficha FTC000018; CPVC Tigre Aquatherm DN22: DE=22, e=2,0, interno **18,0 mm**, catálogo técnico, tabela de tubos [S1/S2]. V = π·di²·L/4000 em litros (L em metros); respectivamente 0,2061 e 0,2545 L/m. t = 60·V/Q. A tabela usa **Q quente=3,9 L/min**, limiar do E21 [S3], como referência de deslocamento, não promessa de estabilidade ou tempo total até a bica.

A vazão de projeto da Arion **não foi publicada na ficha consultada** [S4]: tempo nessa vazão **a confirmar**. Para usá-la: t=60V/(α·QArion), onde α é a fração quente; a mistura faz Qquente menor que Qtotal. Arejador que limite o total abaixo de 3,9 L/min impede o acionamento individual do E21; mesmo acima, a fração quente pode ficar abaixo. Exemplo puramente aritmético: 6 L/min com metade quente = 3 L/min, insuficiente para esse limiar. Não recomendar abrir outro ponto para fazê-lo funcionar.

Valores calculados são **espera incremental até B02/B06**, com água inicialmente fria no ramal, sem o trecho E21→S, partida do queimador, aquecimento das paredes, engates finais nem mistura. Portanto o tempo real até a água quente chegar à torneira/ducha é maior/indeterminado. Usar cada caminho ativo individualmente; não somar água dos dois ramos como espera de um só. O volume da rede instalada é a união geométrica, sem contar duas vezes o trecho compartilhado. C não depende do E21: 3,9 L/min aparece apenas como comparação hidráulica; C1 depende do tanque já aquecido, C2 da vazão/pressão de acionamento e potência, C3 não tem ramal quente exterior e não atende a ducha.

PEX/CPVC conduzem menos calor que metal, mas isso não garante água quente imediata após pausa. O memorial anterior cita isolamento no PEX [S1]. O catálogo Tigre recomenda avaliar isolamento residencial sobretudo acima de 20 m entre aquecedor e consumo, em trechos expostos/exteriores ou com perdas relevantes, a critério do projetista; para aquecimento central, orienta toda a linha [S2]. Não impor ao CPVC a mesma regra do PEX nem transportar o ensaio de fluxo contínuo do catálogo para água parada. O trecho E21→S é desconhecido. Maior área e comprimento aumentam a oportunidade de perda; A1/A2/A5 são mais longas neste cenário. Fechamento de gesso, pedra, MDF ou tinta **não é isolamento térmico dimensionado**. Avaliar capa, temperatura admissível e folgas antes de escolher calha. Metal preto B3 tem risco de toque quente; isolar ou proteger conforme projeto pode prejudicar a estética pretendida. Sem temperaturas, ambiente, espessura/condutividade do isolante e regime de uso, não se atribuem W/m nem economia em reais. C1 tem perdas em espera e C2 demanda potência instantânea; não declarar vencedor energético sem perfil de uso.

## Conexões e ramal frio

Contagens abaixo são mudanças de direção de 90° do esqueleto, não lista de compra. Para A1–A6/B1–B3: **1 tê de divisão + 3 terminais** (origem, pia, ducha), além de registros/misturadores/transições e derivação existente em S. B4: 2 terminais, sem tê de divisão; derivação em S ainda precisa de conexão própria. Em CPVC, cada mudança pode pedir joelho; não contar o tê duas vezes como joelho. Em PEX, bends podem ser contínuos só com raio mínimo, suporte e espaço permitidos pelo fabricante; sem isso, cotar joelhos, não prometer zero emendas. Comprimentos são pelo eixo ortogonal e não descontam arco real.

C1/C2: 1 divisão quente, 3 terminais quentes e alimentação fria local; alívio/dreno de C1 e válvulas/transições adicionais dependem do SKU. O esqueleto local usa saída representativa E=(1950,120,400), não posição de aparelho comprado. B01→E: 0,160+0,090+0,150=0,400 m, 2 mudanças. Mantém-se alimentação fria da Arion e da ducha (B05); **a origem/rota fria da ducha não está comprovada**. Se B05 não existir, outro ramal terá de ser projetado e cotado em todas as famílias. A ligação da pia acima de B02 até a Arion atrás da cuba exige engates de dimensões internas ainda desconhecidas; não foi incorporada como tubo PEX/CPVC fictício.
'''

ELECTRIC = '''## Geração local: encaixe e elétrica

**C1 — teste de um produto real, sem generalizar para todo tanque de 5–15 L.** Rheem México RME-CHN10L: corpo 355×295×355 mm (L×P×A), 10 L, 1500 W, massa vazia 8,89 kg e cerca de 18,89 kg com água [S6]. O manual pede 250 mm em cada lateral: 355+2×250=**855 mm > 564 mm internos do BC43**; também 800 mm livres ao piso e 100 mm ao teto. Por isso não atende a instalação dentro deste gabinete, mesmo que a caixa externa caiba no volume bruto. A ficha/manual indicam **120 V**, embora a página comercial oficial anuncie 127 V: divergência sem solução; não tratar 120 e 127 como equivalentes. IPX4/classe I constam no manual; oferta, certificação e assistência brasileiras não confirmadas. Válvula de alívio e descarga com destino seguro são necessárias, portanto “só fria e tomada” é incompleto. Não instalar conforme essa referência estrangeira no projeto.

No envelope interno R54, o sifão hipotético ocupa X=3035,5–3084,5, Y=5015,5–5290, Z=516–745. Restam apenas **257,5 mm laterais** de cada lado; um corpo de 355 mm não cabe ao lado. Abaixo do sifão: 516−218=**298 mm**, menor que 355. À frente dele: 5015,5−4890=**125,5 mm**, menor que 295. Essas caixas não resolvem encaixes diagonais nem acesso: reforçam que não há encaixe demonstrado. Mesmo um 5 L requer novo SKU, orientação, conexões e serviço conferidos; um 15 L não foi presumido viável. Não refinar cargas/suspensão para contornar essa reprovação de layout.

**C2 — corpo compacto, desempenho condicionado.** Manual Lorenzetti Versátil [S5]: 127 V, 5500 W, IP24, pressão 2–20 mca; alimentação por caixa d’água, não diretamente pela rede pública. Circuito exclusivo, aterramento e ligação por conectores, **sem plugue/tomada**. Corrente nominal calculada 5500/127≈43,3 A. O manual tabela 50 A/10 mm² sob suas condições; isso não dimensiona o circuito do apartamento (método, agrupamento, distância, queda de tensão e quadro com eletricista). Aciona aproximadamente a 1,6 L/min e recomenda fornecimento mínimo 3,2 L/min para estabilidade; monocomando pode adicionar perda de carga. A 3,9 L/min, potência ideal de 5,5 kW elevaria a temperatura em cerca de 20,2 °C (P/(ρ·cp·Q), ρ=1 kg/L, cp=4,186 kJ/kg·K, sem perdas); não é curva certificada nem temperatura garantida.

Dimensões comerciais publicadas pela Sodimac: 122×186×100 mm (L×P×A), **desenho dimensional oficial não obtido**, portanto apenas triagem. Esse paralelepípedo cabe geometricamente em um dos lados de 257,5 mm, mas niple obrigatoriamente horizontal, seletor, conexões, remoção e queda de água precisam de espaço próprio [S5]. Não avançar sobre portas/trilhos nem sobre os volumes BC43_Maos/Desmontagem. Não ligar a saída deste aquecedor ao ramal quente do E21; são alternativas de alimentação, não redes interligadas. Atendimento dos dois pontos pelo mesmo aparelho exige validação específica do fabricante.

**C3 — incompatível com a escolha vigente.** Torneira elétrica substituiria a Arion; não há adaptação demonstrada para converter seu corpo em resistência. Não selecionada nem recomendada essa troca. Sem produto definido, tensão/potência/IP/encaixe específicos ficam a confirmar. Ducha permanece sem aquecimento nessa opção isolada; completar exigiria outra solução e outro custo.

**Instalação existente:** Planta_pontos B01–B08 são hidráulicos; B09–B11 são iluminação. Não há código de tomada para aquecedor no banheiro. Isso não prova ausência física, mas impede contar com tomada/circuito disponível. 127 V é fixado para o apartamento. Não usar o ponto de luz ou uma tomada genérica como alimentação presumida.

**NBR 5410 consultada: edição 2004, corrigida 2008**, texto ABNT em cópia universitária [S7]; vigência/edição aplicável deve ser confirmada pelo RT. §5.1.3.2.2(a): proteção adicional DR ≤30 mA para circuitos que atendem locais com chuveiro. §9.1.2.1 e figuras 16–18: delimitação dos volumes; §9.1.4.1: IPX7/volume0, IPX4/1, IPX3/2 e IPX1/3 no banheiro residencial. §§9.1.4.3.1–3: restrições a comandos/tomadas; tomada no volume3 exige proteção prevista, incluindo DR ≤30 mA. §§9.1.4.4.2–3 admitem aquecedores fixos classe I/II nos volumes1/2, sem dispensar demais requisitos. §9.1.3.1.2 trata equipotencialização suplementar. **Não classificar o gabinete só por estar fora do vidro:** configuração do piso-box, divisões fixas, ducha higiênica e pontos elétricos precisam ser demarcados pelo RT/eletricista. O gabinete não confere IP ao aparelho. Fiação e água devem ter percursos/acessos próprios.

## Memorial e condições comuns

Memorial Cury p.13–14/17 [S0]: forro no banho; alvenaria estrutural com restrições amplas a quebras e alterações dos pontos; reconhecimento de vedações não estruturais não autoriza automaticamente abrir o enchimento e derivar a instalação. Todas as alternativas exigem avaliação de reforma. A/B: acesso à derivação privativa antes do chuveiro, hidráulica, fechamento e teste de estanqueidade antes de fechar. C: elétrica, potência disponível, volumes/IP/DR e hidráulica local; C1 inclui suporte e descarga de alívio. Não usar prumada coletiva nem confundir ausência de rasgo com dispensa de consulta à construtora/RT.

Preservar Arion centralizada atrás da Slim, VIP no lugar, BC43 com portas de correr e frente removível, P19 raso, três comandos de luz, ducha à esquerda e papeleira no lado esquerdo do gabinete (à direita do vaso, posição visual solicitada por Elias em 29/10/2026). Novo fechamento não pode ocupar o vão estreito, impedir o giro do P19 ou bloquear a sequência de retirada do BC43. A fonte geométrica não contém montagem hidráulica completa, logo o estudo não certifica colisões de tubos ou manutenção real.

## Preços observados em 29/10/2026

| Referência | Página/loja | Valor observado | Limite |
|---|---|---|---|
| PEX Amanco 20×1,9, por metro | Ferreira Costa [S8] | R$ 9,90/m | Só tubo; sem conexões, isolamento, frete ou CEP |
| Aquatherm 22 mm, barra 3 m | Sodimac [S9] | A cotar; página sem preço recuperado | Não atualizar o antigo R$ 54,90 como se fosse atual |
| Canaleta Ilumi com tampa 50×50, 2 m | Ferreira Costa [S10] | R$ 102,90/peça | Produto de cabos; referência comercial, uso térmico/hidráulico não validado |
| Versátil 127 V/5500 W | Sodimac [S11] | R$ 319,00 | Só aparelho; elétrica, conexões e instalação excluídas |
| Miniacumulador 5–15 L adequado | Não obtida oferta brasileira validada | A cotar | Exemplo estrangeiro não convertido em orçamento |

Estoque, frete e preço dependem da região. Não há mão de obra cotada, nem duração em dias com fonte. Quantidade de compra precisa considerar cortes, perdas, peças e circuito frio, ausentes destes valores. O custo relativo de B4 não é obra gratuita.

## Rankings e recomendação

Rankings editoriais condicionais, sem escolher por Elias. Para comparar **o objetivo completo**, B4 (pia fria) e C3 (substituição da Arion/ducha não atendida) ficam fora do pódio. C1 fica fora enquanto não houver produto compatível. Empates de nota são resolvidos por acesso, impacto nos móveis e extensão de obra; não por falsa precisão de média ponderada.

- **Mais discreta:** 1º A1 (forro, 5); 2º A4 (baixo atrás da louça, 5, só se houver passagem); 3º A5 (coluna integrada, 4). A1 vence A4 pelo risco de inviabilidade atrás do VIP; A5 supera A2/A3/A6/C2 pelo potencial de integrar a descida com tampa, ainda a compatibilizar.
- **Mais simples/fácil:** 1º B1 (tubo pintado, 4); 2º B2 (calha com tampa, 4); 3º A6 (rodapé técnico, 3). B1/B2 exigem menos acabamento; A6 oferece tampa contínua. Se a passagem baixa falhar, B1/B2 podem usar a rota alta A2, aumentando comprimento e descidas. No escopo reduzido, B4 é mais curto, mas não entrega pia quente.
- **Melhor equilíbrio:** 1º B2 (tampa/acesso e poucos ofícios); 2º A1 (discrição se o forro permitir); 3º A6 (acabamento removível). Esses três primeiros pressupõem avaliação das condições de passagem; não indicam viabilidade comprovada nem menor preço instalado.

**Recomendação:** levar B2 e A1 à avaliação técnica como alternativas principais: B2 se Elias aceitar a faixa visível e priorizar acesso/manutenção; A1 se priorizar discrição e houver passagem no próprio forro. A6 é a terceira via se a louça admitir o rodapé sem avanço. Para dispensar o ramal desde o enchimento, estudar C2 apenas após confirmar circuito e desempenho da Arion/ducha; C1 não tem encaixe/produto demonstrado, e C3 não conserva a escolha atual. A3 exige aceitar pedra em nível superior; A5, espaço dedicado na marcenaria; B3, tubulação contrastante e proteção térmica. Nenhuma opção foi escolhida neste estudo.

**Perguntas de preferência, sem pedir medidas:** aceita uma calha pintada visível? Prefere forro fechado com portinholas? Aceita tubo preto aparente (e eventual proteção térmica)? Aceita avaliar aquecimento elétrico com circuito exclusivo? B4, pia fria, é aceitável como redução de escopo? C3 exigiria perder a Arion/monocomando, mas fica apenas registrado, sem proposta de substituição.

**A confirmar com profissionais/documentação:** ponto exato no enchimento, trecho E21→S, vazão/pressão da Arion e da ducha, fria B05, folga real atrás do VIP, vazio do forro, seções com isolamento, pintura/material, conexões e acessos, SKU elétrico, desenho oficial do Versátil, atendimento simultâneo/separado dos dois pontos, circuito e edição/volumes da NBR aplicável. São os limites dos dados disponíveis; não pedidos de medidas a Elias.

**Outras possibilidades, sem aprofundar:** uma parede falsa contínua esconderia a rede, mas roubaria profundidade do banheiro e alteraria as interfaces do VIP/BC43; não conserva o espaço adotado. Recirculação acrescentaria retorno, bomba, controles e perdas, sem rota de retorno demonstrada; não simplifica esta intervenção. Uma calha alta aparente é variação de B2 pelo percurso A2, já indicada acima, não uma décima quarta solução independente.

## Fontes e reprodução

- **S0:** [Memorial Cury](../../09_Referencias/Plantas_e_manuais/Memorial_descritivo_Cury_Guedala_Park_III_R00_2023-04-03.pdf), p.13–14 e17; [memorial do estudo](Agua_quente_aparente.md); [Planta de pontos](../Planta_pontos/README.md).
- **S1:** [Amanco, FTC000018 PEX](https://eu-assets.contentstack.com/v3/assets/blt573fdbfcb1106c2a/blta8cf04ce053113e1/663a7030190d1b2fa16c17d1/FTC000018_-_FT_PEX.pdf), tabela D/e (20/1,9); §4.1.6 isolamento já citado no memorial anterior. Tabela recuperada por indexação; PDF direto indisponível nesta consulta, sem nova conferência integral do texto.
- **S2:** Tigre, catálogo técnico Aquatherm, [cópia do fabricante no distribuidor](https://www.redebras.com.br/upload-adm/pdf/cpvc-aquatherm.pdf), tabela Tubo Aquatherm 3 metros, código 17000225, DE22/e2, seções Instalações aparentes/Isolamento térmico; consultado 29/10/2026. Produto/isolante a detalhar.
- **S3:** [Manual E21 176](../../09_Referencias/Plantas_e_manuais/Manuais/Rinnai_E21_Manual_176.pdf), características; limiar 3,9 L/min também fixado no pedido de 29/10/2026.
- **S4:** [Cassol/Addra Arion 73131B](https://www.cassol.com.br/torneira-misturador-monocomando-para-banheiro-de-mesa-bica-alta-1x2polegadas-metal-arion-black-addra/p), ficha da marca exclusiva: não fornece curva/vazão nominal; consultada 29/10/2026.
- **S5:** [Lorenzetti Versátil — página oficial](https://www.lorenzetti.com.br/produto/aquecedor-versatil) e [manual 373258 Rev.B](https://www.lorenzetti.com.br/manuais/aquecedorversatil/), §§2,4.1,4.3,6–8, consultados 29/10/2026. Manual prevalece sobre texto comercial genérico.
- **S6:** [Rheem México 10 L](https://www.rheem.com.mx/product/calentador-de-deposito-electrico-mural-10-l/), [ficha oficial](https://media.rheem.com.mx/wp-content/uploads/sites/16/2023/10/Ficha-Mural-.pdf), [manual do fabricante RME-MAN01A, cópia do distribuidor](https://h2otek.com/tienda/wp-content/uploads/2022/05/Manual-Calentador-Electrico-Mural-10L-2021.pdf), dimensões/proteção e instalação, consultados 29/10/2026. Não é seleção comercial brasileira.
- **S7:** [ABNT NBR 5410:2004 corrigida 2008 — cópia na Universidade Nilton Lins](https://universidadeniltonlins.com.br/wp-content/uploads/2019/04/NBR-5410.pdf), itens citados acima; edição aplicável a confirmar pelo RT.
- **S8:** [Ferreira Costa — PEX](https://www.ferreiracosta.com/produto/471249/tubo-pex-s5-com-1-metro-dn20x1,9mm-amanco-hidraulica).
- **S9:** [Sodimac — CPVC](https://www.sodimac.com.br/sodimac-br/product/35329/tubo-aquaterm-22mm-3-metros/35329/).
- **S10:** [Ferreira Costa — canaleta](https://www.ferreiracosta.com/produto/357556/canaleta-com-tampa-50x50-2m-branca-ilumi).
- **S11:** [Sodimac — Versátil](https://www.sodimac.com.br/sodimac-br/product/52476/aquecedor-versatil-3-temperaturas-5500w-127v-branco/52476/). Medidas comerciais são triagem, não substituem desenho do fabricante.
- **S12:** [Eluma/Paranapanema](https://www.paranapanema.com.br/nossos-produtos/eluma/), linha de cobre para água quente/fria; não comprova acabamento preto nem qualquer tubo inox.

Gerar: `python -B ferramentas/estudos/agua_quente_banheiro.py`. Testar: `python -B ferramentas/estudos/test_agua_quente_banheiro.py`. Os dois arquivos comparativos saem da mesma fonte; [planta e elevação de todas as opções](Comparacao_visual_dos_percursos.html). Cotas e cores não são desenho executivo.
'''


def report(g, rs):
    out = ['# Água quente do banheiro — 13 opções em três famílias\n\nEstudo de 29/10/2026; nenhuma escolha executiva. Critérios definidos abaixo; notas condicionais. A espera é incremental no ramal, não o tempo total desde o E21.\n', CRITERIA,
           '## Resumo\n\n| Opção | Família | Discrição | Facilidade | Espera PEX / CPVC até pia, a 3,9 L/min | Custo relativo | Exige RT? |\n|---|---|---:|---:|---|---|---|']
    for o in OPTIONS:
        m = metrics(rs[o['id']]).get('pia')
        wait = ' / '.join(f(v*60/3.9,1)+' s' for v in m['volumes'].values()) if m else 'Pia fria' if o['id']=='B4' else 'Local; sem ramal quente; ducha não atendida'
        if o['id'].startswith('C') and m:
            wait += '; só deslocamento local'
        out.append(f"| {o['id']} — {o['name']} | {o['id'][0]} | {o['d']} | {o['f']} | {wait} | {o['cost']} | Sim |")
    out.extend(['\nA: discretas. B: simples. C: sem extensão desde o enchimento, **não sem ligações locais**. B4/C3 não atendem todo o programa; C1 sem produto/encaixe demonstrado.\n', PREMISES,
                '## Cotas R54 usadas\n\n| Objeto | Caixa global Xmin,Ymin,Zmin → Xmax,Ymax,Zmax (mm) |\n|---|---|'])
    for n in ['Peca159','Peca190','Peca399','Peca400','Peca401','BC43_CaixaBase','BC43_Fundo','BC43_Sifao']:
        out.append(f"| `{n}` | {g['boxes'][n]} |")
    dims=[g['interior'][i+3]-g['interior'][i] for i in range(3)]
    out.append(f"\nCaixa interna antes de sifão/conexões: **{f(dims[0],1)} × {f(dims[1],1)} × {f(dims[2],1)} mm**. SHA256 R54: `{g['sha']}`. Banho {f(g['width'],0)} × {f(g['depth'],0)} mm.\n")
    for o in OPTIONS:
        paths=rs[o['id']]; ms=metrics(paths)
        out.append(f"\n## {o['id']} — {o['name']}\n\n{o['detail']}\n\nDiscrição **{o['d']}/5**, facilidade **{o['f']}/5**, custo **{o['cost']}**.\n\n- **Ofícios:** {o['trades']}.\n- **Operações:** {o['steps']}. Sem estimativa de dias.\n- **Manutenção/limpeza:** {o['access']}\n- **Impactos:** {o['impact']}\n- **RT/construtora e produtos:** {o['rt']}\n")
        if paths:
            out.append('| Destino | Trechos sucessivos (m) | Total (m) | Mudanças 90° no caminho | Volume PEX / CPVC (L) | Espera PEX / CPVC (s) a 3,9 L/min |\n|---|---|---:|---:|---|---|')
            for dest, pts in paths.items():
                m=ms[dest]; seg=' + '.join(f(math.dist(a,b)/1000) for a,b in zip(pts,pts[1:]))
                out.append(f"| {dest} | {seg} | {f(m['length'])} | {m['turns']} | {' / '.join(f(v) for v in m['volumes'].values())} | {' / '.join(f(v*60/3.9,1) for v in m['volumes'].values())} |")
            total=unique_length(paths.values())
            out.append(f"\nRede quente única: **{f(total)} m**, {' / '.join(f(volume(total,d)) for d in DIAMETERS.values())} L (PEX/CPVC), sem duplicar trecho comum. Vazão Arion/espera de uso: **a confirmar**. Perdas térmicas e isolamento: critérios comuns acima; não há cálculo em W.\n")
            if o['id']=='B3':
                out.append('Em B3 os volumes acima são **comparadores de seção PEX/CPVC**, não volume real do cobre/inox ainda sem bitola selecionada.\n')
            if o['id'].startswith('C'):
                out.append('Em C, os tubos locais também são **seções comparativas**: conexões reais do equipamento têm outros diâmetros; reservatório/câmara e engates não incluídos.\n')
        else:
            out.append('Ramal quente externo: **0 m; 0 curvas; 0 L**. Não significa espera física zero no aparelho. Alimentação fria e circuito elétrico dependem de produto; ducha não atendida.\n')
    out.append(ELECTRIC)
    return '\n'.join(out)+'\n'


def svg(g, paths, elevation, ident):
    # Mesma escala horizontal/vertical em cada vista; cotas em milímetros.
    scale=.18 if elevation else .24
    width=2090*scale; height=(2700 if elevation else 1240)*scale
    def point(p):
        return (55+p[0]*scale, 30+(2700-p[2])*scale) if elevation else (55+p[0]*scale, 45+p[1]*scale)
    def rect(u,v,w,h,fill,stroke='#a5aba8'):
        y=30+(2700-v-h)*scale if elevation else 45+v*scale
        return f'<rect x="{55+u*scale}" y="{y}" width="{w*scale}" height="{h*scale}" fill="{fill}" stroke="{stroke}"/>'
    parts=[f'<svg viewBox="0 0 {width+110} {height+100}" role="img" aria-label="{ident}: '+('elevação' if elevation else 'planta')+'">',
           '<style>text{font:12px Arial;fill:#263c38}.pipe{fill:none;stroke-width:3;stroke-linejoin:round}</style>']
    if elevation:
        parts += [rect(0,0,2090,2500,'#faf9f4'),rect(0,0,800,2100,'#dce6dc'),
                  rect(957.5,0,375,800,'#fff'),rect(1490,200,600,545,'#dfd4c1'),
                  rect(1490,745,600,20,'#8b918d'),rect(1490,1150,600,750,'#e0e9eb')]
    else:
        parts += [rect(0,0,2090,1240,'#faf9f4'),rect(0,0,800,1240,'#dce6dc'),
                  rect(0,0,800,300,'#c0cdb9'),rect(957.5,0,375,590,'#fff'),
                  rect(1490,0,600,450,'#dfd4c1')]
    if ident in ['C1','C2']:
        u,v,z=(1950,120,400); x,y=point((u,v,z))
        parts.append(f'<rect x="{x-12}" y="{y-12}" width="24" height="24" fill="#785f9b"/><text x="{x-18}" y="{y-18}">local*</text>')
    if ident=='C3':
        x,y=point((1790,100,900));parts.append(f'<text x="{x-70}" y="{y-10}">Troca da Arion: descartada</text>')
    for dest, pts in paths.items():
        color='#c05b38' if dest=='pia' else '#267c87'
        points=' '.join(f'{point(p)[0]},{point(p)[1]}' for p in pts)
        parts.append(f'<polyline class="pipe" stroke="{color}" points="{points}"/>')
        for p in pts:
            x,y=point(p);parts.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{color}"/>')
        x,y=point(pts[-1]);parts.append(f'<text x="{x+6}" y="{y-6}">{"P" if dest=="pia" else "H"}</text>')
    parts.append(f'<text x="55" y="{height+80}">Box 800 | faixa vaso 690 | gabinete 600 = 2090 mm</text>')
    parts.append('<text x="55" y="18">'+('Elevação — z em altura; teto 2500' if elevation else 'Planta — fundo acima; entrada abaixo; profundidade 1240')+'</text></svg>')
    return ''.join(parts)


def visual(g, rs):
    cards=[]
    for o in OPTIONS:
        ident=o['id']; paths=rs[ident]
        rows=''.join(f'<tr><td>{dest}</td><td>{f(m["length"])} m</td><td>{m["turns"]}</td><td>'+ ' / '.join(f(v*60/3.9,1) for v in m['volumes'].values())+' s</td></tr>' for dest,m in metrics(paths).items())
        cards.append(f'''<article data-family="{ident[0]}" id="{ident}"><header><span class="tag">{ident}</span><h2>{html.escape(o['name'])}</h2></header>
<p>{html.escape(o['detail'])}</p><p><b>Discrição {o['d']}/5 · Facilidade {o['f']}/5 · Custo {o['cost']}</b></p>
<div class="views"><figure>{svg(g,paths,False,ident)}</figure><figure>{svg(g,paths,True,ident)}</figure></div>
<table><thead><tr><th>Destino</th><th>Comprimento</th><th>Curvas 90°</th><th>Espera PEX / CPVC*</th></tr></thead><tbody>{rows or '<tr><td colspan="4">Sem ramal quente exterior; ducha não atendida.</td></tr>'}</tbody></table>
<p><b>Ofícios:</b> {html.escape(o['trades'])}. <b>Operações:</b> {html.escape(o['steps'])}.</p>
<p><b>Acesso e limpeza:</b> {html.escape(o['access'])}</p><p><b>Impactos:</b> {html.escape(o['impact'])}</p>
<p class="condition"><b>RT/construtora:</b> {html.escape(o['rt'])}</p></article>''')
    return '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Água quente — 13 opções | Guedala Park</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1f2ed;color:#253b36;font:16px/1.5 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:32px 24px}h1{font-size:clamp(26px,4vw,42px);line-height:1.15}h2{font-size:23px;margin:0}p{max-width:100ch}a{color:#21666e}nav{display:flex;gap:8px;flex-wrap:wrap;margin:24px 0}button{font:inherit;border:1px solid #71857c;padding:10px 18px;border-radius:4px;background:white;color:#253b36;cursor:pointer}button[aria-pressed=true]{background:#253b36;color:white}article{background:white;border:1px solid #d3dad2;padding:24px;margin:20px 0;border-radius:8px}article header{display:flex;gap:16px;align-items:center}.tag{background:#dce6dc;padding:6px 12px;font-weight:bold}.views{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:center;background:#f9faf7}figure{margin:0}svg{display:block;width:100%;max-height:620px}.condition{border-left:4px solid #b98c3b;padding-left:12px}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;border-bottom:1px solid #d3dad2;padding:8px}small{display:block}article[hidden]{display:none}.summary{padding:20px;background:#e1e9df}.legend{display:flex;gap:20px;flex-wrap:wrap}.hot{color:#a44428}.branch{color:#267c87}@media(max-width:720px){main{padding:18px 12px}article{padding:16px}.views{grid-template-columns:1fr}table{font-size:12px}th,td{padding:5px}}@media print{nav{display:none}article{break-inside:avoid}body{background:white}}
</style></head><body><main><a href="README.md">Banheiro</a><h1>Água quente: o que muda em cada caminho</h1><p>13 propostas · 29/10/2026 · geometria R54 · nenhuma opção escolhida.</p>
<div class="summary"><b>Começar pela comparação:</b> B2 (calha com tampa), A1 (forro existente), A6 (rodapé técnico).<br>Mais discreta: A1 → A4 → A5. Mais simples: B1 → B2 → A6. Condições de passagem podem mudar a ordem.</div>
<p><a href="Comparacao_rotas_agua_quente.md">Abrir estudo completo: critérios das notas, trechos, volumes, fontes, produtos e elétrica</a></p>
<p><b>Geometria medida ≠ hidráulica existente.</b> Posição da derivação S não conhecida: cenário usa borda do enchimento e zS=1,20 m. Teto documental 2,50 m; eixos alto/baixo são hipóteses. Rotas baixas cruzam o envelope do VIP: não há comprovação de passagem atrás dele.</p>
<p>* Espera incremental a 3,9 L/min de água quente, até B02/B06; exclui E21→S, engates, partida e aquecimento do tubo. Vazão Arion a confirmar. Em C é só referência de deslocamento local; não se usa E21. C1 sem produto/encaixe adequado; C3 não conserva Arion nem aquece a ducha. Calha representada pelo eixo, sem seção definida.</p>
<div class="legend"><b class="hot">Laranja: caminho até pia P</b><b class="branch">Azul: caminho até ducha H</b><span>* Quadrado roxo: conexão local hipotética, não tamanho do aparelho</span></div>
<nav aria-label="Filtrar família"><button data-filter="all" aria-pressed="true">Todas (13)</button><button data-filter="A" aria-pressed="false">A · Discretas (6)</button><button data-filter="B" aria-pressed="false">B · Simples (4)</button><button data-filter="C" aria-pressed="false">C · Geração local (3)</button></nav>
''' + ''.join(cards) + '''<small>Gerado por ferramentas/estudos/agua_quente_banheiro.py, a partir da base vinculada ao SHA da R54. Sem alteração do CAD. Desenhos de estudo; não usar para execução.</small></main>
<script>document.querySelectorAll('button[data-filter]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('button[data-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelectorAll('article').forEach(a=>a.hidden=b.dataset.filter!=='all'&&a.dataset.family!==b.dataset.filter)}));</script></body></html>'''


def main():
    g=geometry(); rs=routes(g)
    md=report(g,rs).rstrip()+'\n'; page=visual(g,rs)
    if len(md.encode('utf-8'))>60*1024 or len(page.encode('utf-8'))>1024*1024:
        raise ValueError('Limite de tamanho')
    (OUT/'Comparacao_rotas_agua_quente.md').write_text(md,encoding='utf-8')
    (OUT/'Comparacao_visual_dos_percursos.html').write_text(page,encoding='utf-8')
    print(f'13 opções; MD {len(md.encode())} bytes; HTML {len(page.encode())} bytes; CAD não aberto/alterado.')


if __name__ == '__main__':
    main()
