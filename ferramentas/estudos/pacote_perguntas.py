"""Varredura rastreável de pendências; modelos de consulta, sem envio automático."""
import argparse
import csv
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode = True
import comparador_cotacoes as io

ROOT = io.ROOT
AREA = ROOT / '01_Programa_e_decisoes/Perguntas_em_aberto'
OUT = ROOT.parent / 'outputs/Codex_perguntas_e_risco'
RECIPIENTS = ['Elias', 'RT', 'Construtora', 'Condomínio/administração', 'Oficina/marceneiro', 'Fornecedor', 'Concessionária de gás', 'Outro']
SIGNAL = r'\?|penden|a definir|a confirmar|condicionad|depende|falt[ae]|confirmar|solicitar|pergunt|\[RT\]|\[ADM\]'
# Chaves semânticas estáveis. A varredura conserva todos os trechos de suporte.
# Tema; destinatário; pergunta; bloqueios; tipo; momento; padrão de triagem.
RULES = [
 ('medicao','marcenaria','Oficina/marceneiro','Quem fará o levantamento após as chaves, em quais datas, e quais medidas PD/DIM/MOV/PTO/PR, prumo, esquadro, piso, datum e acessos serão validados antes do executivo?', 'compra|corte|fabricação|obra|mudança','medida real','na vistoria',r'medidas_e_impactos|descricao_fisica|datum|levantamento|medição|medir|prumo|esquadro'),
 ('executivo','marcenaria','Oficina/marceneiro','Qual prazo mínimo, provável e máximo de medição → executivo → fabricação → montagem, incluindo fila, ensaios, ferragens e etapa D05-C? Confirmar a referência de fabricação 5–6 semanas e o que a faz mudar.', 'corte|fabricação|obra|mudança','informação documental','antes de fabricar',r'5.?6 semana|prazo.*(oficina|fabrica|marcenaria)|fila|cronograma'),
 ('rt_escopo','estrutura/laje','RT','Qual escopo de contratação cobre levantamento, projetos/interfaces, visitas, responsabilidade por projeto e execução, ART/RRT e plano de reforma? Informar entregáveis, prazo e preço discriminado.', 'protocolo da reforma|obra|mudança','parecer técnico/ART','antes do protocolo',r'contratar.*(rt|profissional)|responsável técnico|rrt|art\b'),
 ('protocolo','estrutura/laje','Condomínio/administração','Quais documentos, formulários, ART/RRT, laudos, taxas e prazo de análise são exigidos para protocolar a reforma? Como tratar exigências e reapresentações?', 'protocolo da reforma|obra|mudança','informação documental','antes do protocolo',r'protocolo|formulário|análise.*(condom|admin)|documentos.*(exigid|anex)'),
 ('horarios','mudança','Condomínio/administração','Quais dias e horários de obra e serviços ruidosos valem, inclusive sábados/feriados, e quais taxas, avisos e sanções? Esclarecer a redação contraditória do art. 57, f.', 'obra|mudança','informação documental','antes do protocolo',r'horário|feriado|taxa|art\. 57, f'),
 ('elevador','mudança','Condomínio/administração','Como reservar elevador de serviço para materiais e mudança, proteger áreas comuns e retirar entulho? Informar dimensões, carga, horários e prazos de aviso.', 'compra|obra|mudança','autorização','antes da mudança',r'elevador|entulho|áreas comuns|movimentação|aviso prévio'),
 ('manual','estrutura/laje','Construtora','Fornecer memorial descritivo, manual do proprietário e documentos de garantia; indicar quais versões correspondem à Torre 2, final 06.', 'protocolo da reforma|obra','informação documental','antes da vistoria',r'memorial|manual do proprietário'),
 ('estrutura','estrutura/laje','Construtora','Fornecer especificação e planta dos blocos estruturais, limitações de furos/ancoragens e posição das instalações embutidas, com documento identificando a unidade.', 'corte|fabricação|protocolo da reforma|obra','informação documental','antes do protocolo',r'bloco estrutural|alvenaria estrutural|estrutura|rasgo|furar parede'),
 ('acustica_acima','acústica','Construtora','Qual composição real da laje e do piso do andar superior, com ensaio/relatório de desempenho acústico do sistema e identificação da unidade/tipologia?', 'compra|protocolo da reforma|obra','informação documental','antes de comprar',r'andar.*cima|superior.*piso|laje.*acúst|laje.*acust|contrapiso'),
 ('acustica_cond','acústica','Condomínio/administração','Qual critério acústico e documentação/ensaio aceitos para trocar o piso por vinílico Olmo? Há exigências para manta, ruído de impacto e equipamentos?', 'compra|protocolo da reforma|obra','autorização','antes de comprar',r'critério acústico|regra.*ruído|condom.*acúst|art\. 6º, w'),
 ('acustica_rt','acústica','RT','Com a envoltória real, quais caminhos de transmissão dominam e quais intervenções/ensaios de piso, teto, parede, portas e equipamentos são tecnicamente viáveis? Separar isolamento e absorção, custo e perda de altura.', 'compra|protocolo da reforma|obra','parecer técnico/ART','antes de comprar',r'acústic|acustic|isolamento|vibra|transmissão|sonor'),
 ('eletrica','elétrica','RT','Conferir quadro, disjuntores/DR/terra, tensão, circuitos, carga e novos pontos 20 A/forno/iluminação: quais bitolas, proteções, traçados e acessos são necessários? Tampas cegas não demonstram capacidade disponível.', 'compra|protocolo da reforma|obra','parecer técnico/ART','antes do protocolo',r'elétric|eletric|quadro|circuito|disjunt|tensão|20 A|127 V'),
 ('instalacoes_doc','elétrica','Construtora','Fornecer projetos de instalações elétricas, hidráulicas e de gás do final 06, quadro de cargas, eixos/cotas e identificação dos pontos previstos.', 'protocolo da reforma|obra','informação documental','antes da vistoria',r'projetos de instalações|quadro de cargas|diagrama'),
 ('agua','hidráulica','RT','Qual traçado de água quente/fria, material, pressão/vazão dinâmica, acesso e teste atendem pia/lavatório/ducha/Telca e preservam estrutura, manutenção e orçamento? Comparar somente rotas já documentadas.', 'compra|protocolo da reforma|obra','parecer técnico/ART','antes do protocolo',r'água quente|hidráulic|hidraulic|vazão|pressão|sifão|telca|ramal'),
 ('gas_laudo','gás','Construtora','Fornecer laudos de estanqueidade de gás/hidráulica/impermeabilização e registro dos testes da unidade; identificar condições e responsáveis pela primeira ativação.', 'protocolo da reforma|obra|mudança','informação documental','antes da vistoria',r'laudo|estanqueidade|teste de pressão'),
 ('gas','gás','Concessionária de gás','Quais condições documentadas para ativar GN e ligar KE4GC/E21, testar estanqueidade e executar conversão se elegível? Informar agendamento, materiais e custos, sem manipular a instalação por conta própria.', 'compra|obra|mudança','informação documental','antes de comprar',r'gás|\bgn\b|concession|cooktop|exaustão|e21'),
 ('clima','climatização','RT','Confirmar carga térmica total, ventilação/exaustão, regras para climatização e viabilidade de dreno/condensadora/alimentação antes de qualquer compra; separar parcelas de cálculo de solução executiva.', 'compra|protocolo da reforma|obra','parecer técnico/ART','antes de comprar',r'climat|ar.condicionado|térmic|tmy|condensadora'),
 ('impermeab','piso','RT','Que reparos, impermeabilização, cura e ensaios são necessários no box/lavanderia e contrapiso antes dos revestimentos? Confirmar estado entregue e limites dos sistemas escolhidos.', 'compra|obra|mudança','parecer técnico/ART','na vistoria',r'impermeabil|umidade|cura|caimento|ralo'),
 ('piso','piso','Fornecedor','Fornecer ficha do piso Olmo e sistema completo: limites de umidade/planicidade, adesivo, preparo, lote, quantidade e documentação acústica. Confirmar preço entregue e serviço preservado.', 'compra|obra','informação documental','antes de comprar',r'vinílico|olmo|piso|rodapé|revestimento'),
 ('box','pedras','Oficina/marceneiro','Compatibilizar box, porta e BC43: medir as duas paredes verdes (chuveiro e janela), definir altura/paginação e descontar abertura; orçamento usa 1,24×2,47 e hipótese adicional 0,80×2,47 m sem desconto. Conferir vão/eixo de porta e manutenção antes da compra/corte.', 'compra|corte|fabricação|obra','medida real','na vistoria',r'box|bc43|porta.*banheiro|bancada.*porta'),
 ('pedras','pedras','Fornecedor','Confirmar gabarito após inferiores montados, cortes/apoios da pedra Branco Itaúnas, tanque/prateleira e prazo real de fabricação/instalação (7–10 dias ou 1–2 semanas), com frete e montagem discriminados.', 'compra|corte|obra|mudança','informação documental','antes de comprar',r'pedra|granito|gabarito|itaúnas|itaunas'),
 ('ancoragem','marcenaria','RT','Para os aéreos e bancadas, confirmar substrato real, parede/revestimento, contato, ancoragens e instalações ocultas; definir fixadores e responsabilidade técnica, sem inferir capacidade dos estudos nominais.', 'compra|corte|fabricação|obra','parecer técnico/ART','antes de fabricar',r'ancorag|substrato|suspens|aéreos|capacidade|carga|resistên'),
 ('juntas','marcenaria','Oficina/marceneiro','Apresentar produto e montagem/ensaio das juntas, fundos, apoios, contatos, retenções e furação dos móveis indicados nas origens; confirmar Minifix/Confirmat/cavilhas e P19: 12 documentais versus 8 no mapa.', 'compra|corte|fabricação','parecer técnico/ART','antes de fabricar',r'junta|minifix|confirmat|cavilha|ligação|furação|furo|apoio|fundo'),
 ('mecanismos','marcenaria','Oficina/marceneiro','Validar banco de duas tampas com piano/articuladores com trava, cesto, gavetas FGVTN 500/MOVENTO 400 e rodízios: ensaio, fixação, curso, batentes, estabilidade e retirada/manutenção, sem trocar especificação silenciosamente.', 'compra|corte|fabricação','parecer técnico/ART','antes de fabricar',r'banco|cesto|gaveta|fgvtn|movento|rodízio|trava|batente|retirada'),
 ('movimentos','marcenaria','Oficina/marceneiro','Quais folgas e limitadores reais evitam choques de portas, varal carregado, lixeiras, cadeiras e equipamentos, considerando montagem e percurso completo? Mostrar gabarito/ensaio dos casos apontados nas origens.', 'compra|corte|fabricação','medida real','na vistoria',r'colis|choque|movimento|folga|varal|lixeira|circulação|giro'),
 ('chapas','marcenaria','Fornecedor','Confirmar SKU/cor/espessura/faces/formato e processo das chapas: 14 no misto (8 de 1850 + 6 de 2100) não equivalem ao subconjunto de 15 em 1850; resolver 33 bloqueados e fundo P01/Peca208 inteiro antes da compra.', 'compra|corte|fabricação','informação documental','antes de comprar',r'chapa|plano.de.corte|formato|sku|arenza|louro|branco tx'),
 ('fita','marcenaria','Fornecedor','Confirmar regra de borda, cor/SKU, espessura, largura e metragem da fita (191,136 m; 210,2496 m com perda) e os 23 painéis sem regra; separar material e colagem já incluída.', 'compra|corte|fabricação','informação documental','antes de comprar',r'fita|borda|colagem'),
 ('cotacao','marcenaria','Fornecedor','Enviar preço instalado comparável do integral e da etapa D05-C, com inclusões, exclusões, 40 ferragens sem quantidade, créditos reais, frete, tributos, validade, garantia e pagamento. Quais preços dependem de medição e reajuste?', 'compra|fabricação|mudança','informação documental','antes de comprar',r'cotação|proposta|preço|preco|frete|garantia|reajuste|orçament|meta.*mil'),
 ('ilum_produto','iluminação','Fornecedor','Fornecer manuais/SKUs e confirmar comando físico, Alexa/celular, compatibilidade WiZ/Elgin/Shelly, âmbar/dimerização, fontes/perfis acessíveis e preço completo de IL02–IL09; preservar D03-B/D04-A/D06-B.', 'compra|corte|obra','informação documental','antes de comprar',r'ilumina|lumin|elgin|wiz|shelly|âmbar|dimer|led|fonte|plafon'),
 ('amostras','marcenaria','Elias','Após receber as amostras Lume/Areia ao lado do Arenza, qual acabamento final deve ser registrado com código comercial? O pedido A/C de D02 já está definido; confirmar somente a escolha final por amostra.', 'compra|corte','decisão de Elias','antes de comprar',r'amostra|lume|areia|acabamento.*final'),
 ('chaves_data','contrato/atraso','Construtora','Qual data de vistoria/chaves está formalmente comunicada e quais condições/documentos faltam para a entrega? Separar previsão pública, prazo contratual e confirmação individual, sem presumir equivalência de paralisação e atraso.', 'obra|mudança','informação documental','antes da vistoria',r'contrato|atraso|paralisa|chaves|entrega.*imóvel|habite'),
 ('asbuilt','estrutura/laje','Construtora','Fornecer o conjunto como construído (as built) da unidade, com revisões e divergências em relação ao projeto original, identificando paredes, laje e instalações realmente executadas.', 'protocolo da reforma|obra','informação documental','antes da vistoria',r'as built|como construído'),
 ('laje','estrutura/laje','Construtora','Qual espessura, composição e sistema estrutural da laje da unidade? Fornecer detalhe/projeto ou documento técnico correspondente, inclusive restrições para fixação e cargas.', 'compra|protocolo da reforma|obra','informação documental','antes do protocolo',r'laje|espessura.*teto'),
 ('outros','mudança','Outro','Quem deve esclarecer as condições ainda pendentes registradas nas origens abaixo, em qual documento e antes de qual etapa? Responder por origem/código, preservando medidas, valores e condicionantes citados.', 'compra|obra','informação documental','antes de comprar',r'.*')]
