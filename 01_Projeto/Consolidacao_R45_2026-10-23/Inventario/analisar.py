import json, pathlib, math
P=pathlib.Path(__file__).parent
rows=json.loads((P/'Solidos_finitos_ativos_R44.json').read_text(encoding='utf-8'))
A={x['name']:x for x in rows}
tree=json.loads((P/'Arvore_R44.json').read_text(encoding='utf-8'))
T={x['name']:x for x in tree}
def box(n): return A[n]['bbox']
def measure(k,label,value,criterion,status):return dict(id=k,item=label,value_mm=round(value,3),criterion=criterion,status=status)
checks=[
measure('E01','ME23P acima',box('Peca337')[2]-box('Peca351')[5],'300 mm manual; 100 mm escolha F104','100 mm preservados; divergência do manual não encerrada'),
measure('E02','ME23P atrás',7000-box('Peca351')[4],'100 mm','Atende geometria nominal'),
measure('E03','ME23P esquerda',box('Peca351')[0]-box('Peca350')[0],'100 mm de reserva lateral sobre apoio aberto','Atende reserva geométrica; não prova ventilação'),
measure('E04','ME23P direita',box('Peca350')[3]-box('Peca351')[3],'100 mm de reserva lateral sobre apoio aberto','Atende reserva geométrica; não prova ventilação'),
measure('E05','IB6S acima',box('Peca345')[2]-box('Peca138')[5],'100 mm','Atende no nominal; margem zero além do mínimo'),
measure('E06','IB6S atrás',7000-box('Peca138')[4],'100 mm','Atende no nominal; margem zero além do mínimo'),
measure('E07','IB6S direita até apoio micro',box('Peca350')[0]-box('Peca138')[3],'100 mm','Atende no nominal; margem zero além do mínimo'),
measure('E08','Depurador até plano cooktop',box('Peca139')[2]-box('Peca134')[2],'700–850 mm Suggar; referência de bancada cooktop','820 mm nominal; conferir datum do fabricante'),
measure('E09','LG VC4 atrás',7000-box('Peca152')[4],'100 mm','Atende no nominal; conexões reais pendentes'),
measure('E10','ME23P apoio excedente frontal',box('Peca351')[1]-box('Peca350')[1],'Apoio completo; pés reais não modelados','18 mm; datum dos pés e resistência pendentes'),
measure('M01','Espelheiro folga esquerda prateleira',box('PrateleiraEspelhadoR12')[0]-box('Peca401')[3],'Prateleira removível','2 mm nominal'),
measure('M02','Espelheiro folga direita prateleira',box('Peca400')[0]-box('PrateleiraEspelhadoR12')[3],'Prateleira removível','2 mm nominal'),
measure('M03','Espelheiro folga traseira prateleira',box('Peca402')[1]-box('PrateleiraEspelhadoR12')[4],'Prateleira removível','2 mm nominal'),
]
shelves=[]
# Sensitivity calculation, not a certified load capacity. E=2100 N/mm2 and rho=750 kg/m3 are scenarios.
for name,span,depth,t,comment in [('Peca329',511,312,18,'Cozinha C, repetir em Peca330/331'),('Peca339',661,312,18,'Cozinha B'),('Peca362',799,312,18,'Base aéreo lavanderia, cenário somente laterais'),('Peca350',697,470,18,'Micro: hipótese biapoiada; apoios não detalhados'),('PrateleiraEspelhadoR12',560,104,18,'Espelheiro; repetir na segunda'),('Peca110',1850,700,30,'Bancada, entre centros dos pés visíveis; parede não creditada')]:
 I=depth*t**3/12; own=A[name]['volume']/1e9*750
 cases=[]
 for load in [5,10,20]:
  total=load+own;delta=5*total*9.80665*span**3/(384*2100*I)
  cases.append(dict(content_kg=load,total_kg=round(total,3),instantaneous_deflection_mm=round(delta,3),reference_L300_mm=round(span/300,3)))
 shelves.append(dict(name=name,span_mm=span,depth_mm=depth,thickness_mm=t,self_weight_scenario_kg=own,comment=comment,cases=cases))
modules=[]
for n in ['Modulo']+['Modulo%03d'%i for i in range(1,20)]:
 parts=[A[c] for c in T[n]['group'] if c in A and c.startswith(('Peca','BasePlana','Apoio','Prateleira')) and not any(s in A[c]['label'].lower() for s in ['reserva','gabarito','objeto'])]
 modules.append(dict(name=n,label=T[n]['label'],direct_active_parts=len(parts),parts=[dict(name=x['name'],label=x['label'],dimensions_mm=[round(v,3) for v in x['dim']]) for x in parts]))
data=dict(source='R44 aberta, leitura sem modificar; 23/10/2026',checks=checks,shelf_sensitivity=shelves,modules=modules,limits=['Geometria nominal não é medida real do apartamento','Flecha elástica unidirecional simplesmente apoiada, E=2100 e rho=750 são hipóteses de triagem, sem fluência, ligações, umidade ou certificação','L/300 é referência comparativa escolhida neste estudo, não norma de aprovação do móvel','Método não valida capacidade de suporte/ancoragem nem carga concentrada de aparelho sobre pés'])
(P/'Verificacoes_dimensionais.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# Inventário dimensional — leituras da R44','', '| ID | Objeto/verificação | Resultado mm | Critério / situação |','|---|---|---:|---|']
for c in checks:lines.append(f"| {c['id']} | {c['item']} | {c['value_mm']:g} | {c['criterion']}; {c['status']} |")
lines+=['','## Sensibilidade de prateleiras e bancada','','Carga inclui peso próprio estimado com 750 kg/m³. E=2100 N/mm²; prateleira biapoiada ideal. Sem fluência e sem validação de ligações. Não usar como carga admissível.','', '| Peça | Vão × profundidade × espessura mm | 5 kg conteúdo: flecha mm | 10 kg: mm | 20 kg: mm | Referência L/300 mm |','|---|---|---:|---:|---:|---:|']
for s in shelves:lines.append(f"| {s['name']} — {s['comment']} | {s['span_mm']} × {s['depth_mm']} × {s['thickness_mm']} | "+' | '.join(str(c['instantaneous_deflection_mm']) for c in s['cases'])+f" | {s['span_mm']/300:.2f} |")
lines+=['','## Peças por módulo','','Dimensões globais X × Y × Z; elementos móveis detalhados em frentes próprias. Não é lista de corte.']
for m in modules:
 lines+=['',f"### {m['name']} — {m['label']}",'', '| Peça | Nome | X × Y × Z mm |','|---|---|---|']
 for x in m['parts']:lines.append(f"| {x['name']} | {x['label']} | "+' × '.join(f'{v:g}' for v in x['dimensions_mm'])+' |')
(P/'Cotas_e_calculos.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'checks':len(checks),'modules':len(modules),'sensitivity_cases':sum(len(s['cases']) for s in shelves)}))
