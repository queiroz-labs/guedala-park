# Gás natural — rede, ventilação e exaustão (triagem nominal)

30/10/2026. GN confirmado por Elias ([fatos.json](../../ferramentas/fatos.json), id `gas`); aquecedor Rinnai E21 escolhido em F106 ([Aquecedor.md](../Lavanderia/Aquecedor.md)); cooktop Electrolux KE4GC e depurador Suggar DE61IX listados no [Caderno de especificações](../../01_Programa_e_decisoes/Caderno_de_especificacoes.md). **Nenhum comprimento, diâmetro, material ou posição de tubulação do final 06 foi levantado; nada aqui é projeto de gás.** Dimensionar, testar e ligar é papel do RT e da concessionária ([PQ-015, PQ-016](../../01_Programa_e_decisoes/Perguntas_em_aberto/README.md)).

## O que o estudo mostra

| # | Resultado | Base |
|---|---|---|
| 1 | Demanda máxima somada: **42,5 kW = 3,83 m³/h** (E21 33,7 kW + cooktop 8,8 kW). O E21 sozinho é 79% disso. | Manuais |
| 2 | A rede só fecha com folga se o tubo tiver **diâmetro interno ≥ 16 mm no tronco e ≥ 14–16 mm no ramal do E21** em trajetos curtos; 18–20 mm a partir de 8–12 m. O ramal do cooktop aceita 10–12 mm. | Cálculo, hipóteses abaixo |
| 3 | **O E21 exige abertura de ventilação permanente ≥ 100 cm²** (livres). A dispensa só valeria com 382,5 m³ de ambiente; a unidade inteira tem ≈ 104,5 m³ brutos. | Manual Rinnai |
| 4 | **Volume mínimo do ambiente do E21: 6 m³.** A área de serviço sozinha tem ≈ 5,2 m³ nominais: só cumpre se for um ambiente com a cozinha (19,4 m³), sem parede nem porta fechada entre elas. | Manual Rinnai + cotas |
| 5 | O depurador **sem duto** recircula o ar: nada remove o CO₂ e o vapor do cooktop. Dois queimadores a 4 kW por 30 min elevam o CO₂ de ≈ 1.100 ppm (unidade toda, 2 trocas/h) a ≈ 3.600 ppm (cozinha+AS+sala, 0,5 troca/h). | Cálculo estequiométrico |
| 6 | O terminal da **exaustão forçada do E21 (Ø 60 mm, ≤ 5 m, ≤ 3 curvas de 90°)** e a **grelha de ventilação** não constam em nenhum documento do projeto; o memorial proíbe abrir vãos em alvenaria estrutural. É a maior lacuna. | [Memorial, p. 14 §3.1](../../01_Programa_e_decisoes/Memorial_Cury_impactos.md) |

## Dados dos aparelhos

| Item | Valor | Fonte |
|---|---|---|
| E21 REU-E211 FEH GN | 33,7 kW (29.000 kcal/h), consumo máx. 3,04 m³/h, rendimento 86% | [Manual Rinnai](../../09_Referencias/Plantas_e_manuais/Manuais/Rinnai_E21_Manual_176.pdf), tabela 1 |
| Pressão de gás no E21 | 200 mmca ±25% (150–250 mmca dinâmico); entrada G½ | idem |
| Exaustão | B23 forçada, circuito **aberto**; chaminé Ø 60 mm, até 5 m com 3 curvas de 90°; declive de 2° no trecho horizontal; não compartilhar com duto do fogão; terminal ≥ 40 cm acima de janela (recomendado) | idem, itens 3 e 4 |
| Instalação | laterais 200 mm; superfície incombustível; proibido em banheiro e dormitório; tomada exclusiva a ≤ 1 m; registro de esfera na entrada do gás; flexível conforme NBR 14177; rede dimensionada para todos os aparelhos (NBR 15526) | idem |
| Cooktop KE4GC | 3 semirrápidos de 2.000 W + 1 especial de 2.800 W = **8,8 kW**; GN 1,96 kPa (≈ 200 mmca) | [Manual Electrolux](../../09_Referencias/Plantas_e_manuais/Manuais/Electrolux_KE4GR_KE4GC_Manual_250405XATF.pdf) |
| Cooktop, local | exige circulação de ar ou exaustor; correntes de ar não podem apagar a chama | idem |
| Depurador DE61IX | 124 W; modo depurador (recircula) ou exaustor (Ø 120 mm aconselhado); 700–850 mm acima do cooktop; **vazão não informada** no manual; exige boa ventilação se usado com aparelho a gás | [Manual Suggar](../../09_Referencias/Plantas_e_manuais/Manuais/Suggar_DE61IX_DE62IX.pdf) |

