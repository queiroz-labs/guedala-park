import pathlib,json,csv,hashlib,html
p=pathlib.Path(__file__).parent
source=p.parents[1]/'Modelo_FreeCAD/01_Atual/Consolidacao_R42_2026-10-22/Guedala_Park_R42_Consolidado.FCStd'
raw=json.loads((p/'obstaculos_candidatos.json').read_text(encoding='utf-8'))
ob=[r for r in raw if r['name'] in ['Peca049','Peca051','Peca055','Peca144','Peca145','Peca146']]
chairs={'Fechada':[('Ponta_sofa',[655,3890,1095,4360]),('Ponta_cozinha',[655,4940,1095,5410]),('Lateral',[1015,4430,1485,4870])], 'Aberta':[('Lateral_sofa',[1015,3863.333333,1485,4303.333333]),('Lateral_centro',[1015,4430,1485,4870]),('Lateral_cozinha',[1015,4996.666667,1485,5436.666667])]}
rows=[]
for scenario in chairs:
 for pull in [0,200,300]:
  for name,b in chairs[scenario]:
   if 'Ponta' not in name:
    candidates=[r for r in ob if min(b[3],r['bbox'][4])>max(b[1],r['bbox'][1]) and r['bbox'][0]>=b[2]]
    limit=min(candidates,key=lambda r:r['bbox'][0]);gap=limit['bbox'][0]-b[2]-pull
    rows.append(dict(cenario=scenario,cadeira=name,puxar_cm=pull/10,limite=limit['name'],folga_cm=gap/10,tipo='faixa lateral entre envelopes'))
   else:
    gap=(240 if name=='Ponta_sofa' else 742.5)-pull
    rows.append(dict(cenario=scenario,cadeira=name,puxar_cm=pull/10,limite='sofa' if name=='Ponta_sofa' else 'IB6 fechada',folga_cm=gap/10,tipo='folga longitudinal; negativa e sobreposicao'))
# Remaining closed table section near bin pedal remains narrower than the stored lateral chair-to-wall strip.
overall=[dict(cenario=s,puxar_cm=d,min_faixa_lateral_cm=min(102.5,117.5-d) if s=='Fechada' else 81.5-d) for s in chairs for d in [0,20,30]]
report={'fonte':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'metodo':'FreeCAD1.1.4: shapes em coordenadas globais; leitura sem saveDocument. Obstaculos externos selecionados apos varredura de todas shapes na faixa X1485..3600/Y3800..5500/Z0..2100; eixos/planos infinitos nao sao obstaculos fisicos. Folgas sao envelopes de projeto, nao largura ergonomica certificada.','limites':'Parede x2660 em Y3950..5390. Lixeira corpo x2320 em Y5080..5290; pedal x2300 em Y5140..5230 e Z10..30. Trecho antes de Y3950 e depois5390 abre para outros setores: nao impor parede ficticia. Faixa lateral completa considera toda extensao da mesa; nao inclui trajeto de entrada inteiro do apartamento.','premissas':{'insercao_cadeira_cm':26,'projecao_externa_cm':21,'puxar':'Laterais deslocam +X; pontas deslocam para fora em Y. Cenários hipotéticos, sem corpos/pessoas.','IB6':'Aparelhos_compatibilizacao_R03_2026-09-27.md secao4: corpo e reservas documentados; giro nao validado. Nao encontrado eixo/espessura/angulo util de porta validado nos documentos consultados; nao inventada trajetoria.'},'obstaculos':ob,'cenarios_por_cadeira':rows,'gargalo_lateral_por_cenario':overall,'observacoes':['Aberta: corpo da lixeira deixa83.5cm; pedal81.5cm. Separar saliencia baixa do espaco para tronco.','Fechada: tampo x1275 deixa102.5cm ate pedal em Y5140..5200; cadeira lateral terminaY4870 e nao cruza lixeira.','Aberta: faixa limitada pela lixeira afeta a terceira cadeira.','Puxar ponta sofa30cm na mesa fechada produz sobreposicao nominal6cm; +20cm deixa4cm. Nenhuma colisao com parede/lixeira nos tres deslocamentos laterais.','A caixa do pedal foi verificada geometricamente mas dimensoes comerciais/movimento da lixeira nao validados.']}
(p/'Corredor_Berlin_R42.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
with (p/'Corredor_Berlin_R42.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1250" height="930" viewBox="0 0 1250 930"><rect width="1250" height="930" fill="#faf9f5"/><g font-family="Arial" fill="#263745"><text x="30" y="38" font-size="25">Berlin R42 — corredor lateral nas medidas de projeto</text><text x="30" y="66" font-size="16">Inserção26cm hipotética. Sem pessoas; porta IB6 fechada. Valores não certificam conforto.</text>']
for idx,scenario in enumerate(chairs):
 ox=30+idx*620;oy=100;scale=.18
 def rect(b,color,stroke='#415260',dash=''):
  x1,y1,x2,y2=b;svg.append(f'<rect x="{ox+x1*scale}" y="{oy+(6200-y2)*scale}" width="{(x2-x1)*scale}" height="{(y2-y1)*scale}" fill="{color}" stroke="{stroke}" stroke-dasharray="{dash}"/>')
 svg.append(f'<text x="{ox}" y="{oy+18}" font-size="20">{scenario}: '+('2 pontas +1 lateral' if scenario=='Fechada' else '3 laterais')+'</text>')
 rect([2660,3950,2760,5390],'#aeb5b8');rect([2320,5080,2660,5290],'#dd9988');rect([2300,5140,2350,5230],'#a24b3c')
 rect([0,3200,1100,3650],'#c9c6bc');rect([100,3750,550,5550],'#bfa47a')
 rect([475,4100 if scenario=='Fechada' else 3800,1275,5200 if scenario=='Fechada' else 5500],'#d4e4de')
 for name,b in chairs[scenario]:
  rect(b,'#e6c17c')
  for d in [200,300]:
   shift=[d,0,d,0] if 'Ponta' not in name else ([0,-d,0,-d] if name=='Ponta_sofa' else [0,d,0,d])
   rect([v+s for v,s in zip(b,shift)],'none','#c16337' if d==300 else '#347fa0','5 4')
 svg.append(f'<text x="{ox}" y="680" font-size="17">Parede: x266cm; corpo lixeira:232cm; pedal:230cm</text>')
 vals=[r['min_faixa_lateral_cm'] for r in overall if r['cenario']==scenario]
 svg.append(f'<text x="{ox}" y="712" font-size="18">Gargalo lateral: {vals[0]} / {vals[1]} / {vals[2]}cm</text>')
 svg.append(f'<text x="{ox}" y="740" font-size="16">Guardada / puxada20cm (azul) /30cm (laranja)</text>')
 if scenario=='Fechada':svg.append(f'<text x="{ox}" y="776" font-size="16">Ponta sofá:24 /4 /−6cm (sobreposição com30cm)</text>')
 else:svg.append(f'<text x="{ox}" y="776" font-size="16">Gargalo no pedal baixo, junto à cadeira da cozinha.</text>')
svg.append('<text x="30" y="842" font-size="16">Faixa medida em toda a extensão da mesa. Paredes reais do modelo; não há parede contínua fora Y395–539cm.</text><text x="30" y="870" font-size="16">Legenda: lixeira coral; cadeira ocre; linhas tracejadas = hipóteses de recuo. CAD original não alterado.</text></g></svg>')
(p/'Corredor_Berlin_R42.svg').write_text(''.join(svg),encoding='utf-8')
print(json.dumps(overall));print('sha256',report['sha256'])


