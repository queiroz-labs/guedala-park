from pathlib import Path
import json,html,math
here=Path(__file__).resolve().parent
check=json.loads((here/'Verificacao_apoios.json').read_text(encoding='utf-8'))
masses=json.loads((here.parent/'Modelo_FreeCAD/02_Revisoes_e_estudos/Banco_R16_2026-10-14/Massas_tampas_R16.json').read_text(encoding='utf-8'))
moments=[]
for row in masses['rows']:
    m0=row['wood_filled_scenario750_kg'];m1=row['wood_filled_scenario900_kg']
    moments.append({'setor':row['sector'],'envelope_mm':row['wood_envelope_mm'],'massa_madeira_kg':[m0,m1],'momento_fechado_Nm':[m0*9.81*.224,m1*9.81*.224]})
(here/'Solicitacoes_tampas.json').write_text(json.dumps({'hipotese':'Tampa homogênea ocupando todo envelope de20 mm; eixo ideal na borda traseira, centro a224 mm. Só gravidade, exclui almofada/pega/ferragem, pessoa, choque e atrito. Não dimensiona ferragem ou capacidade de assento.','itens':moments},ensure_ascii=False,indent=2),encoding='utf-8')
support_table='| ID | Local e função | Envelope X × Y × Z (mm) | Ligação a detalhar |\n|---|---|---:|---|\n'
for s in check['supports']:
    support_table+=f"| {s['id']} | {s['label']} | {' × '.join(map(str,s['envelope_mm']))} | União ao corpo e apoio/nivelamento no piso |\n"