Os manuais citam NBR 13103, 15526 e 14177. **O texto dessas normas não foi conferido**; os números abaixo vêm dos manuais e de fontes secundárias.

## Demanda de gás

[Demanda.csv](Demanda.csv). Fator 11,09 kW por m³/h, tirado da relação do próprio manual do E21.

| Cenário | kW | m³/h |
|---|---:|---:|
| S1 tudo no máximo (E21 + 4 queimadores) | 42,5 | 3,83 |
| S2 inverno: 14 L/min, 15→45 °C (E21 satura) + 2 semirrápidos | 37,7 | 3,40 |
| S3 chuveiro de 8 L/min, 15→40 °C + 1 semirrápido | 18,2 | 1,64 |
| S4 só E21 no máximo | 33,7 | 3,04 |
| S5 só cooktop, 4 queimadores | 8,8 | 0,79 |

Entrada de 15 °C e vazão do chuveiro são **hipóteses** (mesma entrada da comparação do aquecedor). A rede deve atender o caso em que o RT adotar; o coeficiente de simultaneidade da norma não foi conferido e aqui se usa 100%.

## Rede interna: perda de carga

Método: Darcy–Weisbach com Colebrook, gás de densidade relativa 0,60 (coincide em todas as fontes), viscosidade 1,1·10⁻⁵ Pa·s, 20 °C, pressão inicial 200 mmca, comprimento equivalente = real × 1,3 para conexões (hipótese). A conferência independente pela fórmula clássica de Renouard (baixa pressão) fica a 8% do resultado (29,1 contra 31,5 mmca em 3,04 m³/h, DI 14 mm, 10 m). Rugosidade por material é hipótese: cobre 0,0015, multicamada 0,007, aço 0,045 mm. Tabela completa: [Dimensionamento_rede.csv](Dimensionamento_rede.csv) (DI = diâmetro **interno**; relacionar ao tubo comercial é com o RT).

**Critérios (nenhum é a norma conferida):**

- **20 mmca de queda no caminho inteiro** (≈ 10% de 200 mmca; Comgás/RIP 2009 em material da USP; 2 mbar em documento de projeto citando a NBR 15526:2021). Três fontes secundárias convergem em ≈ 20 mmca.
- **50 mmca** é o máximo que o E21 tolera (200 − 25%), conforme o manual.
- **Velocidade:** 20 m/s (NBR 15526:2012, segundo gabarito universitário) ou 6 m/s (NBR 15526:2021, segundo um documento de projeto). Divergem; aqui se mostram os dois. Com 6 m/s o menor DI é 16 mm (tronco), 14 mm (E21) e 10 mm (cooktop).

**Menor DI (cobre) que mantém a queda do trecho ≤ 20 mmca:**

| Comprimento real | Tronco 3,83 m³/h | Ramal E21 3,04 m³/h | Ramal cooktop 0,79 m³/h |
|---|---:|---:|---:|
| 3 m | 14 mm | 14 mm | 10 mm |
| 5 m | 16 mm | 14 mm | 10 mm |
| 8 m | 18 mm | 16 mm | 10 mm |
| 12 m | 20 mm | 18 mm | 10 mm |
| 18 m | 20 mm | 20 mm | 12 mm |

