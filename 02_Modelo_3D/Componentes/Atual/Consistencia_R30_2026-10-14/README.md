# R30 — juntas da cabeceira, rótulos coerentes, vão do forno e árvore só com o apartamento atual

**Revisão anterior preservada.** O [modelo atual R31](../Consolidacao_R31_2026-10-20/README.md) incorpora os estudos e decisões até 20/10. As afirmações abaixo sobre a R30 descrevem esta revisão histórica.
**20/10/2026 — grelhas e manutenção R02.** [Detalhamento atual](../../../../03_Ambientes/Cozinha/Fischer_Grill/Grelhas_manutencao/README.md): duas grelhas candidatas600 ×90 removíveis, com12 rasgos e272,43 cm² de área aberta cada, réguas fora da passagem de ar e gabarito1:1 para cotação. Foram conferidos195 pares sem sobreposição e retirada frontal hipotética600 mm, sem validar calor/carga/cabos/pessoas. A saída superior agora termina na face perfuradaY6402,5; a hipótese antiga sem grelha real é superada nesse detalhe. Desenvolver acesso às conexões pelo gabinete da pia à esquerda, condicionado à hidráulica, área seca e armazenamento. **GN já confirmado por Elias**; não repetir pergunta sobre tipo de gás. R30/R01 preservadas; sem fabricação, compra ou contato externo.

**19/10/2026 — apoios e ventilação desenvolvidos em R01.** [Solução atual](../../../../03_Ambientes/Cozinha/Fischer_Grill/Apoios_ventilacao/README.md): base plana sobre três nervuras até o piso, vãos livres261,5 mm, entrada inferior e saída superior560 ×60, canal traseiro45 ×560, travessa fora do caminho do ar. KE4GC preservado com recorte520 ×390. Foram conferidos90 pares sem sobreposição e um percurso de ar conectado no estudo; isso não comprova resistência ou resfriamento. Material/ligações/capacidade do apoio, datums dos aparelhos, grelha efetiva, instalações e medidas de campo continuam para o executivo. Fonte R30 preservada; escolha dos aparelhos encerrada.

**Escolha posterior,19/10/2026:** Fischer Infinity com grill, sem turbo, preto127 V,28349-64929, substitui a referência Venax no desenvolvimento. [Estudo localizado e conferência](../../../../03_Ambientes/Cozinha/Fischer_Grill/README.md). Este arquivo R30 permanece com a geometria anterior; não confundir o forno representado aqui com a escolha vigente. A proposta nova é documento separado, sem liberação executiva.

**Complemento documental de 14/10/2026:** conferência forno–cooktop–bancada (histórico: Git `antes-reorganizacao:01_Projeto/Cozinha/Fechamento_R30_2026-10-14/README.md`) e [cortes atualizados](../../../../03_Ambientes/Cozinha/Fechamento/Corte_coccao_R30.html). Correção terminológica do item 7 abaixo: os 517 mm são a largura do **envelope total simplificado**, não do corpo de embutimento de 485 mm citado na fonte arquivada. Os 30 mm laterais foram obtidos em relação ao envelope e não demonstram conformidade completa de instalação. A geometria desta revisão não foi alterada na conferência.

Apartamento R30. Base: R29 inteira (correções 1–5 e curso 500 do roupeiro, confirmado por Elias). R29 e R28 preservadas com SHA256 inalterado. Proposta de estudo, sem liberação de fabricação.

## Item 6 — juntas da cabeceira

Antes: folhas 440,75 / 439,75 / 440,75 / 441,75 e juntas 3 / 4 / 2 mm. As bordas do lado das dobradiças ficaram onde estavam; só as bordas livres mudaram. Assim nenhuma dobradiça, caneco, apoio ou cinemática foi movida.

| Folha | Largura R30 | Antes |
|---|---:|---:|
| Porta 4 | 439,75 | 440,75 |
| Porta 3 | 439,75 | 439,75 |
| Porta 2 | 440,25 | 440,75 |
| Porta 1 (vizinha) | 440,25 | 441,75 |

Juntas conferidas no modelo: **4 / 4 / 4 mm**. A diferença de 0,5 mm entre larguras vem das bordas fixas das dobradiças e não é visível. Juntas de outros ambientes não mudaram: escritório 4 mm, cozinha/lavanderia/banheiro 2 mm.