md='''# Detalhamento construtivo dos móveis

14/10/2026 · Etapa 4 · Base R30 · Propostas para desenvolvimento com o marceneiro.

**[Abrir o caderno visual](Caderno_construtivo.html)** · [Estudo separado no FreeCAD](Estudo_Apoios_Banco_Cesto_R30.FCStd) · [Vista dos apoios](Apoios_propostos.png).

O avanço desta rodada é uma solução geométrica de apoio inferior para banco e cesto, mais a definição das interfaces de tampas, ferragens, manutenção e fixação dos armários. A R30 permanece intacta. O estudo tem 7 novos envelopes de apoio e cópias estáticas dos móveis; não contém controles de movimento nem peças prontas para corte.

## D01 Banco com apoio até o piso

A leitura da R30 confirmou frente e laterais até Z0, posterior começando em Z18 e divisórias começando em Z80 ou Z100. A proposta completa os trechos inferiores sob três divisórias e o posterior, sem inserir reforços dentro dos compartimentos. As prateleiras removíveis dos potes continuam sem função de suporte do assento.

O percurso de carga proposto é: **tampa fechada → bordas da frente/posterior e divisórias → apoios inferiores e ligações do corpo → piso nivelado**. Não repartir a carga igualmente entre apoios nem atribuir ao fundo, à dobradiça ou ao retentor resistência que não foi calculada.

'''+support_table+'''
Nos apoios B02 e B03, o fundo existente de 18 mm fica entre o apoio inferior (Z0–82) e a divisória (Z100–400). Em B01, o apoio chega diretamente à divisória em Z80. B04 preenche o trecho Z0–18 sob o posterior. São encontros de apoio geométrico; o trecho de fundo em compressão, suas uniões e a estabilidade do conjunto precisam ser dimensionados.

**Montagem proposta:** montar e esquadrejar corpo/divisórias, ajustar os apoios inferiores aos respectivos eixos, unir mecanicamente os componentes e nivelar o conjunto antes de instalar as tampas. Usar ligações acessíveis para manutenção; posições e comprimentos de parafusos/cavilhas seguem o painel escolhido, não a caixa CAD. A proteção do piso e o nivelamento entram dentro da altura do envelope: não acrescentar pés ou calços e elevar o assento de 470 mm sem revisar as cotas.

O vão de conteúdo e a organização foram preservados no estudo. A resistência das tampas, especialmente a de 825 mm, não decorre desse apoio adicional: verificar flexão local, carga concentrada, bordas, abertura e uso por pessoas. Não há carga admissível de assento definida nesta entrega.

## D02 Tampas do banco e retenção

Adotar como direção de detalhamento **apoio perimetral para tampa fechada, giro traseiro e retenção independente na posição aberta**, com componentes comuns compatíveis com o espaço disponível. O retentor mantém a tampa aberta; não sustenta o assento ocupado. A dobradiça precisa reproduzir o eixo de estudo ou provocar uma revisão localizada do percurso.

| Setor | Tampa L × P × A (mm) | Almofada e uso | Interface crítica |
|---|---:|---|---|
| 1 Potes/travessas | 387 × 448 × 20 | Conjunto de giro inclui almofada de 50, com acoplamento por definir | Peso do conjunto completo e retenção; painéis internos retirados vazios |
| 2 Bebidas | 366 × 448 × 20 | Retirar almofada antes de abrir, rotina aceita | Preservar retirada diária da térmica |
| 3 Balde | 214 × 448 × 20 | Retirar almofada antes de abrir, rotina aceita | Não ocupar passagem da alça do balde |
| 4 Folha | 825 × 448 × 20 | Retirar almofada e apoiar nos outros setores; rotina ainda proposta | Não ocupar nicho 800 × 350 × 70 nem o recuo de 24 da folha |

Os 20 mm incluem toda a composição da tampa; não são chapa de 20 mais ferragem, reforço e revestimento. Juntas de estudo de 2 mm deixam 8 mm de contato sobre cada lado de divisória de 18; extremidades têm 17 mm, frente 18 e posterior 16. Vedação, batentes e acabamentos não podem consumir essas reservas sem revisão. A regulagem não deve ser obtida forçando a tampa contra o corpo.

**Ficha da ferragem a preencher:** referência e montagem do conjunto; eixo efetivo; volume em fechado/aberto; ângulo e retenção positiva; massa/centro de gravidade suportados; direção e acesso dos parafusos; liberação para manutenção; ausência de interferência com conteúdos e pega. Quantidade e esforços não foram escolhidos. Duas ferragens não implicam divisão igual da carga.

### Solicitação gravitacional da tampa

Sob a hipótese de madeira homogênea com densidade 750–900 kg/m³ e eixo na borda traseira, o centro fica a224 mm. O momento fechado é m × 9,81 × 0,224; durante o giro ideal, M(θ) = M(0) cos θ. Os números servem como entrada de seleção, sem massa de almofada/pega/ferragem, atrito ou impacto:

| Setor | Massa de madeira (kg) | Momento fechado (N·m) |
|---|---:|---:|
'''
for r in moments:
    md+=f"| {r['setor']} | {r['massa_madeira_kg'][0]:.2f}–{r['massa_madeira_kg'][1]:.2f} | {r['momento_fechado_Nm'][0]:.2f}–{r['momento_fechado_Nm'][1]:.2f} |\n"