COLS = ['id','chave','pergunta','destinatario','tema','tipo','bloqueia','impacto','quando','dependencia','status','origens','citacoes','respostas_esperadas','itens_bloqueados','total_itens','prioridade','alerta']


def safe(text):
    for phrase in ['liberado para fabricação','capacidade aprovada','carga liberada']:
        text = re.sub(phrase,'[expressão histórica omitida; condição pendente]',text,flags=re.I)
    text = re.sub(r'https?://\S+', '[link na origem]', text)
    text = re.sub(r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}', '[contato omitido]', text)
    text = re.sub(r'(?<!\d)(?:\+?55\s*)?\(?\d{2}\)?[ .-]*9?\d{4}[ .-]*\d{4}(?!\d)', '[dado omitido]', text)
    text = re.sub(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b', '[documento omitido]', text)
    return text


def normalize(text):
    return re.sub(r'\W+', ' ', io.key(text)).strip()


def deduplicate(rows):
    result, answered = {}, []
    for row in rows:
        if row.get('status') == 'respondida':
            if not row.get('resposta_fonte'):
                raise ValueError('Resposta sem fonte')
            answered.append(row)
            continue
        recipient = row.get('destinatario') or 'Outro'
        if recipient not in RECIPIENTS:
            recipient = 'Outro'
        row = dict(row, destinatario=recipient, alerta='destinatário a confirmar' if recipient == 'Outro' else row.get('alerta',''))
        identity = row.get('chave') or normalize(row['pergunta'])
        if identity not in result:
            result[identity] = row
        else:
            for k in ['origens','citacoes']:
                result[identity][k] = sorted(set(result[identity].get(k, []) + row.get(k, [])))
    return list(result.values()), answered


def source_paths():
    paths = [ROOT/'ESTADO_ATUAL.md']
    for folder in ['01_Programa_e_decisoes','03_Ambientes','04_Moveis','05_Orcamento_e_cronograma','07_Imovel','08_Contratos_e_atraso']:
        paths += sorted((ROOT/folder).rglob('README.md'))
    paths += [ROOT/p for p in ['01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md',
        '01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md','07_Imovel/Roteiro_dia_das_chaves_R01.md',
        '07_Imovel/Checklist_vistoria_dia_das_chaves.md','05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md']]
    paths += list((ROOT.parent/'outputs/Codex_acustica_envoltoria').glob('*.md'))
    return sorted({p for p in paths if p.is_file() and 'Perguntas_em_aberto' not in str(p) and '/Risco/' not in p.as_posix()})


def extract():
    paths = source_paths()
    records = []
    for path in paths:
        # rg lê apenas linhas correspondentes; nenhuma leitura integral do Registro.
        command = ['rg','--no-ignore','-n','-i',SIGNAL,str(path)]
        proc = subprocess.run(command,capture_output=True,encoding='utf-8',errors='replace')
        if proc.returncode not in (0,1):
            raise RuntimeError(proc.stderr)
        relative = path.relative_to(ROOT).as_posix() if ROOT in path.parents else '../outputs/' + path.parent.name + '/' + path.name
        for line in proc.stdout.splitlines():
            match = re.match(r'(\d+):(.*)',line)
            if match and 'Perguntas_em_aberto/README.md' not in match[2]:
                text=match[2]
                if 'somente uma parede verde' in text:
                    text='[Trecho superado: Elias, 30/10/2026, pediu verde no chuveiro e na janela.] '+text
                records.append(dict(arquivo=relative,linha=int(match[1]),texto=text))
    extras = [(ROOT/'07_Imovel/Medidas_e_impactos.csv', ','), (ROOT/'04_Moveis/Dependencias/Descricao_fisica.csv',';')]
    external = ROOT.parent/'outputs'
    extras += [(external/'Codex_cotacao_e_chaves'/name, ';') for name in ['Perguntas_RT.csv','Perguntas.csv','Perguntas_modelo.csv']]
    extras += [(p,';') for p in (external/'Auditoria_quantidades').glob('*.csv')]
    for path, delim in extras:
        if not path.exists():
            continue
        paths.append(path)
        for index,row in enumerate(io.read_csv(path,delim),2):
            code = row.get('codigo_medida', '')
            if code.startswith(('LOG-','POS-')):
                continue
            # Conferências aritméticas OK não geram novas perguntas técnicas.
            text = ' | '.join(f'{k}={v}' for k,v in row.items() if v and k not in {'arquivos_ficha','arquivos_prancha','arquivos_readme','arquivos_orcamento'})
            if re.search(SIGNAL,text,re.I) or 'Medidas_e_impactos' in path.name:
                relative = path.relative_to(ROOT).as_posix() if ROOT in path.parents else '../outputs/'+path.parent.name+'/'+path.name
                records.append(dict(arquivo=relative,linha=index,texto=text))
    return records, paths


def build(records):
    grouped = {}
    for rec in records:
        text = rec['texto']
        # Não transformar relato histórico/decisão pura em nova escolha. Pendência residual fica.
        if re.search(r'(D0[1-6]|U[1-4]|F13|LIX)',text) and re.search(r'respondid|Elias.*27/10',text) and not re.search(r'penden|a confirmar|falta|condicion|depende',text,re.I):
            continue
        content = io.key(rec['arquivo'] + ' ' + text)
        if 'medidas_e_impactos' in rec['arquivo'].lower() or 'Descricao_fisica' in rec['arquivo']:
            matches = [RULES[0]]
        else:
            matches = [r for r in RULES[:-1] if re.search(io.key(r[-1]),content,re.I)] or [RULES[-1]]
        for rule in matches:
            key,theme,recipient,question,blocks,kind,when,_ = rule
            group = grouped.setdefault(key,dict(chave=key,pergunta=question,destinatario=recipient,tema=theme,tipo=kind,bloqueia=blocks,quando=when,status='aberta',origens=[],citacoes=[],alerta=''))
            origin = rec['arquivo'] + ':' + str(rec['linha'])
            group['origens'].append(origin)
            # Citação curta exata, salvo remoção de contato/URL explicitamente marcada.
            hit = re.search(SIGNAL,text,re.I)
            start = max(0, hit.start()-25) if hit else 0
            quote = safe(text[start:start+170])
            group['citacoes'].append(origin + ': ' + quote)
    rows,_ = deduplicate(list(grouped.values()))
    ids = {r[0]:f'PQ-{i:03}' for i,r in enumerate(RULES,1)}
    ids.update(outros='PQ-032',asbuilt='PQ-033',laje='PQ-034')
    dependencies = {'executivo':['medicao','juntas','mecanismos'], 'ancoragem':['estrutura','medicao'],
        'juntas':['medicao','ancoragem'], 'protocolo':['rt_escopo','manual'],
        'agua':['instalacoes_doc'], 'eletrica':['instalacoes_doc'], 'gas':['gas_laudo'],
        'piso':['acustica_cond','acustica_acima'], 'pedras':['medicao','executivo'],
        'box':['medicao'], 'amostras':['chapas']}
    # Evita ciclo executivo↔juntas: os vínculos acima são condições do executivo, não da instalação.
    present = {r['chave'] for r in rows}
    for row in rows:
        key = row['chave']
        row['id'] = ids[key]
        row['dependencia'] = '|'.join(ids[k] for k in dependencies.get(key,[]) if k in present)
        row['itens_bloqueados'] = '|'.join(sorted(set(row['bloqueia'].split('|'))))
        row['total_itens'] = len(row['itens_bloqueados'].split('|'))
        critical = key in {'medicao','executivo','juntas','mecanismos','pedras','chapas','fita'}
        security = row['tema'] in {'estrutura/laje','gás','elétrica','hidráulica'} or key in {'ancoragem','impermeab'}
        row['prioridade'] = 1 if critical else 2 if security else 3
        row['impacto'] = ('prazo/segurança/conformidade: alto' if critical or security else 'custo/prazo: médio') + '; bloqueia ' + row['bloqueia'].replace('|',', ')
        row['respostas_esperadas'] = ''
    ordered = sorted(rows,key=lambda r:(r['prioridade'],-r['total_itens'],r['id']))
    consequences = {
        'medicao':'A: cotas confirmadas → conferir folgas/fechamentos nas fichas R15. B: divergência (incluindo lavanderia 1540/1610) → reabrir corte dos móveis atingidos; sem mudar caixas automaticamente.',
        'executivo':'A: prazo de fabricação 5–6 semanas confirmado → usar a faixa na cadeia após executivo/abastecimento. B: fila ou prazo diferente → rever início/fim relativo às chaves; a mudança não está garantida.',
        'pedras':'A: inferiores montados/gabarito concluído → começa o prazo específico das pedras. B: gabarito pendente → entrega/instalação aguardam; não somar 7–10 dias e 1–2 semanas como dois serviços.',
        'estrutura':'A: bloco/laje e instalações documentados → RT pode definir a solução de fixação. B: substrato desconhecido → furos/ancoragens e fabricação correspondente continuam condicionados.',
        'ancoragem':'A: substrato/contato/ancoragem demonstrados → revisar suspensão de P04/P09/P11/P12/P15/P17 e interfaces. B: ausência de dados → não converter estudos nominais em capacidade de uso.',
        'juntas':'A: produto/junta/ensaio documentados → conferir centros e quantitativos nas fichas. B: P19 continua com 12 documentais versus 8 no mapa → manter bases separadas na cotação.',
        'mecanismos':'A: ensaios e produtos fechados → revisar banco/cesto/gavetas e montagem nas fichas. B: falta trava/engate/curso/fixação → fabricação condicionada, sem repetir estudo nominal.',
        'chapas':'A: formato 2100 compatível e SKU confirmado → conferir conjunto misto. B: somente 1850 → Peca208 não cabe inteira; 15 chapas cobrem outro subconjunto e não completam a compra.',
        'fita':'A: regra e SKU definidos → revisar metragem por borda/peça. B: 23 painéis sem regra → custo da fita permanece parcial, não zero.',
        'movimentos':'A: gabarito confirma percurso/roupa/tampas → documentar a montagem real. B: choque ou falta de folga → revisar os móveis/percurso citados, sem alterar CAD neste pacote.',
        'box':'A: parede/altura confirmadas → atualizar paginação/quantidade e compra do box/revestimento. B: 0,80×2,25 e 1,24×2,47 continuam conflitantes → não deduzir economia; conferir BC43/porta.',
        'rt_escopo':'A: escopo/ART/RRT/visitas contratados → completar plano e anexos. B: ausência de responsável → protocolo e obra continuam pendentes.',
        'eletrica':'A: carga/circuitos reais conferidos → RT dimensiona e compatibiliza a planta de pontos. B: tampas cegas ou pontos não identificados → custos e implantação permanecem pendentes.',
        'agua':'A: rota/acesso/vazão demonstrados → RT compatibiliza água quente e interfaces. B: sem rota/pressão real → compra e obra permanecem condicionadas.',
        'gas_laudo':'A: laudos e condições de ativação documentados → conferir ligação GN/KE4GC/E21 com habilitado. B: ausência de testes/documentos → ativação e uso aguardam.'}
    for row in ordered[:15]:
        # Somente consequências já contidas nas origens; não inventa solução A/B técnica.
        row['respostas_esperadas'] = consequences.get(row['chave'], 'A: condição documental confirmada → revisar os alvos indicados nas origens antes de '+row['bloqueia'].split('|')[0]+'. B: ausente/divergente → manter '+row['bloqueia'].replace('|',', ')+' pendentes; não presumir custo/prazo.')
    for row in ordered:
        if row['chave'] in {'amostras','ilum_produto','cotacao','mecanismos'}:
            row['status']='respondida parcialmente'
    return ordered


def decision_audit():
    path = ROOT/'01_Programa_e_decisoes/Registro_de_decisoes.md'
    proc = subprocess.run(['rg','-n','-i',r'D0[1-6]|U1.*U4|LIX=A|F13=A|sem tubos|10 cm livres acima',str(path)],capture_output=True,encoding='utf-8',errors='replace')
    if proc.returncode not in (0,1):raise RuntimeError(proc.stderr)
    # Decisões comerciais Dxx também têm fonte corrente explícita no roteiro.
    current = ROOT/'01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md'
    answer_rows=[]
    for i,line in enumerate(current.read_text(encoding='utf-8').splitlines(),1):
        if re.search(r'^\s*(?:-\s*)?\*\*D0[1-6].*Elias',line) and re.search(r'27/10',line):
            answer_rows.append(dict(codigo=re.search('D0[1-6]',line)[0],status='respondida',resposta_fonte='01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md:'+str(i),resposta=safe(line)))
    return proc.stdout, answer_rows


def messages(rows):
    directory=AREA/'Mensagens';directory.mkdir(parents=True,exist_ok=True)
    for recipient in RECIPIENTS:
        selected=[r for r in rows if r['destinatario']==recipient]
        name=io.key(recipient).replace('/','_').replace(' ','_')
        placeholder = {'RT':'[RT]','Construtora':'[Construtora]','Condomínio/administração':'[Condomínio]','Fornecedor':'[Fornecedor Fxx]'}.get(recipient,'[Destinatário]')
        lines=['# Consulta — '+recipient,'','Olá, '+placeholder+'.','',
            'Estamos preparando a reforma de um apartamento no 8º andar, Torre 2, final 06.',
            'O projeto tem medidas nominais; precisamos destas informações antes das etapas indicadas.','',
            '**Modelo para revisão e envio pelo solicitante. Nada enviado.**','']
        if recipient=='RT':
            groups=[('Escopo de contratação',[r for r in selected if r['chave']=='rt_escopo']),('Pareceres técnicos',[r for r in selected if r['chave']!='rt_escopo'])]
        elif recipient=='Construtora':
            labels={'manual':'Memorial descritivo e manual','estrutura':'Especificação do bloco estrutural','laje':'Espessura e sistema da laje','asbuilt':'Conjunto as built da unidade','acustica_acima':'Piso do andar de cima e ensaios do sistema','instalacoes_doc':'Projetos de instalações','gas_laudo':'Laudos de gás, hidráulica e impermeabilização','chaves_data':'Comunicação formal de vistoria/chaves'}
            groups=[('Documento: '+labels.get(r['chave'],r['chave']),[r]) for r in selected]
        else:groups=[('Perguntas',selected)]
        index=0
        for title,part in groups:
            if not part:continue
            lines += ['## '+title,'']
            for row in part:
                index+=1
                lines += [f"{index}. **{row['id']}** — {row['pergunta']}",f"   Responder antes de: {row['quando']}. Origens no Perguntas.csv, ID {row['id']}.",'']
        lines += ['Favor responder por ID, anexando o documento aplicável, ART/RRT quando pertinente, croqui cotado ou foto identificada; registrar data, condição e o que continua pendente.','']
        (directory/(name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')


def run(output=OUT):
    output=Path(output).resolve()
    if output==ROOT or ROOT in output.parents:raise ValueError('Brutos devem ficar fora do git')
    output.mkdir(parents=True,exist_ok=True);AREA.mkdir(parents=True,exist_ok=True)
    records,paths=extract(); rows=build(records)
    audit,answers=decision_audit()
    # Dados brutos também ficam externos; não exportar contatos para o pacote.
    io.dump(output/'Extracao_perguntas.json',records)
    (output/'Conferencia_decisoes.txt').write_text(audit,encoding='utf-8')
    public=[];citations=[]
    for row in rows:
        for citation in row['citacoes']:
            origin,_,quote=citation.partition(': ')
            file,_,line=origin.rpartition(':')
            citations.append(dict(id=row['id'],arquivo=file,linha=line,citacao=quote))
        public.append(dict(row,origens=f"Origens.csv: {row['id']} ({len(row['origens'])} origens)",citacoes=' | '.join(row['citacoes'][:2])))
    io.write_csv(AREA/'Perguntas.csv',public,COLS)
    io.write_csv(AREA/'Origens.csv',citations,['id','arquivo','linha','citacao'])
    io.write_csv(AREA/'Respostas_decisoes.csv',answers,['codigo','status','resposta_fonte','resposta'])
    messages(rows)
    top=sorted(rows,key=lambda r:(-r['total_itens'],r['prioridade'],r['id']))[:5]
    manifest=dict(arquivos_varridos=len(paths),trechos_extraidos=len(records),perguntas=len(rows),
        por_destinatario=dict(Counter(r['destinatario'] for r in rows)),por_bloqueio=dict(Counter(b for r in rows for b in r['bloqueia'].split('|'))),
        top5=[dict(id=r['id'],itens=r['itens_bloqueados'],calculo=r['total_itens']) for r in top],
        fontes_sha256={str(p.relative_to(ROOT) if ROOT in p.parents else Path('../outputs')/p.parent.name/p.name):io.sha(p) for p in paths},
        extracao_sha256=io.sha(output/'Extracao_perguntas.json'),perguntas_sha256=io.sha(AREA/'Perguntas.csv'))
    io.dump(output/'Manifesto_perguntas.json',manifest)
    text=['# Perguntas em aberto','',f"**{len(rows)} perguntas deduplicadas**, a partir de {len(records)} trechos de {len(paths)} arquivos. Nada enviado. Cadastro por tema; classificação documental para revisão, sem parecer técnico.",
        '[Perguntas](Perguntas.csv) · [todas as origens/citações por PQ](Origens.csv) · [decisões já respondidas](Respostas_decisoes.csv). IDs semânticos estáveis PQ-001…PQ-034; lacunas de numeração não são perda de pergunta.','',
        '## Destinatários','', '| Destinatário | Perguntas | Modelo |','|---|---:|---|']
    text += [f"| {who} | {manifest['por_destinatario'].get(who,0)} | [mensagem](Mensagens/{io.key(who).replace('/','_').replace(' ','_')}.md) |" for who in RECIPIENTS]
    text += ['', '## Bloqueios e cinco maiores abrangências', '', '| Etapa | Perguntas que a bloqueiam |','|---|---:|']
    text += [f'| {k} | {v} |' for k,v in manifest['por_bloqueio'].items()]
    text += ['', 'Top 5 por **número de classes de etapa diretamente bloqueadas**, sem duplicar a mesma classe. Isso mede abrangência documental, não dias ganhos ou quantidade de peças. Empate: caminho declarado da marcenaria, segurança/conformidade, depois custo. Não há caminho crítico global comprovado.', '']
    text += [f"- {r['id']}: {r['total_itens']} = " + ' + '.join(r['itens_bloqueados'].split('|')) for r in top]
    text += ['', '## Uso e limites','',
        '`python -B ferramentas/estudos/pacote_perguntas.py` (raiz, Python local); testes: `python -B ferramentas/estudos/test_pacote_perguntas.py`.',
        'Varre READMEs recursivos de 01/03/04/05/07/08, estado, plano/roteiro oficial, checklist B1/B2/B3, roteiro de campo, medidas e descrição física; consulta as saídas externas disponíveis. O Registro é consultado somente por rg em códigos/temas, nunca lido inteiro.',
        'Origens.csv mantém uma linha por PQ/origem, com citação curta; Perguntas.csv traz duas citações de consulta e a chave para todas as demais, sem células gigantes. Texto integral extraído e manifesto de hashes ficam em ../outputs/Codex_perguntas_e_risco/. Linha de CSV é registro lógico + cabeçalho; campos multilinha exigem conferência no arquivo. Deduplicação por objetivo semântico conserva as origens; responder por origem/código quando os casos diferirem.',
        'D01–D06 não são reabertas: respostas com fonte estão na tabela separada. Solicitar amostras A/C já foi respondido; a seleção final por amostra e a comprovação técnica continuam pendentes. Decisão de layout não equivale a cumprimento de manual ou ensaio. Remover pergunta respondida exige fonte; resposta parcial permanece. Não inferir resposta de mero uso da palavra confirmado num histórico.',
        'Dependências no CSV representam precedência documental; conferir medidas/datum e contratar RT antes de protocolo, e medição/executivo antes de corte/fabricação. Os 15 primeiros por prioridade recebem consequência A/B conservadora, ligada às próprias origens; não autoriza mudar decisão, peça ou orçamento.',
        'Mensagens são modelos por destinatário, com placeholders. RT separa contratação e pareceres; construtora separa por documento; condomínio cobre protocolo, horários/taxas, piso/ruído e elevador. Sem dados pessoais, contatos ou nome de profissional. Campo Outro exige identificação do destinatário antes de enviar.',
        'Classificação automática tem limites: revisar agrupamentos e contexto nas origens antes de enviar. Trechos históricos não provam pendência atual; decisões explícitas correntes prevalecem. A varredura é rastreável, não certificação de completude técnica.',
        'Publicação: nenhuma alteração em current_release.json/document_library ou no site. Falta registrar este pacote na biblioteca e regenerar/verificar o site em frente autorizada de publicação.', '',
        'SHA256 Extracao_perguntas.json: `'+manifest['extracao_sha256']+'`; Perguntas.csv: `'+manifest['perguntas_sha256']+'`.']
    (AREA/'README.md').write_text('\n'.join(text)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:manifest[k] for k in ['arquivos_varridos','trechos_extraidos','perguntas','por_destinatario','top5']},ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--saida',type=Path,default=OUT)
    run(parser.parse_args().saida)