## Item 8 — rótulos e resíduos

- **624 rótulos** internos de 52 dobradiças `71B3550 —` agora seguem o padrão `peça · folha · altura` (ex.: `173H7100 calço0 · Cabeceira porta 4 - abrir para direita · z80`). Antes diziam `Porta 1`, `Gabinete · esquerda` etc., numeração anterior ao espelhamento. Lista completa em [Rotulos_R30.json](Rotulos_R30.json). As quatro dobradiças do canto R04 já tinham rótulos próprios e não mudaram.
- Peça vazia `Porta 4` (`Folha003`) removida da cabeceira; não havia vínculo nem expressão apontando para ela.
- Grupo de referências R01 (71T7550/79T8500) e as subpeças ocultas da R03 no canto foram rotuladas como `Histórico`. Continuam ocultas e não foram apagadas.

Conferência: 6.032 objetos (R29: 6.041; −9 da peça vazia e sua origem), nenhum inválido, nenhum objeto órfão. Só comprimentos, uma posição de painel e rótulos mudaram.

## Item 7 — vão do forno alargado (decisão de Elias)

A lateral do lado da lavanderia foi deslocada **13 mm** (vão interno 564 → **577 mm**; planilha `Dimensoes006.Comprimento` 600 → 613). A decisão foi de alargar 12 mm, mas o corpo do forno no modelo tem 517 mm, não 516: com 12 mm sobrariam 29,5 mm de cada lado, então foi aplicado 13 mm para chegar aos 30 mm que motivaram a decisão. O forno foi centralizado no vão.

| | R29 | R30 |
|---|---:|---:|
| Lateral do lado da lavanderia | x 3880–3898 | x 3867–3885 |
| Vão interno | 564 | 577 |
| Folga lateral do forno | 24 / 24 mm | **30 / 30 mm** |
| Afastamento LG → lateral | 80 mm | 67 mm |
| Travessa superior de estudo | 564 | 577 |

Conferência: lateral, travessa e forno sem interseção com qualquer peça do modelo; faixa nova estava livre até 900 mm; nenhum objeto inválido.

Continua pendente:

- **Topo do forno** ainda encosta na travessa de estudo (z 660). Só pode subir com a altura real do corpo do KE4GC sob a pedra.
- Atende à instrução de 30 mm laterais da Venax; **não** atende a de 100 mm em toda a volta. A divergência do fabricante segue sem resposta escrita.
- A lateral passa a ficar 13 mm sob a pedra da lavanderia (que termina em x 3880): conferir a emenda das bancadas. O recorte do cooktop continua centrado no vão antigo (deslocamento de 6,5 mm do eixo do vão novo).
- Folga de 50 mm atrás (manual) segue em 15 mm, como já registrado no achado 04.

## Árvore só com o apartamento atual

O apartamento atual ("02 — APARTAMENTO ATUAL — espelhado") é feito de vínculos que mostram, refletidas, as peças da base de edição. Se a base fosse apagada, o apartamento atual sumiria junto, por isso ela foi **recolhida, não apagada**:

- 15 grupos da base (sete ambientes, paredes inteiras, paredes em corte e seis pastas vazias de controles antigos R10–R18) foram para **"99 — BASE DE EDIÇÃO (oculta; alimenta o apartamento atual — não apagar)"**.
- A pasta 99 fica oculta no 3D e **fora da árvore**. Para vê-la: clique com o botão direito na árvore → **Mostrar itens ocultos**.
- No topo da árvore restam: "00 · Dados", "01 — CONTROLES ATUAIS", "02 — APARTAMENTO ATUAL".

Conferência ([Organizacao_base_R30.json](Organizacao_base_R30.json), macro [organizar_base_R30.py](organizar_base_R30.py)): 236 vínculos com geometria comparados antes e depois, nenhum mudou de posição; nenhum objeto inválido; 6.033 objetos (+1 pasta). A macro só salvaria se essa conferência passasse. Nenhuma geometria, medida ou expressão foi alterada.

Para editar uma peça da base, faça nela (pela pasta 99) ou pelos controles; não exiba a base junto com o apartamento atual, porque as duas versões ocupam o mesmo espaço refletido.

## Cadeiras Lina desenhadas