md+='''
No setor1, somar a almofada/acoplamento e sua posição de centro de massa. Nos setores2–4, a rotina retira a almofada antes do giro. Não selecionar mola/pistão apenas por esses pesos. [Contas reproduzíveis](Solicitacoes_tampas.json).

## D03 Gabinete do cesto com base apoiada

A R30 tem laterais iniciando em Z98, base Z80–98 e rodapé frontal recuado50 até Z80. Os três apoios C01–C03 propostos dão continuidade inferior às laterais e apoio traseiro à base. Mantêm recuo frontal50, topo do gabinete900 e bancada920. A parte posterior em U da R29, com abertura450 ×602, permanece livre.

**Percurso de carga proposto:** armação/frente → conjunto comercial de pivôs e retenção → reservas estruturais laterais/base → novos apoios inferiores e rodapé existente → piso. Tanque e pedra precisam de apoio próprio ligado ao corpo; painel superior removível e frente basculante não devem servir de sustentação da bancada.

As reservas de pivô52 ×40 ×44 e pinosØ10 ×20 do modelo continuam ilustrações, não ferragens fabricáveis. A geometria de montagem de uma ferragem escolhida deve ser trazida para o modelo antes de furar. As faixas laterais de52 mm também são disputadas pela hidráulica/mangueira: não contar o mesmo espaço duas vezes.

**Sequência construtiva proposta:** base/apoios e laterais → ligações do posterior em U e conferência de esquadro → suporte independente do tanque/pedra → hidráulica acessível → articulação/frente e retenção → painel superior removível. O fundo em U exige verificar resistência a deformação lateral; não recolocar uma chapa inteira atravessando a hidráulica para obter rigidez.

## D04 Giro, retenção e manutenção do cesto

| Interface | Condição de detalhamento |
|---|---|
| Articulação | Eixo de estudo local Y70/Z120, correspondente a560 desde parede; abertura55°. Ferragem comercial pode exigir revisão do eixo/curso. |
| Limite de abertura | Batente mecânico positivo e retenção contra movimento descontrolado. Limite de software não substitui peça física. |
| Ligação da frente | Transferir esforço à armação nos apoios previstos, com fixação acessível; frente550 ×521 ×18. Não usar apenas o saco como ligação. |
| Painel superior |550 ×222 ×18, Z675–897; fixação removível acessível pela frente com conjunto sustentado. Não depender de cola definitiva para acesso ao sifão. |
| Desacoplamento | Armação deve poder ser retirada com suporte temporário e retenções liberadas de forma controlada; não puxar conjunto solto pelas ferragens. |
| Hidráulica | Preservar abertura do fundo em U e caminho da mangueira. Inspeção e manutenção não exigem retirar pedra/tanque. |

**Uso diário de estudo:** abrir55 → retirar saco445 → endireitar55; voltar em ordem inversa. **Manutenção:** afastar Loop650 para posição temporária proposta → retirar saco → sustentar conjunto → liberar/retirar painel e armação → manutenção → recompor e testar retenção → devolver lixeira. Deslocamentos do painel200 e da armação400 são percursos CAD; não especificam ferramentas, pega ou capacidade humana.

O estudo anterior de sensibilidade do cesto, com frente4,64 kg e conjunto armação/conteúdo de5/8/12 kg, tinha momentos de abertura a55 de17,95/21,27/25,69 N·m e mudança de sentido durante o giro. Essas massas são cenários, não carga útil escolhida. A ferragem deve ser validada com conjunto real, roupa e saco, cheio e vazio; a indicação de50 kg de outro produto não se aplica ao pivô ilustrativo.

## D05 Armários e ligações de montagem

| Conjunto | Direção construtiva | Dados para fechar |
|---|---|---|
| Aéreos | Fixação dimensionada ligada ao corpo/laterais ou travessa estrutural, com regulagem e acesso. Não depender da frente, prateleira removível ou fundo sem verificação. | Material e peso do móvel + conteúdo, suporte da parede, ancoragem, quantidade, resistência das ligações e espaço de montagem. |
| Folga ao teto | Conferir o movimento necessário para instalar/retirar o sistema de suspensão dentro da folga existente. | Escritório/cozinha20 e quarto30 são nominais; elevação de engate e irregularidades reais ainda desconhecidas. |
| Roupeiro e gavetas | Preservar recuo10 da frente à porta e curso500; escolher pega compatível com essa folga. Guias fixadas em material que suporte caixa + frente + conteúdo. | Pega, regulagem real, paralelismo, peso e fixação. Distância62 até a cama é cenário de uso, não corredor livre. |
| Maleiro de correr | Trilhos apoiados no corpo, retenção antidesencaixe e batentes acessíveis. | Aplicação real em folhas baixas/largas e referências de instalação; não converter a caixa de reserva em trilho fabricável. |
| Banheiro inferior | Corpo suspenso com fixação independente da pedra/frentes, acesso ao sifão e bordas protegidas. | Parede e carga, hidráulica real, recorte e vedação. Centro livre não demonstra passagem das conexões. |
| Espelhado | Espelho aplicado ao painel, com sistema de adesivo/retenção e espessura definidos pelo fornecedor; caneco permanece na madeira. | Massa real, camada de adesivo, arestas, montagem e ajuste da dobradiça; CAD hoje tem contato ideal vidro/madeira. |
| Prateleiras e apoios internos | Apoios removíveis com retenção adequada ao uso, sem interferir na passagem do conteúdo. | Painel, vão, carga, flecha, suporte e furação. Não atribuir carga pela área de contato. |
| Gaveta de piso | Rodízios e guias de retirada ligados à caixa; conservar frente e rodapé previstos. | Carga completa, altura, piso e apoio efetivo das rodas; não distribuir peso automaticamente por seis. |

As referências Blum já estudadas permanecem candidatas; a R29 registra56 dobradiças no cenário atual, com três por folha do aéreoC. Este caderno não faz nova seleção comercial nem repete uma calculadora de fabricante. Larguras de portas e juntas devem vir da R30, não das listas antigas R11/R28.

## D06 Informações para o marceneiro devolver

Para cada conjunto, pedir uma proposta que identifique: painel/material e acabamento; massa do conjunto e conteúdo de projeto; carga e uso previstos; desenho das uniões e furações; referência exata das ferragens e seus envelopes; apoios/nivelamento; tolerâncias e regulagens; sequência de montagem e de manutenção. Para o banco, incluir número de ocupantes/carga por assento, carga concentrada e verificação de flecha, sem inferir capacidade pela aparência.

Ensaios de recebimento a definir com o executor: estabilidade/esquadro e contato dos apoios; portas/gavetas nos percursos reais; retenção de tampas e cesto cheio/vazio; acesso ao sifão; retirada/reposição de peças removíveis; ausência de contato de ferragem, roupa ou conteúdos. Critérios e cargas de ensaio dependem do dimensionamento, não foram inventados nesta rodada.

## Conferência desta proposta

- Lidas42 peças selecionadas na R30 para a memória geométrica; o estudo separado copiou42 formas do banco e28 do cesto, incluindo conteúdos/reservas para confronto.
- Sete novos apoios comparados com as cópias: nenhum par apresentou sobreposição volumétrica de caixas; não houve necessidade de cálculo booleano nesses pares. Contatos de face são esperados e não demonstram capacidade.
- Giro ideal contínuo0–55 do cesto contra os três novos apoios: caixa móvel X20–570, Y máximo320. Separações conservadoras2 mm de cada lado e274 até apoio posterior. Nenhuma análise nova de pessoa, saco deformável ou ferragem real.
- Formas do estudo válidas e arquivo salvo; modelo R30 com hash preservado. Não repetidas auditorias gerais ou movimentos antigos sem relação com os novos apoios.

[Geometria lida](Geometria_atual.json) · [Verificação dos novos apoios](Verificacao_apoios.json). As dimensões dos apoios são envelopes de proposta incluindo eventual proteção/nivelamento, não lista de corte. A definição de material, ligações e capacidade permanece como próxima etapa do detalhamento.

## Fontes e precedência

[Banco R16](../Modelo_FreeCAD/02_Revisoes_e_estudos/Banco_R16_2026-10-14/README.md) · [Cesto R15](../Modelo_FreeCAD/02_Revisoes_e_estudos/Cesto_R15_2026-10-14/README.md) · [Manutenção R26](../Modelo_FreeCAD/02_Revisoes_e_estudos/Manutencao_R26_2026-10-14/README.md) · [Correções R29](../Modelo_FreeCAD/02_Revisoes_e_estudos/Correcoes_R29_2026-10-14/README.md) · [R30](../Modelo_FreeCAD/01_Atual/Consistencia_R30_2026-10-14/README.md) · [Roteiro de levantamento](../../04_Visita_ao_apartamento/Roteiro_R30_2026-10-14/README.md).

As novas soluções são propostas de construção, sem atribuir aceite ao usuário. O programa, os equipamentos escolhidos e as decisões de uso anteriores são preservados. Não houve solicitação enviada a terceiros.
'''
(here/'README.md').write_text(md,encoding='utf-8')
# Detailed schematic elevations: X is source-local, Z is height; dimensions in mm.
def rect(x,z,w,h,color,opacity=1):
    return f'<rect x="{100+x*.44:.2f}" y="{300-(z+h)*.44:.2f}" width="{w*.44:.2f}" height="{h*.44:.2f}" fill="{color}" fill-opacity="{opacity}" stroke="#52695e" stroke-width=".7"/>'
