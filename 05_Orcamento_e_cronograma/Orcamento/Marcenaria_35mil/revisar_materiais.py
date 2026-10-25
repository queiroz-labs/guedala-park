"""Triagem de quantitativos; nao e lista de corte ou ordem de compra."""
import json, pathlib, collections, math, re
P=pathlib.Path(__file__).parent
I=P.parents[1]/'Consolidacao_R45_2026-10-23'/'Inventario'
A=json.loads((I/'Solidos_finitos_ativos_R44.json').read_text(encoding='utf-8-sig'))
T={x['name']:x for x in json.loads((I/'Arvore_R44.json').read_text(encoding='utf-8-sig'))}
def ancestors(n,seen=None):
    seen=set() if seen is None else seen
    if n in seen:return seen
    seen.add(n)
    for x in T.get(n,{}).get('parents',[]): ancestors(x,seen)
    return seen
def room(n):
    aa=ancestors(n)
    for name,r in [('Ambiente_quarto','Quarto'),('Ambiente_cozinha','Cozinha'),('Ambiente_lavanderia','Lavanderia'),('Ambiente_escritorio','Escritório'),('Ambiente_banho','Banheiro'),('Ambiente_sala','Sala')]:
        if name in aa:return r
    if n.startswith('BC43_'):return 'Banheiro'
    if n.startswith('BancoR43_'):return 'Sala'
    return 'REVER'
extras={'Peca084','Peca085','Peca086','Peca110','Peca130','Peca249','Peca250'}
starts=('PlacaL','LateralApoioPrincipal','FrenteSimples','ApoioPortaB','FaixaQuina','GavetaComum','FrenteComum','ApoioComum','PrateleiraEspelhado','ApoioOposto','FrenteVizinha','FundoTanque','BasePlana','ApoioEsquerdo','ApoioCentral','ApoioDireito','Contramarco','Ref_Apoio_B','Ref_Sarrafo','ApoioCesto','BancoR43_Painel')
selected=[]
for x in A:
    n=x['name'];lab=x['label'];d=sorted(x['dim']);aa=ancestors(n)
    yes=n in extras or n.startswith(starts)
    if re.fullmatch(r'Peca\d+',n) and int(n[4:])>=206 and any(z.startswith('Modulo') for z in aa) and d[0]<=30 and 'canal técnico' not in lab:yes=True
    if n.startswith('GavetaComum'):yes=lab.startswith(('Lateral comum','Fundo comum','Traseira comum','Dianteira comum','Frente preservada','Frente 130'))
    if n.startswith('MontagemG2') and any(s in lab for s in ['da_gaveta','frontal_da']):yes=True
    if n.startswith('PecaBaixa') and (lab.startswith(('Frente baixa','Fundo18','Lateral18','Parede frente','Reserva apoio lateral'))):yes=True
    if n.startswith('PecaCesto') and (lab.startswith(('Base98','Rodapé80','Painel superior','Frente inferior','Fundo18 da armação'))):yes=True
    if n.startswith('PecaBanco') and lab.startswith(('Frente18','Fundo potes','Fundo demais','Divisória18','Painel posterior','Painel frontal','Prateleira contínua','PecaBancoR006')):yes=True
    if n=='Peca406AtualR31':yes=True
    if n.startswith('ReferenciaCorrer') and lab.startswith(('Apoio frontal','Continuação frontal','Travessa superior frontal')):yes=True
    if n in ['BC43_LateralE','BC43_LateralD','BC43_Base','BC43_Travessa','BC43_CaixaE','BC43_CaixaD','BC43_CaixaBase','BC43_PainelEsquerda','BC43_PainelDireita']:yes=True
    if not yes:continue
    r=room(n)
    # Conservative visual assignment: exposed sides/fronts/bottoms remain decorated;
    # concealed shelves/dividers/backs and drawer boxes are white.
    hidden=any(s in lab.lower() for s in ['fundo','divisória','prateleira curta','sapateira','apoio interno','segundo18','traseira comum','dianteira comum','lateral comum','parede frente/trás','lateral18 baixa'])
    if n.startswith('MontagemG2') and 'Frente_da' not in lab:hidden=True
    if lab.lower().startswith('prateleira') and n not in extras and n!='Peca350':hidden=True
    color='Branco TX' if hidden else {'Quarto':'Arenza','Cozinha':'Arenza','Lavanderia':'Arenza','Escritório':'Off-white','Banheiro':'Bege/claro','Sala':'Arenza'}.get(r,'REVER')
    if r in ('Cozinha','Lavanderia') and any(z in aa for z in ['Modulo008','Modulo009','Modulo010','Modulo011','Modulo014']) and not hidden:color='Azul Petróleo'
    if n in ['Peca110','Peca130','Peca085','Peca086'] or (r=='Escritório' and ('Gaveta' in n or 'Modulo015' in aa)):color='Branco TX' if hidden else 'Arenza'
    if n=='Peca084':color='Off-white'
    if n in ['Peca249','Peca250']:color='EPS proteção (não MDF)'
    area=d[1]*d[2]/1e6
    selected.append(dict(name=n,label=lab,room=r,color_scenario=color,thickness_mm=round(d[0],2),blank_mm=[round(d[2],2),round(d[1],2)],area_m2=round(area,6),rectangular_envelope=True,oversize=min(d[1:])>1830 or max(d[1:])>2730))