As três caixas de 44 × 47 × 94 da sala foram substituídas por um gabarito desenhado da [Cadeira Lina Estofada (Versatile)](https://versatilemoveis.com.br/produto.php?id=783), modelo preferido registrado em 18/09. Forma tirada das fotos do fabricante:
- 4 pés de madeira maciça de seção quadrada, afunilados (38 → 28 mm);
- pés traseiros que sobem como colunas do encosto, inclinadas para trás;
- saia de madeira sob o assento estofado;
- encosto estofado entre as colunas, com duas travessas de madeira no topo.

O fabricante informa só o envelope de 44 L × 47 P × 94 A cm, mantido exatamente. **Medidas estimadas (hipótese):** assento a 47 cm, estofado 5, saia 6, recuo do encosto 3,2 cm no topo. Não é desenho do fabricante; conferir com a cadeira real.

- Cores: madeira #c4a27b (tom Arenza usado no modelo) e estofado greige #d8d0c2.
- Objetos `CadeiraLinaR30_1..3` na base (pasta 99, sala). Os três vínculos do apartamento atual apontam para eles. Posições espelhadas conferidas, iguais às das caixas.
- Caixas antigas ocultas como `Histórico oculto — envelope R09`.
- **Achado 12 (mesa × Lina):** as caixas tinham 10 contatos com a mesa (tampo, travessas, sapata e pedestal), porque ocupavam os vãos da cadeira real. Com o gabarito, **0 contatos** com mesa, banco, paredes e cozinha. A central fica a 2 cm da coluna. Os contatos enchimento × box do banheiro, da mesma pendência, continuam.

Arquivos: [cadeira_lina.py](cadeira_lina.py) (gabarito), [inserir_lina_R30.py](inserir_lina_R30.py) (macro), [Cadeiras_Lina_R30.json](Cadeiras_Lina_R30.json) (conferência). 6.096 objetos, nenhum inválido.

## Cadeira do escritório desenhada

A caixa de cenário do escritório foi substituída por um gabarito da [GenioDesk ErgoChair Ultra Comfort](https://geniodesk.com.br/products/cadeira-ergonomica-ergochair-ultra-comfort), que continua **cenário, sem escolha definitiva**. Medidas do desenho técnico do fabricante: 74,5 cm de largura nos braços, 73 de profundidade, 114,5–133 de altura, assento a 45,5–53 cm, assento de 51 e encosto de 54 de largura, rodízios de 60 mm.

- Posição modelada: assento a 47 cm e topo do apoio de cabeça a 120 cm, dentro das faixas de regulagem. Envelope exato de 74,5 × 73 × 120, igual ao da caixa antiga.
- Peças: base estrela de 5 hastes com rodízios, pistão, mecanismo, assento em tela, encosto em tela inclinado 14°, apoio de cabeça e dois braços com coluna. Inclinação do encosto, altura dos braços (69 cm) e raio da base (32 cm) são estimados pelo desenho; é um gabarito simplificado.
- Cores: estrutura #262626 e tela #3a3a3a.
- `CadeiraEscritorioR30_1` na base (pasta 99, escritório). O vínculo do apartamento atual aponta para ela; posição espelhada conferida. Caixa antiga oculta como histórico.
- Sem contato com bancada, gaveteiro, sofá-cama ou paredes na posição atual. Os braços a 69 cm passam 3 cm abaixo do tampo da bancada (72), se a cadeira for empurrada até a mesa.

Arquivos: [cadeira_escritorio_ultra.py](cadeira_escritorio_ultra.py), [inserir_ultra_R30.py](inserir_ultra_R30.py), [Cadeira_escritorio_R30.json](Cadeira_escritorio_R30.json). 6.128 objetos, nenhum inválido.

**Correção — cadeiras duplicadas:** as quatro cadeiras novas (3 Lina e a do escritório) tinham sido criadas visíveis na base de edição. Ocultar a pasta 99 não oculta o que está dentro dela, e por isso cada uma aparecia duas vezes: pelo vínculo espelhado (correta) e na posição não espelhada da base. As quatro peças da base foram ocultadas, seguindo o padrão dos demais móveis; os vínculos continuam visíveis e com geometria. Nenhum outro objeto da base estava visível. [Registro](Ocultar_cadeiras_base_R30.json).