bank_svg='<svg viewBox="0 0 1000 395" role="img" aria-label="Elevação esquemática do banco: apoios inferiores novos em laranja e divisórias sobre fundos elevados.">'
bank_svg+='<path d="M80 302H925" stroke="#456353"/><text x="85" y="330">Piso de referência</text>'
for x,z,w,h in [(0,0,18,400),(1782,0,18,400),(1402,80,18,320),(1034,100,18,300),(818,100,18,300),(18,82,1384,18),(1420,62,362,18)]:bank_svg+=rect(x,z,w,h,'#c6d3c8')
for c,g,l,p,d in [(s['id'],s['group'],s['label'],s['origin_mm'],s['envelope_mm']) for s in check['supports']]:
    if g=='banco' and c!='B04':
        bank_svg+=rect(p[0],p[2],d[0],d[2],'#cf793c');bank_svg+=f'<text x="{100+p[0]*.44-8}" y="355">{c}</text>'
bank_svg+='<text x="105" y="65">Ponta da cozinha / setor da folha</text><text x="655" y="65">Ponta junto ao sofá</text><text x="105" y="95">Elevação sem frente e sem tampas para mostrar os apoios</text><text x="105" y="385">B04 fica sob o painel posterior, fora desta vista de corte.</text></svg>'
support_rows=''.join(f"<tr><td>{s['id']}</td><td>{html.escape(s['label'])}</td><td>{' × '.join(map(str,s['envelope_mm']))}</td></tr>" for s in check['supports'])
moment_rows=''.join(f"<tr><td>{r['setor']}</td><td>{r['massa_madeira_kg'][0]:.2f}–{r['massa_madeira_kg'][1]:.2f}</td><td>{r['momento_fechado_Nm'][0]:.2f}–{r['momento_fechado_Nm'][1]:.2f}</td></tr>" for r in moments)
page='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guedala Park — construção dos móveis</title><style>*{box-sizing:border-box}body{margin:0;background:#ecefe7;color:#263e35;font:16px/1.55 system-ui}main{max-width:1120px;margin:auto;padding:36px 28px}h1{font-size:36px;line-height:1.15}h2{font-size:26px}h3{font-size:19px}.tag{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#56735e}.card{background:#fffefa;padding:28px;margin:26px 0;border-radius:12px}.note{border-left:4px solid #cf793c;background:#f6eddf;padding:14px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}.strip{background:#dae7dc;padding:15px;border-radius:6px}svg,img{width:100%;height:auto}svg text{font:15px system-ui;fill:#263e35}table{width:100%;border-collapse:collapse;font-size:14px}td,th{padding:10px;text-align:left;border-bottom:1px solid #d9e0d7}th{background:#e5ede3}a{color:#27674d}li{margin:8px 0}button{background:#315e49;color:white;padding:11px 18px;border:0;border-radius:5px;cursor:pointer}footer{font-size:13px;color:#56685d}@media(max-width:650px){main{padding:20px 12px}.card{padding:18px}.grid{grid-template-columns:1fr}h1{font-size:29px}table{font-size:12px}td,th{padding:6px}}@media print{body{background:white}main{padding:0}.card{break-inside:avoid;border:1px solid #ddd;border-radius:0}button{display:none}}</style><main><div class="tag">Guedala Park · etapa 4 · base R30 · 14/10/2026</div><h1>Como construir e manter os móveis</h1><p>Estudo dos apoios do banco e do cesto, interfaces das tampas, montagem e fixação dos armários. Novos apoios em laranja; referências existentes em cinza.</p><p><a href="Estudo_Apoios_Banco_Cesto_R30.FCStd">Abrir estudo separado no FreeCAD</a> · <a href="README.md">Memória completa, contas e fontes</a></p><div class="note">Os sete apoios são propostas geométricas, não peças liberadas para corte. Material, ligações, nivelamento e capacidade ainda precisam de definição. O apartamento R30 permanece intacto.</div>
<section class="card"><h2>D01 · Apoiar o banco até o piso</h2><p>A frente e as laterais já chegam ao piso de referência. A proposta completa os apoios sob três divisórias e o painel posterior, nos vazios abaixo dos compartimentos.</p>'''+bank_svg+'''<div class="strip"><strong>Caminho da carga:</strong> tampa → bordas do corpo e divisórias → apoios inferiores e uniões → piso nivelado.</div><div class="grid"><div><h3>Encontros que precisam de detalhe</h3><p>B01 chega à divisória em Z80. B02 e B03 apoiam o fundo Z82–100, sob as divisórias. B04 preenche os 18 mm sob o posterior.</p></div><div><h3>Altura preservada</h3><p>Proteção do piso e nivelamento entram dentro do envelope dos apoios. Acrescentar pés por baixo mudaria o assento a470 e exige revisar o conjunto.</p></div></div></section>
<section class="card"><h2>D02 · Tampas apoiadas e retidas</h2><p>A tampa fechada descarrega no corpo. Dobradiça e retentor têm funções distintas: conduzir o giro e manter a tampa aberta. O retentor não sustenta uma pessoa sentada.</p><svg viewBox="0 0 1000 310" role="img" aria-label="Detalhe ampliado da junta de duas tampas sobre divisória de18: apoio de8 de cada lado e junta2."><rect x="460" y="150" width="90" height="100" fill="#bfccbf" stroke="#456353"/><rect x="150" y="100" width="350" height="50" fill="#d8c4a7" stroke="#456353"/><rect x="510" y="100" width="340" height="50" fill="#d8c4a7" stroke="#456353"/><path d="M460 270H550M460 260V280M550 260V280" stroke="#456353"/><text x="453" y="301">Divisória18</text><path d="M500 75H510" stroke="#a85e2d"/><text x="458" y="57">Junta2</text><text x="385" y="190">Apoio8</text><text x="565" y="190">Apoio8</text><text x="150" y="84">Tampa · envelope total20</text><text x="150" y="245">Detalhe esquemático ampliado; sem furação definida.</text></svg><p>Extremidades:17 mm de apoio; frente18 e posterior16. Revestimento, reforço e ferragem precisam caber no orçamento de20 mm da tampa. A de825 mm exige verificar flexão e carga concentrada.</p><div class="grid"><div><h3>Rotina preservada</h3><p>Bebidas e balde: retirar almofadas antes de abrir. Potes: a almofada gira com o conjunto, acoplamento pendente. Folha: retirada da almofada e apoio nos outros setores ainda são proposta.</p></div><div><h3>Ficha da ferragem</h3><p>Eixo real, envelope em todo o giro, massa completa, retenção aberta, ângulo, pega, fixações e liberação de manutenção. Ferragem não pode ocupar passagem do conteúdo.</p></div></div><table><tr><th>Setor</th><th>Madeira hipotética · kg</th><th>Momento fechado · N·m</th></tr>'''+moment_rows+'''</table><p>Hipótese: envelope homogêneo, densidade750–900 e centro a224 mm de eixo traseiro ideal. Exclui almofada, pega, ferragem, impacto e pessoa. Os valores não selecionam mola/pistão nem definem capacidade do assento.</p></section>
<section class="card"><h2>D03 · Base estrutural do cesto</h2><p>Laterais existentes começam em Z98. Dois prolongamentos inferiores recuados50 mm e um apoio traseiro sustentam o corpo/base sem fechar a abertura hidráulica do fundo em U.</p><img src="Apoios_propostos.png" alt="Estudo CAD do banco e do cesto com referências transparentes e novos apoios inferiores em laranja"><table><tr><th>ID</th><th>Função</th><th>Envelope X × Y × Z · mm</th></tr>'''+support_rows+'''</table><p>São envelopes incluindo eventual proteção/nivelamento, não lista de corte. As posições locais completas estão na memória geométrica.</p><div class="note">Contra os novos apoios: nenhum volume existente invadido no estado fechado. No giro ideal0–55°, permanecem2 mm de cada lado e274 até o apoio traseiro. Isso não é tolerância de fabricação ou validação de ferragem real.</div></section>
<section class="card"><h2>D04 · Montar para conseguir manter</h2><div class="grid"><div><h3>Montagem do gabinete</h3><ol><li>Base, apoios, laterais e esquadro.</li><li>Fundo em U e ligações estruturais.</li><li>Apoio independente de tanque/pedra.</li><li>Hidráulica acessível.</li><li>Articulação, frente, batente e retenção.</li><li>Painel superior removível pela frente.</li></ol></div><div><h3>Manutenção do cesto</h3><ol><li>Afastar a Loop650, na posição proposta.</li><li>Retirar saco e sustentar o conjunto.</li><li>Liberar retenções; retirar painel/armação.</li><li>Acessar sifão e conexões.</li><li>Recompor, conferir retenção e fechar.</li><li>Devolver a lixeira à posição habitual.</li></ol></div></div><p>Painel superior550 ×222 ×18; abertura traseira450 ×602 preservada. As reservas de pivô e pinos são gabaritos. A articulação precisa de batente físico55°, retenção e desacoplamento acessível. Não tomar o controle de software como mecanismo.</p><p><strong>Carga:</strong> o estudo anterior apresentou17,95–25,69 N·m a55° em cenários de massa, com mudança de sentido do momento durante o giro. A escolha exige o conjunto real cheio e vazio, não a capacidade de outro produto.</p></section>
<section class="card"><h2>D05 · Armários: interfaces a fechar</h2><table><tr><th>Conjunto</th><th>Direção de montagem</th><th>Dependência</th></tr><tr><td>Aéreos</td><td>Fixação ligada ao corpo, com acesso e regulagem.</td><td>Parede, peso e espaço para engatar/retirar dentro da folga ao teto.</td></tr><tr><td>Roupeiro</td><td>Manter recuo10 e curso500; pega compatível.</td><td>Peso das gavetas, paralelismo e fixação das guias.</td></tr><tr><td>Maleiro</td><td>Trilhos, retenção e batentes acessíveis.</td><td>Aplicação em folhas baixas/largas ainda por confirmar.</td></tr><tr><td>Banheiro</td><td>Corpo suspenso; acesso ao sifão; espelho no painel.</td><td>Ancoragem, hidráulica, adesivo/retenção e espessuras reais.</td></tr><tr><td>Prateleiras / gaveta de piso</td><td>Apoios retidos e rodízios ligados à caixa.</td><td>Carga, flecha, piso e apoio efetivo das rodas.</td></tr></table><p>Não ocupar folgas nem criar furação por aproximação. As referências de ferragens já estudadas permanecem candidatas; o caderno não cria uma compra nova.</p></section>
<section class="card"><h2>D06 · O que fechar com o marceneiro</h2><p>Material e acabamento; cargas e massas de uso; desenho das uniões; ferragens exatas e seus volumes; fixação à obra; tolerâncias; sequência de montagem/manutenção e critérios de recebimento.</p><p>Para o banco, definir ocupantes, carga concentrada e flecha. Para o cesto, testar cheio/vazio, retenção e retirada para manutenção. Os conteúdos e o programa aprovado permanecem preservados.</p><div class="strip"><strong>Avanço desta rodada:</strong> sete apoios desenhados e conferidos, estudo CAD separado, caminho de cargas explicitado e interfaces organizadas. <strong>Próximo fechamento:</strong> material, ligações, capacidade e ferragens reais.</div><p><a href="README.md">Ler detalhes e limites completos</a> · <a href="Verificacao_apoios.json">Conferência geométrica</a> · <a href="../../04_Visita_ao_apartamento/Roteiro_R30_2026-10-14/Roteiro_de_conferencia.html">Roteiro da visita</a></p><button onclick="window.print()">Imprimir caderno</button></section><footer>Propostas construtivas baseadas na R30. Nenhuma nova decisão de uso atribuída ao usuário. Dados de fabricantes citados são as fontes já arquivadas; não houve nova seleção comercial ou contato externo.</footer></main></html>'''
(here/'Caderno_construtivo.html').write_text(page,encoding='utf-8')
print('Caderno com seis detalhes e memória construtiva gerados.')