out={'source':str(I),'basis':'R44 active finite solids; R45 preserves principal geometry. Conservative bounding rectangles, including cutouts; finish assignment is a costing scenario, not a CAD edit.','parts':selected}
groups=collections.defaultdict(lambda:dict(n=0,area_m2=0,perimeter_m=0))
for x in selected:
    k=(x['room'],x['color_scenario'],x['thickness_mm']);g=groups[k];g['n']+=1;g['area_m2']+=x['area_m2'];g['perimeter_m']+=2*sum(x['blank_mm'])/1000
out['groups']=[dict(room=k[0],finish=k[1],thickness_mm=k[2],**{a:round(b,3) for a,b in v.items()}) for k,v in groups.items()]
(P/'Levantamento_materiais_2026-10-23.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'parts':len(selected),'area_m2':round(sum(x['area_m2'] for x in selected),3),'groups':out['groups'],'oversize':[x for x in selected if x['oversize']]},ensure_ascii=True,indent=2))

# Cost range: area-based sensitivity only, NOT nesting or a guaranteed material takeoff.
# Whole sheets shared across rooms of the same finish/thickness; allocate that purchase by area.
rooms=['Quarto','Cozinha','Lavanderia','Escritório','Banheiro','Sala','Arremates gerais']
cost={r:[0.,0.] for r in rooms}; details=[]
prices={('Branco TX',18):(365.11,400),('Arenza',18):(435.58,520),('Azul Petróleo',18):(526,618.67),('Off-white',18):(489.94,600),('Bege/claro',18):(500,650),('Branco TX',15):(282.67,330)}
for (finish,th),(lo,hi) in prices.items():
    parts=[x for x in selected if x['color_scenario']==finish and x['thickness_mm']==th]
    area=sum(x['area_m2'] for x in parts)
    counts=[math.ceil(area/(2.75*1.85*y)) for y in [.75,.60]]
    vals=[counts[0]*lo,counts[1]*hi]
    details.append(dict(item=f'{finish} {th} mm',area_m2=round(area,3),sheet_counts_scenario=counts,price_per_sheet=[lo,hi],cost_range=vals,basis='75% / 60% assumed area utilization, whole sheets; not a cut layout'))
    for r in rooms:
        share=sum(x['area_m2'] for x in parts if x['room']==r)/area
        for k in [0,1]:cost[r][k]+=vals[k]*share
def allowance(label,lo,hi,weights,basis):
    details.append(dict(item=label,cost_range=[lo,hi],room_weights=weights,basis=basis))
    for r,w in weights.items():
        cost[r][0]+=lo*w;cost[r][1]+=hi*w
def area_weights(parts):
    total=sum(x['area_m2'] for x in parts)
    return {r:sum(x['area_m2'] for x in parts if x['room']==r)/total for r in rooms if any(x['room']==r for x in parts)}
allowance('Materiais para 16 / 16,2 mm das gavetas',400,700,area_weights([x for x in selected if x['thickness_mm'] in [16,16.2]]),'Provisão sem oferta equivalente confirmada; não substituir espessura automaticamente; trabalho de usinagem permanece em serviços')
allowance('Materiais acabados 30 mm',950,1700,area_weights([x for x in selected if x['thickness_mm']==30]),'2,57 m² nominais; provisão de substrato e faces; preço de chapa crua não é preço de Arenza acabado')
allowance('Tampas Arenza 20 mm',600,1000,{'Sala':1},'0,805 m²; espessura e acabamento especiais sem SKU/cotação; não reduzir para18')
allowance('Painel TV off-white20 mm',700,1100,{'Sala':1},'1,8975 m²; provisão de material acabado sem SKU/cotação')
allowance('Contramarcos 26,5 mm',100,200,{'Cozinha':1},'Material e acabamento sem especificação executiva')
allowance('Substratos da cabeceira',150,300,{'Quarto':1},'Conjunto não discriminado em chapas no inventário; provisão de materiais sem mão de obra')
allowance('Substratos do encosto',150,250,{'Sala':1},'Três painéis; provisão sem mão de obra')
allowance('Espuma/tecido/manta cabeceira',250,500,{'Quarto':1},'Provisão de materiais; não autoriza alterar tecido, densidade ou cor')
allowance('Espuma/tecido/manta encosto e almofadas',350,650,{'Sala':1},'Provisão de materiais; não autoriza alterar conforto ou cor')
allowance('Espelho lateral quarto',350,500,{'Quarto':1},'0,9m² nominal; referência de espelho4mm R$375/m² não aprova espessura do projeto')
allowance('Espelho frontal banheiro',200,300,{'Banheiro':1},'0,444m² de frentes; cortes e acabamento de borda sujeitos a cotação')
allowance('EPS proteção quarto',150,250,{'Quarto':1},'11,8584m² de envelopes, não MDF; provisão inclui perdas e pequenos complementos')
allowance('Proteções/calços adicionais',100,200,{'Lavanderia':.5,'Escritório':.5},'Somente interfaces aplicáveis, quantitativo final em aberto')
perimeters={r:sum(2*sum(x['blank_mm'])/1000 for x in selected if x['room']==r and not x['color_scenario'].startswith('EPS')) for r in rooms}
allowance('Fitas de borda, colas e consumíveis',900,1600,{r:v/sum(perimeters.values()) for r,v in perimeters.items() if v},'Rateio pelo perímetro bruto, sem afirmar todas as bordas fitadas; rolos por cor/largura, sobra e adesivos incluídos, aplicação em serviços')
allowance('Diferença de materiais para áreas úmidas',300,600,{'Cozinha':.6,'Lavanderia':.2,'Banheiro':.2},'Sensibilidade a HR/vedação; não preço de kit nem troca automática de especificação')
allowance('Arremates não detalhados',250,400,{'Arremates gerais':1},'Material adicional fora das peças selecionadas, sem duplicar C06')
result={'date':'2026-10-23','not_quote':True,'not_cut_list':True,'sheet_area_m2':5.0875,'assumed_utilization':[.75,.60],'parts_including_EPS':len(selected),'panel_area_excluding_EPS_m2':round(sum(x['area_m2'] for x in selected if not x['color_scenario'].startswith('EPS')),3),'details':details,'room_ranges':{r:[round(v,2) for v in vals] for r,vals in cost.items()},'totals':[round(sum(v[i] for v in cost.values()),2) for i in [0,1]]}
(P/'Revisao_custos_materiais_2026-10-23.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'ranges':result['room_ranges'],'totals':result['totals'],'sheet_costs':details[:6]},ensure_ascii=True,indent=2))
