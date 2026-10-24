"""Combina evidências R14 sem modificar geometria nem promover hipóteses a liberação."""
from pathlib import Path
import json, re
from collections import defaultdict

STUDY=Path(__file__).resolve().parent
DATA=STUDY/'fabrication'
EVIDENCE=DATA/'r14'
def read(name,folder=EVIDENCE):return json.loads((folder/name).read_text(encoding='utf-8'))
def unique(items):return list(dict.fromkeys(items))

SUMMARIES={
'P01':'RO-62 nas duas portas e FGVTN 500 nas quatro gavetas. Trilhos, varões e ligações têm conferências próprias.',
'P02':'Duas portas independentes com Blum; canecos identificados por peça. Ligações do canto em L continuam específicas.',
'P03':'RO-62 sem Comfort nas duas folhas baixas. Compatibilizar apoio e ligações com o roupeiro.',
'P04':'Blum nas quatro folhas; preservar o recuo diferente da porta vizinha ao canto. Reforço e suspensão seguem em projeto.',
'P05':'Blum nas duas portas. A prateleira hidráulica só recebe recorte após definir cuba e sifão.',
'P06':'Três pares FGVTN 500. Parâmetros do fabricante registrados; engates e datum final exigem conferência.',
'P07':'Grelhas removíveis com M4 e retenção metálica a detalhar. Preservar os canais de ventilação.',
'P08':'Seis rodízios fixos Leão Aço de 38 mm + seis espaçadores rígidos de 1 mm selecionados. Apoio de 39 mm preservado; furação real, carga, guias e batente a conferir.',
'P09':'Blum nas duas portas. Divisor até o fundo forma dois nichos 298 × 312; preservar o retorno de ar de 20 mm do depurador.',
'P10':'Blum nas portas e 20 conjuntos Minifix. Três prateleiras fixas desmontáveis, com furação nominal por peça.',
'P11':'Blum nas portas e 12 conjuntos Minifix. Furação nominal verificada na geometria; carga e suspensão separadas.',
'P12':'Blum nas portas. Ligações da divisória central e suspensão precisam de mapa próprio.',
'P13':'Apoio aberto do micro-ondas. Suporte estrutural e divergência de ventilação continuam pendências de projeto.',
'P14':'Carcaça e cesto têm ligações separadas. O mecanismo basculante a 55° ainda exige solução comprovada para a aplicação.',
'P15':'Blum nas portas e 8 conjuntos Minifix. O vão de 799 mm mantém a necessidade de reforço e carga definida.',
'P16':'MOVENTO 400 selecionada para as duas gavetas. FGVTN 400 sai da lista ativa; corrigir interferências antes de usinar.',
'P17':'Blum nas quatro portas. Ligações das divisórias e distribuição da suspensão continuam específicas.',
'P18':'RO25 no banheiro e quadro removível por quatro M6. Cavilhas e ligações permanentes ficam separadas da retirada.',
'P19':'Blum nas portas, oito apoios Häfele .711 e mapa nominal de 12 conjuntos Minifix para as seis interfaces da caixa. Estudo separado; montagem, espelho e suspensão a validar.',
'P20':'Diretriz de 23/10: dobradiça piano + articulador com trava em cada tampa. Protótipo de oficina, apoio da piano e terminais ainda bloqueiam a furação das tampas.'}

# P20: diretriz piano + trava (Banco_cesto_simples_2026-10-23) substitui a cadeia Southco R47 nas listas ativas.
BANCO='01_Projeto/Banco_cesto_simples_2026-10-23/'
P20_SOUTHCO_ROWS={'Contraplatinas móveis','Suportes fixos das dobradiças','Placas receptoras fixas','Parafusos móveis',
  'Arruelas dos parafusos móveis','Parafusos suporte–corpo','Fixadores da folha fixa de cada Southco ao suporte'}