**As quedas do tronco e do ramal somam.** Exemplos para o E21: tronco 4 m DI 16 + ramal 3 m DI 14 = 23,3 mmca (acima de 20); tronco 4 m DI 18 + ramal 3 m DI 16 = 12,9 mmca; tronco 8 m DI 20 + ramal 5 m DI 18 = 14,1 mmca. Tronco 8 m DI 16 + ramal 5 m DI 14 = 42,9 mmca ainda cabe nos 50 do fabricante, mas deixa o E21 perto do limite de pressão mínima.

## Ventilação permanente e volume

[Ventilacao_e_ar.csv](Ventilacao_e_ar.csv).

- **Abertura mínima: 100 cm² livres** (maior entre 100 cm² e a seção da chaminé, 28,3 cm²). A grelha de 100 cm² livres tem em geral 150–200 cm² brutos; conferir com o fabricante da grelha.
- **Isenção por volume:** 9 m³/kW da soma de potências. Com E21 + cooktop são 382,5 m³; nem a unidade inteira (≈ 104,5 m³ brutos) chega lá. **Há ventilação permanente a prover.**
- **Volume mínimo de 6 m³:** área de serviço 1,29 × 1,54 × 2,60 = 5,2 m³ (nominal); cozinha 3,52 × 1,55 × 2,60 = 14,2 m³. O desenho não confirma parede entre as duas ([Cotas.json](../../06_Entregas/Planta_cotada/Cotas.json)). **Não instalar porta ou parede entre cozinha e AS sem rever esta conta.**
- **Ar de combustão** (estequiométrico 9,52 m³ de ar por m³ de gás, excesso de ar 1,2–2,0, hipótese): 44–73 m³/h com tudo ligado. A 1 m/s, a abertura livre seria 122–203 cm². É uma verificação de projeto, não exigência do manual: o manual pede 100 cm².
- A abertura **tem de ser permanente**. Janela com persiana e vidro fechados não conta.

## Exaustão da cozinha e subprodutos

- Renovação de ar de 10–12 trocas/h aplicada ao volume (regra de guias comerciais, não norma): 142–170 m³/h (cozinha) a 194–233 m³/h (cozinha + AS). Coifas de parede comerciais ficam em 400–800 m³/h. O manual do DE61IX não informa a vazão.
- **Cooktop sem exaustão externa:** por m³ de gás queimado saem ≈ 1,83 kg de CO₂ e ≈ 1,50 kg de vapor de água (estequiometria do metano). Tabela com 2 queimadores a 4 kW (1 hora a 100%; fogo médio ≈ metade): [Combustao_cooktop.csv](Combustao_cooktop.csv), mistura perfeita, sem entrada de ar externo além das trocas indicadas.

| Volume | Trocas/h | CO₂ acima do externo, 30 min | idem, 60 min |
|---|---:|---:|---:|
| cozinha + AS (19,4 m³) | 0,5 | 8.249 ppm | 14.674 ppm |
| cozinha + AS + sala (44,5 m³) | 0,5 | 3.587 ppm | 6.381 ppm |
| cozinha + AS + sala | 2 | 2.563 ppm | 3.506 ppm |
| cozinha + AS + sala | 5 | 1.489 ppm | 1.611 ppm |
| unidade inteira (104,5 m³) | 2 | 1.092 ppm | 1.493 ppm |

Vapor: 4 kW por 30 min geram 0,27 kg de água; em cozinha + AS + sala isso soma 5,3 g/kg. De 22 °C e 60% de UR iria a ≈ 89% sem nenhuma remoção. Isso alimenta o estudo de umidade e condensação.

