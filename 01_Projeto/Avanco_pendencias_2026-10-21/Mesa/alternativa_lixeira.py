import pathlib,json
p=pathlib.Path(__file__).parent
r={'tipo':'proposta nao aplicada: giro90graus da lixeira inteira, mantendo canto da caixa envolvente X2660/Y5290','corpo_bbox_mm':[2450,4950,0,2660,5290,470],'pedal_bbox_mm':[2510,4930,10,2600,4980,30],'transformacao_planta':'x_novo=7740-y_antigo; y_novo=2630+x_antigo (rotacao90graus + translacao)','verificacao':'Corpo no mesmo canto junto a paredeX2660; sem penetracao de parede. Antes do giro, varredura kernel nao encontrou outros obstaculos solidos no retanguloX1485..2660/Y3800..5500 alem lixeira existente. Novo corpo/pedal nao cruzam mesa/cadeiras mesmo puxadas30cm. Pedal terminaY4980, antes da cadeira cozinhaY4996.67; separacao16.67mm entre faixas longitudinais, nao folga de operacao humana.','folgas_aberta_cm':{'guardada':96.5,'puxada20':76.5,'puxada30':66.5},'limitacoes':'Nao comprova tampa aberta, alcance do pedal, acesso humano nem retirada do saco. Sem modelo articulado/ficha de giro. Nao mover efetivamente. A medida34x21 e o pedal sao gabaritoR42, confirmar produto.'}
(p/'Alternativa_giro_lixeira.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1150" height="760"><rect width="1150" height="760" fill="#faf9f5"/><g font-family="Arial" fill="#263745"><text x="25" y="35" font-size="25">Proposta: girar a lixeira90° no mesmo canto — não aplicada</text><text x="25" y="65" font-size="16">Berlin aberta: corpo humano e movimento da tampa/pedal não simulados.</text>']
for k in range(2):
 ox=25+k*570;oy=110;sc=.18
 def box(b,c,d=''):
  x1,y1,x2,y2=b;s.append(f'<rect x="{ox+x1*sc}" y="{oy+(5600-y2)*sc}" width="{(x2-x1)*sc}" height="{(y2-y1)*sc}" fill="{c}" stroke="#485963" stroke-dasharray="{d}"/>')
 s.append(f'<text x="{ox}" y="100" font-size="20">'+('Atual' if k==0 else 'Giro90° proposto')+'</text>')
 box([2660,3950,2760,5390],'#adb6bc');box([475,3800,1275,5500],'#d4e4de');box([100,3750,550,5550],'#bea27a')
 for y in [3863.333333,4430,4996.666667]:
  box([1015,y,1485,y+440],'#e6c17c');box([1315,y,1785,y+440],'none','6 4')
 box([2320,5080,2660,5290] if k==0 else [2450,4950,2660,5290],'#df9c89');box([2300,5140,2350,5230] if k==0 else [2510,4930,2600,4980],'#a44938')
 s.append(f'<text x="{ox}" y="500" font-size="18">Faixa mínima: '+('81,5 /61,5 /51,5cm' if k==0 else '96,5 /76,5 /66,5cm')+'</text>')
 s.append(f'<text x="{ox}" y="530" font-size="16">Guardada /puxada20cm /puxada30cm(tracejado)</text>')
s.append('<text x="25" y="600" font-size="17">Corpo proposto X245–266/Y495–529cm; pedal X251–260/Y493–498cm.</text><text x="25" y="635" font-size="17">Ganho nominal15cm. Sem colisão estática nos envelopes até30cm de recuo lateral.</text><text x="25" y="670" font-size="16">Conferir produto, acionamento do pedal, tampa e passagem com pessoas antes de adotar.</text></g></svg>')
(p/'Alternativa_giro_lixeira.svg').write_text(''.join(s),encoding='utf-8')