P20_ROWS=[
  dict(item='Dobradiça piano das tampas 971 e 825',reference='Piano aço zincado 1800 × 30 mm (Mega Full USH-160) ou 2000 × 30; referência dimensional Mahler Ref.54',
       quantity=2,unit='trechos cortados de 1–2 barras',status='Proposta de cotação; protótipo pendente',
       assembly='Um trecho na borda traseira de cada tampa. Apoio fixo e rebaixo ocultos na junta de 2 mm do encosto ainda a detalhar.',
       sources=[{'title':'Preços e conjunto proposto R01','path':BANCO+'Precos_e_conjunto_R01.md'}]),
  dict(item='Articuladores com trava das tampas',reference='Bigfer 04.03.185/183 epóxi branco (dir./esq.) ou equivalente conferido na peça',
       quantity=4,unit='unidades (1 par por tampa)',status='Proposta de cotação; protótipo pendente',
       assembly='Terminais 22 mm (tampa 971) e 30 mm (tampa 825) abaixo da face inferior; posições nominais na conferência, não gabarito de furação.',
       sources=[{'title':'Conferência nominal das ferragens simples','path':BANCO+'Conferencia/Resultado.md'}])]
P20_CHECKS={
  'Fornecedor: eixo–face e sentido F0/R0 do CAD ou desenho cotado exato; a cota 20,3 é envelope, não eixo.':
    'Projeto: detalhar apoio fixo e rebaixo da piano na junta de 2 mm do encosto; o encosto é reserva de volume, não apoio resistente.',
  'Projeto/oficina: recalcular massa/CG com dobradiças,contraplatinas,parafusos e batente;0,5 kgdemetais móveis anterior não comprovado.':
    'Projeto/oficina: recalcular massa/CG das tampas com piano, articuladores e batente; esforço nominal 2,4–3,9 kgf na borda dianteira.',
  'Oficina/metalurgia: fechar suportes,contraplatinas e batente independente antes dos furos das tampas; bolsas sob almofadas já autorizadas, mas dimensões finais dependem do mecanismo.':
    'Oficina: montar protótipo com 1 piano e 2 pares de articuladores antes dos furos das tampas; conferir engate da trava, terminais e batente.'}

def revise_p20(hardware,decisions,drilling,project,workshop,assembly):
    hardware=[r for r in hardware if r['item'] not in P20_SOUTHCO_ROWS and 'Southco' not in r['item']]+[dict(r) for r in P20_ROWS]
    decisions=[d for d in decisions if 'Southco' not in d['item']]
    decisions.insert(0,dict(item='Mecanismo das tampas',reference='Dobradiça piano + articulador com trava por tampa',quantity=None,unit='',
      status='Diretriz de 23/10/2026; produto e montagem pendentes',
      reason='Solução mais simples e barata pedida por Elias, mantendo as duas tampas presas. Southco E6 (R47) fica como alternativa histórica, fora da lista ativa.',
      sources=[{'title':'Diretriz banco e cesto','path':BANCO+'Diretriz.md'}]))
    drilling=[d for d in drilling if 'Southco' not in d['item']]
    for row in hardware+drilling+decisions:
        for field in ['reference','fastener']:
            if isinstance(row.get(field),str):
                row[field]=row[field].replace('; suportes/contraplatinasM6 do estudoSouthcoR47','; apoio fixo da piano e articuladores a detalhar')
    project=[P20_CHECKS.get(c,c) for c in project]
    workshop=[P20_CHECKS.get(c,c) for c in workshop]
    assembly=[s.replace('Dobradicas de atrito','Dobradiça piano e articuladores') for s in assembly if 'contraplatinas' not in s and not s.startswith('Southco e batente R47')]
    assembly.append('Southco E6 e batente R47 permanecem em estudo separado como alternativa; não usar Rockler traseira rejeitada como especificação vigente.')
    return hardware,decisions,drilling,project,workshop,assembly