- **O depurador em modo exaustor** (Ø 120 mm até o exterior) remove CO₂ e vapor, mas exige duto e saída, e o memorial proíbe abrir vãos. Em modo depurador só filtra gordura e cheiro. A escolha é de Elias e do RT, com a ventilação permanente e o terminal dimensionados em conjunto.
- O manual do depurador diz que, usado com aparelho a gás, exige boa ventilação do ambiente.

## Distâncias e condições a conferir

| Condição | Valor | Estado no projeto |
|---|---|---|
| E21: laterais livres | 200 mm | A conferir na parede técnica (P14/P15 e varal) |
| E21: parede | incombustível; fora de móvel de madeira | Já anotado como condição em Lista_equipamentos |
| E21: tomada | exclusiva, ≤ 1 m, aterrada | L07 a 150 cm (nominal) |
| E21: gás | registro de esfera na entrada, flexível NBR 14177 | A projetar |
| E21: terminal da chaminé | Ø 60, ≤ 5 m, ≤ 3 curvas, declive 2°, ≥ 40 cm acima de janela | **Sem trajeto nem terminal definidos** (L08 a 215 cm, a projetar) |
| Cooktop: folgas | 50 mm atrás, 60 mm à frente do recorte; 800 mm até armário superior | Registrado em [Lista_equipamentos](../Equipamentos/Lista_equipamentos.csv) |
| Depurador sobre o cooktop | 700–850 mm | Conferir a altura real do fundo do aéreo |
| Cooktop sobre o forno | 200 mm entre fundo do cooktop e topo do forno | Já anotado no projeto |

## Perguntas novas (ligadas a PQ-015, PQ-016, PQ-017)

| Id | Pergunta | Destinatário |
|---|---|---|
| G-01 | Existe duto, prisma ou terminal previsto para a exaustão do aquecedor a gás no final 06? Onde, com que diâmetro e comprimento? A convenção permite terminal na fachada? | Construtora / condomínio |
| G-02 | Onde e como fica a abertura de ventilação permanente de 100 cm² livres para o ambiente do E21 sem abrir vão na alvenaria estrutural? O caixilho tem grelha? | RT / construtora |
| G-03 | Qual a vazão, a pressão e o diâmetro/material da rede entregue até os dois pontos, e a unidade foi dimensionada para ≈ 42,5 kW (3,83 m³/h)? | Construtora / concessionária |
| G-04 | Cozinha e área de serviço são um único ambiente para fins de volume (≥ 6 m³ e ventilação)? Pode haver porta entre elas? | RT |
| G-05 | O depurador pode operar em modo exaustor com duto Ø 120 mm até o exterior, ou só em modo depurador? Que medida de ventilação compensa o cooktop? | RT / condomínio |
| G-06 | Qual coeficiente de simultaneidade e critério de queda de pressão a concessionária e a NBR 15526 vigente aplicam a esta unidade? | RT / concessionária |

## Dia das chaves (proposta; não altera o pipeline de medidas)

Fotografar etiqueta do medidor ou da previsão de medição; ponto de gás da cozinha e da lavanderia com tampão e registro (posição e altura); material e diâmetro visíveis da tubulação; existência de duto ou saída para exaustão perto do ponto do E21; grelha ou veneziana no caixilho da área de serviço; largura livre das laterais do E21; ausência de parede entre cozinha e AS. Não abrir registro nem testar vazamento: isso é com a concessionária e a construtora.

## Limites

- Sem trajetos, comprimentos ou diâmetros reais; as tabelas são varredura paramétrica, não projeto.
- Excesso de ar, rugosidade, fator de conexões, entrada de água a 15 °C e uso dos queimadores são hipóteses.
- Critérios de queda e velocidade vêm de fontes secundárias que divergem; confirmar com a norma vigente.

## Reproduzir

```powershell
python -B ferramentas/estudos/gas_natural.py
python -B ferramentas/estudos/test_gas_natural.py
```

19 testes: demanda, queda de carga (inclusive contra Renouard), ventilação e estequiometria.