def build():
    old=read('hardware-audit.json',DATA)
    finish=read('finish-audit.json',DATA)
    fields=read('field-review.json')
    joinery=read('joinery.json')
    mechanisms=read('mechanisms.json')
    hinge_maps=read('hinge-drilling-maps.json')
    geometry=read('joinery-geometry.json')
    result={'revision':'R14','date':'2026-10-23','cadRevision':'R45','source_sha256':joinery['source_sha256'],
      'scope':'Seleções de projeto e mapas nominais. Sem alteração da R45, sem medição realizada e sem liberação geral de fabricação.',
      'quantityRules':old['countRules'],
      'budgetNote':'Recotar dobradiças Blum: a provisão anterior de FGVTN não confirma o preço desta seleção.',
      'modules':{}}
    for code,o in old['modules'].items():
        j=joinery['modules'][code];m=mechanisms['modules'][code]
        replaced=set(m.get('replacedItems',[]))
        hardware=[dict(r) for r in o['hardwareRows'] if r['item'] not in replaced]
        hardware+=m.get('hardwareRows',[])
        # Joinery decisions replace the generic undefined line, not the mechanisms.
        for row in hardware:
            if row['item']=='Ligações dos painéis da carcaça':
                row.update(reference=j['decisions'][0]['reference'],status='Estratégia selecionada; mapa parcial',assembly=j['decisions'][0]['reason']+' Consultar as interfaces ainda sem mapa na ficha.')
            elif row['item']=='Suspensão do móvel e interface com a parede':
                row.update(reference='Ligação interna acessível ao fundo/laterais; não adotar SAH215 sem rebaixo',status='Detalhamento de projeto pendente',assembly='Definir ferragem e ligação à caixa em projeto. Substrato e instalações ocultas são levantamento; ancoragem é dimensionada depois.')
        if code in ['P10','P11','P15','P19']:
            hardware=[r for r in hardware if 'Minifix' not in r['item']]
            qty={'P10':20,'P11':12,'P15':8,'P19':12}[code]
            for item,ref in [('Caixas Minifix','Häfele 262.26.034'),('Pinos Minifix','Häfele S100 262.28.920')]:
                hardware.append(dict(item=item,reference=ref,quantity=qty,unit='unidades',status='Selecionado em projeto',assembly='Um conjunto por caixa + pino. Posições nominais na seção de furação; validar na chapa real.'))
        if code=='P19':
            for row in hardware:
                if row['item']=='Apoios das duas prateleiras':row['status']='Selecionado em projeto'
                if row['item']=='Ligações dos painéis da carcaça':row.update(status='Mapa nominal emitido em estudo separado; prova pendente',assembly=j['decisions'][0]['reason'])
        if code=='P18':
            for row in hardware:
                if row['item'] in ['Confirmat de união do quadro','Cavilhas da união permanente do quadro','Parafusos de retirada do quadro','Porcas transversais','Cavilhas da interface desmontável']:
                    row['status']='Selecionado em projeto; conferir usinagem'
        if code=='P07':
            for row in hardware:
                if row['item']=='Roscas retidas das grelhas':
                    row.update(reference='Placa/porca metálica M4 retida, desmontável; seção e fixação a detalhar',status='Estratégia selecionada; desenho pendente',assembly='Não aplicar RAMPA SKD30 automaticamente em MDF. Conferir retenção da placa e acesso na oficina.')
        decisions=m.get('decisions',[])+j['decisions']
        drilling=m.get('drilling',[])+j['drilling']
        for i,row in enumerate(drilling,1):
            row['id']=f'{code}-F{i:02}'
            if code=='P08' and not row.get('sources'):
                row['sources']=[{'title':'Pendência de produto registrada na auditoria R13; não é manual de furação','path':'01_Projeto/Estudo_interativo/fabrication/hardware-audit.json'}]
        checks=unique(m.get('technicalChecks',[])+j['technicalChecks'])
        extras={
          'P01':[old['modules']['P01']['technicalChecks'][4],old['modules']['P01']['technicalChecks'][5]],
          'P02':['Revisar as quatro formas de dobradiças do canto registradas como inválidas no inventário. O mapa de canecos não repara os sólidos do mecanismo.'],
          'P07':['Dimensionar as ligações da base/nervuras e réguas sem fechar ventilação; definir comprimento e cabeça dos M4 conforme a retenção metálica escolhida.'],
          'P13':['Resolver a divergência de ventilação: a escolha F104 mantém 100 mm acima do ME23P, enquanto o manual pede 300 mm. A furação do suporte permanece condicionada a essa compatibilização.']}
        checks+=extras.get(code,[])
        project=[];workshop=[]
        for check in checks:
            check=check.replace('interfaces listadas em unmappedInterfaces','interfaces listadas em “Ligações ainda sem mapa”')
            if check.startswith(('Em chapa real:','Com a ferragem física:','Oficina:','Oficina/metalurgia:','Fornecedor/oficina:')):workshop.append(check)
            else:project.append(check)
        project+=[('Códigos externos escolhidos em24/10: Arauco Beige Matt nas frentes do gabinete e Louro Freijó Poro nas laterais aparentes. Fechar substrato, composição com Branco TX, bordas/veios e faces ainda parciais; conferir amostra.' if code in ['P18','P19'] else 'Fechar substrato e códigos de chapa, composição Branco TX/padrão aparente, bordas e veios por peça. As faces ainda parciais estão marcadas na lista de peças.')]
        # Product measurements formerly classified as apartment measurements.
        extra={
          'P05':['Conferir os produtos de cuba, válvula e sifão e seus gabaritos antes do recorte; a posição da saída existente é medida no apartamento.'],
          'P13':['Conferir pés, cabo e envelope do micro-ondas real em oficina. A divergência de ventilação deve ser resolvida em projeto.'],
          'P14':['Ensaiar saco, armação e retirada em oficina; conferir produto e gabarito do tanque.'],
          'P16':['Ensaiar encaixe, curso e retirada com MOVENTO 400 e os reforços finais da bancada.'],
          'P18':['Conferir gabaritos de cuba/válvula/sifão, retirada do quadro e acesso à ferramenta em pré-montagem.'],
          'P20':['Medir almofadas/espuma e pesar o conjunto móvel real em oficina; conferir bolsões, eixo e batente no protótipo.']}
        workshop+=extra.get(code,[])
        assembly=unique(finish['modules'][code].get('assembly',[])+[s for s in o.get('assembly',[]) if not s.startswith('Alternativa FGVTN H0:') and 'no estudo FGVTN' not in s])
        fixes={
          'P06':{'Abertura total e amortecimento das três gavetas constam das escolhas; SKU, regulagem e fixação ainda precisam de projeto.':'FGVTN 54FGOC12500TSX0 selecionada para as três gavetas; conferir engates, regulagem e fixação.'},
          'P07':{'Base e apoios R31 são detalhe proposto; fixação dos insertos e sustentação precisam de validação.':'Base e apoios R31 preservados; detalhar e provar a retenção metálica M4 e a sustentação.'},
          'P10':{'Prateleiras atuais encostam nas laterais: a alternativa Minifix é para montagem fixa.':'Montar as três prateleiras fixas desmontáveis com os 20 conjuntos Minifix do módulo; não usar pinos soltos para as mesmas ligações.','Se optar por removíveis, revisar folgas e suportes; não comprar pinos presumindo encaixe do CAD sem alteração.':'Conferir acesso aos Minifix e sequência de montagem antes de fechar a caixa.'},
          'P16':{'Abertura total foi escolhida; amortecimento das gavetas do escritório não foi confirmado.':'MOVENTO 400 com BLUMOTION S selecionada: abertura total e amortecimento. Compatibilizar retirada e gancho antes de usinar.'},
          'P19':{'Prateleiras removíveis preservam folgas nominais de 2 mm; oito apoios são candidatos e ancoragem permanece a definir.':'Prateleiras removíveis preservam folgas nominais de 2 mm; oito apoios Häfele .711 selecionados. Carga da prateleira e ancoragem continuam em projeto.'}}
        assembly=[fixes.get(code,{}).get(s,s) for s in assembly]
        assembly+=m.get('assembly',[])+j.get('assembly',[])
        if code=='P20':
            hardware,decisions,drilling,project,workshop,assembly=revise_p20(hardware,decisions,drilling,project,workshop,assembly)
            for i,row in enumerate(drilling,1):row['id']=f'{code}-F{i:02}'
        drawings=[]
        for draw in hinge_maps:
            if draw['module']==code:
                draw=dict(draw,title='Canecos Blum',status='Centros do CAD R45; Ø35 e profundidade 13 mm. Validar primeira peça. Parafusos e calços: ver tabela.')
                drawings.append(draw)
        if code in ['P11','P15']:
            groups=defaultdict(list)
            for pos in geometry['modules'][code]['positions']:groups[pos['board']].append(pos)
            for part,positions in groups.items():
                p=positions[0];b=p['panel_bbox_global_mm']
                drawings.append(dict(partId=part,title='Alojamentos Minifix',width=b[3]-b[0],height=b[4]-b[1],thickness=18,
                 face='Face superior' if p['access']=='top' else 'Face inferior',origin='Origem: canto X mínimo/Y mínimo da peça no CAD.',
                 orientation='U=+X global; V=+Y global. Plano de coordenadas, não vista espelhada da face virada.',
                 holes=[dict(x=v['cam_offset_from_Xmin_mm'],y=v['offset_from_Ymin_mm'],diameter=15,depth='13,5 +0,5') for v in positions],
                 status='Mapa nominal testado sem colisão. Passagem de aresta e piloto da lateral estão na tabela; provar em retalho.'))
        if code=='P10':
            groups=defaultdict(list)
            for p in j['nominalPositions']:groups[p['board']].append(p)
            for part,positions in groups.items():
                p=positions[0]
                drawings.append(dict(partId=part,title='Alojamentos Minifix',width=511,height=312,thickness=18,
                 face='Face superior' if p['access']=='top' else 'Face inferior',origin='Origem: X=2366/Y=6670 no CAD, o canto mínimo deste painel.',
                 orientation='U=+X global; V=+Y global. Plano de coordenadas, não vista espelhada da face virada.',
                 holes=[dict(x=v['cam_offset_from_Xmin_mm'],y=v['offset_from_Ymin_mm'],diameter=15,depth='13,5 +0,5') for v in positions],
                 status='Mapa nominal do estudo R45. Passagem e piloto nas laterais: tabela de furação; provar em retalho.'))
        if code=='P19':
            for part,w,h,face,holes in [
                ('Peca403',564,108,'Superior interna',[(34,26),(34,82),(530,26),(530,82)]),
                ('Peca404',564,108,'Inferior interna',[(34,26),(34,82),(530,26),(530,82)]),
                ('Peca402',564,714,'Frontal interna do fundo',[(34,102),(34,612),(530,102),(530,612)])]:
                drawings.append(dict(partId=part,title='Alojamentos Minifix P19 — estudo separado',width=w,height=h,thickness=18,face=face,origin='Canto mínimo do painel no sistema local Modulo018.',orientation='U=+X local; V=+Y para base/tampo e +Z para fundo. Ler a face de entrada; não espelhar automaticamente.',holes=[dict(x=x,y=y,diameter=15,depth='13,5 +0,5') for x,y in holes],status='Mapa nominal de24/10/2026; CSV e verificação no fechamento do banheiro. Acesso, montagem e resistência não liberados.'))
        result['modules'][code]=dict(name=o['name'],summary=SUMMARIES[code],decisions=decisions,drilling=drilling,hardwareRows=hardware,
          projectChecks=unique(project),workshopChecks=unique(workshop),technicalChecks=unique(project+workshop),assembly=unique(assembly),
          fieldChecks=fields['modules'][code]['fieldChecks'],resolvedChecks=unique(m.get('resolvedChecks',[])+j['resolvedChecks']),
          unmappedInterfaces=j['unmappedInterfaces'],drawings=drawings,sourcePaths=['01_Projeto/Estudo_interativo/fabrication/technical-r14.json'])
    (DATA/'technical-r14.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('R14 compilada: '+str(sum(len(v['drilling']) for v in result['modules'].values()))+' operações e '+str(sum(len(v['drawings']) for v in result['modules'].values()))+' vistas nominais.')

if __name__=='__main__':build()
